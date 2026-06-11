---
name: ttrpg-bootstrap
description: Bootstrap a new isolated tabletop RPG session. Loads the right flavor pack, creates the session folder, walks the player through character creation, and opens the first scene.
version: 3.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# TTRPG Bootstrap

Bootstrap a fresh tabletop RPG session with strict per-session memory isolation and explicit flavor-pack boundaries. This skill covers everything from "I want to start a game" through the first scene.

## Companion Skills

- `/ttrpg-bootstrap` (this skill): set up a new session, load the right pack, walk through character creation, open the first scene.
- `/ttrpg-recover` (bundled separately): the GM automatically invokes this after a context-engine compression boundary. The recovery skill tells the GM to read the data files re-pasted by the engine, compare them against the recent transcript, update the files to reflect what just happened, and continue play.

Both skills live in the same plugin (`ttrpg-runner`) and share the same session files; `ttrpg-recover` does not bootstrap a new session and `ttrpg-bootstrap` does not need to know about compression.

## Native Support

`/ttrpg-bootstrap` should tell the player, early and plainly, that these settings are natively supported:

- `cyberpunk`
- `dnd`
- `mistborn` (single pack with `Era 1` or `Era 2` sections selected by `mistborn_era`)
- `pokemon`
- `expanse`

If the requested game is outside that list, say that any TTRPG is still possible but the session will run with reduced features: no native flavor pack and no pack-specific reference set.

## Mistborn Pack Layout

`mistborn` uses a base `PACK.md` plus exactly one era file in the `resources/` folder.

- Ask for `Era 1` or `Era 2` before character creation or worldbuilding.
- Load `flavorpacks/mistborn/PACK.md` as the always-on ruleset.
- Load the matching era file: `flavorpacks/mistborn/resources/mistborn_era_1.md` or `flavorpacks/mistborn/resources/mistborn_era_2.md`.
- Record the answer in the `story.md` header block (see "Session Metadata" below) so a resumed session remembers it.
- Read exactly one era file per Mistborn session, paired with the base `PACK.md`. Era content lives in `mistborn/resources/` alongside the base pack.

## Flavor Pack Loading Rules

These rules are mandatory. They exist to stop cross-setting contamination while still allowing intentional crossovers of two native packs.

- Determine the requested setting before you worldbuild. If the player has not named a setting, ask.
- If the player names a single native setting, load `flavorpacks/<pack>/PACK.md`. Single-setting play is single-pack.
- If the player explicitly names a crossover of two native settings, load BOTH `flavorpacks/<pack>/PACK.md` files, record both pack names in the `story.md` header block, and treat the session as a native crossover. Each pack keeps its own rules, tone, and reference tree; the player and GM blend them at the table. Do not silently demote a native crossover to generic mode.
- When a crossover has two systems that conflict (stat blocks, magic systems, tech trees, damage scales, progression, etc.), the GM must ask the player how to resolve the conflict before worldbuilding. Do not pick silently. Examples: "Do we use the `cyberpunk` stat block or the `pokemon` stat block?", "Which magic/tech system applies, and how do the other system's powers map onto it?", "How does damage scale across both?", "How does progression work?". Record the player's answers in the `story.md` header block and stick to them for the whole session.
- Only read deeper pack references from a pack that is active in the current session. A pack that is not loaded in this session must never be consulted.
- Within an active pack, only read deeper references from that same pack. A `cyberpunk` reference is not a valid source for a `pokemon` beat and vice versa, even in a crossover; each pack's own rules and tone stay internally consistent.
- If the player says `cyberpunk` and nothing else, do not load `pokemon`. If the player says `cyberpunk + pokemon` (or any other explicit crossover), load both.
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
- The plugin's structured tools are there to avoid brittle hand-edits. Use `ttrpg_roll` for any risky or uncertain action that needs a fair, auditable number. The post-compaction state is the data files, not a tool the GM invokes; the recovery skill asks the LLM to keep the data files in sync with the recent transcript, and the engine re-pastes those files on the next compression.
- Keep the fiction system-inspired and genre-faithful without quoting proprietary rulebooks as if they were bundled in the repo.
- Do not rely on bundled seed libraries of names, quests, rumors, events, or NPCs. Those were intentionally removed to prevent repeated content across sessions.
- Do not use a database, bootstrap pipeline, or online-downloaded search index for pack knowledge.
- If curated external reference material is ever added to the repo, store it as markdown with source citations at the top of the file.
- Support both solo play and multiplayer play. If multiple Discord users are in the session, track exactly which human maps to which character slug.
- Wait for the player to explicitly authorize play before opening the first scene, narrating fiction, or rolling dice. Finishing setup, confirming the setting, or completing character creation is not a green light to begin.
- During character creation, always offer one or more suggested initial loadouts (starting gear, resources, and any setting-specific kits) that the player can accept, modify, or reject. Do not finish a character without surfacing concrete starting options for the player to react to.
- Do not begin initializing other players' characters until the player has finished their character creation. If someone else, interjects, politely request that they wait their turn but acknowledge their character creation.

## Skill Layout

This skill lives inside the plugin's own `skill/ttrpg-bootstrap/` folder so it travels with the code that bundles it. The companion `ttrpg-recover` skill lives next to it in `skill/ttrpg-recover/`. Hermes loads them via `skill_view("ttrpg-runner:ttrpg-bootstrap")` and `skill_view("ttrpg-runner:ttrpg-recover")`.

```text
skill/
  ttrpg-bootstrap/
    SKILL.md                       # this file
    templates/
      character.md
      event.md
      location.md
      secrets.md
      session-summary.md
    flavorpacks/
      core/                        # always-on common rules and tips
        PACK.md                    # loaded for every session, any setting
      cyberpunk/
        PACK.md                    # base pack, no subpacks
      dnd/
        PACK.md
      pokemon/
        PACK.md
      expanse/
        PACK.md
      mistborn/
        PACK.md                    # canonical Mistborn ruleset, always on
        resources/
          mistborn_era_1.md        # Era 1: Final Empire, Terris, Skaa, Heroes of the Trilogy
          mistborn_era_2.md        # Era 2: Industrial Scadrial, Elendel, the Roughs, Nobles
  ttrpg-recover/
    SKILL.md                       # post-compaction recovery instructions
```

## Active Session Directory

Configured `ttrpg_runner.base_dir` (default `~/.hermes/ttrpg-runner`) is the root.

```text
<base-dir>/
  sessions/
    <session-id>/
      story.md            # running fiction + session metadata header
      timeline.md         # beat-by-beat chronology
      gm-notes.md         # hidden planning
      secrets.md          # GM-only truths
      characters/         # markdown dossiers
      locations/
      events/
      rolls/              # JSON dice audit trail
```

## What Lives Where

- `story.md` — running fiction and scene recap. Opens with a `> Session Metadata` block that records the selected game, active flavor packs, support level, mistborn era (when relevant), and session start time. The metadata block is the only place the campaign's identity is persisted.
- `timeline.md` — concise beat-by-beat chronology.
- `gm-notes.md` — hidden planning notes, stakes, and hooks.
- `secrets.md` — GM-only truths that must never be printed in player chat (hidden agendas, true identities, ticking bombs, GM-triggered twists).
- `characters/<slug>.md` — canonical markdown sheets for PCs, companions, and important NPCs. Plain text, no JSON parsing.
- `locations/<slug>.md` — named places with sensory details and hidden layers.
- `events/<slug>.md` — missions, incidents, betrayals, and turning points.
- `rolls/<stamp>-<label>.json` — optional audit trail for important dice calls.

There is no separate `session.json`. The compression engine re-pastes the data files (above) into the working context on every compression, and the recovery skill asks the LLM to keep them in sync with the recent transcript. Adding a `session.json` mirror would duplicate that state and risk drift, so the plugin does not maintain one.

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
   If the setting is a single native pack (`cyberpunk`, `dnd`, `mistborn`, `pokemon`, or `expanse`), say it is natively supported and load that pack's `PACK.md`. For `mistborn`, the main `mistborn/PACK.md` is the always-on ruleset; the era-specific material lives in `mistborn/resources/mistborn_era_1.md` or `mistborn/resources/mistborn_era_2.md`. Load both the base `PACK.md` and the chosen era file for any Mistborn session.
   If the setting is an explicit crossover of two native packs, say both are natively supported, load both base `PACK.md` files and treat the session as a native crossover. Only ask the `mistborn` era question if `mistborn` is one of the active packs.
   If it is anything else (a non-native setting, or a crossover involving a non-native setting), say the game is still possible with reduced features and stay in generic mode.

3. Resolve the base directory.
   Use configured `ttrpg_runner.base_dir` if supplied. Otherwise use `~/.hermes/ttrpg-runner`.

4. Load native-pack references only when needed.
   For each active pack, read only that pack's docs.
   Start with `flavorpacks/<pack>/PACK.md` for every active pack. Open deeper markdown files from the same pack only when the current turn actually needs them.
   For `mistborn`, the main `mistborn/PACK.md` is the always-on ruleset (dice, magic, character sheet, conflicts, damage, missions, and pack-wide events). The `mistborn/resources/mistborn_era_1.md` or `mistborn/resources/mistborn_era_2.md` file adds era-specific setting, factions, missions, and events. Read era files only when the active session's `mistborn_era` calls for them.
   **The core pack is always on.** Before the first scene of any session (native, native crossover, or generic mode), read `flavorpacks/core/PACK.md`. It holds the setting-agnostic operating rules the GM needs every turn: Discord output formatting, the whitespace discipline rule, multiplayer turn management, dice-and-roll interleaving, and the roll display format. The `post_tool_call` hook tags that file as a required asset pack the moment it is read, so the context engine repastes it after every compression boundary. Treat the core pack as required reading, not optional context, and keep its rules in scope for the rest of the run.
   Load order is core first, then the chosen setting pack. The `flavorpacks/core/PACK.md` file is the only source of truth for the always-on common rules.

5. Create or resume a session by hand.
   Hermes manages the session directory directly with its file tools.

   - New session: create a fresh `<session-id>` folder and seed `story.md` (with the Session Metadata block, see above), `timeline.md`, `gm-notes.md`, `secrets.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories. Use `templates/secrets.md` as the starting shape for `secrets.md` so the GM-only banner and the "do not print" rules are present from the first turn. There is no `session.json` to seed - the metadata header inside `story.md` is the identity record.
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
   - Watch for a "Session Data Update Required" bridge message from the context engine. When it appears, switch to the `ttrpg-recover` skill for the rest of the turn: read the recent transcript the engine kept verbatim, compare it against the data files re-pasted by the engine, update the files to reflect what just happened, and continue play.

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

- **Storage.** Put every GM-only truth in `secrets.md`. The file lives next to `gm-notes.md` and is read by the GM, not the table.
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
- `load_ttrpg_context_files(session_id)` plugin tool (used by `ttrpg-recover`) - returns the list of asset packs the active session has loaded, so the post-compaction GM can decide which to reload. **The list is generated automatically**: the `post_tool_call` hook watches every file the GM reads and registers any asset pack (`PACK.md` under `skill/ttrpg-bootstrap/flavorpacks/`) the moment it enters scope. The skill never has to call this list-builder by hand; the hook does it for free. This tool is only for *reading* the list, not for adding to it.
- `flavorpacks/core/PACK.md` - the always-on common-rules asset pack (Discord formatting, whitespace discipline, multiplayer turn management, dice-and-roll interleaving, roll display format). Read it once at the start of every session, before the first scene, and keep its rules in scope for the rest of the run. The `post_tool_call` hook tags it as an active pack so the context engine repastes it after every compression boundary.
- `templates/character.md` - canonical markdown sheet for PCs, companions, and NPCs. Use this instead of any JSON shape.
- `templates/secrets.md` - GM-only secrets ledger; never printed in chat.
- The companion skill `ttrpg-recover` is loaded automatically after a context-engine compression; switch into it the moment a "Session Data Update Required" bridge message appears in the working context.

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
- Do not invoke `ttrpg-recover` outside of a real compression boundary. The recovery skill is for post-compaction work, not for normal play.
- Do not skip the core pack or load it "only when needed." `flavorpacks/core/PACK.md` is required reading for every session; load it at the start of every session and keep its guidance in scope, just like the setting pack.

## Verification

The skill is working correctly when all of the following are true:

- The agent tells the player that `cyberpunk`, `dnd`, `mistborn`, `pokemon`, and `expanse` are natively supported.
- The agent also says unsupported TTRPGs are possible with reduced features.
- For `mistborn`, the agent asks for `Era 1` or `Era 2`, records it in the `story.md` Session Metadata block, and loads `mistborn/resources/mistborn_era_1.md` or `mistborn/resources/mistborn_era_2.md` alongside the base `mistborn/PACK.md`.
- Only the chosen native pack is loaded for a native game.
- No database bootstrap or search step is required for play.
- The active session folder contains `story.md`, `timeline.md`, `gm-notes.md`, `secrets.md`, and the `characters/`, `locations/`, `events/`, and `rolls/` directories.
- The Session Metadata block at the top of `story.md` records the selected game, flavor packs, support level, and (when relevant) mistborn era.
- The current scene's new facts are written back into the active session's files using Hermes file tools.
- No scene content was produced by mixing another flavor pack or another saved session into the current one.
- Player-facing output uses Discord-native markdown: `###` scene headers, `**bold**` anchors, `>` block quotes for NPC speech, fenced code blocks for dice cards, and `-#` for ambient tags.
- `flavorpacks/core/PACK.md` was loaded at the start of the session and remains in scope, including the whitespace discipline rule.
- Every markdown file the agent brought into context during the run was registered automatically by the `post_tool_call` hook, so `load_ttrpg_context_files(session_id)` can return the full list of asset packs the session used (with the core pack always present).
