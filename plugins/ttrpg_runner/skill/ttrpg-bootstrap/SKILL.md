---
name: ttrpg-bootstrap
description: Bootstrap a new isolated tabletop RPG session. Loads the right flavor pack, creates the session folder, walks the player through character creation, and opens the first scene.
version: 3.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# TTRPG Bootstrap

Bootstrap a fresh tabletop RPG session with strict per-session memory isolation and explicit flavor-pack boundaries. This skill covers everything from "I want to start a game" through the first scene.

## Native Support

`/ttrpg-bootstrap` should tell the player, early and plainly, that these settings are natively supported:

- `cyberpunk` (`/ttrpg-cyberpunk`)
- `dnd` (`/ttrpg-dnd`)
- `mistborn` (`/ttrpg-mistborn`, with an `Era 1` / `Era 2` follow-up question for the era file)
- `pokemon` (`/ttrpg-pokemon`)
- `expanse` (`/ttrpg-expanse`)

If the requested game is outside that list, say that any TTRPG is still possible but the session will run with reduced features: no native flavor pack and no pack-specific reference set.

## Pack Skill Layout

Each flavor pack ships as its own first-class skill in the plugin. Every pack skill is a directory named `ttrpg-<pack>` containing a `SKILL.md` (the always-on ruleset for that pack) and, when the pack has era-specific or setting-specific submaterial, a `resources/` subdirectory. The agent loads packs through the standard `skill_view` tool:

- `skill_view("ttrpg-<pack>")` reads the base `SKILL.md` of the pack
- `skill_view("ttrpg-<pack>", "resources/<file>.md")` reads a specific reference inside the pack

This matches the standard Hermes skill layout, so any future pack (and any future era / subpack) follows the same pattern. Mistborn is the existing example that already uses `resources/` for its era files.

### Mistborn subpack flow

Mistborn is a two-file pack: the base `SKILL.md` (always on) plus exactly one era file from `ttrpg-mistborn/resources/`. The two are tightly coupled — the base pack says "read this with one era file," and a single era file is useless without the base pack. The era answer is the gate that triggers both files to load in the same turn.

1. As soon as the player says they want Mistborn, ask for `Era 1` or `Era 2` and **wait** for the answer. Do not start loading the base pack yet — the era you pair it with is fixed by their answer.
2. The instant the player answers (e.g. "era 1" / "the final empire"), load both in the same turn, before any other step:
   - `skill_view("ttrpg-mistborn")` — the always-on Mistborn ruleset
   - `skill_view("ttrpg-mistborn", "resources/era_1.md")` *or* `skill_view("ttrpg-mistborn", "resources/era_2.md")` — whichever era they chose
   Loading the era file is part of resolving native support, not a follow-up you can defer. If the era file is not in scope, the base pack is not fully usable.
3. Record the era in the `story.md` Session Metadata block (see "Session Metadata" below) so a resumed session remembers it.
4. Read exactly one era file per Mistborn session, paired with the base `SKILL.md`. Era content lives in `ttrpg-mistborn/resources/` alongside the base pack.

## Flavor Pack Loading Rules

These rules are mandatory. They exist to stop cross-setting contamination while still allowing intentional crossovers of two native packs.

- Determine the requested setting before you worldbuild. If the player has not named a setting, ask.
- If the player names a single native setting, load that pack's base `SKILL.md` with `skill_view("ttrpg-<pack>")` (and any required `resources/` file for that pack). Single-setting play is single-pack.
- If the player explicitly names a crossover of two native settings, load BOTH packs' base `SKILL.md` files, record both pack names in the `story.md` header block, and treat the session as a native crossover. Each pack keeps its own rules, tone, and reference tree; the player and GM blend them at the table. Do not silently demote a native crossover to generic mode.
- When a crossover has two systems that conflict (stat blocks, magic systems, tech trees, damage scales, progression, etc.), the GM must ask the player how to resolve the conflict before worldbuilding. Do not pick silently. Examples: "Do we use the `ttrpg-cyberpunk` stat block or the `ttrpg-pokemon` stat block?", "Which magic/tech system applies, and how do the other system's powers map onto it?", "How does damage scale across both?", "How does progression work?". Record the player's answers in the `story.md` header block and stick to them for the whole session.
- Only read deeper pack references from a pack that is active in the current session. A pack that is not loaded in this session must never be consulted.
- If the player says `cyberpunk` and nothing else, do not load `pokemon`. If the player says `cyberpunk + pokemon` (or any other explicit crossover), load both. In this case, you may access resources from both packs.
- If the player changes settings mid-conversation, stop and confirm whether they want to abandon the current session and start a new one, or shift the current session into a new single-pack or crossover mode.
- A crossover that includes a non-native setting runs in generic mode for the unsupported portion. Do not load native-pack reference docs in generic mode, and do not blend native-pack docs into a generic session.

## When to Use

Use this skill when the player wants to:

- start a new one-shot or campaign in a native pack, in a native crossover of two packs, or in a generic unsupported setting
- roll dice or resolve checks during play
- keep persistent story records for the current session only
- resume a previously saved session by explicit request
- generate setting-faithful hooks, NPCs, factions, locations, rumors, or complications without mixing settings

## First Principles

- Treat `/ttrpg-bootstrap` as a session bootstrap command.
- Unless the player explicitly says `resume`, `load`, `continue`, or names an existing session, create a brand new isolated play session.
- Never mix data from other saved sessions into the current session.
- Hermes reads and writes the active session's files directly with its file tools. There is no controller layer.
- The plugin's structured tools are there to avoid brittle hand-edits. Use `ttrpg_roll` for any risky or uncertain action that needs a fair, auditable number.
- Keep the fiction system-inspired and genre-faithful without quoting proprietary rulebooks as if they were bundled in the repo.
- Do not rely on bundled seed libraries of names, quests, rumors, events, or NPCs. Those were intentionally removed to prevent repeated content across sessions.
- Do not use a database, bootstrap pipeline, or online-downloaded search index for pack knowledge.
- If curated external reference material is ever added to the repo, store it as markdown with source citations at the top of the file.
- Support both solo play and multiplayer play. If multiple Discord users are in the session, track exactly which human maps to which character slug.
- Wait for the player to explicitly authorize play before opening the first scene, narrating fiction, or rolling dice. Finishing setup, confirming the setting, or completing character creation is not a green light to begin.
- During character creation, always offer one or more suggested initial loadouts (starting gear, resources, and any setting-specific kits) that the player can accept, modify, or reject. Do not finish a character without surfacing concrete starting options for the player to react to.
- Do not begin initializing other players' characters until the player has finished their character creation. If someone else, interjects, politely request that they wait their turn but acknowledge their character creation.

## Skill Layout

Every skill in this plugin lives as its own first-class skill directory under `skill/`, so it can be installed, symlinked, and loaded with `skill_view` exactly the same way as a built-in Hermes skill. The flavor-pack skills sit alongside the bootstrap skill; the templates folder stays under `ttrpg-bootstrap` because it is bootstrap-only scratch.

```text
skill/
  ttrpg-bootstrap/                # /ttrpg-bootstrap slash command
    SKILL.md                      # this file
    templates/
      character.md
      event.md
      location.md
      secrets.md
      session-summary.md
  ttrpg-core/                     # /ttrpg-core - always-on common rules
    SKILL.md
  ttrpg-clean/                    # /ttrpg-clean - compact and dedupe session files
    SKILL.md
  ttrpg-cyberpunk/                # /ttrpg-cyberpunk
    SKILL.md                      # base pack, no subpacks
  ttrpg-dnd/                      # /ttrpg-dnd
    SKILL.md
  ttrpg-pokemon/                  # /ttrpg-pokemon
    SKILL.md
  ttrpg-expanse/                  # /ttrpg-expanse
    SKILL.md
  ttrpg-mistborn/                 # /ttrpg-mistborn
    SKILL.md                      # base pack (always on once era is chosen)
    resources/
      era_1.md                    # Era 1: Final Empire, Terris, Skaa, Heroes of the Trilogy
      era_2.md                    # Era 2: Industrial Scadrial, Elendel, the Roughs, Nobles
```

## Active Session Directory

Configured `ttrpg_runner.base_dir` (default `~/.hermes/ttrpg-runner`) is the root.

```text
<base-dir>/
  sessions/
    <session-id>/
      story.md            # running fiction + session metadata header
      timeline.md         # beat-by-beat chronology
      secrets.md          # GM-only truths, twists, and behind-the-screen planning
      characters/         # markdown dossiers
      locations/
      events/
      rolls/              # JSON dice audit trail
```

## What Lives Where

- `story.md` — running fiction and scene recap. Opens with a `> Session Metadata` block that records the selected game, active flavor packs, support level, mistborn era (when relevant), and session start time. The metadata block is the only place the campaign's identity is persisted.
- `timeline.md` — concise beat-by-beat chronology.
- `secrets.md` — GM-only file. Holds two things, both of which must never be printed in player chat: (1) `Active Secrets` / `Burned Secrets` (hidden agendas, true identities, ticking bombs, GM-triggered twists) and (2) `GM Planning Notes` (open clocks, stakes, hooks, what to do if the players go off-script). The old `gm-notes.md` file is gone; everything the GM keeps behind the screen lives in this one file.
- `characters/<slug>.md` — canonical markdown sheets for PCs, companions, and important NPCs. Plain text, no JSON parsing.
- `locations/<slug>.md` — named places with sensory details and hidden layers.
- `events/<slug>.md` — missions, incidents, betrayals, and turning points.
- `rolls/<stamp>-<label>.json` — optional audit trail for important dice calls.

There is no separate `session.json`. The data files (above) are the canonical state; adding a `session.json` mirror would duplicate that state and risk drift, so the plugin does not maintain one.

## Append-Only Session Files

The data files in a session folder are **append-only**. This is a deliberate performance rule, not a suggestion.

- **What "append-only" means.** Every write to a session file adds new content at the end (a new timeline entry, a new beat in `story.md`, a new secret, a new planning note, a new dossier, a new roll). The model never opens an existing session file, reads it, edits a line, and saves it back. That round-trip is exactly what we are avoiding.
- **Why it matters.** Skim, append, close. Skim, append, close. That is the steady-state loop the GM runs on every turn. Open-read-edit-save invites stale-context bugs, partial overwrites, and accidentally rewriting a fact the table has already accepted as canon. Append-only writes are O(1) and cannot lose what the table already saw.
- **How it stays small.** Files grow, so the plugin ships a `ttrpg-clean` skill. The player or the GM runs `/ttrpg-clean` when a file is getting long; the LLM then opens that one file, merges redundant entries, drops resolved and stale items, and rewrites the file under 100 lines. `/ttrpg-clean` is the only sanctioned read-modify-write path for session data.
- **Where append-only does not apply.** The first write of a brand-new session still seeds each file from its template (this is bootstrap, not in-flight play). The Session Metadata header at the top of `story.md` is updated in place on resume (it is the identity record, not a beat). Dossier files for a specific character, location, or event are the dossier for that one entity and are appended to as that entity evolves; they are not edited retroactively to rewrite an entity's history.
- **If you catch yourself editing in place, stop.** Use the append path. If the append path cannot express the change, run `/ttrpg-clean` and let the compactor rewrite the file.

This rule is load-bearing. If a turn would otherwise require editing a session file in place, change the beat so it does not, or queue the change for the next `/ttrpg-clean`.

## Session Metadata

The first thing inside `story.md` is a small block that records the session's identity. Bootstrap writes it on session creation; resume updates the `Last Resumed` line. Treat it as the canonical record of what is being played. Example:

```markdown
# <Campaign Title>

> **Game**: Cyberpunk 2077  
> **Flavor Packs**: cyberpunk  
> **Support Level**: native  
> **Mistborn Era**: (n/a)  
> **Started**: 2026-06-10T12:34:56Z  
> **Last Resumed**: 2026-06-10T18:01:22Z  

## Story
...running fiction starts here...
```

- `Game` is the human-facing name the player gave (free text).
- `Flavor Packs` is a comma-separated list of native pack names; one entry for a single-pack session, two for a native crossover, `none` for reduced-feature generic mode.
- `Support Level` is `native` or `reduced`.
- `Mistborn Era` is `era1`, `era2`, or `(n/a)`.
- The rest of the file is free-form running fiction and scene recap.

## Procedure

1. Establish the table and the game.
   Ask whether the player wants solo or multiplayer play, then identify the requested setting before you start creating content.
   If the setting is `mistborn`, ask for `Era 1` or `Era 2` before character creation or worldbuilding.
   Do not open the first scene, narrate fiction, or roll dice until the player has explicitly said `start`, `begin`, `go`, or otherwise authorized play. Finishing setup, confirming the setting, building the character roster, or completing character creation is not a green light to begin the story. When in doubt, ask before you narrate.
   When you walk the player through character creation, propose at least one suggested initial loadout (starting gear, resources, and any setting-specific kits such as Mistborn metals, Cyberpunk cyberware, or DND 5e starting equipment) and let the player accept, modify, or swap it. Surface this offer before the character sheet is locked so the player always has concrete starting options on the table.

2. Resolve native support.
   If the setting is a single native pack (`cyberpunk`, `dnd`, `mistborn`, `pokemon`, or `expanse`), say it is natively supported and load that pack's base `SKILL.md` with `skill_view("ttrpg-<pack>")`. For `mistborn`, the era question from step 1 is the gate: do not start loading the base pack until the player has picked an era, and the moment they answer, load `skill_view("ttrpg-mistborn")` together with `skill_view("ttrpg-mistborn", "resources/era_1.md")` or `skill_view("ttrpg-mistborn", "resources/era_2.md")` in the same turn. A Mistborn session without its era file is incomplete; do not move on to character creation, worldbuilding, or scene narration until both files are in scope.
   If the setting is an explicit crossover of two native packs, say both are natively supported, load both base `SKILL.md` files with `skill_view` and treat the session as a native crossover. Only ask the `mistborn` era question if `mistborn` is one of the active packs.
   If it is anything else (a non-native setting, or a crossover involving a non-native setting), say the game is still possible with reduced features and stay in generic mode.

3. Resolve the base directory.
   Use configured `ttrpg_runner.base_dir` if supplied. Otherwise use `~/.hermes/ttrpg-runner`.

4. Load native-pack references only when needed.
   For each active pack, read only that pack's docs.
   Start with `skill_view("ttrpg-<pack>")` for every active pack — that returns the base `SKILL.md`. Open deeper markdown files from the same pack with `skill_view("ttrpg-<pack>", "resources/<file>.md")` only when the current turn actually needs them.
   For `mistborn`, the base `SKILL.md` is the always-on ruleset (dice, magic, character sheet, conflicts, damage, missions, and pack-wide events). The `resources/era_1.md` or `resources/era_2.md` file adds era-specific setting, factions, missions, and events. Read era files only when the active session's `mistborn_era` calls for them.
   **The core pack is always on.** Before the first scene of any session (native, native crossover, or generic mode), load `ttrpg-core` with `skill_view("ttrpg-core")`. It holds the setting-agnostic operating rules the GM needs every turn: Discord output formatting, the whitespace discipline rule, multiplayer turn management, dice-and-roll interleaving, and the roll display format. Treat the core pack as required reading, not optional context, and keep its rules in scope for the rest of the run.
   Load order is core first, then the chosen setting pack. The `ttrpg-core` skill is the only source of truth for the always-on common rules.

5. Create or resume a session by hand.
   Hermes manages the session directory directly with its file tools.

   - New session: create a fresh `<session-id>` folder and seed `story.md` (with the Session Metadata block, see above), `timeline.md`, `secrets.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories. Use `templates/secrets.md` as the starting shape for `secrets.md` so the GM-only banner, the append-only rule, the "do not print" rules, and the `GM Planning Notes` section are present from the first turn. There is no `session.json` to seed - the metadata header inside `story.md` is the identity record. There is no `gm-notes.md`; the planning space lives in `secrets.md` under `GM Planning Notes`.
   - Resume flow: list the saved sessions, let the player choose one, then read only that session's files. The Session Metadata header in `story.md` tells you what game, packs, era, and support level to reload.

6. Record the chosen game in the `story.md` Session Metadata block.
   Always set:

   - `Game`: the human-facing name the player asked for
   - `Flavor Packs`: a comma-separated list of native pack names (one entry for single-pack, two for a native crossover), or `none` for unsupported games
   - `Support Level`: `native` or `reduced`
   - `Mistborn Era`: `era1`, `era2`, or `(n/a)`
   - `Started`: current UTC ISO timestamp on creation
   - `Last Resumed`: current UTC ISO timestamp whenever the session is reopened

8. Run the game by editing the active session's files.
   On every turn:

   - Skim `story.md` (the metadata header plus the current scene) and `timeline.md` first.
   - Identify the active speaker in multiplayer sessions before applying any request.
   - Use `ttrpg_roll` for risky or uncertain actions.
   - For native packs only, consult the active pack's markdown references when you need tone, gameplay cadence, or a curated fact reminder.
   - If a markdown reference file includes external material, keep the citations block at the top intact when you update it.
   - Format every player-facing message with Discord-native markdown per the core pack. Dice cards go in fenced code blocks, NPC speech in block quotes, and scene openings under `###` headings.
   - Write the resulting state changes back into the active session files. When a beat changes the campaign state, update the data file (or dossier) that owns that fact - do not invent a parallel JSON mirror.

9. Close each turn with a game-facing handoff.
   Summarize what changed, what the player can do next, and what pressures or leads are now in motion.

## Session Isolation Rules

These rules are non-negotiable.

- Every new invocation creates a brand-new session folder unless the player explicitly resumes one.
- Never read another session's files on your own.
- Never quote, paraphrase, or carry over prior-session content into a fresh session.
- The active session directory is the only authoritative memory for the current run.
- A native pack's markdown references are reference material only, never a hidden source of prior-session canon.
- If a leak occurs, acknowledge it, scrub it from the current session files, and continue using only the active session and the active pack(s).

## GM Secrets Handling

Some facts in a session belong to the GM and the GM alone. The moment one of those facts lands in player-visible chat, in-character dialogue, a recap, a shared handout, an ambient insert, or a "soft hint" message, it stops being a secret and starts being table canon. Treat that line as load-bearing.

Every active session ships with a `secrets.md` file seeded from `templates/secrets.md`. The template's banner is not decoration; it is the operational rule.

- **Storage.** Put every GM-only truth in `secrets.md`. The file also holds `GM Planning Notes` for behind-the-screen planning, so the GM does not need a separate planning file. The file is read by the GM, not the table, and is append-only (see "Append-Only Session Files" above).
- **Never print.** Do not paste `secrets.md` contents, summaries, paraphrases, hints, or confirmations into any player-facing Discord message. Spoiler tags do not count; anything the player can click to reveal has already been exposed.
- **No soft reveals.** Do not let an NPC, ambient insert, or "as you recall" passage leak a secret by accident. If a secret is in `secrets.md`, it does not appear in the fiction until the GM deliberately opens the door.
- **Refuse close guesses politely.** If a player gets hot and names a secret out loud, the GM does not confirm, deny, or echo it. Answer in the GM voice, redirect the spotlight, and let the table earn the reveal through play.
- **Track lifecycle.** Every entry in `secrets.md` has a status: `dormant`, `active`, `about_to_fire`, or `resolved`. Move statuses as the scene evolves. Burned or fired secrets get archived in the `Burned Secrets` section so the GM does not re-use the same twist.
- **Surface cover is mandatory.** Each secret records what the players currently believe. The GM uses that cover to keep the fiction coherent without leaking the truth.
- **Reveal triggers are GM-only.** The "Reveal Trigger" and "If Exposed" fields tell the GM when and how the secret is allowed to surface. The table does not see them. Do not describe trigger conditions in chat.
- **Cross-session hygiene.** Secrets are session-scoped. Never carry a `secrets.md` from a prior session into a new one. A fresh session gets a fresh `secrets.md`.
- **Leak protocol.** If a secret accidentally reaches the player, acknowledge it in the GM voice, move the entry to `Burned Secrets` in the same `secrets.md`, and continue play without relying on it. Do not pretend the leak did not happen and do not retcon player knowledge.

What belongs in `secrets.md` includes: hidden NPC agendas, true identities, secret faction goals, planted evidence, ticking bombs the players cannot see, GM-triggered twists, the real reason a scene is the way it is, and any fact that would change player behavior the moment it surfaced.

## Reference

- `ttrpg_roll` plugin tool - fair dice rolling via Python's uniform `randint`.
- `ttrpg-core` - the always-on common-rules skill (Discord formatting, whitespace discipline, multiplayer turn management, dice-and-roll interleaving, roll display format). Load it once at the start of every session with `skill_view("ttrpg-core")`, before the first scene, and keep its rules in scope for the rest of the run.
- `ttrpg-clean` - the compactor skill. The only sanctioned read-modify-write path for session data. Run `/ttrpg-clean` when a session file is getting long and the LLM will open that file, merge redundant entries, drop resolved and stale items, and rewrite it under 100 lines. See "Append-Only Session Files" above for why this exists.
- `templates/character.md` - canonical markdown sheet for PCs, companions, and NPCs. Use this instead of any JSON shape.
- `templates/secrets.md` - GM-only file; holds `Active Secrets`, `Burned Secrets`, and `GM Planning Notes`. Never printed in chat.

## Pitfalls

- Do not pretend unsupported games have native-pack features when they do not.
- Do not load more than one pack in the same session unless the player explicitly asked for a native crossover.
- Do not claim copyrighted rules text is bundled in the repository.
- Do not ship or consult reusable seed-data libraries of quests, rumors, events, locations, NPCs, or names. Author fresh material for each session.
- Do not build, refresh, or search a pack database. This skill no longer uses one.
- Do not paste uncited downloaded reference material into the repo. Convert it into markdown and place source citations at the top.
- Do not skip session creation; the session folder is the memory boundary.
- Do not let pack references override player-authored facts from the active session.
- Do not let one player's request, inventory, XP, or consequence land on another player's character in multiplayer play.
- Do not print the contents of `secrets.md` (or any paraphrase, hint, or spoiler-tagged copy of it) into player-facing chat. The instant a secret is rendered to a player it stops being a secret.
- Do not store character stats, skills, derived values, inventory, or XP in JSON. Character sheets are markdown; the data files hold the campaign state. There is no `session.json` to duplicate into.
- Do not skip the core pack or load it "only when needed." `ttrpg-core` is required reading for every session; load it with `skill_view("ttrpg-core")` at the start of every session and keep its guidance in scope, just like the setting pack.
- Do not answer a Mistborn era question and then move on. The era answer is the trigger: in the same turn, run `skill_view("ttrpg-mistborn")` and `skill_view("ttrpg-mistborn", "resources/era_1.md")` (or `resources/era_2.md`) before doing anything else. Asking the era question without loading the era file leaves the base pack half-loaded.
- Do not edit a session file in place to rewrite history. Session files are append-only. The only sanctioned read-modify-write path is `/ttrpg-clean`. If a turn feels like it needs a hand-edit, change the beat or queue it for the next clean.

## Verification

The skill is working correctly when all of the following are true:

- The agent tells the player that `cyberpunk`, `dnd`, `mistborn`, `pokemon`, and `expanse` are natively supported.
- The agent also says unsupported TTRPGs are possible with reduced features.
- For `mistborn`, the agent asks for `Era 1` or `Era 2`, records it in the `story.md` Session Metadata block, and loads `skill_view("ttrpg-mistborn")` together with `skill_view("ttrpg-mistborn", "resources/era_1.md")` or `skill_view("ttrpg-mistborn", "resources/era_2.md")`.
- Only the chosen native pack is loaded for a native game.
- No database bootstrap or search step is required for play.
- The active session folder contains `story.md`, `timeline.md`, `secrets.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories. There is no `gm-notes.md`.
- The Session Metadata block at the top of `story.md` records the selected game, flavor packs, support level, and (when relevant) mistborn era.
- The current scene's new facts are written back into the active session's files using Hermes file tools.
- No scene content was produced by mixing another flavor pack or another saved session into the current one.
- Player-facing output uses Discord-native markdown: `###` scene headers, `**bold**` anchors, `>` block quotes for NPC speech, fenced code blocks for dice cards, and `-#` for ambient tags.
- `ttrpg-core` was loaded with `skill_view("ttrpg-core")` at the start of the session and remains in scope, including the whitespace discipline rule.
- In-flight turns append to session files instead of editing them in place; when a file grows past a comfortable size, `/ttrpg-clean` is invoked rather than a hand-edit.
