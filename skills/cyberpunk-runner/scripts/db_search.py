#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from cyberpunk_lib import connect_db, format_json, resolve_base_dir, session_path


def query_entries(conn: sqlite3.Connection, query: str | None, category: str | None, tag: str | None, limit: int) -> list[dict]:
    params = []
    where = []
    sql = "SELECT entry_id, dataset, category, name, summary, tags_json, details_json, source_name, source_url FROM entries"

    if category:
        where.append("category = ?")
        params.append(category)
    if tag:
        where.append("tags_json LIKE ?")
        params.append(f'%"{tag}"%')
    if query:
        try:
            fts = conn.execute(
                "SELECT entry_id FROM entries_fts WHERE entries_fts MATCH ? LIMIT ?",
                (query, limit),
            ).fetchall()
            ids = [row[0] for row in fts]
            if ids:
                placeholders = ",".join("?" for _ in ids)
                sql += f" WHERE entry_id IN ({placeholders})"
                params = ids + params
                if where:
                    sql += " AND " + " AND ".join(where)
            else:
                where.append("(name LIKE ? OR summary LIKE ? OR details_json LIKE ?)")
                like = f"%{query}%"
                params.extend([like, like, like])
        except sqlite3.OperationalError:
            where.append("(name LIKE ? OR summary LIKE ? OR details_json LIKE ?)")
            like = f"%{query}%"
            params.extend([like, like, like])

    if where and " WHERE " not in sql:
        sql += " WHERE " + " AND ".join(where)
    elif where and " WHERE " in sql and " AND " not in sql.split(" WHERE ", 1)[1]:
        pass

    sql += " ORDER BY name LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    return [
        {
            "entry_id": row["entry_id"],
            "dataset": row["dataset"],
            "category": row["category"],
            "name": row["name"],
            "summary": row["summary"],
            "tags": json.loads(row["tags_json"]),
            "details": json.loads(row["details_json"]),
            "source_name": row["source_name"],
            "source_url": row["source_url"],
        }
        for row in rows
    ]


def search_session_text(base_dir: Path, session_id: str, query: str, limit: int) -> list[dict]:
    root = session_path(base_dir, session_id)
    results = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if query.lower() in text.lower():
            results.append(
                {
                    "file": str(path),
                    "excerpt": next((line.strip() for line in text.splitlines() if query.lower() in line.lower()), ""),
                }
            )
        if len(results) >= limit:
            break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the cyberpunk-runner knowledge base and optional session archive.")
    parser.add_argument("query", nargs="?", default=None)
    parser.add_argument("--base-dir", default=None)
    parser.add_argument("--category", default=None)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--session-id", default=None)
    args = parser.parse_args()

    base_dir = resolve_base_dir(args.base_dir)
    conn = connect_db(base_dir)
    payload = {
        "knowledge_results": query_entries(conn, args.query, args.category, args.tag, args.limit),
        "session_results": [],
    }
    conn.close()

    if args.session_id and args.query:
        payload["session_results"] = search_session_text(base_dir, args.session_id, args.query, args.limit)

    print(format_json(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
