# Session Data Model

Each session lives under:

```text
<base-dir>/sessions/<session-id>/
```

## Required Files

- `session.json`: structured state for programmatic updates
- `story.md`: rich narrative recap and running fiction
- `timeline.md`: concise bullet chronology
- `gm-notes.md`: hidden planning notes, stakes, and future hooks

## Required Directories

- `characters/`
- `locations/`
- `events/`
- `rolls/`

## session.json Shape

```json
{
  "session_id": "20260604-neon-ashes-a1b2c3",
  "created_at": "2026-06-04T00:00:00Z",
  "updated_at": "2026-06-04T00:00:00Z",
  "theme": "stolen biometric vault",
  "tone": "neon-noir",
  "player_request": "Run a one-shot about a black clinic extraction.",
  "status": "active",
  "clocks": [
    {"name": "Clinic lockdown", "value": 1, "max": 6}
  ],
  "threads": [
    "Who sold the route?"
  ],
  "factions": [
    {"name": "Morrow Array", "stance": "hostile", "heat": 2}
  ],
  "leads": [
    "Damaged courier drone with partial route data"
  ],
  "notes": [
    "Player favors stealth over open war"
  ]
}
```

## Dossier Conventions

Character, location, and event files are markdown so Hermes can read and edit them naturally.

Use one file per important entity with a slug filename such as:

- `characters/rook-vale.md`
- `locations/glass-canal-night-market.md`
- `events/clinic-extraction-goes-loud.md`

## Isolation Boundary

The session directory is the authoritative context boundary for play.
If the user wants a fresh game, create a fresh session directory.
If the user wants to resume, load exactly one saved session directory unless they explicitly request a crossover.
