"""ttrpg-runner Hermes plugin.

Wires:

* A dice-rolling Python helper into a Hermes tool.
* A custom story-aware context engine that replaces the built-in
  ``ContextCompressor`` when selected. The engine re-pastes the
  active session's data files into the compressed context, asks the
  LLM to keep them in sync with the recent transcript, and never
  pattern-matches characters, locations, or threads.
* Two bundled skills:
    * ``/ttrpg-bootstrap`` - load with ``ctx.register_skill("ttrpg-bootstrap", ...)``
      for setting up a new session, loading the right pack, and
      walking through character creation.
    * ``/ttrpg-recover`` - load with ``ctx.register_skill("ttrpg-recover", ...)``
      for the post-compaction pass that tells the GM to read the
      recent transcript and the data files re-pasted by the engine
      and update the data files to reflect what just happened.

Install by dropping this directory into ``~/.hermes/plugins/ttrpg-runner/``
(or enabling it as a bundled plugin under ``<repo>/plugins/``). Then:

    plugins:
      enabled:
        - ttrpg-runner

    context:
      engine: "ttrpg-runner"
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from . import lib, schemas, tools
from .context_engine import TTRPGContextEngine

logger = logging.getLogger(__name__)

PLUGIN_DIR = lib.PLUGIN_DIR
BUNDLED_SKILLS = lib.BUNDLED_SKILLS
PACK_SKILL_ROOTS = lib.PACK_SKILL_ROOTS


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def _extract_path_args(args: dict[str, Any]) -> list[str]:
    """Best-effort extraction of file paths from a tool's args.

    Hermes file tools can be named anything (``read_file``, ``cat``,
    ``file_read``, ``view``, etc.) and accept the path under different
    keys. We look at the common ones and return every value that looks
    like a path string.
    """
    paths: list[str] = []
    if not isinstance(args, dict):
        return paths
    for key in (
        "file_path",
        "path",
        "file",
        "filename",
        "filepath",
        "uri",
    ):
        value = args.get(key)
        if isinstance(value, str) and value:
            paths.append(value)
    for key in ("file_paths", "paths"):
        value = args.get(key)
        if isinstance(value, list):
            paths.extend(item for item in value if isinstance(item, str) and item)
    return paths


def _on_pre_tool_call(
    tool_name: str,
    args: dict[str, Any],
    task_id: str,
    **kwargs: Any,
) -> None:
    """Refuse destructive ttrpg-runner tool calls when ``TTRPG_SAFETY_LOCK``
    is set in the environment. Mostly useful for tests and emergency
    trip-wires; harmless in normal use.
    """
    if not tool_name.startswith("ttrpg_"):
        return
    if os.environ.get("TTRPG_SAFETY_LOCK"):
        logger.warning(
            "ttrpg-runner tool %s blocked by TTRPG_SAFETY_LOCK (task %s)",
            tool_name,
            task_id,
        )
        raise PermissionError("ttrpg-runner tools are locked in this session")


def make_post_tool_call_hook(engine: TTRPGContextEngine):
    """Return a ``post_tool_call`` hook that watches for pack-skill
    ``SKILL.md`` reads and registers them as active packs on the engine.
    """

    def _on_post_tool_call(
        tool_name: str,
        args: dict[str, Any],
        result: str,
        task_id: str,
        duration_ms: int,
        **kwargs: Any,
    ) -> None:
        # Opt-in audit log for the plugin's own tool calls.
        if tool_name.startswith("ttrpg_") and os.environ.get("TTRPG_AUDIT_LOG"):
            try:
                payload = json.loads(result) if isinstance(result, str) else result
            except (TypeError, ValueError):
                payload = result
            logger.info(
                "ttrpg-runner audit: tool=%s task=%s duration_ms=%s result=%s",
                tool_name,
                task_id,
                duration_ms,
                payload,
            )

        # Active-pack tracking: if the GM just read a pack skill's
        # SKILL.md, register it on the engine so the next compression
        # repastes it into the working context.
        for path_arg in _extract_path_args(args):
            if lib.is_pack_skill_md(path_arg):
                engine.register_active_pack(path_arg)
                logger.debug(
                    "ttrpg-runner: registered active pack %s via %s",
                    path_arg,
                    tool_name,
                )
            session_dir = lib.find_session_dir(path_arg)
            if session_dir is not None:
                engine.register_active_session(session_dir)
                logger.debug(
                    "ttrpg-runner: registered active session %s via %s",
                    session_dir,
                    tool_name,
                )

    return _on_post_tool_call


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def _register_tools(ctx: Any) -> None:
    for name, schema in schemas.ALL_SCHEMAS.items():
        handler = tools.HANDLERS.get(name)
        if handler is None:
            logger.warning("ttrpg-runner: no handler for %s, skipping", name)
            continue
        ctx.register_tool(
            name=name,
            toolset="ttrpg-runner",
            schema=schema,
            handler=handler,
            description=schema.get("description", ""),
        )


def _register_skill(ctx: Any) -> None:
    for name, path in BUNDLED_SKILLS.items():
        if not path.is_file():
            logger.info(
                "ttrpg-runner: no %s bundled, skipping skill registration",
                path,
            )
            continue
        ctx.register_skill(name, path)


def _register_context_engine(ctx: Any) -> None:
    # Respect a config-driven context length if the host exposes it.
    context_length = 200_000
    threshold_ratio = 0.5
    config = getattr(ctx, "config", None)
    if isinstance(config, dict):
        compression = config.get("compression") or {}
        if isinstance(compression.get("threshold_ratio"), (int, float)):
            threshold_ratio = float(compression["threshold_ratio"])
        if isinstance(compression.get("context_length"), (int, float)):
            context_length = int(compression["context_length"])
        context_cfg = config.get("context") or {}
        if isinstance(context_cfg.get("threshold_ratio"), (int, float)):
            threshold_ratio = float(context_cfg["threshold_ratio"])
        if isinstance(context_cfg.get("context_length"), (int, float)):
            context_length = int(context_cfg["context_length"])

    engine = TTRPGContextEngine(
        context_length=context_length,
        threshold_ratio=threshold_ratio,
        pack_skill_roots=PACK_SKILL_ROOTS,
    )
    if hasattr(ctx, "register_context_engine"):
        try:
            ctx.register_context_engine(engine)
            logger.info(
                "ttrpg-runner: registered context engine %r",
                engine.name,
            )
        except Exception as exc:
            # A second engine attempting to register is rejected; that's
            # a normal single-select provider behavior, not a bug here.
            logger.info(
                "ttrpg-runner: context engine not registered (%s)", exc
            )
    else:
        logger.debug(
            "ttrpg-runner: ctx has no register_context_engine; skipping"
        )
    # Stash the engine on the ctx so the post_tool_call hook closure
    # (created below) can find it without a global. The host may not
    # # expose a setattr, so guard with getattr.
    if getattr(ctx, "ttrpg_runner_engine", None) is None:
        try:
            setattr(ctx, "ttrpg_runner_engine", engine)
        except Exception:  # pragma: no cover - defensive
            pass


def register(ctx: Any) -> None:
    """Plugin entry point - invoked once at Hermes startup."""
    _register_tools(ctx)
    _register_skill(ctx)
    _register_context_engine(ctx)

    engine = getattr(ctx, "ttrpg_runner_engine", None)
    if engine is not None:
        post_hook = make_post_tool_call_hook(engine)
    else:  # pragma: no cover - defensive
        post_hook = _on_pre_tool_call  # type: ignore[assignment]

    try:
        ctx.register_hook("pre_tool_call", _on_pre_tool_call)
        ctx.register_hook("post_tool_call", post_hook)
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("ttrpg-runner: hook registration failed: %s", exc)

    logger.debug(
        "ttrpg-runner plugin loaded from %s (%d tools, %d skills)",
        PLUGIN_DIR,
        len(schemas.ALL_SCHEMAS),
        sum(1 for p in BUNDLED_SKILLS.values() if p.is_file()),
    )
