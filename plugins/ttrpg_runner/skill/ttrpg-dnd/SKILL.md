---
name: ttrpg-dnd
description: Heroic-fantasy setting pack for ttrpg-runner. Wonder, danger, ruins, politics, monsters, and difficult heroism. Load only when the player explicitly wants DND-style play.
version: 3.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# DND Flavor Pack

Load this pack only when the player explicitly wants DND, Dungeons and Dragons, or classic heroic fantasy with native support.

## Tone Targets

- wonder, danger, and difficult heroism
- ruins, politics, monsters, and old magic
- treasure with consequences
- communities worth saving or failing

## Opening Frame

- Start with a grounded situation and a real choice.
- Do not open with the party already doomed, imprisoned, or facing the final boss.
- Let the first danger be visible before it becomes personal.

## Organic Creation Principle

- Invent fresh villages, cults, ruins, factions, and bargains.
- Use this pack's markdown references for inspiration, not random replacement for authored play.
- Keep the world feeling ancient, local, and myth-haunted.

## Stat Guidance

Character definitions (stats, derived trackers, sheet anchors) and the roll/combat math live in [`resources/game_definitions.md`](./resources/game_definitions.md). That file is a supplementary pack: it pairs with this `SKILL.md`, or can be loaded on its own when a non-DND session wants to import DND's character sheet and combat resolution.

## Gameplay Loop

1. Ground the party in a place with needs, rumors, and visible risk.
2. Offer two or more approaches: diplomacy, caution, force, or ingenuity.
3. Roll when danger, opposition, or uncertain magic enters the scene.
4. Spend success on progress and failure on complications, not dead stops.
5. Let the world remember broken oaths, slain monsters, and public deeds.
6. Record discoveries, treasure, scars, and faction shifts in the session files.

## Ambient Inserts

- Render tavern notices, heraldic proclamations, temple sermons, job boards, campfire rumors, and caravan gossip as short in-fiction prose blocks.
- Let public notices hint at danger without forcing the party's hand.
- Roughly one in three inserts should expose a lead the party can follow.

## Pressure Levers

- hungry wilderness and hostile weather
- noble obligations and church politics
- cursed relics and monster ecology
- debt, oaths, and dangerous patronage

## GM Playbook

### Strong Ingredients

- places with layered history
- monsters with motives beyond simple violence
- treasure that changes social relationships
- hard choices between safety, greed, and mercy

### Good Mission Seeds

- recover a relic before a rival temple weaponizes it
- escort a witness through monster-held hills
- expose a baron whose miracle harvest is necromancy
- delve a ruin whose guardians still think the old empire lives
- win a dragon's map by solving the feud it has been quietly farming for decades
- steal a saint's bell from a monastery that uses it to hide a much darker prison
- survive a festival contest where every "friendly game" is a cover for a coup
- negotiate safe passage through a haunted orchard whose ghosts only answer to children and oathbreakers

## Discord Rendering

- Open scenes with a `###` heading that names the **place** (ruin, keep, tavern, road) and the **time of day** in `-#` subtext.
- Use `> ` block quotes for NPC speech and the bardic "voice from offstage" that describes omens and portents.
- Use `__...__` underline for **enchanted**, **blessed**, or **cursed** objects and locations so they read as touched by magic.
- Italicize spell names, deity names, and proper nouns with `*...*` so the lore reads as lore.
- Use `||...||` spoilers only for genuine plot twists and hidden lore. Do not spoiler the obvious.
- Render stat blocks and monster entries as fenced code blocks so the numbers do not reflow.

## Source Manifest

This pack does not ship reusable story seed data.

That is intentional: the agent should author fresh quests, ruins, factions, towns, names, and complications every session instead of drawing from a bundled library that can repeat.

This pack also does not ship any downloaded source dump.

If curated external references are ever added here, convert them into markdown files and place a citations block at the top that names each source URL before any adapted notes.
