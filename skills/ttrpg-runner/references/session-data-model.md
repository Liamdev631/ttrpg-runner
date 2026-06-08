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
- `secrets.md`

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
  "player_character_refs": [
    {
      "user_id": "112233445566778899",
      "username": "liamb",
      "slug": "rook-vale",
      "name": "Rook Vale",
      "concept": "ex-clinic courier"
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

- Character files are **markdown** (`characters/<slug>.md`) and are the canonical sheets. Plain text, no JSON parsing on the hot path.
- The markdown template lives at `templates/character.md`. Pack-specific stat labels replace the `STAT_*` placeholders; everything else stays the same shape across packs.
- `session.json > player_character_refs` is a routing table only: it carries `user_id`, `username`, `slug`, `name`, and a one-line `concept` so the GM can identify whose turn it is. It does **not** mirror the full sheet.
- The exact stat labels and genre details should match the active flavor pack or the unsupported game's agreed system.
- Pack-specific fields such as `mistborn_era` are allowed when the active flavor pack needs them.
- Shared sections such as `Stats`, `Derived`, `Skills`, `Progression`, `Inventory`, `Special Features`, and status tracking should stay consistent across packs, even though they live in markdown.
- `Inventory` and `Special Features` are intentionally generic so each pack can interpret them in setting-appropriate ways.

## Source Of Truth

Character data has one and only one storage location: the markdown file at `characters/<slug>.md`.

- Read the markdown file when the GM needs the full sheet.
- The `player_character_refs` array in `session.json` is the lightweight routing table for "who is playing which character". It is not a copy of the sheet and is allowed to drift from it; if it does, fix the markdown and rewrite only the ref.
- Never store stats, skills, derived values, inventory, or XP in `session.json`. Those belong in the markdown file and only the markdown file.
- Companion pokemon and recurring NPCs also live as `characters/<slug>.md` files, using the same template with the `Kind` field set to `companion` or `npc`. No separate NPC schema.

## Secrets File

`secrets.md` is the GM-only ledger for facts that must never reach player-facing chat: hidden NPC agendas, true identities, secret faction goals, planted evidence, ticking bombs the GM is holding, and the real reason a scene is the way it is. It is seeded from `templates/secrets.md`, lives next to `gm-notes.md`, and is read by the GM, not the table.

- One entry per secret, with a stable title the GM can reference in private planning.
- Each entry carries a status (`dormant`, `active`, `about_to_fire`, `resolved`), the surface cover the players currently believe, the reveal trigger, and the consequences if the secret is exposed.
- Burned or fired secrets get archived in the `Burned Secrets` section of the same file so the GM can audit the twist budget without re-using the same beat.
- Treat `secrets.md` as out-of-band GM memory. It is allowed to be read and written by the GM during a turn, but its contents must never be echoed, paraphrased, or spoiler-tagged into a player-visible message.

## Isolation Boundary

The session directory is the authoritative context boundary for play.
If the user wants a fresh game, create a fresh session directory.
If the user wants to resume, load exactly one saved session directory unless they explicitly request a crossover.
A `secrets.md` from a prior session never carries over into a new session. Every new session gets its own blank secrets file.
