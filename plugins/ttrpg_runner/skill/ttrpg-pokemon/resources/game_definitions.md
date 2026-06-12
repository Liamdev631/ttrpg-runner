# Pokemon Game Definitions

This is a **supplementary** file for `ttrpg-pokemon`. It pairs with
the base `SKILL.md` and is also designed to load on its own when a
non-Pokemon session wants to borrow Pokemon's stat block and
companion turn rules (for example, a `ttrpg-dnd` run where every
party member has a partner that shares their turn).

`SKILL.md` and this file are the two halves of one system. The
character definitions (stats, derived trackers, trainer + partner
sheet shape) and the combat rules (Companion Turn Rules, when to
roll) only make sense together. Always load both, or load this
file on its own when the player has explicitly asked to import
Pokemon combat into a different pack.

## Character Definitions

The Pokemon character sheet is built from six stats, four derived
trackers, and a trainer-plus-partner pair.

### Stats

- `BND` - trust, empathy, and partnership
- `SPD` - speed, agility, chase scenes
- `PWR` - direct force and athletic impact
- `INS` - observation, instinct, and field reading
- `GRT` - resilience, courage, and grit
- `TEK` - gadgets, medicine, research, and technical work

### Derived Trackers

- `HP = GRT + 4`
- `Defense = SPD`
- `Stress = INS`
- `Reputation` starts at `0`

### Character Anchors

Every trainer has a short sheet and an active partner sheet. The
trainer drives the story; the partner shares the trainer's turn
(see Combat Mechanics below).

**Trainer slots:**

- a **concept** (one-line identity, e.g. "quiet kid from a fishing town")
- a **home region** (where they come from; informs rival flavor and ecology)
- a **goal** (what they want from this journey)
- a **specialty** (gadgets, contests, ranger work, research, ...)
- a **loadout** (starting bag, pokedex, daypack, chosen during character creation)

**Partner slots:**

- a **species** (and evolution line)
- a **nature** (how the partner reacts under pressure)
- a **move list** (four moves the partner knows at session start)
- a **bond** (`BND` score; gates the Companion Turn Rules)

## Combat Mechanics

### Companion Turn Rules

Pokemon are **companions, not party members with their own initiative**. They share their trainer's life, their trainer's spotlight, and their trainer's turn.

- **No independent initiative.** A pokemon never rolls for or holds its own place in the turn order. It acts when its trainer acts.
- **One action per trainer turn.** When a trainer's turn comes up, they pick the action for the active partner: a move, a command, a held-back reaction, an item use, a free bond check, or a deliberate pass. The partner does not get a separate "second turn" later in the round.
- **Only one partner acts at a time.** If a trainer owns multiple partners (party roster, PC storage, on-site ranger callouts), the trainer picks **one** partner for the current turn. The rest are staged, recalled, or held in reserve.
- **Swaps are the trainer's call.** Switching the active partner is a trainer action, not a free interrupt. A swap costs the trainer's action for the turn unless the GM rules a context-appropriate exception (ball recall mid-leap, recall-and-resend on a downed ally, etc.).
- **Reactions are automatic, not chosen.** Some moves, abilities, or items are flagged as reactions. A pokemon reaction does **not** wait for the trainer's turn and does **not** require the trainer to declare it. The GM watches the trigger conditions, then chooses whether and when the reaction fires.
- **The GM controls reaction timing.** The GM decides when a reaction triggers, what it targets, and in what order it resolves relative to other reactions in the scene. The goal is to make the reaction useful to the player: the partner defends the trainer, protects a downed ally, or seizes a clear opening without burying the table in bookkeeping. If a reaction would be a net negative to the party, the GM may hold it for a better moment or skip it for the round.
- **Tell the player, not the chat.** When a reaction fires, narrate the effect in the GM voice and mark it on the partner's sheet. The player should never have to "remember" to use a reaction; the GM runs that clock.
- **Bond and trust gate the rules.** A partner acting against its trainer's intent, refusing a command, or breaking from formation is a `BND` moment, not a mechanics moment. The companion rules ride on top of bond, not the other way around.

### When To Roll

Roll when a capture, race, rescue, or conflict becomes uncertain. The
base resolution rules in `ttrpg-core` apply; the six stats above are
the `STAT` field in the standard check card.
