# Pokemon Flavor Pack

Load this pack only when the player explicitly wants Pokemon-style play with native support.

## Tone Targets
- friendship, discovery, and competitive ambition
- bright wonder with room for danger and grief
- communities, ecosystems, and travel
- rivalry without cruelty as the default mode

## Opening Frame
- Start with curiosity and choice, not instant catastrophe.
- Let the trainer and partner establish direction before the region tests them.
- Escalate danger through player movement, rival pressure, or ecological imbalance.

## Organic Creation Principle
- Invent fresh towns, gym circuits, ranger problems, research mysteries, and team schemes.
- Use this pack's markdown references as tone support, not as a replacement for authored scenes.
- Treat partner bonds and local culture as core drivers of play.

## Stat Guidance
- `BND` - trust, empathy, and partnership
- `SPD` - speed, agility, chase scenes
- `PWR` - direct force and athletic impact
- `INS` - observation, instinct, and field reading
- `GRT` - resilience, courage, and grit
- `TEK` - gadgets, medicine, research, and technical work

Suggested derived trackers:
- `HP = GRT + 4`
- `Defense = SPD`
- `Stress = INS`
- `Reputation` starts at `0`

## Companion Turn Rules

Pokemon are **companions, not party members with their own initiative**. They share their trainer's life, their trainer's spotlight, and their trainer's turn.

- **No independent initiative.** A pokemon never rolls for or holds its own place in the turn order. It acts when its trainer acts.
- **One action per trainer turn.** When a trainer's turn comes up, they pick the action for the active partner: a move, a command, a held-back reaction, an item use, a free bond check, or a deliberate pass. The partner does not get a separate "second turn" later in the round.
- **Only one partner acts at a time.** If a trainer owns multiple partners (party roster, PC storage, on-site ranger callouts), the trainer picks **one** partner for the current turn. The rest are staged, recalled, or held in reserve.
- **Swaps are the trainer's call.** Switching the active partner is a trainer action, not a free interrupt. A swap costs the trainer's action for the turn unless the GM rules a context-appropriate exception (ball recall mid-leap, recall-and-resend on a downed ally, etc.).
- **Reactions are automatic, not chosen.** Some moves, abilities, or items are flagged as reactions. A pokemon reaction does **not** wait for the trainer's turn and does **not** require the trainer to declare it. The GM watches the trigger conditions, then chooses whether and when the reaction fires.
- **The GM controls reaction timing.** The GM decides when a reaction triggers, what it targets, and in what order it resolves relative to other reactions in the scene. The goal is to make the reaction useful to the player: the partner defends the trainer, protects a downed ally, or seizes a clear opening without burying the table in bookkeeping. If a reaction would be a net negative to the party, the GM may hold it for a better moment or skip it for the round.
- **Tell the player, not the chat.** When a reaction fires, narrate the effect in the GM voice and mark it on the partner's sheet. The player should never have to "remember" to use a reaction; the GM runs that clock.
- **Bond and trust gate the rules.** A partner acting against its trainer's intent, refusing a command, or breaking from formation is a `BND` moment, not a mechanics moment. The companion rules ride on top of bond, not the other way around.

## Ambient Inserts
- Use `templates/ad-crawl.md` for Pokedex blurbs, trainer network notices, contest posters, radio chatter, league ads, and ranger alerts.
- Let the world feel bright and lively without turning every public message into a cutscene.
- Roughly one in three inserts should hint at a route problem, social opportunity, or rival thread the table can chase.

## Pressure Levers
- rival trainers and league expectations
- habitat disruption and local crises
- criminal teams, smuggling rings, and unethical labs
- public image, trust, and endangered partnerships

## Discord Rendering
- Lean on `-#` subtext for **route**, **weather**, and **time of day**. The road is half the game.
- Use `> ` block quotes for trainer speech, professor dialogue, and the partner's inner voice.
- Italicize species and partner names with `*...*` so the world's terms read as the world's terms.
- Use `__...__` underline for **rare** creatures, **legendary** items, and **signature** moves that should feel elevated.
- Use `||...||` spoilers for evolutions, hidden identities, and crisis reveals the table should choose when to uncover.
- Render party sheets, move lists, and PC rosters as fenced code blocks so the data does not wrap on mobile.

## Pack References
- `flavorpacks/pokemon/references/gameplay-loop.md`
- `flavorpacks/pokemon/references/gm-playbook.md`
- `flavorpacks/pokemon/references/source-manifest.md`
