#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cyberpunk_lib import (
    append_text,
    format_json,
    generate_session_id,
    list_sessions,
    load_session,
    resolve_base_dir,
    session_path,
    slugify,
    utc_now,
    write_json,
    write_text,
)


def create_session(base_dir: Path, theme: str, tone: str, player_request: str) -> dict:
    session_id = generate_session_id(theme, tone, player_request)
    root = session_path(base_dir, session_id)
    for folder in [root / "characters", root / "locations", root / "events", root / "rolls"]:
        folder.mkdir(parents=True, exist_ok=True)

    now = utc_now()
    payload = {
        "session_id": session_id,
        "created_at": now,
        "updated_at": now,
        "theme": theme,
        "tone": tone,
        "player_request": player_request,
        "status": "active",
        "clocks": [],
        "threads": [],
        "factions": [],
        "leads": [],
        "notes": [],
    }
    write_json(root / "session.json", payload)
    write_text(
        root / "story.md",
        (
            f"# Story Log: {session_id}\n\n"
            f"- Theme: {theme}\n"
            f"- Tone: {tone}\n"
            f"- Player Request: {player_request}\n\n"
            "## Opening Frame\n\n"
            "Session created. Add the opening scene here.\n"
        ),
    )
    write_text(root / "timeline.md", f"# Timeline: {session_id}\n\n- {now}: Session created.\n")
    write_text(
        root / "gm-notes.md",
        (
            "# GM Notes\n\n"
            "## Pressure\n\n"
            "- Identify who benefits if the crew fails.\n\n"
            "## Hooks\n\n"
            "- Add the first twist after the opener lands.\n"
        ),
    )
    write_text(root / "characters" / "index.md", "# Character Dossiers\n\n- Add major character files in this directory.\n")
    write_text(root / "locations" / "index.md", "# Location Dossiers\n\n- Add major location files in this directory.\n")
    write_text(root / "events" / "index.md", "# Event Dossiers\n\n- Add mission beats and major events in this directory.\n")
    write_text(root / "rolls" / "index.md", "# Roll Log\n\n- JSON roll records are written to this directory.\n")
    return {"session_id": session_id, "path": str(root), "session": payload}


def show_session(base_dir: Path, session_id: str) -> dict:
    root = session_path(base_dir, session_id)
    payload = load_session(base_dir, session_id)
    return {
        "session": payload,
        "path": str(root),
        "files": sorted(str(path) for path in root.rglob("*") if path.is_file()),
    }


def note_session(base_dir: Path, session_id: str, note: str, section: str) -> dict:
    session = load_session(base_dir, session_id)
    session.setdefault("notes", []).append(note)
    session["updated_at"] = utc_now()
    write_json(session_path(base_dir, session_id) / "session.json", session)
    append_text(session_path(base_dir, session_id) / f"{section}.md", f"\n- {session['updated_at']}: {note}\n")
    return {"session_id": session_id, "updated_at": session["updated_at"], "note": note, "section": section}


def add_clock(base_dir: Path, session_id: str, name: str, max_value: int, value: int) -> dict:
    session = load_session(base_dir, session_id)
    session.setdefault("clocks", []).append({"name": name, "value": value, "max": max_value})
    session["updated_at"] = utc_now()
    write_json(session_path(base_dir, session_id) / "session.json", session)
    return {"session_id": session_id, "clock": {"name": name, "value": value, "max": max_value}}


def record_roll(base_dir: Path, session_id: str, label: str, payload: str) -> dict:
    root = session_path(base_dir, session_id) / "rolls"
    stamp = utc_now().replace(":", "-")
    path = root / f"{stamp}-{label.replace(' ', '-').lower()}.json"
    content = json.loads(payload)
    write_json(path, content)
    return {"session_id": session_id, "path": str(path)}


def write_dossier(base_dir: Path, session_id: str, entity_type: str, name: str, body: str) -> dict:
    folder_map = {
        "character": "characters",
        "location": "locations",
        "event": "events",
    }
    folder = session_path(base_dir, session_id) / folder_map[entity_type]
    path = folder / f"{slugify(name)}.md"
    content = f"# {name}\n\n{body.strip()}\n"
    write_text(path, content)

    index_path = folder / "index.md"
    index_entry = f"- [{name}]({path.name})\n"
    if index_path.exists():
        current = index_path.read_text(encoding="utf-8")
        if index_entry not in current:
            append_text(index_path, index_entry)
    return {"session_id": session_id, "path": str(path), "entity_type": entity_type, "name": name}


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage isolated cyberpunk-runner sessions.")
    parser.add_argument("--base-dir", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("--theme", required=True)
    create.add_argument("--tone", required=True)
    create.add_argument("--player-request", required=True)

    subparsers.add_parser("list")

    show = subparsers.add_parser("show")
    show.add_argument("--session-id", required=True)

    note = subparsers.add_parser("note")
    note.add_argument("--session-id", required=True)
    note.add_argument("--section", choices=["story", "timeline", "gm-notes"], default="timeline")
    note.add_argument("--note", required=True)

    clock = subparsers.add_parser("add-clock")
    clock.add_argument("--session-id", required=True)
    clock.add_argument("--name", required=True)
    clock.add_argument("--max", type=int, default=6)
    clock.add_argument("--value", type=int, default=0)

    roll = subparsers.add_parser("record-roll")
    roll.add_argument("--session-id", required=True)
    roll.add_argument("--label", required=True)
    roll.add_argument("--payload", required=True, help="JSON string returned by dice.py")

    dossier = subparsers.add_parser("write-dossier")
    dossier.add_argument("--session-id", required=True)
    dossier.add_argument("--entity-type", choices=["character", "location", "event"], required=True)
    dossier.add_argument("--name", required=True)
    dossier.add_argument("--body", required=True)

    args = parser.parse_args()
    base_dir = resolve_base_dir(args.base_dir)

    if args.command == "create":
        payload = create_session(base_dir, args.theme, args.tone, args.player_request)
    elif args.command == "list":
        payload = {"sessions": list_sessions(base_dir)}
    elif args.command == "show":
        payload = show_session(base_dir, args.session_id)
    elif args.command == "note":
        payload = note_session(base_dir, args.session_id, args.note, args.section)
    elif args.command == "add-clock":
        payload = add_clock(base_dir, args.session_id, args.name, args.max, args.value)
    elif args.command == "write-dossier":
        payload = write_dossier(base_dir, args.session_id, args.entity_type, args.name, args.body)
    else:
        payload = record_roll(base_dir, args.session_id, args.label, args.payload)

    print(format_json(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
