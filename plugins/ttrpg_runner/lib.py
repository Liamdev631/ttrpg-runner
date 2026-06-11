"""Internal helpers for the ttrpg-runner plugin.

Pure functions and filesystem utilities only - no Hermes imports.

After the tool consolidation, the plugin only ships ``ttrpg_roll``,
so this module just exposes the path constants the entry point needs
(``__init__.py`` reads ``BOOTSTRAP_SKILL_FILE`` and ``RECOVER_SKILL_FILE``
to bundle both skills) and the one dice primitive the roll tool calls.
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

FLAVORPACKS_DIR = BOOTSTRAP_SKILL_DIR / "flavorpacks"
TEMPLATES_DIR = BOOTSTRAP_SKILL_DIR / "templates"

# Convenience map: ``BUNDLED_SKILLS[name] -> Path`` for the skill files
# the plugin entry point registers. The names are the slash-prefixed
# names that the GM types (``/ttrpg-bootstrap``, ``/ttrpg-recover``)
# without the slash.
BUNDLED_SKILLS: dict[str, Path] = {
    "ttrpg-bootstrap": BOOTSTRAP_SKILL_FILE,
    "ttrpg-recover": RECOVER_SKILL_FILE,
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


def is_flavor_pack_pack_md(path: str | Path) -> bool:
    """Return True if ``path`` is a flavor-pack ``PACK.md`` under the
    bootstrap skill's ``flavorpacks/`` tree. The context-engine hook
    uses this to detect which files count as active pack content.
    """
    p = Path(path)
    if p.name != "PACK.md":
        return False
    try:
        p_resolved = p.resolve()
        packs_resolved = FLAVORPACKS_DIR.resolve()
    except OSError:
        return False
    return packs_resolved in p_resolved.parents


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
