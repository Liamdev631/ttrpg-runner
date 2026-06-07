# Session Data Model

Each session lives under:

```text
<base-dir>/sessions/<session-id>/
```

## Required Files

- `session.json`
- `story.md`
- `timeline.md`
- `gm-notes.md`

## Required Directories

- `characters/`
- `locations/`
- `events/`
- `rolls/`

## session.json Shape

```json
{
  "session_id": "20260607-rusted-choir-a1b2c3",
  "created_at": "2026-06-07T00:00:00Z",
  "updated_at": "2026-06-07T00:00:00Z",
  "game": "cyberpunk",
  "flavor_pack": "cyberpunk",
  "support_level": "native",
  "mistborn_era": null,
  "theme": "stolen biotech manifest",
  "tone": "tense and cinematic",
  "player_request": "Run a one-shot for two players.",
  "status": "active",
  "players": [
    {
      "user_id": "112233445566778899",
      "username": "liamb",
      "display_name": "Liam",
      "character_slug": "rook-vale"
    }
  ],
  "player_characters": [
    {
      "user_id": "112233445566778899",
      "username": "liamb",
      "slug": "rook-vale",
      "name": "Rook Vale",
      "concept": "ex-clinic courier",
      "stats": {
        "REF": 4,
        "TEK": 3,
        "COO": 3,
        "BOD": 2,
        "INT": 2,
        "CHA": 2
      },
      "skills": [
        {"path": "REF/Firearms", "rank": 2}
      ],
      "derived": {
        "hp": 6,
        "defense": 4,
        "stress": 3,
        "reputation": 0
      },
      "inventory": ["heavy pistol", "medkit"],
      "special_features": ["targeting optics"],
      "level": 1,
      "xp": 0,
      "xp_to_next_level": 10,
      "xp_log": [],
      "skill_entries": [],
      "status": "active"
    }
  ],
  "party": {
    "relationship_model": "former crew",
    "how_they_met": "They survived a failed pickup together.",
    "shared_hooks": ["Both distrust the fixer who hired them last time"]
  },
  "clocks": [
    {"name": "Security sweep", "value": 1, "max": 6}
  ],
  "threads": ["Who leaked the route?"],
  "factions": [
    {"name": "Morrow Array", "stance": "hostile", "heat": 2, "reputation": -1}
  ],
  "leads": ["Damaged courier drone with route residue"],
  "notes": ["Player favors stealth over direct conflict"]
}
```

## Dossier Conventions

- Character files are JSON and are the canonical sheets.
- `session.json > player_characters` is a denormalized mirror for quick lookup during play.
- The exact stat labels and genre details should match the active flavor pack or the unsupported game's agreed system.
- Pack-specific fields such as `mistborn_era` are allowed when the active flavor pack needs them.
- Shared fields such as `skills`, `derived`, `xp_log`, `skill_entries`, and status tracking should stay consistent across packs.
- `inventory` and `special_features` are intentionally generic so each pack can interpret them in setting-appropriate ways.

## Mirroring Rule

When a player-character sheet changes, update both:

- `characters/<player-slug>.json`
- the matching object in `session.json > player_characters`

If they drift, prefer the player JSON as the source of truth and rewrite the session mirror from it.

## Isolation Boundary

The session directory is the authoritative context boundary for play.
If the user wants a fresh game, create a fresh session directory.
If the user wants to resume, load exactly one saved session directory unless they explicitly request a crossover.
