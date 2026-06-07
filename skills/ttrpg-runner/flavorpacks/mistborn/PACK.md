# Mistborn Flavor Pack

Load this pack only when the player explicitly wants Mistborn, the Mistborn Adventure Game, or Scadrian play.

## Mandatory Era Choice
- If the player does not specify an era, ask for `Era 1` or `Era 2` before character creation or worldbuilding.
- Record the answer in `session.json` as `mistborn_era`.
- Once chosen, keep character options, factions, institutions, equipment, and tone locked to that era for the session.
- If the player wants to jump eras mid-campaign, confirm a new session or an explicit timeskip/alt-history reset first.

## Tone Targets
- metal, ash, scarcity, and hidden power
- crews built on trust, secrets, and leverage
- class pressure, law, and the cost of power
- miracles that feel physical, costly, and visible

## Opening Frame
- Start with the crew's cause, target, and method.
- Let the first scene expose both a social pressure and a practical obstacle.
- Make metals, props, and place matter immediately.

## Organic Creation Principle
- Invent fresh crews, houses, constables, syndicates, contracts, cases, and betrayals every session.
- Use the imported markdown references for rules, terminology, and setting texture, not as a seed-data vending machine.
- Keep magical action concrete: what metal is in play, what is being stored or burned, what it costs, and what collateral it causes.

## Rules Backbone
- Use `references/Base Game/Character Sheet Definitions.md` for the core stat model.
- Use `references/Base Game/Rolling the Dice.md`, `references/Base Game/Contests.md`, `references/Base Game/Conflicts.md`, and `references/Base Game/Damage.md` for resolution.
- Use `references/Base Game/Magic/Allomancy.md`, `references/Base Game/Magic/Feruchemy.md`, `references/Base Game/Magic/Hemalurgy.md`, and `references/Base Game/Magic/Metals.md` for metallic arts.
- Use the supplement folders only when the current era, faction, or character concept actually calls for them.

## Era Lock
- `era1`: Final Empire and immediate-collapse play. The imported `Base Game`, `Nobles - The Golden Mandate`, `Skaa - Tin & Ash`, and `Terris - Wrought of Copper` references are fully in-bounds.
- `era2`: industrial Scadrial. No character may have more than one Allomantic power. No character may have more than one Feruchemical power. Twinborn are allowed as one Allomantic power plus one Feruchemical power.
- In `era2`, do not present Mistborn or full Feruchemists as standard player-character options.
- In `era2`, do not reuse the Steel Ministry, plantation skaa oppression, or great-house rule as present-day defaults. Treat imported Era 1 institution docs as history unless the table explicitly wants legacy fallout.

## Stat Guidance
- `Physique` - speed, strength, endurance, direct force
- `Charm` - presence, leadership, deception, rapport
- `Wits` - analysis, awareness, planning, improvisation
- `Resources` - wealth, tools, and paid reach
- `Influence` - favors, status, institutional leverage
- `Spirit` - luck, resolve, and metaphysical endurance

Suggested resiliences:
- `Health = Physique + Resources`
- `Reputation = Charm + Influence`
- `Willpower = Wits + Spirit`

## Discord Rendering
- Open scenes with a `###` heading naming the job, district, manor, rail line, or case, then follow with `-#` subtext for era, city, and local conditions.
- Use `> ` block quotes for whispered crew plans, clipped noble dialogue, broadsheets, and law reports.
- Italicize metal names, house names, and place names with `*...*` when they carry setting weight.
- Use `__...__` underline for active metals, tapped traits, and burdens that are immediately changing the scene.
- Use `||...||` spoilers for hidden identities, Hemalurgic secrets, and unseen manipulations.
- Render dice pools, metal charges, and character sheets as fenced code blocks.

## Time Manipulation And Turn Order

The setting canonically supports time bubbles via bendalloy (speeds up the Allomancer) and cadmium (slows the Allomancer). When a player activates one of these abilities, the fair-rotation turn order from the main `SKILL.md` Multiplayer Turn Management section is suspended for the duration of the bubble.

- A speed bubble (bendalloy burning) gives the players inside the bubble a few additional actions before the bubble falls and normal turn order resumes.
- A slow bubble (cadmium burning) gives players outside the bubble a few additional actions, since they can act with far less resistance from the slowed party.
- The GM decides how many bonus turns fit the scene's stakes and the bubble's remaining charges. Cross-check charge cost and bubble duration against the `references/Base Game/Magic/Allomancy.md` and `Metals.md` rules.
- When the bubble drops, return to standard turn order with the same explicit `> **Up next: <player name>**` handoff.

## Pack References
- `references/era-rules.md`
- `references/gameplay-loop.md`
- `references/gm-playbook.md`
- `references/source-manifest.md`
- `references/README.md`
- `references/Base Game/...`
- `references/Nobles - The Golden Mandate/...`
- `references/Skaa - Tin & Ash/...`
- `references/Terris - Wrought of Copper/...`
