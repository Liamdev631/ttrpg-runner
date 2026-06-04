# Source Manifest

`cyberpunk-runner` installs a local knowledge base from two layers.

## Layer 1: Bundled Open Data Packs

These ship inside the repository under `assets/seed_data/` and are always available offline.
They cover cyberpunk-friendly material such as:

- factions and megacorps
- districts and landmarks
- gigs and mission structures
- cyberware and street tech
- rumors, slang, ads, weather, and complications
- names and identity fragments

The bundled packs are original/openly shareable and intended for improvisational play.

## Layer 2: Optional Public Enrichment

`scripts/bootstrap_sources.py` can optionally fetch public summaries from internet sources listed in `assets/public_sources.json`.
These enrich the local database with high-level genre context without blocking gameplay.

By default the current enrichment profile includes Wikipedia summary endpoints for genre topics such as:

- Cyberpunk
- Megacorporation
- Dystopia
- Cyberware
- Virtual reality
- Artificial intelligence
- Hacker culture

If public enrichment fails due to rate limits or missing network access, the skill still works from the bundled data packs.

## Database Output

Bootstrap writes a SQLite database to:

```text
<base-dir>/knowledge/cyberpunk.db
```

The database stores a normalized `entries` table plus an optional full-text search table when SQLite FTS5 is available.
