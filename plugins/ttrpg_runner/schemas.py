"""Tool schemas — what the LLM sees for ttrpg-runner tools.

Kept intentionally minimal. The agent drives session state directly
with Hermes' built-in filesystem and skill tools; the plugin only
contributes the one piece of custom logic the host does not have:
fair dice rolling.
"""
from __future__ import annotations

ROLL = {
    "name": "ttrpg_roll",
    "description": (
        "Roll a generic dice expression such as 2d6+1 or 4d8-2. Returns "
        "individual die results, modifier, and the auditable total. Use "
        "for any dice call the system would otherwise have to fake. "
        "Optional seed makes the roll reproducible for audit."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Dice expression like 1d20+5 or 3d6.",
            },
            "seed": {
                "type": "string",
                "description": "Optional RNG seed for reproducible rolls.",
                "default": None,
            },
        },
        "required": ["expression"],
    },
}

ALL_SCHEMAS = {
    "ttrpg_roll": ROLL,
}
