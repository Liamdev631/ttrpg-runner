# GM Playbook

## Tone Targets

Good cyberpunk play usually mixes:

- intimate human need
- institutional violence
- seductive technology
- social stratification
- style under pressure

## Fun Features To Lean On

- ad crawls that foreshadow trouble
- rumors that are half-true and commercially motivated
- named neighborhoods with distinct texture
- implants that solve one problem and create another
- corps with brand identity and deniable violence
- clocks that turn comfort into crisis

## Good Mission Seeds

- extract someone who does not want to be rescued
- steal data that turns out to be alive
- smuggle medical hardware through a labor riot
- impersonate a vanished executive during a live media event
- shut down a predictive-policing model before it profiles the crew

## Consequences That Matter

Prefer consequences that create new play instead of dead ends:

- the target survives but now owns the crew a favor
- a gang offers protection at a terrible political price
- the heat clock advances and a checkpoint network comes online
- the crew earns cash but loses anonymity
- an NPC ally gets leverage, fear, or ambition from the outcome

## Session Close

End strong by capturing:

- the immediate aftermath
- new leads
- faction reactions
- unresolved threats
- what the player can do next

## Ad Crawl Timing

Drop a full ad crawl (use `templates/ad-crawl.md`) when the player:

- waits more than a beat in an elevator, transit station, or holding cell
- stares at a wall screen or bar holo while planning
- walks into a clinic, motel, fixer lobby, or corpo atrium
- passes a sky-bike banner, drone float, or graffiti projector between scenes

Drop a one-line brand mention (skip the template) during chases, firefights, and tight conversations. Roughly one in three crawls should plant a hook worth chasing; track the hook in `session.json` under `ad_hooks` and the corresponding dossier under `events/`.

## Opening Frame & Breathing Room

The opening scene is a contract with the player. If the first beat drops the runner into a city where multiple factions are already mobilized against them, the player has nothing to push against — only things being pushed at them. That is not tension, it is a trap, and it kills agency on turn one.

- The opening scene must give the player room to act before the world acts on them. The runner should have at least one full beat — usually more — to orient, choose, and move before any major external pressure lands.
- No pre-mobilized antagonists at session start. The first scene must not begin with the runner already being hunted, already being tracked, already on kill-lists, already mid-chase, already pinned in a firefight, already surrounded, or already mid-extraction. Antagonists, hunters, factions, fixers, and threats are introduced *after* the runner has had room to move and the player has chosen how to engage.
- Calibrate pressure to difficulty, but always start at the floor. "Medium difficulty" means pressure ramps at a medium *pace*, not that the first scene is mid-crisis. A medium session should still open with the runner able to walk, talk, buy a drink, take a job, or refuse one without dying in the first ten minutes.
- Stakes are introduced, not inflicted. The opening scene can hint at stakes — a rumor on the feed, a job offer on a back channel, a contact asking to meet, a body in an alley, a red flag on a public board — but the runner is not yet on the hook for any of it.
- No pre-loaded clocks against the crew. The first scene must not begin with a `Heat`, `Wanted`, `Time Bomb`, `Hunt`, or `Surveillance` clock already in motion. Clocks start at zero (or are seeded only as background flavor that does not yet touch the crew). The agent builds clocks *in response to* the runner's choices, not before them.
- The first choice belongs to the player, not the script. The opening frame presents a situation and asks what the runner does. It does not present a situation that has already resolved itself and then narrate the consequences. The player should always be able to point at the first beat and say "that was my decision, not a cutscene."

## Stat & Skill Guidance

- When the fiction implies a contested action, pick the single best `STAT/Skill` path from the player sheet and call a `red-check` with `--stat <stat> --skill <skill>`. **Roll first, narrate second.** The agent writes a short setup beat, calls `dice.py`, and *then* continues the scene in light of the tool's output — it does not narrate the outcome of a risky action and then call the dice to confirm what it already wrote.
- Difficulty ladder (suggested): 8 routine, 12 trained, 16 expert, 20 elite.
- When in doubt, roll. The agent never invents the outcome of a contested, risky, or uncertain action (combat, chase, hack, lockpick, negotiation against a stubborn NPC, intimidation, seduction, deception, perception, search, investigation, medical treatment, jury-rigging, vehicle handling under pressure, stealth, escape, forgery, interrogation, bargaining). Pure description and zero-stakes color — walking across a room, ordering a drink, hearing an ad crawl — is narrated freely without a roll.
- `opposed` rolls are reserved for head-to-head contests: chases, duels, hack-vs-ICE, bargaining, and any other direct contest between the runner and a named NPC whose dossier has a `STAT/Skill` of its own.
- The agent must always cite the `STAT/Skill` and the difficulty it is calling, so the player can audit the roll against their sheet, and must accept the tool's verdict (hit, partial, miss, botch, critical) without rewriting the fiction to fit a pre-decided outcome.

## XP Triggers (background awards)

Award 1–3 XP in the background — write to the dossier and `session.json`, do not pause the scene to ask. Common triggers:

- Survived a major scrape (combat, chase, ambush, cyberware rejection, extraction under fire) — +1 to +3
- Completed or partially completed a job — +2 to +3
- Uncovered a major lead or turned a hidden system inside out — +1 to +2
- Made a risky call the fiction rewarded — +1 to +2
- Meaningful character moment (confronted a trauma, broke a bad habit, kept faith with a contact) — +1
- Took heat for the crew or paid a real cost (lost a contact, took a debuff, spent street cred) — +1 to +2

Always include a one-line reason and an ISO timestamp in the `xp_log` so the player can audit it.

## Level-Up Conversation

When XP hits 10, the agent stops the action just long enough to:

1. Announce the level-up in the fiction (the runner feels sharper, faster, more present).
2. Update `level`, reset `xp` to 0, and refresh `xp_to_next_level` to 10.
3. Offer the three-path choice:
   - **Four background-relevant skills** — agent proposes four, player picks one.
   - **Four random skills** — agent invents four wildly different paths, player picks one.
   - **Direct request** — player names a skill; agent grants as-is, simplifies to a weaker version, or downgrades to a neighboring skill. Always explain the simplification in-character.
4. Write the new skill (or upgraded rank) into the player dossier and `skill_entries` with full Description, Frequency, Effect, and Limitations. If the skill was simplified or limited, that is part of the entry.

A skill the player already has can be upgraded past the typical 0–4 ceiling up to rank 6; treat **+1 rank per level-up for the same skill** as the rule, and never grant a rank that would trivialize the fiction.
