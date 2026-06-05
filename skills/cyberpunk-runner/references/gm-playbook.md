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
