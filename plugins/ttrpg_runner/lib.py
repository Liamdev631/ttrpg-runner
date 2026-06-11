"""Internal helpers for the ttrpg-runner plugin.

Pure functions and filesystem utilities only - no Hermes imports.

After the tool consolidation, the plugin only ships ``ttrpg_roll``,
so this module just exposes the path constants the entry point needs
(``__init__.py`` reads ``BUNDLED_SKILLS`` to register every skill the
plugin ships) and the one dice primitive the roll tool calls.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any

PLUGIN_DIR = Path(__file__).resolve().parent
SKILL_DIR = PLUGIN_DIR / "skill"
BOOTSTRAP_SKILL_DIR = SKILL_DIR / "ttrpg-bootstrap"
RECOVER_SKILL_DIR = SKILL_DIR / "ttrpg-recover"
BOOTSTRAP_SKILL_FILE = BOOTSTRAP_SKILL_DIR / "SKILL.md"
RECOVER_SKILL_FILE = RECOVER_SKILL_DIR / "SKILL.md"

TEMPLATES_DIR = BOOTSTRAP_SKILL_DIR / "templates"

# Each flavor pack ships as its own skill directory under ``skill/``.
# The base pack's ``SKILL.md`` carries the always-on rules for that
# pack; the era files (and any other era-specific resources) live in
# the pack skill's ``resources/`` subdirectory and are loaded on
# demand via ``skill_view``.
PACK_SKILL_ROOTS: tuple[Path, ...] = (
    SKILL_DIR / "ttrpg-core",
    SKILL_DIR / "ttrpg-cyberpunk",
    SKILL_DIR / "ttrpg-dnd",
    SKILL_DIR / "ttrpg-mistborn",
    SKILL_DIR / "ttrpg-pokemon",
    SKILL_DIR / "ttrpg-expanse",
)

# Convenience map: ``BUNDLED_SKILLS[name] -> Path`` for the skill files
# the plugin entry point registers. Names are the slash-command names
# the GM types (``/ttrpg-bootstrap``, ``/ttrpg-mistborn``, ...) without
# the leading slash.
BUNDLED_SKILLS: dict[str, Path] = {
    "ttrpg-bootstrap": BOOTSTRAP_SKILL_FILE,
    "ttrpg-recover": RECOVER_SKILL_FILE,
    "ttrpg-core": SKILL_DIR / "ttrpg-core" / "SKILL.md",
    "ttrpg-cyberpunk": SKILL_DIR / "ttrpg-cyberpunk" / "SKILL.md",
    "ttrpg-dnd": SKILL_DIR / "ttrpg-dnd" / "SKILL.md",
    "ttrpg-mistborn": SKILL_DIR / "ttrpg-mistborn" / "SKILL.md",
    "ttrpg-pokemon": SKILL_DIR / "ttrpg-pokemon" / "SKILL.md",
    "ttrpg-expanse": SKILL_DIR / "ttrpg-expanse" / "SKILL.md",
}

# ---------------------------------------------------------------------------
# Dice
# ---------------------------------------------------------------------------

DICE_RE = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$",
    re.IGNORECASE,
)


def rng(seed: str | None = None) -> random.Random:
    return random.Random(seed)


def roll_expression(expression: str, rng: random.Random) -> dict[str, Any]:
    match = DICE_RE.match(expression.strip())
    if not match:
        raise ValueError(f"Unsupported dice expression: {expression}")
    count = int(match.group("count") or 1)
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or 0)
    # randint is uniform over the inclusive range, which keeps every
    # face equally likely.
    rolls = [rng.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    return {
        "mode": "expression",
        "expression": expression,
        "count": count,
        "sides": sides,
        "modifier": modifier,
        "rolls": rolls,
        "total": total,
    }


def format_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=True)


def is_pack_skill_md(path: str | Path) -> bool:
    """Return True if ``path`` is the ``SKILL.md`` of one of the
    plugin's bundled pack skills. The context-engine hook uses this
    to detect which files count as active pack content; the engine
    repastes any active pack's ``SKILL.md`` after a compression
    boundary.
    """
    p = Path(path)
    if p.name != "SKILL.md":
        return False
    try:
        p_resolved = p.resolve()
        roots_resolved = tuple(root.resolve() for root in PACK_SKILL_ROOTS)
    except OSError:
        return False
    return p_resolved.parent in roots_resolved


def find_session_dir(path: str | Path) -> Path | None:
    """Return ``.../sessions/<session-id>`` when ``path`` points
    anywhere inside a tracked session directory.

    This lets the plugin follow the active session through normal file
    reads and writes without relying on a host-specific session API.
    """
    try:
        resolved = Path(path).expanduser().resolve()
    except OSError:
        return None
    parts = resolved.parts
    for index, part in enumerate(parts[:-1]):
        if part != "sessions":
            continue
        if index + 1 >= len(parts):
            return None
        return Path(*parts[: index + 2])
    return None
