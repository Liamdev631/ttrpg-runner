"""ttrpg-runner Hermes plugin.

Wires:

* A dice-rolling Python helper into a Hermes tool.
* One bundled bootstrap skill (``/ttrpg-bootstrap``) and one
  first-class skill per supported flavor pack.

Install by dropping this directory into
``~/.hermes/plugins/ttrpg-runner/`` (or enabling it as a bundled
plugin under ``<repo>/plugins/``). Then:

    plugins:
      enabled:
        - ttrpg-runner
"""
from __future__ import annotations

import logging
from typing import Any

from . import lib, schemas, tools

logger = logging.getLogger(__name__)

PLUGIN_DIR = lib.PLUGIN_DIR
BUNDLED_SKILLS = lib.BUNDLED_SKILLS


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


def register(ctx: Any) -> None:
    """Plugin entry point - invoked once at Hermes startup."""
    _register_tools(ctx)
    _register_skill(ctx)

    logger.debug(
        "ttrpg-runner plugin loaded from %s (%d tools, %d skills)",
        PLUGIN_DIR,
        len(schemas.ALL_SCHEMAS),
        sum(1 for p in BUNDLED_SKILLS.values() if p.is_file()),
    )
