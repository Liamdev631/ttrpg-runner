#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import re
import sys

from ttrpg_lib import format_json


DICE_RE = re.compile(r"^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$", re.IGNORECASE)


def roll_expression(expression: str, rng: random.Random) -> dict:
    match = DICE_RE.match(expression.strip())
    if not match:
        raise ValueError(f"Unsupported dice expression: {expression}")
    count = int(match.group("count") or 1)
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or 0)
    # randint is uniform over the inclusive range, which keeps every face equally likely.
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


def red_check(stat: int, skill: int, modifier: int, difficulty: int | None, rng: random.Random) -> dict:
    die = rng.randint(1, 10)
    total = die + stat + skill + modifier
    outcome = None
    if difficulty is not None:
        if total >= difficulty + 5:
            outcome = "strong-success"
        elif total >= difficulty:
            outcome = "success"
        elif total <= difficulty - 5:
            outcome = "hard-failure"
        else:
            outcome = "failure"
    return {
        "mode": "red-check",
        "die": die,
        "stat": stat,
        "skill": skill,
        "modifier": modifier,
        "difficulty": difficulty,
        "total": total,
        "outcome": outcome,
        "crit_signal": "critical-success" if die == 10 else "critical-failure" if die == 1 else None,
    }


def opposed(attacker: int, defender: int, rng: random.Random) -> dict:
    attack_die = rng.randint(1, 10)
    defend_die = rng.randint(1, 10)
    attack_total = attacker + attack_die
    defend_total = defender + defend_die
    if attack_total > defend_total:
        winner = "attacker"
    elif defend_total > attack_total:
        winner = "defender"
    else:
        winner = "tie"
    return {
        "mode": "opposed",
        "attack_die": attack_die,
        "defend_die": defend_die,
        "attacker": attacker,
        "defender": defender,
        "attack_total": attack_total,
        "defend_total": defend_total,
        "winner": winner,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Roll generic dice for ttrpg-runner.")
    parser.add_argument("--seed", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    expr = subparsers.add_parser("roll", help="Roll a generic dice expression such as 2d6+1.")
    expr.add_argument("expression")

    red = subparsers.add_parser("red-check", help="Roll a fast 1d10 + stat + skill + modifier check.")
    red.add_argument("--stat", type=int, required=True)
    red.add_argument("--skill", type=int, required=True)
    red.add_argument("--modifier", type=int, default=0)
    red.add_argument("--difficulty", type=int, default=None)

    opp = subparsers.add_parser("opposed", help="Roll an opposed 1d10 contest.")
    opp.add_argument("--attacker", type=int, required=True)
    opp.add_argument("--defender", type=int, required=True)

    args = parser.parse_args()
    rng = random.Random(args.seed)

    if args.command == "roll":
        payload = roll_expression(args.expression, rng)
    elif args.command == "red-check":
        payload = red_check(args.stat, args.skill, args.modifier, args.difficulty, rng)
    else:
        payload = opposed(args.attacker, args.defender, rng)

    print(format_json(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
