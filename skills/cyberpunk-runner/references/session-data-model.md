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
  "player_character": {
    "name": "Rook Vale",
    "concept": "ex-clinic ripperdoc turned courier",
    "stats": {
      "BOD": 4, "REF": 4, "TEK": 3, "INT": 3, "COO": 2, "CHA": 2
    },
    "skills": [
      {"path": "REF/Shoot", "rank": 3},
      {"path": "TEK/Ripperdoc", "rank": 2},
      {"path": "CHA/Persuade", "rank": 1}
    ],
    "derived": {
      "hp": 8,
      "evasion": 4,
      "composure": 2,
      "street_cred": 0
    },
    "cyberware": ["Mantis blades", "Subdermal armor (light)", "Kiroshi optics mk.3"],
    "level": 1,
    "xp": 0,
    "xp_to_next_level": 10,
    "xp_log": [
      {"amount": 2, "reason": "Survived the Morrow Array ambush", "at": "2026-06-04T01:15:00Z"}
    ],
    "skill_entries": [
      {
        "path": "REF/Shoot",
        "rank": 3,
        "description": "Fast, accurate fire with sidearms, SMGs, and assault rifles.",
        "frequency": "at-will",
        "effect": "+3 to all REF/Shoot red-checks; may fire twice in a single Action Phase at rank 3+.",
        "limitations": "Requires a readied ranged weapon. Suppressive fire or called shots still demand a roll."
      }
    ],
    "status": "alive"
  },
  "clocks": [
    {"name": "Clinic lockdown", "value": 1, "max": 6}
  ],
  "threads": [
    "Who sold the route?"
  ],
  "factions": [
    {"name": "Morrow Array", "stance": "hostile", "heat": 2, "reputation": -1}
  ],
  "leads": [
    "Damaged courier drone with partial route data"
  ],
  "ad_hooks": [
    {"brand": "Bluepill Express", "tag": "1-800-BLU-DICK", "hint": "Possible front for ripperdoc black market"}
  ],
  "notes": [
    "Player favors stealth over open war"
  ]
}
```

The `player_character` block is the agent's reference for every stat-aware `red-check` — pick the stat and skill by `path` (e.g. `REF/Shoot`) and pass both numbers to `dice.py`. The `ad_hooks` array tracks brand names, contact numbers, and addresses the agent has dropped into ad crawls so the player can chase them later.

`xp` is awarded in the background by the agent; when it reaches `xp_to_next_level` (default `10`) a level-up fires. The agent then updates `level`, resets `xp`, and lets the player pick from the three-path choice (background skills, random skills, or a direct request — see SKILL.md "XP & Leveling"). Every skill on the player or any NPC must also live in `skill_entries` with `description`, `frequency`, `effect`, and `limitations` so the dossier and the JSON stay in lockstep.

## Dossier Conventions

Each entity gets its own file in the matching subfolder. **Character files are JSON**; location and event files are markdown. The character JSON is the canonical sheet, and `session.json > player_character` is a denormalized mirror of the player's character JSON so the agent can look up stats without re-parsing the file.

### Character files (`characters/<slug>.json`)

- One JSON file per important character (player and NPCs).
- Build the file from `templates/character.json` so every field is present and `skill_entries` lines up with the `skills` array.
- `slug` should be a stable, file-safe identifier (e.g. `rook-vale`, not `Rook Vale!`).
- The full schema (stats, derived, skills, cyberware, `xp_log`, `skill_entries`, hooks, secrets, relationship notes) lives in `templates/character.json`; treat it as the contract.
- `characters/index.md` is a short markdown roll-call of every character file, kept in sync as characters are created or retired.

### Location and event files (markdown)

- `locations/<slug>.md` — neighborhood, corp HQ, club, transit line, hideout — anything with a name.
- `events/<slug>.md` — a mission beat, a heist, a betrayal, a public incident.
- Use the matching starter template (`templates/location.md`, `templates/event.md`) and fill it in.

### Player-character mirroring

When the player sheet changes (HP, evasion, composure, street cred, level, XP, skills, `skill_entries`, status), update **both**:

- `characters/<player-slug>.json` — the canonical player dossier
- `session.json > player_character` — the denormalized session-scoped view used for stat-aware checks and quick lookups

The two files must agree at all times. If they drift, prefer the player JSON as the source of truth and rewrite the `player_character` block from it.

## Isolation Boundary

The session directory is the authoritative context boundary for play.
If the user wants a fresh game, create a fresh session directory.
If the user wants to resume, load exactly one saved session directory unless they explicitly request a crossover.
