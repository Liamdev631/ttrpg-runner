"""Tool handlers — what runs when the LLM calls a ttrpg-runner tool.

Handler contract (per the Hermes plugin guide):

* Signature: ``def handler(args: dict, **kwargs) -> str``
* Return:    Always a JSON string. Success and errors alike.
* Never raise: catch exceptions and return ``{"error": "..."}`` JSON.
* Accept ``**kwargs`` for forward compatibility.
"""
from __future__ import annotations

import json
from typing import Any

from . import lib


def _payload(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=True)


def roll(args: dict[str, Any], **kwargs) -> str:
    """Roll a generic dice expression. Optional seed for reproducibility."""
    expression = (args.get("expression") or "").strip()
    if not expression:
        return _payload({"error": "expression is required"})
    try:
        rng = lib.rng(args.get("seed"))
        return _payload(lib.roll_expression(expression, rng))
    except ValueError as exc:
        return _payload({"error": str(exc)})


HANDLERS = {
    "ttrpg_roll": roll,
}
