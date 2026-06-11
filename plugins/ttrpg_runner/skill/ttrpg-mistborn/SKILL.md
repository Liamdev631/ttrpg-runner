---
name: ttrpg-mistborn
description: Mistborn-flavored setting pack for ttrpg-runner. The base pack is the always-on Mistborn ruleset; pair it with exactly one era file from resources/ (era_1.md or era_2.md) based on the player answer. Load only when the player explicitly wants a Mistborn game.
version: 3.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# Mistborn GM Pack

This is a lightweight GM-facing split of the source primer. Read this file together with exactly one era file:

- `resources/era_1.md`
- `resources/era_2.md`

The goal is speed at the table, not full lore coverage.

# What Stays Shared

Use this pack for rules and assumptions that work in both eras:

- crew-first play
- trait-driven characters
- dice pools, nudges, complications, and conflicts
- standings and recovery
- the basic shape of Allomancy, Feruchemy, and Hemalurgy

Anything tied to a specific social order, metal list, faction, or tech level belongs in an era file instead.

# Campaign Setup

Start with the crew, not the individual character sheets.

Have the table answer three questions:

- What is the crew's common cause?
- Who is the crew's primary target?
- What is the crew's preferred method?

Those answers give you the campaign's first jobs, enemies, and complications.

Good Mistborn crews usually form around one of these patterns:

- criminals with a purpose
- rebels with limited resources
- investigators hunting hidden truths
- retainers serving a powerful patron
- survivors trying to stay ahead of a larger machine

# Character Basics

Keep characters short, readable, and playable.

Each PC should have:

- a concept
- a drive
- a profession
- a specialty
- a distinctive feature
- a defining personality trait

Traits matter more than deep backstory. If a detail will not help during play, leave it out.

# Core Resolution

Most rolls use a dice pool built from:

- an Attribute or Standing
- helpful or harmful Traits
- useful gear
- Circumstances

General rules:

- normal pools run from 2 to 10 dice
- if the pool would go above 10, the extra dice become free Nudges on success
- if the pool would go below 2, roll 2 dice and reduce the final Outcome accordingly
- roll the pool and take the best matching pair as the result
- each `6` rolled is a Nudge

Use these roll types:

- Challenge: one character acts against a difficulty
- Contest: two or more characters directly oppose each other
- Conflict: one character tries to defeat another physically, socially, or mentally

Use difficulty 1 to 5:

- 1 simple
- 2 challenging
- 3 difficult
- 4 very hard
- 5 nearly impossible

Outcome matters more than pass/fail. Positive Outcome means success with increasing quality. Negative Outcome means failure with Complications.

# Complications And Nudges

Complications are the cost of a bad roll. Keep them concrete and immediate:

- lose time
- make noise
- break gear
- expose a secret
- create a new threat

Nudges let success do more or let failure hurt less.

Use Nudges to:

- add damage in a conflict
- reduce Complications
- save time
- gain a small situational bonus
- ask for one more useful detail
- set up the next action

When in doubt, spend a Nudge to make the current scene more decisive, not more complicated.

# Conflict Summary

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

# Recovery And Time

The game runs on short dramatic units:

- Beats: brief moments of action
- Short Breathers: quick recovery pauses
- Long Breathers: full reset scenes

Default recovery:

- Resilience usually recovers slowly over days
- a Short Breather restores part of what was lost
- a Long Breather restores all lost Resilience

Standings also recover over time, which helps keep pressure on crews between jobs.

# Standings

The three Standings are shared across eras:

- `Resources`: money, property, and purchasing power
- `Influence`: favors, access, and political pull
- `Spirit`: luck, intuition, and narrative momentum

Standings are meant to be spent. If players never risk them, you are probably not putting enough pressure on their priorities.

Use them to answer questions like:

- Can the crew buy this?
- Who owes them a favor?
- Can the player ask for a useful hint?
- Can someone rally bystanders or pull strings?

# Metallic Arts

The three Metallic Arts are always present, but the era file decides what is normal, rare, or banned.

## Allomancy

Allomancers ingest metal and burn it for power.

Shared GM truths:

- ratings matter more than long rules text
- metal supply is a pacing tool
- impurity, scarcity, and surprise are all valid complications

## Feruchemy

Feruchemists store traits in personal metalminds and tap them later.

Shared GM truths:

- storing should visibly change how the character behaves
- tapping should feel deliberate and costly
- access to the right metalminds matters

## Hemalurgy

Hemalurgy steals power through spikes and should usually remain dangerous, illegal, and story-defining.

Shared GM default:

- keep Hemalurgy mostly in villain hands unless the whole campaign is built around it

# Shared GM Defaults

Use these defaults unless an era file says otherwise:

- keep full-system powerhouses rare
- treat god metals as plot devices, not routine inventory
- make kandra, koloss, and spiked beings feel unusual
- reward clever plans more than exhaustive rules lookups
- if a lore detail does not help the current scene, simplify it
