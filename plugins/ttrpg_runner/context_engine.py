"""Story-aware context engine for ttrpg-runner.

Replaces Hermes' built-in ``ContextCompressor`` with one that:

* Triggers at the same 50%-of-context threshold as the built-in default.
* Loads every session data file (story, timeline, gm-notes, secrets,
  characters, locations, events, rolls) from the active session
  folder and re-pastes them as system messages inside the compressed
  context, so the GM has the full campaign state to work with after
  compression.
* Repastes the active flavor pack's ``PACK.md`` (and active subpack's
  ``PACK.md`` for packs that have them) into the compressed context
  so the GM never loses the operating rules of the current setting.
* Appends a "recent transcript" tail of the last N messages verbatim
  so the model never loses the immediate scene.
* Emits a "session data update required" bridge message asking the
  LLM to write the campaign state back into the data files based on
  the recent transcript. The data files are the persistent state -
  there is no separate JSON mirror.

The engine is registered through the plugin's ``register(ctx)`` hook
via ``ctx.register_context_engine(TTRPGContextEngine(...))``. Set

    context:
      engine: "ttrpg-runner"

in ``config.yaml`` to activate it (or pick it in
``hermes plugins`` -> Provider Plugins -> Context Engine).

## Active Session Tracking

The engine does not pattern-match characters or locations out of the
transcript. Instead, the plugin's ``post_tool_call`` hook watches the
GM's normal file reads and writes, registers any ``PACK.md`` under
``skill/ttrpg-bootstrap/flavorpacks/`` as an active pack, and tracks
the current ``sessions/<session-id>/`` directory. When the engine
compresses, it reads every data file from that directory and emits
them as system messages. The data files are the canonical state; the
LLM is asked to keep them in sync with the recent transcript.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.context_engine import ContextEngine  # type: ignore


# Heuristic token estimate when the API does not report usage.
_CHARS_PER_TOKEN = 4


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // _CHARS_PER_TOKEN)


def _read_text_safe(path: Path) -> str | None:
    """Read ``path`` as UTF-8 text. Return None on any I/O or decode
    error so a missing or malformed file does not crash compression.
    """
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError, UnicodeDecodeError):
        return None


def _message_text(message: dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    chunks.append(str(item["text"]))
                elif "content" in item:
                    chunks.append(str(item["content"]))
        return "\n".join(chunks)
    return str(content or "")


def _role(message: dict[str, Any]) -> str:
    return str(message.get("role") or "user")


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------


class TTRPGContextEngine(ContextEngine):
    """Lossy-with-session-files context compressor for TTRPG sessions.

    Compared with the built-in ``ContextCompressor``:

    * Same threshold semantics (50% of context window by default).
    * Compressed payload always re-pastes the active session's data
      files (``story.md``, ``timeline.md``, ``gm-notes.md``,
      ``secrets.md``, plus everything under ``characters/``,
      ``locations/``, ``events/``, and ``rolls/``) as system messages
      so the GM still has the full campaign state after compression.
    * The active flavor pack's ``PACK.md`` (plus any active subpack's
      ``PACK.md``) is read from disk and repasted in full into the
      compressed context, so the GM never loses the operating rules
      of the current setting across a compression boundary.
    * The last ``protect_last_n`` user/assistant/tool turns are kept
      verbatim, so the model still sees the immediate scene.
    * A "session data update required" bridge message asks the LLM
      to write the campaign state back into the data files based on
      the recent transcript. The data files are the persistent
      state - there is no separate JSON mirror.

    The engine never pattern-matches characters, locations, factions,
    or threads. The data files are the source of truth; the LLM owns
    keeping them in sync with what actually happened at the table.
    """

    DEFAULT_PROTECT_LAST_N = 12
    # Top-level session data files. Dossiers under characters/,
    # locations/, events/, and rolls/ are picked up by directory walk.
    SESSION_TOP_LEVEL_FILES: tuple[str, ...] = (
        "story.md",
        "timeline.md",
        "gm-notes.md",
        "secrets.md",
    )
    SESSION_DOSSIER_DIRS: tuple[str, ...] = (
        "characters",
        "locations",
        "events",
        "rolls",
    )

    def __init__(
        self,
        context_length: int = 200_000,
        threshold_ratio: float = 0.5,
        protect_last_n: int = DEFAULT_PROTECT_LAST_N,
        packs_dir: str | Path | None = None,
    ) -> None:
        self.context_length = int(context_length)
        self.threshold_ratio = float(threshold_ratio)
        self.protect_last_n = int(protect_last_n)
        self.threshold_tokens = int(self.context_length * self.threshold_ratio)
        self.last_prompt_tokens = 0
        self.last_completion_tokens = 0
        self.last_total_tokens = 0
        self.compression_count = 0
        self._focus_topic: str | None = None
        self._packs_dir: Path | None = (
            Path(packs_dir).resolve() if packs_dir else None
        )
        # Ordered list of PACK.md paths. Order is preserved so a base
        # pack's content comes before its subpack's content.
        self._active_pack_files: list[Path] = []
        self._active_session_dir: Path | None = None

    # ---- identity --------------------------------------------------------

    @property
    def name(self) -> str:
        return "ttrpg-runner"

    # ---- active pack tracking -------------------------------------------

    @property
    def active_pack_files(self) -> list[Path]:
        """Read-only view of the active PACK.md paths, in load order."""
        return list(self._active_pack_files)

    @property
    def active_session_dir(self) -> Path | None:
        """Tracked active session directory, when the host exposed one
        through normal file activity.
        """
        return self._active_session_dir

    def register_active_pack(self, pack_path: str | Path) -> None:
        """Mark a ``PACK.md`` as active for the current session.

        Order is preserved so a base pack loads before its subpack.
        The path is resolved against the engine's ``packs_dir`` when
        it is relative.
        """
        path = Path(pack_path)
        if not path.is_absolute() and self._packs_dir is not None:
            path = self._packs_dir / path
        path = path.resolve()
        if path in self._active_pack_files:
            return
        self._active_pack_files.append(path)

    def set_active_packs(self, pack_paths: list[str | Path]) -> None:
        """Replace the active-pack list with ``pack_paths`` in order."""
        self._active_pack_files = []
        for raw in pack_paths:
            self.register_active_pack(raw)

    def clear_active_packs(self) -> None:
        """Drop all tracked active packs. Used on session reset."""
        self._active_pack_files = []

    def register_active_session(self, session_dir: str | Path) -> None:
        """Track the current ``sessions/<session-id>`` directory."""
        path = Path(session_dir).expanduser().resolve()
        self._active_session_dir = path

    # ---- required overrides ---------------------------------------------

    def update_from_response(self, usage: dict[str, Any]) -> None:
        if not usage:
            return
        self.last_prompt_tokens = int(
            usage.get("prompt_tokens", self.last_prompt_tokens) or 0
        )
        self.last_completion_tokens = int(
            usage.get("completion_tokens", self.last_completion_tokens) or 0
        )
        total = usage.get("total_tokens")
        if total is not None:
            self.last_total_tokens = int(total)
        else:
            self.last_total_tokens = (
                self.last_prompt_tokens + self.last_completion_tokens
            )

    def should_compress(self, prompt_tokens: int | None = None) -> bool:
        if prompt_tokens is not None:
            return prompt_tokens >= self.threshold_tokens
        return self.last_total_tokens >= self.threshold_tokens

    def compress(
        self,
        messages: list[dict[str, Any]],
        current_tokens: int | None = None,
        focus_topic: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        if focus_topic is not None:
            self._focus_topic = focus_topic

        if not messages:
            return messages

        # Always keep the first system message (it carries the agent's
        # core instructions).
        head: list[dict[str, Any]] = []
        for message in messages:
            if _role(message) == "system":
                head.append(message)
                break

        # Carve off the most recent user/assistant turns verbatim.
        head_ids = {id(m) for m in head}
        tail: list[dict[str, Any]] = []
        for message in reversed(messages):
            if id(message) in head_ids:
                continue
            role = _role(message)
            if role in ("user", "assistant", "tool"):
                tail.append(message)
                if len(tail) >= self.protect_last_n:
                    break
        tail.reverse()

        # Read the active pack PACK.md files from disk and repaste them
        # as system messages, in load order, just before the session
        # data files.
        pack_messages = self._build_active_pack_messages()

        # Read every session data file from the active session folder
        # and emit each as a system message. These files are the
        # canonical persistent state - there is no separate JSON
        # mirror. Files are emitted in a fixed order so the LLM sees
        # the campaign arc (story) before the supporting records.
        session_messages = self._build_session_messages()

        # Emit a bridge message asking the LLM to keep the data files
        # in sync with the recent transcript. The data files land in
        # the working context above the tail so the LLM has both the
        # state and the recent transcript in one place.
        bridge_message = self._build_bridge_message()

        self.compression_count += 1
        return [
            *head,
            *pack_messages,
            *session_messages,
            bridge_message,
            *tail,
        ]

    # ---- helpers --------------------------------------------------------

    def _build_active_pack_messages(self) -> list[dict[str, Any]]:
        """Read every tracked active PACK.md and wrap it as a system
        message. Missing files are skipped silently so a stale tracker
        does not crash compression.
        """
        messages: list[dict[str, Any]] = []
        for pack_path in self._active_pack_files:
            try:
                content = pack_path.read_text(encoding="utf-8")
            except (FileNotFoundError, OSError, UnicodeDecodeError):
                continue
            # Resolve a human-readable label relative to the packs dir
            # when we know it, so the repasted block is self-describing.
            label = pack_path.name
            if (
                self._packs_dir is not None
                and self._packs_dir in pack_path.parents
            ):
                try:
                    label = str(
                        pack_path.relative_to(self._packs_dir).with_suffix("")
                    )
                except ValueError:
                    label = pack_path.name
            messages.append(
                {
                    "role": "system",
                    "content": (
                        f"## Active Flavor Pack: {label}\n\n{content}"
                    ),
                }
            )
        return messages

    def _build_session_messages(self) -> list[dict[str, Any]]:
        """Read every data file from the active session folder and
        wrap each as a system message. These messages are the
        persistent campaign state - there is no separate JSON mirror.

        Missing files are skipped silently so a fresh session does
        not crash compression. Dossiers under ``characters/``,
        ``locations/``, ``events/``, and ``rolls/`` are walked in
        alphabetical order so the order is stable across compressions.
        """
        if self._active_session_dir is None:
            return []
        messages: list[dict[str, Any]] = []
        for filename in self.SESSION_TOP_LEVEL_FILES:
            path = self._active_session_dir / filename
            content = _read_text_safe(path)
            if content is None:
                continue
            messages.append(
                {
                    "role": "system",
                    "content": (
                        f"## Session File: {filename}\n\n{content}"
                    ),
                }
            )
        for dirname in self.SESSION_DOSSIER_DIRS:
            dir_path = self._active_session_dir / dirname
            if not dir_path.is_dir():
                continue
            try:
                entries = sorted(
                    entry
                    for entry in dir_path.iterdir()
                    if entry.is_file()
                )
            except OSError:
                continue
            for entry in entries:
                content = _read_text_safe(entry)
                if content is None:
                    continue
                rel = f"{dirname}/{entry.name}"
                messages.append(
                    {
                        "role": "system",
                        "content": f"## Session File: {rel}\n\n{content}",
                    }
                )
        return messages

    def _build_bridge_message(self) -> dict[str, Any]:
        """Emit a bridge system message asking the LLM to keep the
        session data files in sync with the recent transcript.

        The data files are the persistent state. The recent
        transcript is in the protected tail below. The LLM's job is
        to read the recent transcript, update the relevant data files
        (story, timeline, characters, locations, events, rolls, and
        gm-notes / secrets as needed), and continue the scene.
        """
        if self._active_session_dir is not None:
            session_label = str(self._active_session_dir)
        else:
            session_label = "(no active session folder tracked)"
        lines: list[str] = [
            "## Session Data Update Required",
            "",
            "The session data files for the active session have been "
            "re-pasted into this compressed context just above. They are "
            "the canonical persistent state. Below this message is the "
            "protected tail of the most recent transcript.",
            "",
            f"**Active session folder**: `{session_label}`",
            "",
            "**Your job this turn**:",
            "",
            "1. Read the recent transcript below.",
            "2. Update the relevant data files (write the changes to "
            "disk with the host's filesystem tools, replacing the old "
            "contents where the campaign has moved on):",
            "   - `story.md` for the running fiction and scene recap",
            "   - `timeline.md` for new beats",
            "   - `characters/<slug>.md`, `locations/<slug>.md`, "
            "`events/<slug>.md` for new or changed entities",
            "   - `rolls/<stamp>-<label>.json` for important dice",
            "   - `gm-notes.md` for hidden planning, stakes, and hooks",
            "   - `secrets.md` for GM-only truths (never printed in chat)",
            "3. Compose the next player-facing response using the "
            "updated files and the recent transcript.",
            "",
            "Do not invent characters, locations, factions, or threads "
            "that are not visible in the recent transcript or in the "
            "data files above. The data files are the source of truth; "
            "the transcript is the input.",
        ]
        if self._focus_topic:
            lines.append("")
            lines.append(f"**Focus topic**: {self._focus_topic}")
        return {"role": "system", "content": "\n".join(lines)}

    # ---- optional ABC hooks --------------------------------------------

    def on_session_reset(self) -> None:
        self.last_prompt_tokens = 0
        self.last_completion_tokens = 0
        self.last_total_tokens = 0
        self.compression_count = 0
        self._focus_topic = None
        self.clear_active_packs()
        self._active_session_dir = None

    def update_model(
        self,
        model: str,
        context_length: int,
        threshold_ratio: float | None = None,
    ) -> None:
        self.context_length = int(context_length)
        if threshold_ratio is not None:
            self.threshold_ratio = float(threshold_ratio)
        self.threshold_tokens = int(self.context_length * self.threshold_ratio)

    def get_status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "last_prompt_tokens": self.last_prompt_tokens,
            "last_completion_tokens": self.last_completion_tokens,
            "last_total_tokens": self.last_total_tokens,
            "threshold_tokens": self.threshold_tokens,
            "context_length": self.context_length,
            "compression_count": self.compression_count,
            "protect_last_n": self.protect_last_n,
            "active_pack_count": len(self._active_pack_files),
            "active_pack_files": [str(p) for p in self._active_pack_files],
            "active_session_dir": (
                str(self._active_session_dir)
                if self._active_session_dir is not None
                else None
            ),
            "engine_class": self.__class__.__name__,
        }
