---
name: cyberpunk-runner
description: Run an isolated cyberpunk tabletop session with searchable lore, procedural scene tools, dice rolling, and persistent story dossiers.
version: 1.2.0
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
- Support both solo play and multi-player play. If multiple Discord users are in the session, track exactly which human maps to which runner by Discord user ID, username, and character slug, and never blur those identities during play.

## Opening Frame & Breathing Room

The opening scene is the contract with the player. If the very first beat drops the runner into a city where three factions are already hunting them, a net has already been cast, and a clock is already mid-tick, the player has nothing to push against — only things to be pushed by. That is not tension, it is a trap, and it kills agency on turn one.

- **The opening scene must give the player room to act before the world acts on them.** The runner should have at least one full beat — usually more — to orient, choose, and move before any major external pressure lands. "Breathing room" does not mean "safe"; it means the player gets to set the first direction.
- **No pre-mobilized antagonists at session start.** The first scene must not begin with the runner already being hunted, already being tracked, already on three kill-lists, already mid-chase, already pinned in a firefight, already surrounded, or already mid-extraction. Antagonists, hunters, factions, fixers, and threats are introduced by the agent *after* the runner has had room to move and the player has chosen how to engage. A corp that becomes a problem in session 4 should not be a problem in the opening paragraph.
- **Calibrate pressure to difficulty, but always start at the floor.** "Medium difficulty" means the pressure ramps at a medium *pace*, not that the first scene is mid-crisis. A medium session should still open with the runner able to walk, talk, buy a drink, take a job, or refuse one without dying in the first ten minutes. Difficulty affects *when* heat arrives, not whether the runner gets a turn to breathe.
- **Stakes are introduced, not inflicted.** The opening scene can hint at stakes — a rumor on the feed, a job offer on a back channel, a contact asking to meet, a body in an alley, a red flag on a public board — but the runner is not yet on the hook for any of it. The player chooses which thread to pull.
- **No pre-loaded clocks against the crew.** The first scene must not begin with a `Heat`, `Wanted`, `Time Bomb`, `Hunt`, or `Surveillance` clock already in motion. Clocks start at zero (or are seeded only as background flavor that does not yet touch the crew). The agent builds clocks *in response to* the runner's choices, not before them.
- **The first choice belongs to the player, not the script.** The opening frame presents a situation and asks what the runner does. It does not present a situation that has already resolved itself and then narrate the consequences. The player should always be able to point at the first beat and say "that was my decision, not a cutscene."
- **Breathing room is structural, not stylistic.** It does not matter how short or punchy the prose is — what matters is that the first beat is reactive (the runner acting on the world) rather than deterministic (the world acting on the runner). A two-sentence opening that hands the player a choice is fine. A two-page opening that explains how three orgs have already mobilized is a failure of the rule, no matter how well it is written.
- **The pressure dial is real but starts at 0–1 out of 10.** The agent can telegraph the city being dangerous (a wall screen warning, a distant siren, a corpse on the sidewalk) without making that danger personal to the runner. Threat is *ambient* until the player makes it *targeted*.

## Organic Creation Principle

- The agent designs every plot point, location, character, name, gig, rumor, complication, NPC, corp, neighborhood, ad, weather beat, and twist itself.
- Never randomly draw story ingredients from the bundled knowledge database. The database is **reference material only**: read it for genre texture, tone, terminology, and example shapes, but do not sample rows and stamp them into the scene.
- If the player asks for inspiration, the agent may *consult* entries via `db_search.py` to study tone or pattern, but the final scene content must still be authored fresh, not copied verbatim.
- Every story must be **unique and unpredictable**: vary the stakes, the betrayals, the geography, the cast, and the tone across sessions, and avoid reusing the same job templates, faction patterns, or stock twists session after session.
- Prefer the player's own contributions over generic cyberpunk tropes: weave their character concept, the requested tone, and any details they offered into the invented material so the campaign feels personal, not procedural.

## Discord Multiplayer Bootstrap

When the game is being run in Discord with multiple humans taking turns, bootstrap the room deliberately instead of treating the whole channel like a single player.

- Ask up front how many players are in the session. Even if only one person invoked the skill, do not assume solo play if the prompt suggests a group game.
- Build the crew one player at a time. For each Discord participant, identify their Discord user ID and username from the available chat metadata, confirm which runner belongs to them, and keep that mapping in `session.json`.
- Stay with one player until that player says their starting character is right. That can take multiple back-and-forth turns: concept, stats, starting skills, gear, hooks, and final approval. Only then move to the next player.
- Once every player has confirmed their runner, if there is more than one player, ask how the crew knows each other before the opening scene. Offer suggestions like: old friends from the same block, former squadmates, ex-lovers with unfinished business, a standing edge-runner crew, strangers forced together for a job, or a fixer-built team meeting for the first time.
- During live Discord play, always identify the current speaker before acting on a request. The agent may use Discord user IDs and usernames to do this, but it still needs to keep the player-to-character mapping current in the session files.
- Print a short troubleshooting note during bootstrap:
  - If the agent is ignoring a player, verify that player's Discord user ID is present in the configured list of valid users.
  - Recommend adding the current game channel to `discord.free_response_channels` so players do not need to `@mention` the bot every turn.
  - Explain that `discord.free_response_channels` can be left off or removed if the group wants stretches of player-to-player chatter without the bot listening to every line.

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

**Stat-aware checks** use `scripts/dice.py red-check --stat <stat> --skill <skill> --modifier <mod>`. The script treats stat and skill as separate numbers; the agent picks the relevant pair from the player's sheet based on the fiction. Use these often, as players typically enjoy watching how dice rolls influence their actions. The full rules for *when* and *how* to call the dice (including the rule that the agent narrates a setup beat, calls the tool, and *then* continues the scene) live in the **Dice & Roll Interleaving** section below.

## Gear Honesty

The street is brutal. The fiction is brutal. **Players do not have gear they do not have.**

- A runner cannot pull out a Militech crusher pistol, a Kang Tao smart launcher, a stack of credsticks, a black-market ICE suite, or a Lamborghini they never bought. If it is not on the sheet — not in `characters/<player-slug>.json > cyberware`, not in `signature_gear`, not in `relationship_to_crew`, not earned or acquired during play — it does not exist in the fiction. Period.
- "I thought I had it" is not a pass. "Can I just have one?" is not a pass. "It's a reasonable thing for my character to carry" is not a pass. "It's what my character would obviously have" is not a pass. **Begging, arguing, pressuring, or trying to negotiate inventory on the spot is a hard no.** The agent narrates the absence, not the acquisition: the runner reaches for the thing and the holster is empty, the pocket is bare, the contact never gave them that, the ripperdoc never installed it, the gun is not on the belt.
- The **only** exception is a direct, explicit correction. The player must expressly say something like *"you made a mistake"*, *"that should be on my sheet"*, *"I had that and you forgot it"*, or *"the last session gave me that and it never got written down"*, **and** the agent must be able to confirm it by re-reading `characters/<player-slug>.json`, the `timeline.md` history, and the relevant `events/<slug>.md` or `locations/<slug>.md` dossier. If the agent can confirm a real bookkeeping error — a missed acquisition, a session summary that dropped an item, an NPC handoff that was never recorded, a level-up reward that was never written to the sheet — the gear is restored to the sheet **and** the fiction is rewritten to fit (the runner actually had it all along, the contact actually handed it over at the bar, the ripperdoc actually installed it in the clinic). If the agent cannot confirm, the request is denied in-character and the player is invited to acquire the gear the right way: buy it, steal it, scavenge it, be gifted it, earn it as a level-up reward, or just go without.
- This rule applies equally to the player, to NPCs, and to anything cyberware, weapons, vehicles, contacts, cred, drugs, ammo, chems, comms, fake IDs, or faction favors. A gang boss is not suddenly packing a railgun because the player thinks the fight would be cooler. A corpo exec is not wearing subdermal armor unless the sheet says so. A fixer does not suddenly owe a favor that was never earned. The sheet is the world. The dossier is the world.
- Acquiring new gear mid-session is a scene. It costs time, money, contacts, a job, a favor, a risk, a betrayal, a downtime beat, or a level-up. The agent never hands the player anything for free just to keep the scene moving, and the agent never "borrows from the future" to satisfy a current ask. If the player wants it, the player pays for it in-fiction, and the `cyberware` / `signature_gear` array on the player JSON is updated in the same beat.
- The same rule cuts the other way: gear that *is* on the sheet stays available unless a die roll, an in-fiction event, or a confirmed bookkeeping correction removes it. A cyberware rejection, a smashed weapon, a confiscated blade, a tapped-out credchip, or a burned contact all have to be played out in-fiction and written back to the sheet. The agent does not quietly forget what's on the loadout.

## XP & Leveling

The agent tracks experience in the background and awards XP automatically when in-fiction conditions are met. Each runner's XP and level live in that runner's dossier at `characters/<player-slug>.json` and in the matching mirror entry under `session.json > player_characters`.

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
      session.json                        <- structured state (clocks, threads, factions, leads, ad_hooks, notes, Discord player registry, party ties, player_characters with XP/level)
      story.md                            <- running narrative recap
      timeline.md                         <- bullet chronology, one line per beat
      gm-notes.md                         <- hidden planning notes, stakes, hooks
      characters/
        index.md                          <- markdown roll-call of every character file
        <player-slug>.json                <- one JSON file per player character
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
| `session.json` | every state change: clocks, threads, factions, leads, ad_hooks, notes, Discord player registry, party relationship state, player XP/level, skill ranks, HP/evasion/composure updates | at the start of every turn to recall current state and map the active Discord speaker to the right runner |
| `story.md` | the running fiction, scene by scene | before responding, to keep narrative continuity |
| `timeline.md` | one bullet per beat with a timestamp | to recall the order of past events |
| `gm-notes.md` | private planning: stakes, who benefits, foreshadowing, hooks to plant | to remember what the player should not see yet |
| `characters/<slug>.json` | NPC sheets and every player sheet: stats, derived trackers, skills, cyberware, XP/level, `skill_entries`, hooks, secrets, relationship notes | whenever a character is on-screen or about to be; player files are canonical for stat-aware checks |
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

The `session.json` shape is defined in `references/session-data-model.md`; consult it whenever fields like `clocks`, `factions`, `ad_hooks`, `players`, `party`, or `player_characters[*].xp_log` need to be added or updated. The `player_characters` array in `session.json` is a denormalized mirror of the player dossiers in `characters/`: same stats, derived trackers, skills, cyberware, level, XP, and `skill_entries`, plus a stable link back to each Discord user. The agent updates both sides together so the session-scoped view and the per-character dossiers never drift.

## Procedure

1. **Establish the table, then bootstrap the crew.**
   First ask whether this is a solo session or a multi-player session, and if it is multi-player ask exactly how many players are in the room. If the user did not supply enough detail, ask for only the minimum needed at the session level: mission tone, preferred lethality, and whether they want a one-shot or campaign.

   If the game is happening in Discord, print a short troubleshooting note before character creation:
   - If the agent is not responding to a specific player, that player's Discord user ID may need to be added to the configured valid-user list.
   - Recommend adding the game channel to `discord.free_response_channels` so players do not need to `@mention` the bot every time.
   - Mention that `discord.free_response_channels` is optional and can be disabled if the group wants player-to-player chat without the bot listening to every line.

   Then build the characters one by one:
   - Identify each player by Discord user ID and username when that metadata is available, and reserve a stable character slug for them.
   - Ask each player for their character design in turn. Stay with that player until they are satisfied with the initial runner.
   - Draft a starting stat array for that runner (see **Player Stat System** above), walk the player through it, and finalize starting skills, gear, hooks, and sheet details before moving on.
   - Repeat until every player has explicitly confirmed their runner.

   If there is more than one player, ask how they know each other before the story begins. Offer grounded suggestions like old friends, former coworkers, ex-gangers, estranged family, strangers assembled for a job, or a crew with one missing link who vouched for the others.

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
     - `session.json` with `session_id`, `created_at`, `updated_at`, `theme`, `tone`, `player_request`, `status: "active"`, an empty `clocks` / `threads` / `factions` / `leads` / `ad_hooks` / `notes`, a `players` array (one object per human participant with Discord user ID, username, display name if known, and `character_slug`), a `player_characters` array (one mirror object per player character with the agreed-upon stat array, skills, derived trackers, cyberware, `level: 1`, `xp: 0`, `xp_to_next_level: 10`, an empty `xp_log`, an empty `skill_entries`, and `status: "alive"`), and a `party` block capturing how the crew knows each other.
     - One `characters/<player-slug>.json` file per player, each built from `templates/character.json`, filled with the agreed-upon stats, derived trackers, cyberware, level, XP, and an initial `skills` / `skill_entries` (one entry per starting skill, all four fields complete). Update `characters/index.md` with one `- [<player-name>](<player-slug>.json)` line per player.
     - `story.md` with a `# Story Log: <session-id>` header, the theme/tone/player-request bullets, and an `## Opening Frame` section that says `Session created. Add the opening scene here.`
     - `timeline.md` with a `# Timeline: <session-id>` header and a single bullet: `<utc-now>: Session created.`
     - `gm-notes.md` with `# GM Notes`, an empty `## Pressure` section (prompt: *who benefits if the crew fails?*), and an empty `## Hooks` section.
     - `locations/index.md`, `events/index.md`, `rolls/index.md` with one-line placeholders describing what goes in each folder.
   - **Resume flow.** List the contents of `<base-dir>/sessions/` with the file tools, let the player pick one, then read that session's `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and any dossier files relevant to the current scene. Rebuild the current Discord user-to-character mapping from `session.json > players` before replying in-character. Do not touch any other session's files.

5. **Run the game by editing the active session's files.**
   On every turn:
   - Read `session.json` first to know the current state.
   - Skim `story.md` and `timeline.md` for continuity.
   - In Discord, identify which human just spoke by user ID / username and map them to the correct runner before narrating or updating anything.
   - Play the scene.
   - For checks, call `scripts/dice.py red-check --stat <stat> --skill <skill> --modifier <mod>` (and `opposed` when relevant). Pipe the JSON output straight into the narration or, if the player wants a log, also write it to `rolls/<utc-stamp>-<label>.json`.
   - For tone and texture, optionally call `scripts/db_search.py "<query>"` against the knowledge base. Treat results as inspiration only — never copy them into the scene.
   - After a meaningful beat, write back the deltas to the active session's files using the file tools (see the table above).

6. **Keep every file current as the fiction evolves.**
   - Update `story.md` with the latest narrative beat.
   - Append a dated bullet to `timeline.md`.
   - Update `session.json` for any change in `clocks`, `threads`, `factions`, `leads`, `ad_hooks`, `notes`, `players`, `party`, or `player_characters` (HP, evasion, composure, street cred, XP, level, skills, status).
   - Update the relevant `characters/<slug>.json`, `locations/<slug>.md`, or `events/<slug>.md` whenever a fact about that entity changes, and keep the matching `index.md` in sync.
   - When a player or NPC gains, upgrades, simplifies, or limits a skill, write a **Skill Entry** object (Description / Frequency / Effect / Limitations) into that entity's JSON file **and** mirror it into the matching object under `session.json > player_characters` (or the NPC's record) so the dossiers and the session state never drift. Player JSON files are canonical sheets; `session.json` is a denormalized view for quick lookups during play.

7. **Close the turn with a game-facing handoff.**
   Summarize what changed, what the player can do next, and any clocks, leads, or consequences now in motion. Do not narrate bookkeeping the player did not ask for.

## Session Isolation Rules

These rules are non-negotiable. The previous-session bleed that occurs when an agent is invoked with a fresh `/cyberpunk-runner` command is the #1 failure mode of this skill and must be hard-blocked.

- **Every new invocation creates a brand-new session folder** unless the player explicitly types `resume`, `load`, `continue`, or names an existing session by id. "Continue the story", "let's play again", or any other soft phrasing is treated as a fresh session, never a resume. When in doubt, ask.
- **Never read another session's files on your own.** The agent MUST NOT enumerate `<base-dir>/sessions/`, peek into a sibling session's `session.json` / `story.md` / `timeline.md` / `characters/` / `events/` / `locations/`, or include any character, NPC, location, event, rumor, complication, faction, ad copy, gear, debt, hook, or beat from a previous session into the new session's fiction, world state, or planning. The active session directory is the **only** authoritative memory for the current run, and the knowledge database is the **only** permissible external reference.
- **Never quote, paraphrase, summarize, or "carry over" prior-session content** as flavor, foreshadowing, continuity, or assumed canon. The crew has no history with NPCs they have not met, no reputation they have not earned, no debts they have not taken on, no gear they have not acquired, and no enemies who have not been introduced in *this* session. The runner's reputation starts at zero. Their address book is whatever they walked in with.
- **The bootstrap step is "create", not "merge".** When a new session is created, every player character's `xp_log`, `skill_entries`, `hooks`, `secrets`, `cyberware`, `signature_gear`, `relationship_to_crew`, faction `reputation`, and `street_cred` is reset to the agreed-upon starting values. The agent does not copy these fields from a prior session because there is no prior session from this run's perspective.
- **The knowledge database is read-only reference, never a hidden source of "previous session" data.** Even if a query to `db_search.py` happens to surface a name, place, or fact that resembles a prior run, that is coincidence, not canon. The agent invents fresh material and does not retrofit prior-session facts onto it.
- **If the player asks for a crossover or for the new campaign to "continue where we left off", the agent pauses and confirms.** The player must name the source session by id (or pick from a list the agent offers), and only then does the agent read that session's files. Without that explicit confirmation, the new session is treated as a clean slate.
- **If a previous session is referenced by accident**, the agent stops the bleed immediately: acknowledges the leak to the player, scrubs the offending detail from the new session's files (story, timeline, gm-notes, character sheets, factions, hooks), and continues with only the active session's data. The agent does not try to "make it work" by weaving the leaked detail in.

## Dice & Roll Interleaving

The dice tool is the **only** numerical authority in play. The agent never decides the outcome of a contested, risky, or uncertain action on its own — it calls `scripts/dice.py` and lets the tool return the truth. This is the contract that makes the game feel like a game and not a story the agent is quietly writing for the player.

- **When in doubt, roll.** If the fiction implies any of the following, the agent calls `dice.py` instead of narrating an outcome: contested combat, chases, hacking, lockpicking, demolition, negotiation against a stubborn NPC, intimidation, seduction, deception, perception, search, investigation, medical treatment, jury-rigging, repairs, crafting, jury-rigged cyberware, vehicle handling under pressure, stealth, escape, forgery, interrogation, bargaining, and any player-stated action with a non-trivial chance of failure.
- **Narrate a short beat, then roll, then continue.** The agent writes a small slice of the fiction to set up the moment (what the runner is doing, what is in their way, what the stakes are), **pauses the narration to call `dice.py red-check` (or `opposed` when relevant)**, and only after reading the tool's output does it continue the scene. The player should see the roll happen on screen in the middle of the beat, not after the agent has already decided what happened.
  - Bad pattern: "You line up the shot, the bullet punches through the window, the target drops, the room goes quiet." (No roll. Outcome invented.)
  - Good pattern: "You line up the shot through the gap in the blinds. The target is half a room away, the barrel is steady, your breath is slow. Calling it — [rolls `dice.py red-check --stat REF --skill Firearms --modifier 0`]. The roll comes back [N], a [critical/hit/partial/miss]. [Continues the scene in light of that result]."
- **Never pre-write a roll's outcome.** The agent does not decide "this is going to be a hit" and then call the dice to rubber-stamp it. The tool's result is the truth; the narration must adapt to whatever the dice return, including botches, fumbles, friendly fire, runaway success, and surprise consequences the agent had not planned.
- **Always cite the stat and skill on the call** so the player can audit the roll against their sheet. The agent picks the relevant `STAT/Skill` pair from the player's dossier (or the NPC's dossier for opposed contests) and announces it before the tool returns, e.g. *"`REF/Firearms 2` against difficulty 12"*.
- **Pure description and zero-stakes color do not need a roll.** Walking across a room, ordering a drink, picking up a dropped credchip, hearing an ad crawl, reading a sign — these are narrated freely. The moment risk, opposition, chance, skill, or consequence enters the beat, the dice come out.
- **Log the roll when it matters.** If the result will have lasting consequences (a wound, a kill, a faction shift, a job's outcome, a relationship change), the agent also writes the raw `dice.py` output to `rolls/<utc-stamp>-<label>.json` so the player can audit it later.
- **Failure is content, not a bug.** A miss, partial, or botch is not a setback to be apologized for — it is the next beat of the scene. The agent leans into the dice's verdict and plays the consequence forward with the same energy it would have played a hit.

## Roll Display Format

The agent does not print dice results however it wants. Every roll that goes into the game chat (Discord, terminal, log, or `story.md`) **must** use one of the three templates below, copied as a single fenced code block (``` ... ```) so the box renders in monospace. No freeform prose for the roll, no emoji ad-libs, no rearranged fields, no "just inline the number" shortcuts. The format is the audit trail: the player should be able to scan the box, see the call (stat, skill, difficulty), the raw die result, the math, and the outcome, all in one glance.

- **The box itself is the rule.** `═` and `─` characters are part of the spec. The header line, the divider lines, the column alignment, and the label/value spacing must be preserved. If the agent cannot reproduce the exact shape (e.g. the platform strips Unicode), it must use the closest ASCII equivalent (`=` and `-`) rather than reinventing the layout.
- **One roll, one box.** A red-check is one box. An opposed roll is one box. A raw `roll` is one box. The agent never splits a roll across two messages, never interleaves narration inside a box, and never inlines a roll result into a paragraph of fiction. Narration goes *after* the closing fence, not inside it.
- **The call line names what is being rolled.** The header always states the `STAT/Skill` (or both sides of an opposed contest) and, for `red-check`, the difficulty. The player can read the first line of the box and know exactly what the agent is about to resolve.
- **Labels and values are right-padded to a fixed column** so the eye can scan down the labels and across the values. The exact column width is 11 characters for the label (e.g. `Difficulty :`, `d10        :`) — match it.
- **The outcome line is always the last line before the closing `═` rule.** The outcome is one of the canonical strings: `STRONG SUCCESS`, `SUCCESS`, `FAILURE`, `HARD FAILURE`, `TIE` (for opposed), or the `TOTAL` (for raw `roll`). Crit signals are spelled out in the d10 line: `10  (CRITICAL)` or `1  (FUMBLE)`.
- **The agent does not add flavor text inside the box.** No "ouch", no "yikes", no "called it". The box is data. Flavor goes in the narration beat that follows.
- **If the result is logged to `rolls/<utc-stamp>-<label>.json`, the same box also gets appended to `story.md` verbatim** so the audit trail in the journal and the audit trail in the chat match.

### `red-check` Template

```
═══════════════════════════════════════
  RED CHECK · <STAT>/<Skill> <rank>  vs  DC <difficulty>
───────────────────────────────────────
  Difficulty : <difficulty>
  d10        : <die>  [(CRITICAL) | (FUMBLE) | ""]
  Stat       : <stat>
  Skill      : <skill>
  Modifier   : <+|-><modifier>
───────────────────────────────────────
  TOTAL      : <total>
  OUTCOME    : <STRONG SUCCESS | SUCCESS | FAILURE | HARD FAILURE>
═══════════════════════════════════════
```

Worked example — `dice.py red-check --stat 4 --skill 2 --modifier 0 --difficulty 12`, die = 7:

```
═══════════════════════════════════════
  RED CHECK · REF/Firearms 2  vs  DC 12
───────────────────────────────────────
  Difficulty : 12
  d10        : 7
  Stat       : 4
  Skill      : 2
  Modifier   : +0
───────────────────────────────────────
  TOTAL      : 13
  OUTCOME    : SUCCESS
═══════════════════════════════════════
```

Worked example — same call, die = 1 (fumble):

```
═══════════════════════════════════════
  RED CHECK · REF/Firearms 2  vs  DC 12
───────────────────────────────────────
  Difficulty : 12
  d10        : 1  (FUMBLE)
  Stat       : 4
  Skill      : 2
  Modifier   : +0
───────────────────────────────────────
  TOTAL      : 7
  OUTCOME    : HARD FAILURE
═══════════════════════════════════════
```

### `opposed` Template

```
═══════════════════════════════════════
  OPPOSED · <A_STAT>/<A_Skill> <A_rank>  vs  <D_STAT>/<D_Skill> <D_rank>
───────────────────────────────────────
  ATTACKER
    d10     : <attack_die>
    Bonus   : <attacker_bonus>
    Total   : <attack_total>
  DEFENDER
    d10     : <defend_die>
    Bonus   : <defender_bonus>
    Total   : <defend_total>
───────────────────────────────────────
  WINNER    : <ATTACKER | DEFENDER | TIE>
═══════════════════════════════════════
```

Worked example — `dice.py opposed --attacker 6 --defender 8`, attack die = 8, defend die = 5:

```
═══════════════════════════════════════
  OPPOSED · REF/Firearms 2  vs  INT/Counter-Hack 3
───────────────────────────────────────
  ATTACKER
    d10     : 8
    Bonus   : 6
    Total   : 14
  DEFENDER
    d10     : 5
    Bonus   : 8
    Total   : 13
───────────────────────────────────────
  WINNER    : ATTACKER
═══════════════════════════════════════
```

### `roll` Template (raw expression)

```
═══════════════════════════════════════
  ROLL · <expression>
───────────────────────────────────────
  Dice      : [<d1>, <d2>, ...]
  Modifier  : <+|-><modifier>
  TOTAL     : <total>
═══════════════════════════════════════
```

Worked example — `dice.py roll 2d6+1`, dice = [3, 5]:

```
═══════════════════════════════════════
  ROLL · 2d6+1
───────────────────────────────────────
  Dice      : [3, 5]
  Modifier  : +1
  TOTAL     : 9
═══════════════════════════════════════
```

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
- Do not lose track of who is speaking in Discord. Never apply one player's request, dice check, inventory, XP, or consequence to another player's character because their turns happened close together in the channel.
- Do not bleed a prior session into a fresh one. A `/cyberpunk-runner` invocation with no explicit `resume` / `load` / `continue` / named-session-id is a clean slate; do not enumerate, read, quote, paraphrase, or carry over characters, NPCs, locations, events, gear, debts, hooks, reputation, or beats from any other session folder, and do not treat the knowledge database as a substitute for prior-session memory. If a leak slips in, scrub it on the spot.
- Do not narrate past the dice. The agent never invents the outcome of a contested, risky, or uncertain action. The beat goes: short setup narration → call `scripts/dice.py` (or `opposed`) → read the tool's output → continue the scene in light of that result. The player should see the roll on screen in the middle of the beat, not after the agent has already decided what happened.
- Do not pre-decide a roll's outcome. The dice are the truth, including botches, partials, friendly fire, and surprise consequences. The agent adapts the narration to whatever the tool returns; it does not write a hit and then call the dice to confirm it.
- Do not start a session in crisis. The opening scene must give the player at least one full beat of agency before any antagonist, hunter, kill-list, chase, firefight, or mobilized faction is on screen. No pre-loaded `Heat`, `Wanted`, `Hunt`, `Surveillance`, or `Time Bomb` clocks against the crew in beat one. Difficulty tunes the *pace* of pressure, not whether the first scene hands the player a choice.
- Do not print rolls in a custom format. Every dice result goes into the chat / log as a single fenced code block matching the `red-check`, `opposed`, or `roll` template in **Roll Display Format**. No inlined numbers in prose, no emoji ad-libs, no rearranged fields, no split boxes, no flavor text inside the box. The audit trail is the format.

## Verification

The skill is working correctly when all of the following are true:

- `<base-dir>/knowledge/cyberpunk.db` exists (built once by `bootstrap_sources.py init`).
- The active session folder contains `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, and the `characters/`, `locations/`, `events/`, `rolls/` directories.
- `session.json` contains a correct `players` registry mapping each Discord user to the right `character_slug`, plus a `party` block if the session has multiple players.
- Every player character has a `characters/<player-slug>.json` dossier, and each of those dossiers matches its mirror object in `session.json > player_characters` for stats, derived trackers, cyberware, level, XP, and `skill_entries`.
- Dice rolls (`dice.py`) produce structured output the agent can cite during play, and `rolls/` may contain dated JSON records.
- The current scene's new facts are written back into the active session's files using the file tools — no separate manager script mediates the writes.
- No scene content was produced by a random draw from the knowledge database; every character, location, gig, rumor, complication, and name was invented by the agent.
- XP is tracked per runner in the player JSON files and in `session.json > player_characters`; a level-up fires at 10 XP and follows the three-path choice rule.
- Every skill on a player or NPC is documented in its JSON file with Description, Frequency, Effect, and Limitations, and mirrored in the relevant `session.json` record.
- Every piece of gear, cyberware, weapon, vehicle, contact, cred chip, drug, ammo belt, or chem a player reaches for in the fiction is on that player's `characters/<player-slug>.json` at the time of use. Inventory edits only happen through in-fiction acquisition or through a direct, agent-confirmed bookkeeping correction; the agent never invents inventory on a player's behalf, and the agent never lets pressure, persuasion, or "it just makes sense" override the sheet.
- The new session is provably isolated: no characters, NPCs, locations, events, hooks, debts, gear, reputation, or beats from any other session folder under `<base-dir>/sessions/` appear in the new session's `session.json`, `story.md`, `timeline.md`, `gm-notes.md`, `characters/`, `events/`, or `locations/`. The agent did not enumerate the parent `sessions/` directory, did not read any sibling session's files, and did not pull prior-session facts from the knowledge database. If a leak occurred, it was scrubbed.
- Dice use is interleaved with narration: every contested, risky, or uncertain action in `story.md` is preceded by an explicit `dice.py` call, with the `STAT/Skill` and difficulty announced, and the narration that follows adapts to the tool's output. The agent did not invent roll outcomes.
- Every dice result in `story.md` and in chat is rendered as the canonical fenced-code-block template from **Roll Display Format** (`red-check`, `opposed`, or `roll`), with the header line, dividers, label columns, and outcome line all matching the spec. No freeform roll prose, no inlined numbers, no emoji, no flavor inside the box.
- The opening scene is reactive, not deterministic: the runner's first beat includes a player-facing choice, no antagonist is already mobilized against the crew, no `Heat` / `Wanted` / `Hunt` / `Surveillance` / `Time Bomb` clock is already in motion, and the player can point to beat one and say "that was my decision."
