#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

from cyberpunk_lib import (
    connect_db,
    create_schema,
    database_path,
    format_json,
    insert_entries,
    load_public_sources,
    load_seed_packs,
    read_json,
    resolve_base_dir,
    reset_database,
    source_state_path,
    utc_now,
    write_json,
)


def fetch_wikipedia_summaries(source: dict) -> list[dict]:
    records = []
    for title in source.get("titles", []):
        encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        request = urllib.request.Request(url, headers={"User-Agent": "cyberpunk-runner/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
            continue
        if payload.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
            continue
        records.append(
            {
                "dataset": source["id"],
                "category": "public-reference",
                "name": payload.get("title", title),
                "summary": payload.get("extract", "No summary available."),
                "tags": ["public", "wikipedia", "genre-reference"],
                "details": {
                    "content_urls": payload.get("content_urls", {}),
                    "description": payload.get("description"),
                },
            }
        )
    return records


def load_seed_records() -> list[tuple[str, str, str, str | None, str | None, list[dict]]]:
    payloads = []
    for pack in load_seed_packs():
        source_id = pack["dataset"]
        source_name = pack.get("source_name", source_id)
        source_url = pack.get("source_url")
        license_text = pack.get("license")
        records = []
        for record in pack.get("records", []):
            item = dict(record)
            item["dataset"] = pack["dataset"]
            item["category"] = pack["category"]
            records.append(item)
        payloads.append((source_id, source_name, "seed", source_url, license_text, records))
    return payloads


def build_database(base_dir: str | None, with_public: bool, force_refresh: bool) -> dict:
    base_path = resolve_base_dir(base_dir)
    existing_db = database_path(base_path)
    existing_state_path = source_state_path(base_path)
    if existing_db.exists() and existing_state_path.exists() and not force_refresh:
        state = read_json(existing_state_path)
        state["reused_existing"] = True
        return state

    conn = connect_db(base_path)
    create_schema(conn)
    reset_database(conn)

    stats = {"seed_sources": 0, "seed_records": 0, "public_sources": 0, "public_records": 0, "database": str(database_path(base_path))}

    for source_id, source_name, kind, source_url, license_text, records in load_seed_records():
        inserted = insert_entries(conn, source_id, source_name, kind, source_url, license_text, records)
        stats["seed_sources"] += 1
        stats["seed_records"] += inserted

    public_state = []
    if with_public:
        for source in load_public_sources().get("sources", []):
            if source.get("kind") != "wikipedia_summaries":
                continue
            records = fetch_wikipedia_summaries(source)
            inserted = insert_entries(
                conn,
                source["id"],
                source.get("source_name", source["id"]),
                "public",
                source.get("source_url"),
                source.get("license"),
                records,
            )
            stats["public_sources"] += 1
            stats["public_records"] += inserted
            public_state.append({"source_id": source["id"], "records": inserted})

    state = {
        "updated_at": utc_now(),
        "with_public": with_public,
        "force_refresh": force_refresh,
        "reused_existing": False,
        "stats": stats,
        "public_state": public_state,
    }
    write_json(source_state_path(base_path), state)
    conn.close()
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap public/open cyberpunk data for cyberpunk-runner.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create or refresh the cyberpunk knowledge database.")
    init_parser.add_argument("--base-dir", default=None)
    init_parser.add_argument("--skip-public", action="store_true", help="Skip optional public internet enrichment.")
    init_parser.add_argument("--force-refresh", action="store_true", help="Rebuild the database even if it already exists.")

    show_parser = subparsers.add_parser("show", help="Show the last recorded bootstrap state.")
    show_parser.add_argument("--base-dir", default=None)

    args = parser.parse_args()

    if args.command == "init":
        state = build_database(args.base_dir, with_public=not args.skip_public, force_refresh=args.force_refresh)
        print(format_json(state))
        return 0

    base_path = resolve_base_dir(args.base_dir)
    state = read_json(source_state_path(base_path), default={"status": "missing", "database": str(database_path(base_path))})
    print(format_json(state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
