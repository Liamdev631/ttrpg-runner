---
name: cyberpunk-runner
description: Run an isolated cyberpunk tabletop session with searchable lore, procedural scene tools, dice rolling, and persistent story dossiers.
version: 1.0.0
author: OpenAI
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [games, cyberpunk, tabletop, storytelling, python, simulation]
    category: games
    config:
      - key: cyberpunk_runner.base_dir
        description: Root directory for the cyberpunk-runner knowledge base and saved sessions.
        default: "~/.hermes/cyberpunk-runner"
        prompt: Directory for cyberpunk-runner data
      - key: cyberpunk_runner.default_tone
        description: Default session tone when the player does not specify one.
        default: "neon-noir"
        prompt: Default campaign tone
      - key: cyberpunk_runner.public_enrichment
        description: Whether to try public internet enrichment during bootstrap.
        default: "true"
        prompt: Enable optional public knowledge enrichment
---

# Cyberpunk Runner

Run a fresh, high-energy cyberpunk tabletop session with strict per-session memory isolation.

## When to Use

Use this skill when the player wants to:

- start a new cyberpunk one-shot or campaign
- generate gigs, NPCs, neighborhoods, corps, rumors, complications, or news crawls
- roll dice or resolve checks during play
- keep persistent story records for the current session only
- resume a previously saved cyberpunk session by explicit request

## First Principles

- Treat `/cyberpunk-runner` as a session bootstrap command.
- Unless the player explicitly says `resume`, `load`, or names an existing session, create a brand new isolated play session.
- Never mix data from other saved sessions into the current session.
- Use the Python helper scripts for authoritative setup, search, scene generation, dice, and session management.
- Keep the fiction system-agnostic and genre-faithful rather than quoting proprietary rulebooks.

## Procedure

1. Establish the player's ask.
   If the user did not supply enough detail, ask for only the minimum needed: mission tone, character concept, preferred lethality, and whether they want a one-shot or campaign.

2. Bootstrap the local knowledge base if needed.
   Run:

   ```bash
   python3 scripts/bootstrap_sources.py init --base-dir "<configured-base-dir>"
   ```

   If the user's configured value is available in context, pass it explicitly. Otherwise use the default `~/.hermes/cyberpunk-runner`.

3. Create or resume a session.
   For a new session run:

   ```bash
   python3 scripts/session_manager.py \
     --base-dir "<configured-base-dir>" \
     create \
     --theme "<campaign-or-mission-theme>" \
     --player-request "<the user's opening request>" \
     --tone "<configured-or-requested-tone>"
   ```

   For a resume flow, list sessions or inspect the requested session first:

   ```bash
   python3 scripts/session_manager.py list --base-dir "<configured-base-dir>"
   python3 scripts/session_manager.py show --base-dir "<configured-base-dir>" --session-id "<session-id>"
   ```

4. Read only the active session's state.
   Start with `session.json`, `story.md`, and any dossier files relevant to the current scene.

5. Use the tools during play.
   - Search genre data with `db_search.py`
   - Generate hooks or twists with `scene_oracle.py`
   - Resolve uncertainty with `dice.py`
   - Persist state changes with `session_manager.py`, especially `note`, `add-clock`, and `write-dossier`

6. Keep the story archive current.
   After each meaningful scene, update:
   - `story.md` with the narrative summary
   - `timeline.md` with concise chronological beats
   - `characters/`, `locations/`, or `events/` with any changed dossier state
   - `session.json` for clocks, leads, heat, objectives, and unresolved threats

7. End each major turn with a clear game-facing handoff.
   Summarize what changed, what the player can do next, and any clocks or consequences now in motion.

## Session Isolation Rules

- Every new invocation creates a new session folder unless the player explicitly asks to resume.
- The active session directory is the only authoritative memory for the current run.
- Do not search, quote, or reuse another session's dossiers unless the player intentionally loads that session.
- If the player asks for a crossover, make them choose the source session first.

## Script Reference

Use these helpers as the operational interface:

- `scripts/bootstrap_sources.py`: build the searchable SQLite knowledge base from bundled seed data and optional public enrichment sources
- `scripts/db_search.py`: search knowledge records by query, category, or tags, and optionally search inside a chosen session archive
- `scripts/scene_oracle.py`: generate gigs, rumors, complications, ad copy, encounter pressure, names, and weather
- `scripts/dice.py`: generic dice expressions plus cyberpunk-style action checks and opposed rolls
- `scripts/session_manager.py`: create, inspect, list, and update session state, clocks, roll logs, and markdown dossiers

Read these deeper references only when needed:

- `references/gameplay-loop.md`
- `references/session-data-model.md`
- `references/source-manifest.md`
- `references/gm-playbook.md`

Use these templates when drafting or refreshing dossiers:

- `templates/character.md`
- `templates/location.md`
- `templates/event.md`
- `templates/session-summary.md`

## Play Style

- Lead with strong sensory detail, hard choices, and escalating pressure.
- Keep the city reactive: corps retaliate, gangs adapt, the street remembers.
- Offer risky options, partial victories, ugly trade-offs, and memorable consequences.
- Make side characters feel connected to systems of money, violence, debt, media, and surveillance.
- Keep the pacing sharp and fun: jobs, betrayals, downtime, black clinics, data heists, busted transit lines, and neon weather.

## Pitfalls

- Do not claim copyrighted rules text as if it were included in the repository.
- Do not skip session creation; the session folder is the memory boundary.
- Do not let the knowledge database override player-authored facts from the active session.
- Do not overwrite dossiers casually; preserve continuity and consequences.
- Do not use another saved session as hidden context.

## Verification

The skill is working correctly when all of the following are true:

- `bootstrap_sources.py` reports a valid database path
- `session_manager.py create` or `show` returns a valid session directory
- the active session contains `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and dossier folders
- searches and dice rolls produce structured output the agent can cite during play
- the current scene's new facts are written back into the active session archive
