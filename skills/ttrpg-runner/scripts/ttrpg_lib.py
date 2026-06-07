#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE_DIR = Path("~/.hermes/ttrpg-runner").expanduser()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or "session"


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


def sessions_dir(base_dir: Path) -> Path:
    return ensure_dir(base_dir / "sessions")


def flavorpacks_dir() -> Path:
    return resolve_skill_root() / "flavorpacks"


def supported_flavor_packs() -> list[str]:
    packs = []
    for path in sorted(flavorpacks_dir().iterdir()):
        if path.is_dir():
            packs.append(path.name)
    return packs


def normalize_flavor_pack(flavor_pack: str) -> str:
    normalized = slugify(flavor_pack).replace("-", "")
    aliases = {
        "cyberpunk": "cyberpunk",
        "dnd": "dnd",
        "dungeonsdragons": "dnd",
        "mistborn": "mistborn",
        "mistbornadventuregame": "mistborn",
        "scadrial": "mistborn",
        "scadrian": "mistborn",
        "pokemon": "pokemon",
        "theexpanse": "expanse",
        "expanse": "expanse",
    }
    canonical = aliases.get(normalized, slugify(flavor_pack))
    if canonical not in supported_flavor_packs():
        supported = ", ".join(supported_flavor_packs())
        raise ValueError(f"Unsupported flavor pack '{flavor_pack}'. Supported packs: {supported}")
    return canonical


def flavor_pack_root(flavor_pack: str) -> Path:
    return flavorpacks_dir() / normalize_flavor_pack(flavor_pack)


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
