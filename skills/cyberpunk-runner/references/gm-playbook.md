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

## Stat & Skill Guidance

- When the fiction implies a contested action, pick the single best `STAT/Skill` path from the player sheet and call a `red-check` with `--stat <stat> --skill <skill>`.
- Difficulty ladder (suggested): 8 routine, 12 trained, 16 expert, 20 elite.
- For non-combat challenges, the agent narrates the result first and only rolls when the outcome is uncertain or interesting.
- `Opposed` rolls are reserved for head-to-head contests: chases, duels, hack-vs-ICE, bargaining.

## XP Triggers (background awards)

Award 1–3 XP in the background — write to `characters/<player-slug>.json` (the canonical sheet) and `session.json`, do not pause the scene to ask. Common triggers:

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
4. Write the new skill (or upgraded rank) into `characters/<player-slug>.json` and the matching entry into `skill_entries` with full Description, Frequency, Effect, and Limitations. If the skill was simplified or limited, that is part of the entry. Mirror the same `skill_entries` object into `session.json > player_character.skill_entries` so the dossier and the session state stay aligned.

A skill the player already has can be upgraded past the typical 0–4 ceiling up to rank 6; treat **+1 rank per level-up for the same skill** as the rule, and never grant a rank that would trivialize the fiction.
