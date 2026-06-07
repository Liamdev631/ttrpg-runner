# Discord Output Formatting

This skill renders to Discord. Use Discord-native markdown so messages look clean and scannable in chat.

> **Source:** [Discord Markdown Text 101 (Chat Formatting: Bold, Italic, Underline)](https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline)
>
> **Related:** [Discord Spoiler Tags](https://support.discord.com/hc/en-us/articles/360022320632)

## Discord-Specific Gotchas

These are the only formatting rules that differ from standard CommonMark and they will bite you if you forget them.

- `__text__` is **underline**, not bold. Discord borrowed the underline syntax from MediaWiki. Use `**text**` for bold.
- Discord does **not** render pipe tables. Use bullet lists, headings, or code blocks instead.
- Headings (`#`, `##`, `###`) only render at the **start of a message line**. Leading spaces silently break them.
- Inline code (`` `text` ``) and code blocks cancel every other formatting inside them. Do not try to bold text inside a code block.
- Spoiler tags `||text||` are also cancelled by code blocks.
- Lists require a **single space** between the marker and the text (`- item`, `1. item`, `> quote`). No space, no list.
- Nested lists require **two spaces** of indent before the next `-` or `*`.
- Masked links must use the full `https://` URL. Bare domains do not become clickable.

## Text Formatting

Use these liberally to give the player's eye anchors on every turn.

| Effect | Syntax | Example |
| --- | --- | --- |
| Bold | `**text**` | **important beat** |
| Italic | `*text*` or `_text_` | *emotional beat* |
| Bold Italic | `***text***` | ***critical moment*** |
| Underline | `__text__` | __quiet aside__ |
| Underline Bold | `__**text**__` | __**major flag**__ |
| Underline Italic | `__*text*__` | __*half-remembered*__ |
| Underline Bold Italic | `__***text***__` | __***legendary***__ |
| Strikethrough | `~~text~~` | ~~replaced fact~~ |
| Spoiler | `\|\|text\|\|` | \|\|hidden truth\|\| |
| Inline code | `` `text` `` | `1d20+5` |
| Masked link | `[label](https://url)` | [Session File](https://example.com) |

Avoid mixing more than three of these on the same phrase. Two is plenty. Three is the ceiling.

## Organizational Formatting

### Headers

Headers mark the beat. Use them on top of every distinct block you send to the player.

```text
# Big Beat (scene title, chapter, act break)
## Mid Beat (location, faction focus, single NPC)
### Small Beat (single sub-decision, single die call)
```

There must be a single space between the `#` and the heading text. No leading whitespace on the line.

### Subtext

`-# ` produces the small grey subtext line under a message. Use it for ambient tags, timestamps, or system notes the player can ignore.

```text
-# West Market Station, 22:14 local - rain steady on the platform
```

The `-#` must be at the very start of the line.

### Lists

```text
- Streets are loud tonight.
  - Two rival crews on the same corner.
  - Cops pretending not to see it.
- Atram bus is fifteen minutes out.
* Atram bus is fifteen minutes out.
1. You step off the platform.
2. You wait for the next one.
3. You cut through the alley.
```

Indent nested items by exactly two spaces.

### Block Quotes

Single-line `>` is a quote or a soft aside. Use it for inner monologue, NPC speech, and the GM voice when it is breaking the fourth wall.

```text
> "You don't owe them anything." - Rin
```

Multi-line `>>>` is a quoted block. Use it when a block of text is being attributed to a single source, such as a flashback or an intercepted message.

```text
>>> Intercepted transmission, 03:12:
>>>
>>> "...the package is warm. Repeat, the package is warm.
>>> Expect a buyer at the south gate by 04:00."
```

Always put a single space after `>` and `>>>`.

## Code Blocks

Code blocks are the workhorse of the skill. Use them for dice roll cards, JSON state snapshots, stat sheets, and any block of text that must render with fixed width.

Single-line inline code is for short tokens, expressions, or commands:

```text
Roll `1d20 + REF + 3` to see if the door holds.
```

Multi-line fenced code blocks are for the roll cards, the character sheets, and any tabular data. Discord treats ``` ```text ``` and ``` ``` ``` identically for prose; the language tag is just a hint to the renderer.

```text
```
=======================================
  CHECK * REF/Stealth 3 vs DC 12
---------------------------------------
  Difficulty : 12
  d10        : 7
  Stat       : 4
  Skill      : 3
  Modifier   : +0
---------------------------------------
  TOTAL      : 14
  OUTCOME    : SUCCESS
=======================================
```
```

Do not try to bold, italicize, or spoiler text inside a code block. Discord will not render it.

## Block Quotes vs Code Blocks for Dice

Use both. The code block carries the numbers. The block quote carries the meaning.

```text
**REF / Stealth vs DC 12**

```
=======================================
  CHECK * REF/Stealth 3 vs DC 12
---------------------------------------
  Difficulty : 12
  d10        : 7
  Stat       : 4
  Skill      : 3
  Modifier   : +0
---------------------------------------
  TOTAL      : 14
  OUTCOME    : SUCCESS
=======================================
```

> The guard's flashlight passes over the crate. You don't breathe.
```

This pairing keeps the math auditable and the fiction in the player's voice.

## Spoilers

Use `||...||` for any beat the player should be able to choose not to see. Common cases:

- Plot twists they have not earned yet
- Hidden NPC intentions
- GM-only notes that leak into a shared channel
- Optional lore dumps from a flavor pack

Do not use spoilers for routine dice results, ambient inserts, or NPC dialogue the player already heard.

## Message Shape Patterns

These are the canonical message shapes the agent should reach for during play. Mix and match, but do not invent new ones when one of these fits.

### Turn Header

```text
### West Market Station - 22:14
-# Night shift, light rain, two corps on edge
```

### Beat Description

```text
**Rin** waits at the south platform with a brown envelope in her lap.

> "You didn't come last week. I figured you were dead."

*She slides the envelope across the bench toward you.*
```

### Choice Menu

```text
**What do you do?**

1. Take the envelope and ask why she is nervous.
2. Ignore the envelope and ask who is watching.
3. Walk past her toward the south gate.
```

### Dice Card

See "Block Quotes vs Code Blocks for Dice" above.

### Session Handoff

```text
### End of Beat
- You owe **Yuki** a follow-up call.
- The south gate job opens at 04:00.
- `HP 12/12`, `Stress 2/6`, `¥4,200` in the account.

> -# Session file: `~/.hermes/ttrpg-runner/sessions/<id>/`
```

## Style Rules for This Skill

- Open every scene response with a `###` heading that names the beat.
- Use `-#` for ambient context the player can skim.
- Bold the most important noun or verb in every paragraph of fiction.
- Use block quotes for NPC speech and GM voice.
- Use code blocks for dice cards, stat blocks, and JSON.
- Use spoilers only for genuine surprises or hidden notes.
- Never use Discord tables. Use bullet lists or code blocks instead.
- Keep each message scannable in under five seconds. If a message is longer than ten short paragraphs, split it across multiple Discord messages.
