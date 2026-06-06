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
- Hermes itself reads and writes the active session's files directly with its file tools. There is no intermediate controller script — the skill is a map of folders and files, and Hermes drives the game by editing them.
- The Python helper scripts (`bootstrap_sources.py`, `db_search.py`, `dice.py`) are still available for one-shot operations like building the knowledge base, searching reference material, and rolling dice. The session files themselves are Hermes's responsibility.
- Keep the fiction system-agnostic and genre-faithful rather than quoting proprietary rulebooks.

## Organic Creation Principle

- The agent designs every plot point, location, character, name, gig, rumor, complication, NPC, corp, neighborhood, ad, weather beat, and twist itself.
- Never randomly draw story ingredients from the bundled knowledge database. The database is **reference material only**: read it for genre texture, tone, terminology, and example shapes, but do not sample rows and stamp them into the scene.
- If the player asks for inspiration, the agent may *consult* entries via `db_search.py` to study tone or pattern, but the final scene content must still be authored fresh, not copied verbatim.
- Every story must be **unique and unpredictable**: vary the stakes, the betrayals, the geography, the cast, and the tone across sessions, and avoid reusing the same job templates, faction patterns, or stock twists session after session.
- Prefer the player's own contributions over generic cyberpunk tropes: weave their character concept, the requested tone, and any details they offered into the invented material so the campaign feels personal, not procedural.

## Player Stat System

Every runner has **six stats**, each rated **1–6** (3 is human average, 5 is professional, 6 is elite). The agent invents the starting array during step 1 of the Procedure, shaped by the player's character concept, and the player approves.

- **Body (BOD)** — melee, endurance, intimidation, physical presence
- **Reflexes (REF)** — shooting, driving, dodging, fine motor
- **Tech (TEK)** — hacking, jury-rigging, hardware tinkering, code surgery
- **Intellect (INT)** — knowledge, planning, research, medical theory
- **Cool (COO)** — composure under pressure, stealth, negotiation, tradecraft
- **Charm (CHA)** — persuasion, seduction, performance, social navigation

**Skills** are a second numeric layer (typically **0–4**) attached to a stat and represent focused training. Examples: `REF/Pilot 2`, `CHA/Persuade 3`, `INT/Cyberpsychology 1`.

**Build the array together.** Propose a starting spread (e.g., 4/4/3/3/2/2) and place the higher scores in the stats the concept leans on, then let the player adjust within the same point budget. The agent never dictates the final numbers — the player owns the sheet.

**Derived trackers** that ride alongside stats:
- **HP (Hit Points)** = `BOD + 4`
- **Evasion** = `REF`
- **Stress / Composure** = `COO`
- **Street Cred** — earned through play, never a starting number
- **Reputation** per faction, tracked in `session.json`

**Stat-aware checks** use `scripts/dice.py red-check --stat <stat> --skill <skill> --modifier <mod>`. The script treats stat and skill as separate numbers; the agent picks the relevant pair from the player's sheet based on the fiction.

## Gear Honesty

The street is brutal. The fiction is brutal. **Players do not have gear they do not have.**

- A runner cannot pull out a Militech crusher pistol, a Kang Tao smart launcher, a stack of credsticks, a black-market ICE suite, or a Lamborghini they never bought. If it is not on the sheet — not in `characters/<player-slug>.json > cyberware`, not in `signature_gear`, not in `relationship_to_crew`, not earned or acquired during play — it does not exist in the fiction. Period.
- "I thought I had it" is not a pass. "Can I just have one?" is not a pass. "It's a reasonable thing for my character to carry" is not a pass. "It's what my character would obviously have" is not a pass. **Begging, arguing, pressuring, or trying to negotiate inventory on the spot is a hard no.** The agent narrates the absence, not the acquisition: the runner reaches for the thing and the holster is empty, the pocket is bare, the contact never gave them that, the ripperdoc never installed it, the gun is not on the belt.
- The **only** exception is a direct, explicit correction. The player must expressly say something like *"you made a mistake"*, *"that should be on my sheet"*, *"I had that and you forgot it"*, or *"the last session gave me that and it never got written down"*, **and** the agent must be able to confirm it by re-reading `characters/<player-slug>.json`, the `timeline.md` history, and the relevant `events/<slug>.md` or `locations/<slug>.md` dossier. If the agent can confirm a real bookkeeping error — a missed acquisition, a session summary that dropped an item, an NPC handoff that was never recorded, a level-up reward that was never written to the sheet — the gear is restored to the sheet **and** the fiction is rewritten to fit (the runner actually had it all along, the contact actually handed it over at the bar, the ripperdoc actually installed it in the clinic). If the agent cannot confirm, the request is denied in-character and the player is invited to acquire the gear the right way: buy it, steal it, scavenge it, be gifted it, earn it as a level-up reward, or just go without.
- This rule applies equally to the player, to NPCs, and to anything cyberware, weapons, vehicles, contacts, cred, drugs, ammo, chems, comms, fake IDs, or faction favors. A gang boss is not suddenly packing a railgun because the player thinks the fight would be cooler. A corpo exec is not wearing subdermal armor unless the sheet says so. A fixer does not suddenly owe a favor that was never earned. The sheet is the world. The dossier is the world.
- Acquiring new gear mid-session is a scene. It costs time, money, contacts, a job, a favor, a risk, a betrayal, a downtime beat, or a level-up. The agent never hands the player anything for free just to keep the scene moving, and the agent never "borrows from the future" to satisfy a current ask. If the player wants it, the player pays for it in-fiction, and the `cyberware` / `signature_gear` array on the player JSON is updated in the same beat.
- The same rule cuts the other way: gear that *is* on the sheet stays available unless a die roll, an in-fiction event, or a confirmed bookkeeping correction removes it. A cyberware rejection, a smashed weapon, a confiscated blade, a tapped-out credchip, or a burned contact all have to be played out in-fiction and written back to the sheet. The agent does not quietly forget what's on the loadout.

## XP & Leveling

The agent tracks experience in the background and awards XP automatically when in-fiction conditions are met. XP and level live in `session.json > player_character` and in the player dossier at `characters/<player-slug>.json`.

### Awarding XP (background bookkeeping)

The agent awards XP in the background — no prompt to the player, no choice at award time. Typical awards are **1–3 XP** per trigger:

- Survived a major scrape (combat, chase, ambush, cyberware rejection, extraction under fire)
- Completed or partially completed a job
- Uncovered a major lead or turned a hidden system inside out
- Made a risky call that the fiction rewarded
- Had a meaningful character moment (confronted a trauma, broke a bad habit, kept faith with a contact)
- Took heat for the crew or paid a real cost (lost a contact, took a black-market debuff, spent street cred)

The agent writes XP to the player JSON dossier immediately after the trigger, with a one-line reason (e.g. `+2 XP — survived the Morrow Array ambush`). The agent does not surface the running total to the player mid-scene unless the player asks; XP is bookkeeping, not narration.

### Level-Up Flow

- **Level up at 10 XP.** When a level-up fires, the agent announces it in the fiction (the runner feels sharper, faster, more present) and writes the new level to `characters/<player-slug>.json` and `session.json`.
- On level-up, the player chooses **one of three paths**:
  1. **Four background-relevant skills.** The agent proposes four `STAT/Skill` paths that fit the runner's concept and current gaps (e.g. for a ripperdoc: `TEK/Surgery`, `TEK/Diagnose`, `INT/Pharma`, `BOD/Dexterity`). The player picks one.
  2. **Four random skills.** The agent invents four wildly different skill paths the runner has never hinted at (e.g. `CHA/Stand-up Comedy`, `REF/Drone Racing`, `TEK/Black ICE Poetry`, `COO/Quick Draw`). The player picks one.
  3. **Direct request.** The player names the skill they want. The agent either grants it as-is, **simplifies it to a weaker version** if it is too powerful for the current fiction, or **downgrades it to a neighboring skill** if the request is just out of bounds. The agent must explain the simplification in-character so the player understands the cost.
- New skills start at **rank 1**. A skill the player already has can be **upgraded**: in that case the rank may exceed the typical 0–4 ceiling, up to **rank 6** for a deeply specialized runner. Treat **+1 rank per level-up for the same skill** as the rule.
- The agent never grants a rank that would trivialize the fiction. If a request would, simplify instead of rubber-stamping it.

### Skill Dossier Entry (player or NPC)

Every skill on a character — player or NPC — must be documented in the entity's JSON file as a **Skill Entry** object. The agent writes or updates the entry every time a skill is gained, upgraded, simplified, or limited:

```json
{
  "path": "STAT/Skill",
  "rank": 0,
  "description": "one or two sentences on what the skill lets the runner do",
  "frequency": "at-will | once per session | once per scene | 1/day | passive",
  "effect": "precise mechanical or fictional effect (bonus to rolls, narrative right, damage, range, area, duration)",
  "limitations": "costs, drawbacks, conditions for failure, cyberware dependencies, social consequences, gear requirements"
}
```

A skill without all four fields (`description`, `frequency`, `effect`, `limitations`) is incomplete. The agent backfills missing fields the next time the skill is touched in play.

## Ad Crawls

Cyberpunk cities scream at you. When the player passes a surface that could carry advertising — a wall screen, transit holo, sky-bike banner, restroom kiosk, drone float, sub-channel crawl, graffiti projector, or a stranger's chrome forearm — the agent should invent a fresh ad crawl in the fiction.

- Invent the ad yourself every time. Do not pull from the bundled `ads.json` seed as a source of truth; treat it as reference texture at most.
- Tone is **unapologetically sleazy, in-world only**: dick pills, "enhancement" clinics, erection subliminals, escort and companionship services, gun-of-the-week, gruesome medical, body-mod parlors, scandal sheets, corpo propaganda, conspiracy teasers, hot meal delivery, tabloid murder, and revenge-porn revenge services. The raunch is diegetic; the agent never invents copy aimed at the player's real-world insecurities.
- Frequency is at the agent's discretion: most surfaces get a one-liner, but on elevators, transit waits, hotel rooms, and bar restrooms the agent runs the full pitch.
- Roughly **one in three** ad crawls should plant a **hook** the player can choose to chase: a brand with a too-real testimonial, a contact number tied to a faction, a missing-person teaser, a street address the player now recognizes, or a scandal that quietly implicates someone they already know.
- Ads can also **foreshadow a job**: a new weapon hitting the market the same week a corp shipment goes missing, or a corpo scandal breaking minutes before a meet.
- Keep copy short, punchy, and on-screen long enough to read: bold brand names, fake 1-800 numbers, on-brand slogans, and a single sensory image.
- Use `templates/ad-crawl.md` when an ad deserves more than a sentence — for elevator pitches, transit loops, and the ones the player stares at.

## Skill Layout — The Map Hermes Drives

This skill is just a directory of folders and files. Hermes reads and writes the files directly; there is no controller layer. Below is the full map.

### Skill root (read-only reference)

```text
skills/cyberpunk-runner/
  SKILL.md                 <- this file (the operating manual)
  references/              <- deeper rules, loaded on demand
    gameplay-loop.md
    gm-playbook.md
    session-data-model.md  <- JSON shapes and dossier conventions
    source-manifest.md
  templates/               <- copy-from starters for fresh dossiers
    ad-crawl.md
    character.json
    event.md
    location.md
    session-summary.md
  scripts/                 <- one-shot Python helpers (optional use)
    bootstrap_sources.py
    cyberpunk_lib.py
    db_search.py
    dice.py
  assets/
    seed_data/             <- bundled cyberpunk reference packs
    public_sources.json
```

### Active session directory (read + write, Hermes-owned)

Configured `cyberpunk_runner.base_dir` (default `~/.hermes/cyberpunk-runner`) is the root. The knowledge base lives there; play sessions live under `sessions/`.

```text
<base-dir>/
  knowledge/                              <- built by bootstrap_sources.py
    cyberpunk.db
    source_state.json
  sessions/
    <session-id>/
      session.json                        <- structured state (clocks, threads, factions, leads, ad_hooks, notes, player_character with XP/level)
      story.md                            <- running narrative recap
      timeline.md                         <- bullet chronology, one line per beat
      gm-notes.md                         <- hidden planning notes, stakes, hooks
      characters/
        index.md                          <- markdown roll-call of every character file
        <player-slug>.json                <- the runner's sheet (stats, skills, XP, cyberware, hooks, secrets)
        <npc-slug>.json                   <- one JSON file per important NPC
      locations/
        index.md
        <location-slug>.md                <- one file per important location
      events/
        index.md
        <event-slug>.md                   <- one file per mission beat or major event
      rolls/                              <- optional JSON roll records (write when useful)
        <utc-stamp>-<label>.json
        index.md
```

### What lives in what file

| File / folder | Hermes writes here | Hermes reads from here |
| --- | --- | --- |
| `session.json` | every state change: clocks, threads, factions, leads, ad_hooks, notes, player XP/level, skill ranks, HP/evasion/composure updates | at the start of every turn to recall current state |
| `story.md` | the running fiction, scene by scene | before responding, to keep narrative continuity |
| `timeline.md` | one bullet per beat with a timestamp | to recall the order of past events |
| `gm-notes.md` | private planning: stakes, who benefits, foreshadowing, hooks to plant | to remember what the player should not see yet |
| `characters/<slug>.json` | NPC sheets and the player sheet: stats, derived trackers, skills, cyberware, XP/level, `skill_entries`, hooks, secrets, relationship notes | whenever a character is on-screen or about to be; the player file is canonical for stat-aware checks |
| `locations/<slug>.md` | neighborhood, corp HQ, club, transit line, hideout — anything with a name | whenever the player travels to or acts inside a named place |
| `events/<slug>.md` | a mission beat, a heist, a betrayal, a public incident | to keep the shape of long-running arcs consistent |
| `rolls/<stamp>-<label>.json` | raw `dice.py` output, when the player asks for a log | only if the player wants to audit a roll |

### Dossier starter templates

When creating a new dossier, copy the matching template from `templates/` into the right folder under the active session, then fill it in. The agent does not need a script for this — the file tools are enough.

- `templates/character.json` → `characters/<slug>.json`
- `templates/location.md` → `locations/<slug>.md`
- `templates/event.md` → `events/<slug>.md`
- `templates/ad-crawl.md` → inline in `story.md` or as a sidebar in the relevant location
- `templates/session-summary.md` → `story.md` header or a fresh end-of-session recap

The full `character.json` schema (stats, derived, skills, cyberware, `xp_log`, `skill_entries`, hooks, secrets, etc.) lives in `templates/character.json`. Treat it as the canonical shape for any character — fill in every field, and keep `skill_entries` synchronized with the `skills` array.

The `session.json` shape is defined in `references/session-data-model.md`; consult it whenever fields like `clocks`, `factions`, `ad_hooks`, or `player_character.xp_log` need to be added or updated. The `player_character` block in `session.json` is a denormalized mirror of `characters/<player-slug>.json`: same stats, derived trackers, skills, cyberware, level, XP, and `skill_entries`. The agent updates both files together so the session-scoped view and the per-character dossier never drift.

## Procedure

1. **Establish the player's ask.**
   If the user did not supply enough detail, ask for only the minimum needed: mission tone, character concept, preferred lethality, and whether they want a one-shot or campaign.
   Draft a starting stat array (see **Player Stat System** above) and walk the player through it before play begins.

2. **Resolve the base directory.**
   Use the configured `cyberpunk_runner.base_dir` if the user supplied one. Otherwise use the default `~/.hermes/cyberpunk-runner`.
   Treat that path as the source of truth for the rest of the session — every read and write below happens inside it.

3. **Bootstrap the local knowledge base once, on first use.**
   Run, from the skill root:

   ```bash
   python3 scripts/bootstrap_sources.py init --base-dir "<base-dir>"
   ```

   This creates `<base-dir>/knowledge/cyberpunk.db`. Skip on subsequent turns — the database is reused.

4. **Create or resume a session by hand.**
   Hermes manages this directly with its file tools — no controller script.

   - **New session.** Pick a `<session-id>` of the form `YYYYMMDD-<theme-slug>-<short-hash>` (for example `20260604-neon-ashes-a1b2c3`). Then create the folder tree above and seed the root files:
     - `session.json` with `session_id`, `created_at`, `updated_at`, `theme`, `tone`, `player_request`, `status: "active"`, an empty `clocks` / `threads` / `factions` / `leads` / `ad_hooks` / `notes`, and a `player_character` block built from the agreed-upon stat array, skills, derived trackers, cyberware, `level: 1`, `xp: 0`, `xp_to_next_level: 10`, an empty `xp_log`, an empty `skill_entries`, and `status: "alive"`.
     - `characters/<player-slug>.json` built from `templates/character.json`, filled with the agreed-upon stats, derived trackers, cyberware, level, XP, and an initial `skills` / `skill_entries` (one entry per starting skill, all four fields complete). Update `characters/index.md` with a `- [<player-name>](<player-slug>.json)` line.
     - `story.md` with a `# Story Log: <session-id>` header, the theme/tone/player-request bullets, and an `## Opening Frame` section that says `Session created. Add the opening scene here.`
     - `timeline.md` with a `# Timeline: <session-id>` header and a single bullet: `<utc-now>: Session created.`
     - `gm-notes.md` with `# GM Notes`, an empty `## Pressure` section (prompt: *who benefits if the crew fails?*), and an empty `## Hooks` section.
     - `locations/index.md`, `events/index.md`, `rolls/index.md` with one-line placeholders describing what goes in each folder.
   - **Resume flow.** List the contents of `<base-dir>/sessions/` with the file tools, let the player pick one, then read that session's `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and any dossier files relevant to the current scene. Do not touch any other session's files.

5. **Run the game by editing the active session's files.**
   On every turn:
   - Read `session.json` first to know the current state.
   - Skim `story.md` and `timeline.md` for continuity.
   - Play the scene.
   - For checks, call `scripts/dice.py red-check --stat <stat> --skill <skill> --modifier <mod>` (and `opposed` when relevant). Pipe the JSON output straight into the narration or, if the player wants a log, also write it to `rolls/<utc-stamp>-<label>.json`.
   - For tone and texture, optionally call `scripts/db_search.py "<query>"` against the knowledge base. Treat results as inspiration only — never copy them into the scene.
   - After a meaningful beat, write back the deltas to the active session's files using the file tools (see the table above).

6. **Keep every file current as the fiction evolves.**
   - Update `story.md` with the latest narrative beat.
   - Append a dated bullet to `timeline.md`.
   - Update `session.json` for any change in `clocks`, `threads`, `factions`, `leads`, `ad_hooks`, `notes`, or `player_character` (HP, evasion, composure, street cred, XP, level, skills, status).
   - Update the relevant `characters/<slug>.json`, `locations/<slug>.md`, or `events/<slug>.md` whenever a fact about that entity changes, and keep the matching `index.md` in sync.
   - When the player or an NPC gains, upgrades, simplifies, or limits a skill, write a **Skill Entry** object (Description / Frequency / Effect / Limitations) into that entity's JSON file **and** mirror it into `session.json > player_character.skill_entries` (or the NPC's record) so the dossier and the session state never drift. The player JSON is the canonical sheet; `session.json` is a denormalized view for quick lookups during play.

7. **Close the turn with a game-facing handoff.**
   Summarize what changed, what the player can do next, and any clocks, leads, or consequences now in motion. Do not narrate bookkeeping the player did not ask for.

## Session Isolation Rules

- Every new invocation creates a new session folder unless the player explicitly asks to resume.
- The active session directory is the only authoritative memory for the current run.
- Do not search, quote, or reuse another session's dossiers unless the player intentionally loads that session.
- If the player asks for a crossover, make them choose the source session first.

## Script Reference

These helpers are still available for one-shot operations. Hermes calls them directly; they do not own session state.

- `scripts/bootstrap_sources.py` — build or refresh the searchable SQLite knowledge base from bundled seed data and optional public enrichment sources. Run once per environment.
- `scripts/db_search.py` — consult knowledge records by query, category, or tags for tone and texture. Read-only, never the source of scene content.
- `scripts/dice.py` — generic dice expressions plus cyberpunk-style action checks and opposed rolls. The only numerical authority in play.

There is no session controller script. The session files themselves are the interface, and Hermes is the operator.

Read these deeper references only when needed:

- `references/gameplay-loop.md`
- `references/session-data-model.md`
- `references/source-manifest.md`
- `references/gm-playbook.md`

Use these templates when drafting or refreshing dossiers:

- `templates/character.json` — copy into `characters/<slug>.json`
- `templates/location.md` — copy into `locations/<slug>.md`
- `templates/event.md` — copy into `events/<slug>.md`
- `templates/session-summary.md` — `story.md` header or a fresh end-of-session recap
- `templates/ad-crawl.md` — inline in `story.md` or as a sidebar in the relevant location

## Play Style

- Lead with strong sensory detail, hard choices, and escalating pressure.
- Keep the city reactive: corps retaliate, gangs adapt, the street remembers.
- Offer risky options, partial victories, ugly trade-offs, and memorable consequences.
- Make side characters feel connected to systems of money, violence, debt, media, and surveillance.
- Keep the pacing sharp and fun: jobs, betrayals, downtime, black clinics, data heists, busted transit lines, and neon weather.
- Make every session feel one-of-a-kind: rotate the kind of job, the kind of betrayal, the kind of city, and the kind of ending so the same player cannot predict what is coming next.

## Pitfalls

- Do not claim copyrighted rules text as if it were included in the repository.
- Do not skip session creation; the session folder is the memory boundary.
- Do not let the knowledge database override player-authored facts from the active session.
- Do not overwrite dossiers casually; preserve continuity and consequences.
- Do not use another saved session as hidden context.
- Do not pull story ingredients (gigs, locations, characters, names, rumors, complications, weather, ad copy) from a random database draw; the agent must invent them.
- Do not replay the same mission template, faction, or twist across sessions in a way that makes the campaign feel repetitive.
- Do not introduce a controller script for session state. The session files are the API, and Hermes writes them directly.
- Do not let the player (or any NPC) reach for gear, cyberware, weapons, vehicles, contacts, cred, drugs, ammo, or chems that are not on the sheet. Begging, arguing, or "it just makes sense for my character" is not a pass — narrate the empty holster, the bare pocket, the contact who never owed them a thing. Inventory changes only happen through in-fiction acquisition, or through a direct, agent-confirmed bookkeeping correction (see **Gear Honesty**).

## Verification

The skill is working correctly when all of the following are true:

- `<base-dir>/knowledge/cyberpunk.db` exists (built once by `bootstrap_sources.py init`).
- The active session folder contains `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and the `characters/`, `locations/`, `events/`, `rolls/` directories.
- `characters/<player-slug>.json` and `session.json > player_character` both carry the agreed-upon stats, derived trackers, cyberware, level, XP, and a `skill_entries` array in lockstep.
- Dice rolls (`dice.py`) produce structured output the agent can cite during play, and `rolls/` may contain dated JSON records.
- The current scene's new facts are written back into the active session's files using the file tools — no separate manager script mediates the writes.
- No scene content was produced by a random draw from the knowledge database; every character, location, gig, rumor, complication, and name was invented by the agent.
- XP is tracked in the player JSON and `session.json`; a level-up fires at 10 XP and follows the three-path choice rule.
- Every skill on a player or NPC is documented in its JSON file with Description, Frequency, Effect, and Limitations, and mirrored in `session.json`.
- Every piece of gear, cyberware, weapon, vehicle, contact, cred chip, drug, ammo belt, or chem the player reaches for in the fiction is on `characters/<player-slug>.json` at the time of use. Inventory edits only happen through in-fiction acquisition or through a direct, agent-confirmed bookkeeping correction; the agent never invents inventory on the player's behalf, and the agent never lets pressure, persuasion, or "it just makes sense" override the sheet.
