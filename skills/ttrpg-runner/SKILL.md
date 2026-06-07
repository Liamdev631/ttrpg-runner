---
name: ttrpg-runner
description: Run an isolated tabletop RPG session with shared dice tools, persistent dossiers, and setting-specific flavor packs.
version: 2.0.0
author: OpenAI
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [games, tabletop, storytelling, simulation, python, ttrpg]
    category: games
    config:
      - key: ttrpg_runner.base_dir
        description: Root directory for ttrpg-runner saved sessions.
        default: "~/.hermes/ttrpg-runner"
        prompt: Directory for ttrpg-runner data
      - key: ttrpg_runner.default_tone
        description: Default session tone when the player does not specify one.
        default: "adventurous"
        prompt: Default campaign tone
---

# TTRPG Runner

Run a fresh tabletop RPG session with strict per-session memory isolation and explicit flavor-pack boundaries.

## Native Support

`/ttrpg-runner` should tell the player, early and plainly, that these settings are natively supported:

- `cyberpunk`
- `dnd`
- `mistborn`
- `pokemon`
- `expanse`

If the requested game is outside that list, say that any TTRPG is still possible but the session will run with reduced features: no native flavor pack and no pack-specific reference set.

## Flavor Pack Loading Rules

These rules are mandatory and exist to stop cross-setting contamination.

- Determine the requested setting before you worldbuild. If the player has not named a setting, ask.
- If the setting matches one native pack, load only `flavorpacks/<pack>/PACK.md` for that pack.
- Only read deeper pack references from the same pack, and only when they are actually needed.
- Never read, quote, or blend material from any other pack during that session.
- If the player says `cyberpunk`, do not load `pokemon`. If they say `pokemon`, do not load `dnd`. One pack only.
- If the player changes settings mid-conversation, stop and confirm whether they want to abandon the current session and start a new one.
- Unsupported settings run in generic mode. Do not load native-pack reference docs in generic mode.
- If the player wishes to merge two settings, explain that this leaves native-pack mode. Stay in generic unsupported mode unless the user explicitly wants a custom crossover session.

## When to Use

Use this skill when the player wants to:

- start a new one-shot or campaign in a native pack or in a generic unsupported setting
- roll dice or resolve checks during play
- keep persistent story records for the current session only
- resume a previously saved session by explicit request
- generate setting-faithful hooks, NPCs, factions, locations, rumors, or complications without mixing settings

## First Principles

- Treat `/ttrpg-runner` as a session bootstrap command.
- Unless the player explicitly says `resume`, `load`, `continue`, or names an existing session, create a brand new isolated play session.
- Never mix data from other saved sessions into the current session.
- Hermes reads and writes the active session's files directly with its file tools. There is no controller layer.
- Shared Python helpers (`dice.py`, `ttrpg_lib.py`) are available for dice rolling and lightweight filesystem/session helpers.
- Keep the fiction system-inspired and genre-faithful without quoting proprietary rulebooks as if they were bundled in the repo.
- Do not rely on bundled seed libraries of names, quests, rumors, events, or NPCs. Those were intentionally removed to prevent repeated content across sessions.
- Do not use a database, bootstrap pipeline, or online-downloaded search index for pack knowledge.
- If curated external reference material is ever added to the repo, store it as markdown with source citations at the top of the file.
- Support both solo play and multiplayer play. If multiple Discord users are in the session, track exactly which human maps to which character slug.
- Wait for the player to explicitly authorize play before opening the first scene, narrating fiction, or rolling dice. Finishing setup, confirming the setting, or completing character creation is not a green light to begin.
- During character creation, always offer one or more suggested initial loadouts (starting gear, resources, and any setting-specific kits) that the player can accept, modify, or reject. Do not finish a character without surfacing concrete starting options for the player to react to.

## Skill Layout

```text
skills/ttrpg-runner/
  SKILL.md
  references/
    session-data-model.md
    discord-formatting.md
  templates/
    ad-crawl.md
    character.json
    event.md
    location.md
    session-summary.md
  scripts/
    dice.py
    ttrpg_lib.py
  flavorpacks/
    cyberpunk/
      PACK.md
      references/
    dnd/...
    mistborn/...
    pokemon/...
    expanse/...
```

## Active Session Directory

Configured `ttrpg_runner.base_dir` (default `~/.hermes/ttrpg-runner`) is the root.

```text
<base-dir>/
  sessions/
    <session-id>/
      session.json
      story.md
      timeline.md
      gm-notes.md
      characters/
      locations/
      events/
      rolls/
```

## What Lives Where

- `session.json`: structured state, active game metadata, clocks, threads, factions, leads, player registry, and player-character mirrors.
- `story.md`: running fiction and scene recap.
- `timeline.md`: concise beat-by-beat chronology.
- `gm-notes.md`: hidden planning notes, stakes, and hooks.
- `characters/<slug>.json`: canonical sheets for PCs and important NPCs.
- `locations/<slug>.md`: named places with sensory details and hidden layers.
- `events/<slug>.md`: missions, incidents, betrayals, and turning points.
- `rolls/<stamp>-<label>.json`: optional audit trail for important dice calls.

## Procedure

1. Establish the table and the game.
   Ask whether the player wants solo or multiplayer play, then identify the requested setting before you start creating content.
   If the setting is `mistborn`, ask for `Era 1` or `Era 2` before character creation or worldbuilding.
   Do not open the first scene, narrate fiction, or roll dice until the player has explicitly said `start`, `begin`, `go`, or otherwise authorized play. Finishing setup, confirming the setting, building the character roster, or completing character creation is not a green light to begin the story. When in doubt, ask before you narrate.
   When you walk the player through character creation, propose at least one suggested initial loadout (starting gear, resources, and any setting-specific kits such as Mistborn metals, Cyberpunk cyberware, or DND 5e starting equipment) and let the player accept, modify, or swap it. Surface this offer before the character sheet is locked so the player always has concrete starting options on the table.

2. Resolve native support.
   If the setting is `cyberpunk`, `dnd`, `mistborn`, `pokemon`, or `expanse`, say it is natively supported and load only that pack's `PACK.md`.
   If it is anything else, say the game is still possible with reduced features and stay in generic mode.

3. Resolve the base directory.
   Use configured `ttrpg_runner.base_dir` if supplied. Otherwise use `~/.hermes/ttrpg-runner`.

4. Load native-pack references only when needed.
   For native packs, read only the active pack's docs.
   Start with `flavorpacks/<pack>/PACK.md`, then open deeper markdown files from the same pack only when the current turn actually needs them.
   If the active pack is `mistborn`, read `flavorpacks/mistborn/references/era-rules.md` immediately after `PACK.md` and before opening imported source files.
   Also load `references/discord-formatting.md` once per session so player-facing messages render with Discord-native markdown.

5. Create or resume a session by hand.
   Hermes manages the session directory directly with its file tools.

   - New session: create a fresh `<session-id>` folder and seed `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories.
   - Resume flow: list the saved sessions, let the player choose one, then read only that session's files.

6. Record the chosen game in `session.json`.
   Always store:

   - `game`: the human-facing name the player asked for
   - `flavor_pack`: the active native pack name, or `null` for unsupported games
   - `support_level`: `native` or `reduced`
   - `mistborn_era`: `era1` or `era2` when the active pack is `mistborn`; otherwise `null`

7. Run the game by editing the active session's files.
   On every turn:

   - Read `session.json` first.
   - Skim `story.md` and `timeline.md` for continuity.
   - Identify the active speaker in multiplayer sessions before applying any request.
   - Use `scripts/dice.py` for risky or uncertain actions.
   - For native packs only, consult the active pack's markdown references when you need tone, gameplay cadence, or a curated fact reminder.
   - If a markdown reference file includes external material, keep the citations block at the top intact when you update it.
   - Format every player-facing message with Discord-native markdown per `references/discord-formatting.md`. Dice cards go in fenced code blocks, NPC speech in block quotes, and scene openings under `###` headings.
   - Write the resulting state changes back into the active session files.

8. Close each turn with a game-facing handoff.
   Summarize what changed, what the player can do next, and what pressures or leads are now in motion.

## Session Isolation Rules

These rules are non-negotiable.

- Every new invocation creates a brand-new session folder unless the player explicitly resumes one.
- Never read another session's files on your own.
- Never quote, paraphrase, or carry over prior-session content into a fresh session.
- The active session directory is the only authoritative memory for the current run.
- A native pack's markdown references are reference material only, never a hidden source of prior-session canon.
- If a leak occurs, acknowledge it, scrub it from the current session files, and continue using only the active session and the active pack.

## Discord Output Formatting

All player-facing output is rendered into Discord. Every message should use Discord-native markdown so it reads clean in chat.

- The full Discord formatting reference lives at `references/discord-formatting.md`. Read it before composing the first message of a session.
- Open every scene response with a `###` heading that names the beat.
- Use `-#` for ambient context (time, place, weather) the player can skim.
- Bold the most important noun or verb in each paragraph of fiction.
- Use `>` block quotes for NPC speech and the GM voice.
- Use fenced code blocks for dice cards, stat blocks, and any JSON state.
- Use `||...||` spoilers for plot twists, hidden NPC intentions, and GM-only notes that leak into a shared channel.
- Do not use Discord tables. Use bullet lists or code blocks instead.
- Keep each message scannable in under five seconds. Split anything longer than ten short paragraphs across multiple messages.
- Do not paste prose inside code blocks expecting it to be formatted. Code blocks cancel every other markdown rule.

### Discord-Specific Gotchas To Avoid

- `__text__` is **underline**, not bold. Always use `**text**` for bold.
- Headings, subtext, and list markers must be the first non-whitespace character on a line, followed by a single space.
- Spoiler tags and inline code cancel every other formatting inside them.
- Do not try to embed a list inside a code block or a code block inside a list item. Compose the dice card and the fiction in separate messages when both are needed.

## Dice And Roll Interleaving

The dice tool is the numerical authority in play.

- When in doubt, roll.
- Narrate a short setup beat, call `scripts/dice.py`, then continue the scene after reading the tool output.
- Never pre-write a risky action's outcome and then roll to justify it.
- Always cite the stat and skill being rolled so the player can audit the call.
- Pure description and zero-stakes color do not need a roll.
- Use `scripts/dice.py roll <expression>` for generic dice expressions.
- Use `scripts/dice.py red-check --stat <stat> --skill <skill> --modifier <mod> --difficulty <dc>` for fast checks.
- Use `scripts/dice.py opposed --attacker <bonus> --defender <bonus>` for direct contests.

## Roll Display Format

Each roll shown to the player should be rendered as a single fenced code block using a consistent box shape. ASCII is preferred for portability.

When the roll is the centerpiece of a beat, wrap the code block in Discord-native chrome so the player can read the math, the meaning, and the consequences in one screen.

`red-check`:

````text
**REF / Stealth vs DC 12**

```
=======================================
  CHECK * <STAT>/<Skill> <rank> vs DC <difficulty>
---------------------------------------
  Difficulty : <difficulty>
  d10        : <die>
  Stat       : <stat>
  Skill      : <skill>
  Modifier   : <+|-><modifier>
---------------------------------------
  TOTAL      : <total>
  OUTCOME    : <STRONG SUCCESS | SUCCESS | FAILURE | HARD FAILURE>
=======================================
```

> <one-sentence narrative consequence, in the GM voice>
````

`opposed`:

````text
**Melee Clash: BOD/Fight 4 vs BOD/Fight 3**

```
=======================================
  OPPOSED * <A_STAT>/<A_Skill> vs <D_STAT>/<D_Skill>
---------------------------------------
  ATTACKER  : <die + bonus = total>
  DEFENDER  : <die + bonus = total>
---------------------------------------
  WINNER    : <ATTACKER | DEFENDER | TIE>
=======================================
```

> <one-sentence narrative consequence, in the GM voice>
````

`roll`:

````text
**Wild Die: 2d6+1**

```
=======================================
  ROLL * <expression>
---------------------------------------
  Dice      : [<d1>, <d2>, ...]
  Modifier  : <+|-><modifier>
  TOTAL     : <total>
=======================================
```
````

The bold heading is the label, the fenced code block is the auditable math, and the block quote is the consequence. This three-line shape is the default for any roll that matters in play.

For low-stakes or off-screen rolls, the code block alone is fine.

## Script Reference

- `scripts/dice.py` - fair dice rolling via Python's uniform `randint`.
- `scripts/ttrpg_lib.py` - shared helpers for filesystem layout, pack resolution, and session utilities.
- `references/session-data-model.md` - canonical session and dossier shape.
- `references/discord-formatting.md` - Discord-native markdown reference for player-facing output.

## Pitfalls

- Do not pretend unsupported games have native-pack features when they do not.
- Do not load more than one pack in the same session.
- Do not claim copyrighted rules text is bundled in the repository.
- Do not ship or consult reusable seed-data libraries of quests, rumors, events, locations, NPCs, or names. Author fresh material for each session.
- Do not build, refresh, or search a pack database. This skill no longer uses one.
- Do not paste uncited downloaded reference material into the repo. Convert it into markdown and place source citations at the top.
- Do not skip session creation; the session folder is the memory boundary.
- Do not let pack references override player-authored facts from the active session.
- Do not narrate past the dice.
- Do not let one player's request, inventory, XP, or consequence land on another player's character in multiplayer play.

## Verification

The skill is working correctly when all of the following are true:

- The agent tells the player that `cyberpunk`, `dnd`, `mistborn`, `pokemon`, and `expanse` are natively supported.
- The agent also says unsupported TTRPGs are possible with reduced features.
- Only the chosen native pack is loaded for a native game.
- No database bootstrap or search step is required for play.
- The active session folder contains `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories.
- `session.json` records the selected game and whether support is `native` or `reduced`.
- `session.json` records `mistborn_era` when the active pack is `mistborn`.
- The current scene's new facts are written back into the active session's files using Hermes file tools.
- No scene content was produced by mixing another flavor pack or another saved session into the current one.
- Player-facing output uses Discord-native markdown: `###` scene headers, `**bold**` anchors, `>` block quotes for NPC speech, fenced code blocks for dice cards, and `-#` for ambient tags.
