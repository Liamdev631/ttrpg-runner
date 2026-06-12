# Cyberpunk Game Definitions

This is a **supplementary** file for `ttrpg-cyberpunk`. It pairs
with the base `SKILL.md` and is also designed to load on its own
when a non-Cyberpunk session wants to borrow Cyberpunk's stat
block and HEAT meter (for example, a `ttrpg-dnd` run where every
loud move escalates HEAT and the city hits back on a timer).

`SKILL.md` and this file are the two halves of one system. The
character definitions (stats, derived trackers, the street-level
sheet shape) and the combat rules (HEAT meter, when to roll) only
make sense together. Always load both, or load this file on its
own when the player has explicitly asked to import Cyberpunk
combat into a different pack.

## Character Definitions

The Cyberpunk character sheet is built from six stats, four
derived trackers, and a small set of street-level anchors.

### Stats

- `BOD` - force, endurance, intimidation
- `REF` - shooting, driving, dodging, precision
- `TEK` - hacking, repair, code surgery
- `INT` - planning, medicine, research
- `COO` - stealth, nerve, composure
- `CHA` - persuasion, seduction, performance

### Derived Trackers

- `HP = BOD + 4`
- `Defense = REF`
- `Stress = COO`
- `Reputation` starts at `0`

### Character Anchors

Every crew member has a short sheet built from these slots. Keep
the sheet under one screen; street-level characters live or die
on small advantages, not long backstories.

- a **handle** (street name, used in fiction)
- a **role** (solo, netrunner, tech, fixer, nomad, media, exec)
- a **gig focus** (what kind of work they take: theft, escort, data heist, wet work, ...)
- a **signature piece** (one favored weapon, program, vehicle, or implant)
- a **loadout** (starting gear, chosen during character creation)

## Combat Mechanics

### HEAT METER

A single escalating score for police, corp security, and algorithmic attention on the crew's current block or district. Every illegal or conspicuous action adds heat. When a threshold is crossed, the city hits back on a timer.

#### Gaining heat

- Civilian reports a crime: `+1`
- Crime in an area not yet abandoned to urban chaos: `+2`
- Firearms involved: `+2`
- Automatic or military-grade weapons: `+10`
- Large-scale arson or explosives: `+5`
- Target is a corporate citizen: `+5`
- More than two suspects: `+2`
- Suspects have obvious cyberware: `+2`
- Face on the news holding heavy hardware: `+30`

Heat is local. The same job in a quiet residential block costs more heat than the same job in an industrial ruin. Hackers can spend a turn manipulating the meter — pump a rival crew's score before a job, scrub a trace after — which is also why gangs pay good money for gifted netrunners.

#### Response levels

- `5` — Two-/three-man patrol, pistols and flak vests, `1d6×10` minutes.
- `10` — Patrol grows by one; automatics issued.
- `15` — `2d6` patrols plus one aerial unit, automatic weapons.
- `20` — Urban Combat Unit: three 5-man teams, combat plate, autos, CS grenades, remote corporate hacker, `1d6` aerial support.
- `25+` — YOU WOKE THE HIVE. Bridges blocked, transport closed, `1d6` UCU elements deployed.

Cops are a malevolent omnipresent threat meter, not a wall. Use them to break rests, force scene changes, and drain resources. The crew should never get comfortable at high heat.

### When To Roll

Roll when the scene becomes risky, opposed, or unstable. The base
resolution rules in `ttrpg-core` apply; the six stats above are the
`STAT` field in the standard check card.
