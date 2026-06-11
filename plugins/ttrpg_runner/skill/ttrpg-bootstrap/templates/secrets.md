# GM Secrets

> **GM EYES ONLY. NEVER PRINT THIS FILE'S CONTENTS TO PLAYER-FACING CHAT.**
>
> The instant a secret is rendered into a player-visible Discord message, in-character speech, NPC dialogue, ambient insert, recap, or shared handout, it stops being a secret and becomes table canon. Treat that line as load-bearing.
>
> This file holds everything only the GM is allowed to know: hidden NPC agendas, true identities, secret faction goals, planted evidence, ticking bombs the players cannot see, GM-triggered twists, the real reason a scene is the way it is, and the GM's own behind-the-screen planning (open clocks, stakes, hooks, what to do if the players go off-script).
>
> **This file is append-only.** New beats, secrets, and planning notes are appended to the end of the appropriate section. Old entries are never edited, deleted, or rewritten in place. To merge or shrink this file, run `/ttrpg-clean`; the LLM will open it, compact the entries, deduplicate, and rewrite it under 100 lines.
>
> Do not summarize, paraphrase, or "soft reveal" secrets in chat. Do not paste spoiler-tagged copies of this file. Do not echo a secret back when a player guesses close to it. Let the players earn reveals through play, and let the GM decide when (or if) a secret ever surfaces.

## Active Secrets

### {{secret_title}}

- **Domain:** {{faction | npc | location | item | event | plot}}
- **Status:** {{dormant | active | about_to_fire | resolved}}
- **Players Suspect:** {{none | partial | wrong | confirmed_but_not_proven}}
- **Reveal Trigger:** {{what would expose this to the table}}
- **True Content:** {{the real fact, GM only}}
- **Surface Cover:** {{what the players currently believe instead}}
- **If Exposed:** {{consequences, who moves, what changes}}

### {{secret_title}}

- **Domain:** {{faction | npc | location | item | event | plot}}
- **Status:** {{dormant | active | about_to_fire | resolved}}
- **Players Suspect:** {{none | partial | wrong | confirmed_but_not_proven}}
- **Reveal Trigger:** {{what would expose this to the table}}
- **True Content:** {{the real fact, GM only}}
- **Surface Cover:** {{what the players currently believe instead}}
- **If Exposed:** {{consequences, who moves, what changes}}

## Burned Secrets

> Secrets that already leaked, fired, or were resolved. Keep the record so the GM does not re-use the same twist, but they are no longer protected information.

- [{{date}}] {{secret_title}} — {{how it surfaced or was retired}}

## GM Planning Notes

> Behind-the-screen planning that does not need to stay a secret from a rules standpoint, but does need to stay out of player chat. Append-only: each new beat adds a dated entry at the end of this section. Run `/ttrpg-clean` to compact.

- **Open Clocks:** {{clocks_with_progress}}
- **Stakes:** {{stakes}}
- **Hooks:** {{hooks}}
- **If The Players Go Off-Script:** {{fallback_beats}}
- **Next Moves:** {{next_moves}}

### {{utc_now}} — {{planning_note_title}}

- **What:** {{what_is_being_planned}}
- **Why:** {{why_it_matters}}
- **Trigger:** {{what_brings_this_into_play}}
- **Backup If Ignored:** {{fallback}}
