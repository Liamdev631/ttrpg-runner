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
  "player_request": "Run a Discord one-shot about a black clinic extraction for two runners.",
  "status": "active",
  "players": [
    {
      "user_id": "112233445566778899",
      "username": "liamb",
      "display_name": "Liam",
      "character_slug": "rook-vale"
    },
    {
      "user_id": "998877665544332211",
      "username": "case",
      "display_name": "Case",
      "character_slug": "nyx-sable"
    }
  ],
  "player_characters": [
    {
      "user_id": "112233445566778899",
      "username": "liamb",
      "slug": "rook-vale",
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
    {
      "user_id": "998877665544332211",
      "username": "case",
      "slug": "nyx-sable",
      "name": "Nyx Sable",
      "concept": "burned netrunner with a talent for synthetic identities",
      "stats": {
        "BOD": 2, "REF": 3, "TEK": 5, "INT": 4, "COO": 3, "CHA": 2
      },
      "skills": [
        {"path": "TEK/Netrun", "rank": 3},
        {"path": "INT/Research", "rank": 2},
        {"path": "COO/Stealth", "rank": 1}
      ],
      "derived": {
        "hp": 6,
        "evasion": 3,
        "composure": 3,
        "street_cred": 0
      },
      "cyberware": ["Deck interface plugs", "Ghost-mask subdermals"],
      "level": 1,
      "xp": 0,
      "xp_to_next_level": 10,
      "xp_log": [],
      "skill_entries": [],
      "status": "alive"
    }
  ],
  "party": {
    "relationship_model": "former crew",
    "how_they_met": "Rook once patched Nyx up after a botched data theft, and they have kept each other alive ever since.",
    "shared_hooks": [
      "Both owe favors to the same fixer",
      "Both distrust Morrow Array"
    ]
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

The `players` array is the human-participant registry. Use it to map Discord user IDs and usernames to stable `character_slug` values before applying any request, consequence, inventory use, XP award, or dice check. The `player_characters` array is the agent's quick-reference mirror for stat-aware `red-check` calls — pick the right runner first, then pick the stat and skill by `path` (e.g. `REF/Shoot`) and pass both numbers to `dice.py`. The `ad_hooks` array tracks brand names, contact numbers, and addresses the agent has dropped into ad crawls so the players can chase them later.

`xp` is awarded in the background by the agent on a per-runner basis; when a runner reaches `xp_to_next_level` (default `10`) a level-up fires for that specific character. The agent then updates `level`, resets `xp`, and lets that player pick from the three-path choice (background skills, random skills, or a direct request — see SKILL.md "XP & Leveling"). Every skill on any player or NPC must also live in `skill_entries` with `description`, `frequency`, `effect`, and `limitations` so the dossiers and the JSON stay in lockstep.

## Dossier Conventions

Each entity gets its own file in the matching subfolder. **Character files are JSON**; location and event files are markdown. Character JSON files are the canonical sheets, and `session.json > player_characters` is a denormalized mirror of the player-character dossiers so the agent can look up stats without re-parsing the files.

### Character files (`characters/<slug>.json`)

- One JSON file per important character (player and NPCs).
- Build the file from `templates/character.json` so every field is present and `skill_entries` lines up with the `skills` array.
- `slug` should be a stable, file-safe identifier (e.g. `rook-vale`, not `Rook Vale!`).
- The full schema (stats, derived, skills, cyberware, `xp_log`, `skill_entries`, hooks, secrets, relationship notes) lives in `templates/character.json`; treat it as the contract.
- `characters/index.md` is a short markdown roll-call of every character file, kept in sync as characters are created or retired.
- If the character belongs to a Discord player, `session.json > players` should also contain that player's `user_id`, `username`, and `character_slug`.

### Location and event files (markdown)

- `locations/<slug>.md` — neighborhood, corp HQ, club, transit line, hideout — anything with a name.
- `events/<slug>.md` — a mission beat, a heist, a betrayal, a public incident.
- Use the matching starter template (`templates/location.md`, `templates/event.md`) and fill it in.

### Player-character mirroring

When a player-character sheet changes (HP, evasion, composure, street cred, level, XP, skills, `skill_entries`, status), update **both**:

- `characters/<player-slug>.json` — the canonical player dossier
- the matching object in `session.json > player_characters` — the denormalized session-scoped view used for stat-aware checks and quick lookups

The two representations must agree at all times. If they drift, prefer the player JSON as the source of truth and rewrite the matching `player_characters` entry from it. In multi-player Discord sessions, also verify that `session.json > players` still points the correct `user_id` at the correct `character_slug`.

## Isolation Boundary

The session directory is the authoritative context boundary for play.
If the user wants a fresh game, create a fresh session directory.
If the user wants to resume, load exactly one saved session directory unless they explicitly request a crossover.
