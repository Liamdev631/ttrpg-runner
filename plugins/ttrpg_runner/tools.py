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
    """Roll one or more dice expressions in a single batched call."""
    requests = args.get("rolls")
    if not isinstance(requests, list) or not requests:
        return _payload(
            {"error": "rolls must be a non-empty list of {expression, seed?} objects"}
        )
    results: list[dict[str, Any]] = []
    for index, request in enumerate(requests):
        if not isinstance(request, dict):
            return _payload(
                {"error": f"rolls[{index}] must be an object with an 'expression' field"}
            )
        expression = (request.get("expression") or "").strip()
        if not expression:
            return _payload({"error": f"rolls[{index}].expression is required"})
        try:
            rng = lib.rng(request.get("seed"))
            results.append(lib.roll_expression(expression, rng))
        except ValueError as exc:
            return _payload(
                {"error": str(exc), "index": index, "expression": expression}
            )
    return _payload({"mode": "batch", "count": len(results), "results": results})


HANDLERS = {
    "ttrpg_roll": roll,
}
