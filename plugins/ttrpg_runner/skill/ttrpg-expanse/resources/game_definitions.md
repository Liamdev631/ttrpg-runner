# Expanse Game Definitions

This is a **supplementary** file for `ttrpg-expanse`. It pairs with
the base `SKILL.md` and is also designed to load on its own when a
non-Expanse session wants to borrow Expanse's hard-SF stat block
and derived math (for example, a `ttrpg-dnd` run where the party
uses `FOR` / `AGI` / `ACC` and zero-g rules apply in shipboard
fights).

`SKILL.md` and this file are the two halves of one system. The
character definitions (stats, derived trackers, shipboard sheet
shape) and the combat rules (when to roll, what rolls in vacuum)
only make sense together. Always load both, or load this file on
its own when the player has explicitly asked to import Expanse
combat into a different pack.

## Character Definitions

The Expanse character sheet is built from six stats, four derived
trackers, and a small set of shipboard anchors.

### Stats

- `FOR` - force, EVA labor, physical pressure
- `AGI` - movement, zero-g control, quick reactions
- `ACC` - shooting, piloting precision, targeting
- `INT` - engineering, medicine, analysis
- `PER` - awareness, scans, situational reading
- `COM` - command, negotiation, social poise

### Derived Trackers

- `HP = FOR + 4`
- `Defense = AGI`
- `Stress = PER`
- `Reputation` starts at `0`

### Character Anchors

Every crew member has a short sheet built from these slots. Keep
the sheet under one screen; shipboard characters live or die on
their training, not their backstory.

- a **role** (pilot, engineer, medic, gunner, belter, marine, political officer, ...)
- a **shipboard posting** (which station or vessel they ride)
- a **specialty** (one system they understand better than anyone else at the table)
- a **side** (which faction, employer, or cause they answer to)
- a **loadout** (starting gear, vac suit, sidearm, tool kit, chosen during character creation)

## Combat Mechanics

### When To Roll

Roll when vacuum, violence, acceleration, or politics become
uncertain. The base resolution rules in `ttrpg-core` apply; the
six stats above are the `STAT` field in the standard check card.
