# DND Game Definitions

This is a **supplementary** file for `ttrpg-dnd`. It pairs with the
base `SKILL.md` and is also designed to load on its own when a
non-DND session wants to borrow DND's stat block and roll combat
(for example, a `ttrpg-pokemon` run that resolves fights with
DND's six stats, HP, and Defense math).

`SKILL.md` and this file are the two halves of one system. The
character definitions (stats, derived trackers, what a sheet looks
like) and the combat rules (when to roll, how the math lands) only
make sense together. Always load both, or load this file on its
own when the player has explicitly asked to import DND combat into
a different pack.

## Character Definitions

The DND character sheet is built from six stats, four derived
trackers, and a small set of concept anchors.

### Stats

- `STR` - force, lifting, grappling, breaking
- `DEX` - finesse, stealth, ranged attacks, balance
- `CON` - toughness, endurance, poison resistance
- `INT` - lore, analysis, investigation
- `WIS` - intuition, perception, survival
- `CHA` - leadership, charm, intimidation, presence

### Derived Trackers

- `HP = CON + 4`
- `Defense = DEX`
- `Stress = WIS`
- `Reputation` starts at `0`

### Character Anchors

Every DND PC has a short, readable sheet built from these slots.
Keep the sheet under one screen.

- a **concept** (one-line identity, e.g. "exiled paladin")
- a **class** (how the character fights: fighter, rogue, wizard, cleric, ranger, bard, ...)
- a **background** (where they came from: soldier, noble, urchin, scholar, ...)
- a **specialty** (one thing they do better than anyone else at the table)
- a **loadout** (starting gear, chosen during character creation)

## Combat Mechanics

### When To Roll

Roll when danger, opposition, or uncertain magic enters the scene.
The base resolution rules in `ttrpg-core` apply; the six stats above
are the `STAT` field in the standard check card.
