# Mistborn Game Definitions

This is a **supplementary** file for `ttrpg-mistborn`. It pairs with
the base `SKILL.md` (and the era file loaded for the current
campaign) and is also designed to load on its own when a non-Mistborn
session wants to borrow Mistborn's dice-pool character shape and
Conflict Summary (for example, a `ttrpg-dnd` run that resolves fights
with the Mistborn action / defense / Burden ladder instead of
HP-vs-DC).

`SKILL.md` and this file are the two halves of one system. The
character definitions (what a sheet looks like, which trait slots
exist) and the conflict rules (how a fight resolves, how a Burden
is taken) only make sense together. Always load both, or load
this file on its own when the player has explicitly asked to
import Mistborn combat into a different pack.

The base pack's "Core Resolution" and "Complications And Nudges"
sections still govern how every roll is built. This file covers
the character sheet and the conflict layer that sits on top.

## Character Definitions

Mistborn characters are short, readable, and trait-driven. The
sheet is built from a small list of concept anchors plus the dice
pool inputs (Attribute, Standing, Traits, gear, Circumstances).

### Sheet Inputs

Every Mistborn roll is a dice pool. The pool is built from:

- an **Attribute** or **Standing** (see the base pack's Standings)
- helpful or harmful **Traits** (from the concept anchors below)
- useful **gear**
- **Circumstances**

The Conflict Summary below uses three Resilience tracks that the
sheet has to keep:

- `Health`
- `Reputation`
- `Willpower`

### Character Anchors

Keep characters short, readable, and playable. Each PC should have:

- a **concept**
- a **drive**
- a **profession**
- a **specialty**
- a **distinctive feature**
- a **defining personality trait**

Traits matter more than deep backstory. If a detail will not help
during play, leave it out.

## Combat Mechanics

### Conflict Summary

Conflicts cover combat, social pressure, and mental struggle with the same core logic.

GM shorthand:

- each round starts with declared actions
- rolled action dice determine when characters actually act
- unused action dice become defense dice
- a character normally gets one reaction or one defense against a given action, not both

Damage is simple:

- base damage is 1
- add weapon or tool bonuses
- add 1 damage per Nudge spent on damage

Wounds matter when one hit strips a large chunk of the target's remaining Resilience:

- about 25 percent: Serious Burden
- about 50 percent: Grave Burden

At 0 in a Resilience track, the character is defeated in that arena:

- `Health`: unconscious, dying, or dead
- `Reputation`: disgraced
- `Willpower`: emotionally or mentally broken

Use defeat to push the story forward. Do not stop at "you lose."
