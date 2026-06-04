#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import random
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_BASE_DIR = Path("~/.hermes/cyberpunk-runner").expanduser()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or "cyberpunk-session"


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:6]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is None:
            raise FileNotFoundError(path)
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content)
        if not content.endswith("\n"):
            handle.write("\n")


def resolve_skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_base_dir(base_dir: str | None) -> Path:
    candidate = Path(base_dir).expanduser() if base_dir else DEFAULT_BASE_DIR
    return candidate.resolve()


def knowledge_dir(base_dir: Path) -> Path:
    return ensure_dir(base_dir / "knowledge")


def sessions_dir(base_dir: Path) -> Path:
    return ensure_dir(base_dir / "sessions")


def database_path(base_dir: Path) -> Path:
    return knowledge_dir(base_dir) / "cyberpunk.db"


def source_state_path(base_dir: Path) -> Path:
    return knowledge_dir(base_dir) / "source_state.json"


def load_seed_packs() -> list[dict[str, Any]]:
    seed_dir = resolve_skill_root() / "assets" / "seed_data"
    return [read_json(path) for path in sorted(seed_dir.glob("*.json"))]


def load_public_sources() -> dict[str, Any]:
    return read_json(resolve_skill_root() / "assets" / "public_sources.json", default={"sources": []})


def connect_db(base_dir: Path) -> sqlite3.Connection:
    db_path = database_path(base_dir)
    ensure_dir(db_path.parent)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sources (
            source_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            url TEXT,
            license TEXT,
            fetched_at TEXT NOT NULL,
            record_count INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS entries (
            entry_id TEXT PRIMARY KEY,
            dataset TEXT NOT NULL,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            summary TEXT NOT NULL,
            tags_json TEXT NOT NULL,
            details_json TEXT NOT NULL,
            source_name TEXT NOT NULL,
            source_url TEXT,
            license TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(entry_id UNINDEXED, name, summary, tags, details)"
        )
    except sqlite3.OperationalError:
        pass
    conn.commit()


def reset_database(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM sources")
    conn.execute("DELETE FROM entries")
    try:
        conn.execute("DELETE FROM entries_fts")
    except sqlite3.OperationalError:
        pass
    conn.commit()


def insert_entries(
    conn: sqlite3.Connection,
    source_id: str,
    source_name: str,
    kind: str,
    url: str | None,
    license_text: str | None,
    records: Iterable[dict[str, Any]],
) -> int:
    now = utc_now()
    count = 0
    buffered = []
    fts_rows = []
    for record in records:
        category = record.get("category") or record.get("kind") or "misc"
        dataset = record.get("dataset") or source_id
        name = record["name"]
        summary = record.get("summary", "")
        tags = record.get("tags", [])
        details = record.get("details", {})
        entry_id = record.get("entry_id") or f"{source_id}:{slugify(name)}"
        buffered.append(
            (
                entry_id,
                dataset,
                category,
                name,
                summary,
                json.dumps(tags, ensure_ascii=True),
                json.dumps(details, ensure_ascii=True),
                source_name,
                url,
                license_text,
                now,
            )
        )
        fts_rows.append((entry_id, name, summary, " ".join(tags), json.dumps(details, ensure_ascii=True)))
        count += 1

    conn.executemany(
        """
        INSERT OR REPLACE INTO entries (
            entry_id, dataset, category, name, summary, tags_json, details_json,
            source_name, source_url, license, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        buffered,
    )
    try:
        conn.executemany(
            "INSERT OR REPLACE INTO entries_fts(entry_id, name, summary, tags, details) VALUES (?, ?, ?, ?, ?)",
            fts_rows,
        )
    except sqlite3.OperationalError:
        pass
    conn.execute(
        "INSERT OR REPLACE INTO sources(source_id, name, kind, url, license, fetched_at, record_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (source_id, source_name, kind, url, license_text, now, count),
    )
    conn.commit()
    return count


def format_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=True)


def load_session(base_dir: Path, session_id: str) -> dict[str, Any]:
    return read_json(sessions_dir(base_dir) / session_id / "session.json")


def session_path(base_dir: Path, session_id: str) -> Path:
    return sessions_dir(base_dir) / session_id


def list_sessions(base_dir: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(sessions_dir(base_dir).glob("*/session.json"), reverse=True):
        payload = read_json(path)
        payload["path"] = str(path.parent)
        items.append(payload)
    return items


def generate_session_id(theme: str, tone: str, request: str) -> str:
    date_stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    theme_slug = slugify(theme or tone or "run")[:24]
    token = short_hash(f"{theme}|{tone}|{request}|{utc_now()}")
    return f"{date_stamp}-{theme_slug}-{token}"


def rng(seed: str | None = None) -> random.Random:
    return random.Random(seed)
