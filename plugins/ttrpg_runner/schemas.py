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
        "Roll one or more dice expressions in a single call, e.g. 2d6+1, "
        "4d8-2, or 1d20. Pass a list under ``rolls`` to batch independent "
        "rolls together; this avoids an extra round trip when the GM "
        "needs several dice results at once. Each item returns its own "
        "individual die results, modifier, and auditable total. An "
        "optional per-item seed makes a roll reproducible for audit."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "rolls": {
                "type": "array",
                "minItems": 1,
                "description": (
                    "Batch of roll requests. Each request is an object with "
                    "an ``expression`` and an optional ``seed``."
                ),
                "items": {
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
            },
        },
        "required": ["rolls"],
    },
}

ALL_SCHEMAS = {
    "ttrpg_roll": ROLL,
}
