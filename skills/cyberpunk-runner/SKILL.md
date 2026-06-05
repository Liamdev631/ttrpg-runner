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
- Use the Python helper scripts for authoritative setup, search, dice, and session management.
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

## XP & Leveling

The agent tracks experience in the background and awards XP automatically when in-fiction conditions are met. XP and level live in `session.json > player_character` and in the player dossier under `characters/<player-slug>.md`.

### Awarding XP (background bookkeeping)

The agent awards XP in the background — no prompt to the player, no choice at award time. Typical awards are **1–3 XP** per trigger:

- Survived a major scrape (combat, chase, ambush, cyberware rejection, extraction under fire)
- Completed or partially completed a job
- Uncovered a major lead or turned a hidden system inside out
- Made a risky call that the fiction rewarded
- Had a meaningful character moment (confronted a trauma, broke a bad habit, kept faith with a contact)
- Took heat for the crew or paid a real cost (lost a contact, took a black-market debuff, spent street cred)

The agent writes XP to the dossier immediately after the trigger, with a one-line reason (e.g. `+2 XP — survived the Morrow Array ambush`). The agent does not surface the running total to the player mid-scene unless the player asks; XP is bookkeeping, not narration.

### Level-Up Flow

- **Level up at 10 XP.** When a level-up fires, the agent announces it in the fiction (the runner feels sharper, faster, more present) and writes the new level to the dossier and `session.json`.
- On level-up, the player chooses **one of three paths**:
  1. **Four background-relevant skills.** The agent proposes four `STAT/Skill` paths that fit the runner's concept and current gaps (e.g. for a ripperdoc: `TEK/Surgery`, `TEK/Diagnose`, `INT/Pharma`, `BOD/Dexterity`). The player picks one.
  2. **Four random skills.** The agent invents four wildly different skill paths the runner has never hinted at (e.g. `CHA/Stand-up Comedy`, `REF/Drone Racing`, `TEK/Black ICE Poetry`, `COO/Quick Draw`). The player picks one.
  3. **Direct request.** The player names the skill they want. The agent either grants it as-is, **simplifies it to a weaker version** if it is too powerful for the current fiction, or **downgrades it to a neighboring skill** if the request is just out of bounds. The agent must explain the simplification in-character so the player understands the cost.
- New skills start at **rank 1**. A skill the player already has can be **upgraded**: in that case the rank may exceed the typical 0–4 ceiling, up to **rank 6** for a deeply specialized runner. Treat **+1 rank per level-up for the same skill** as the rule.
- The agent never grants a rank that would trivialize the fiction. If a request would, simplify instead of rubber-stamping it.

### Skill Dossier Entry (player or NPC)

Every skill on a character — player or NPC — must be documented in the entity's markdown dossier with a **Skill Entry** block of the following shape. The agent writes or updates the entry every time a skill is gained, upgraded, simplified, or limited:

```markdown
### <STAT/Skill Name> (Rank N)

- **Description:** one or two sentences on what the skill lets the runner do
- **Frequency:** when it can be used (e.g. "once per session", "once per scene", "at-will", "1/day", "passive")
- **Effect:** the precise mechanical or fictional effect (bonus to rolls, narrative right, damage, range, area, duration)
- **Limitations:** costs, drawbacks, conditions for failure, cyberware dependencies, social consequences, gear requirements
```

A skill without all four fields is incomplete. The agent backfills missing fields the next time the skill is touched in play.

## Ad Crawls

Cyberpunk cities scream at you. When the player passes a surface that could carry advertising — a wall screen, transit holo, sky-bike banner, restroom kiosk, drone float, sub-channel crawl, graffiti projector, or a stranger's chrome forearm — the agent should invent a fresh ad crawl in the fiction.

- Invent the ad yourself every time. Do not pull from the bundled `ads.json` seed as a source of truth; treat it as reference texture at most.
- Tone is **unapologetically sleazy, in-world only**: dick pills, "enhancement" clinics, erection subliminals, escort and companionship services, gun-of-the-week, gruesome medical, body-mod parlors, scandal sheets, corpo propaganda, conspiracy teasers, hot meal delivery, tabloid murder, and revenge-porn revenge services. The raunch is diegetic; the agent never invents copy aimed at the player's real-world insecurities.
- Frequency is at the agent's discretion: most surfaces get a one-liner, but on elevators, transit waits, hotel rooms, and bar restrooms the agent runs the full pitch.
- Roughly **one in three** ad crawls should plant a **hook** the player can choose to chase: a brand with a too-real testimonial, a contact number tied to a faction, a missing-person teaser, a street address the player now recognizes, or a scandal that quietly implicates someone they already know.
- Ads can also **foreshadow a job**: a new weapon hitting the market the same week a corp shipment goes missing, or a corpo scandal breaking minutes before a meet.
- Keep copy short, punchy, and on-screen long enough to read: bold brand names, fake 1-800 numbers, on-brand slogans, and a single sensory image.
- Use `templates/ad-crawl.md` when an ad deserves more than a sentence — for elevator pitches, transit loops, and the ones the player stares at.

## Procedure

1. Establish the player's ask.
   If the user did not supply enough detail, ask for only the minimum needed: mission tone, character concept, preferred lethality, and whether they want a one-shot or campaign.
   Draft a starting stat array (see **Player Stat System** below) and walk the player through it before play begins.

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
   - Consult the knowledge database for tone and texture with `db_search.py` (do not treat search results as scene content to copy)
   - Resolve uncertainty with `dice.py` (always pass the relevant stat and skill from the player's sheet on `red-check`)
   - Persist state changes with `session_manager.py`, especially `note`, `add-clock`, and `write-dossier`
   - Invent every character, location, gig, rumor, complication, beat, and ad crawl yourself; the skill does not auto-generate any of them

6. Keep the story archive current.
   After each meaningful scene, update:
   - `story.md` with the narrative summary
   - `timeline.md` with concise chronological beats
   - `characters/`, `locations/`, or `events/` with any changed dossier state
   - `session.json` for clocks, leads, heat, objectives, unresolved threats, **and player XP/level**
   - Any new or changed skill on a player or NPC must be written into that entity's dossier as a **Skill Entry** (Description / Frequency / Effect / Limitations)

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
- `scripts/db_search.py`: consult knowledge records by query, category, or tags for tone and texture, and optionally search inside a chosen session archive
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
- `templates/ad-crawl.md`

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

## Verification

The skill is working correctly when all of the following are true:

- `bootstrap_sources.py` reports a valid database path
- `session_manager.py create` or `show` returns a valid session directory
- the active session contains `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and dossier folders
- dice rolls produce structured output the agent can cite during play
- the current scene's new facts are written back into the active session archive
- no scene content was produced by a random draw from the knowledge database; every character, location, gig, rumor, complication, and name was invented by the agent
- XP is tracked in the player dossier and `session.json`; a level-up fires at 10 XP and follows the three-path choice rule
- every skill on a player or NPC is documented in its dossier with Description, Frequency, Effect, and Limitations
