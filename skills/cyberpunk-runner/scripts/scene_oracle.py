#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import sys

from cyberpunk_lib import connect_db, format_json, resolve_base_dir


def pick(conn, category: str, rng: random.Random) -> dict:
    rows = conn.execute(
        "SELECT name, summary, details_json FROM entries WHERE category = ? ORDER BY name",
        (category,),
    ).fetchall()
    if not rows:
        return {"name": f"missing:{category}", "summary": "No entries available.", "details_json": "{}"}
    return dict(rng.choice(rows))


def gig(conn, rng: random.Random) -> dict:
    gig_seed = pick(conn, "gig", rng)
    location = pick(conn, "location", rng)
    complication = pick(conn, "complication", rng)
    rumor = pick(conn, "rumor", rng)
    return {
        "type": "gig",
        "title": gig_seed["name"],
        "pitch": gig_seed["summary"],
        "primary_location": location["name"],
        "location_color": location["summary"],
        "complication": complication["summary"],
        "street_rumor": rumor["summary"],
    }


def rumor(conn, rng: random.Random) -> dict:
    item = pick(conn, "rumor", rng)
    return {"type": "rumor", "headline": item["name"], "rumor": item["summary"]}


def ad(conn, rng: random.Random) -> dict:
    item = pick(conn, "ad-copy", rng)
    return {"type": "ad", "brand": item["name"], "copy": item["summary"]}


def handle(conn, rng: random.Random) -> dict:
    items = [pick(conn, "name-fragment", rng)["name"] for _ in range(2)]
    return {"type": "handle", "value": " ".join(items)}


def weather(conn, rng: random.Random) -> dict:
    item = pick(conn, "weather", rng)
    return {"type": "weather", "name": item["name"], "effect": item["summary"]}


def complication(conn, rng: random.Random) -> dict:
    item = pick(conn, "complication", rng)
    return {"type": "complication", "name": item["name"], "effect": item["summary"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Procedural scene oracle for cyberpunk-runner.")
    parser.add_argument("command", choices=["gig", "rumor", "ad", "handle", "weather", "complication"])
    parser.add_argument("--base-dir", default=None)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    conn = connect_db(resolve_base_dir(args.base_dir))

    if args.command == "gig":
        payload = gig(conn, rng)
    elif args.command == "rumor":
        payload = rumor(conn, rng)
    elif args.command == "ad":
        payload = ad(conn, rng)
    elif args.command == "handle":
        payload = handle(conn, rng)
    elif args.command == "weather":
        payload = weather(conn, rng)
    else:
        payload = complication(conn, rng)

    conn.close()
    print(format_json(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
