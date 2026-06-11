---
name: ttrpg-refresh
description: Refresh the agent against the active ttrpg-runner session after Hermes has compressed the conversation. Call this skill every time you notice a context-compression marker, a context-pressure warning, an obviously missing scene from its own recall, a session metadata block it has not actually loaded, or a tool result that has been pruned by the compressor.
version: 1.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# TTRPG Refresh

The recovery skill for `ttrpg-runner`. It exists because Hermes
periodically compresses the conversation to keep the working
context inside the model's window. When that happens, the agent's
in-context memory of the campaign shrinks to a structured summary
and the rest of the table's history is gone from the LLM's head.
This skill is how the agent re-loads itself against the active
session's canonical files so play continues seamlessly.

`/ttrpg-refresh` is a slash command. The agent should invoke it on
its own initiative every time it notices that compression has
occurred; it does not wait for the player to type it. The recovery
loop is a normal part of the agent's per-turn discipline, not a
manual cleanup the table has to remember.

## When Compression Happens

Hermes runs two independent compression systems (see the upstream
guide at `https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching`):

- **Gateway Session Hygiene.** Pre-agent, fires at 85% of context
  length. Safety net for sessions that grew large between turns
  (overnight Discord / Telegram backlog).
- **Agent ContextCompressor.** In-loop, fires at the configured
  `compression.threshold` (default 50% of context). This is the
  normal compression path the agent will see most often.

Both layers follow the same 4-phase algorithm: (1) prune old tool
results, (2) decide head / middle / tail boundaries, (3) generate a
structured summary of the middle, (4) assemble head + summary +
tail. On subsequent compressions the previous summary is updated
in place rather than rebuilt from scratch, so the agent will see a
"running" summary that grows over the campaign.

## Compression Markers The Agent Watches For

Compression is not announced. The agent has to notice it. The
following markers are the canonical signals; if the agent sees
any of them, it should call `/ttrpg-refresh` before doing
anything else that turn.

- **First-compaction system-prompt note.** On the first
  compression of a session, Hermes appends a note to the system
  prompt. The note is a literal substring the agent can grep
  for:

  > `[Note: Some earlier conversation turns have been compacted...]`

  If the system prompt (or anything that looks like the system
  prompt) contains that string, compression has happened at
  least once.

- **Standalone assistant summary message.** After the head
  messages, Hermes inserts an assistant turn that begins with a
  literal marker and then the structured summary. The marker is:

  > `[CONTEXT COMPACTION] Earlier turns were compacted...`

  An assistant turn whose first line starts with that string is
  the in-context summary of everything that was compressed.

- **Pruned tool results.** Phase 1 of the compression algorithm
  replaces the body of any old tool result (>200 chars) outside
  the protected tail with:

  > `[Old tool output cleared to save context space]`

  If the agent sees a tool result that is exactly that string, or
  a series of tool results that all read like that string, the
  underlying tool output is gone from the context. The agent
  cannot trust its recall of what those tool calls originally
  returned. It must re-open the file or re-run the tool if the
  fact matters.

- **Context-pressure warning.** Hermes emits a warning when the
  prompt hits 85% of the compression threshold. The warning
  format is:

  > `⚠️ Context is 85% to compaction threshold (42,500/50,000 tokens)`

  The exact numbers change with the model and the configured
  threshold; the leading `⚠️ Context is 85% to compaction
  threshold` substring is the load-bearing part. Seeing this
  warning means compression is imminent or has just happened;
  the next turn may already be a post-compression turn.

- **Improbable recall gaps.** Soft signal. If the agent catches
  itself unable to remember a fact the table has clearly already
  established (a named NPC, a location, a secret, a clock, a
  prior beat) — and especially if it has to invent a placeholder
  to keep moving — that is itself a compression artifact. The
  right move is to call `/ttrpg-refresh`, not to bluff.

- **First turn of a resumed session.** Not strictly a compression
  event, but a session that resumes after a long absence is in
  the same shape as a post-compression turn: the agent has a
  fresh context and the campaign's truth lives on disk. Treat
  resume as an implicit compression marker.

## What Refresh Does

`/ttrpg-refresh` runs a six-step recovery loop. The point is to
rebuild the in-context state of the active session from disk
without re-reading the full conversation, and to re-load the
operating rules the agent needs in scope to keep running the
table.

The agent follows the steps in order; the order matters because
some steps depend on earlier steps' outputs.

1. **Identify the active session.** Re-read the Session Metadata
   block at the top of `story.md` (the `> **Game**: ...`,
   `> **Flavor Packs**: ...`, `> **Started**: ...`, `> **Last
   Resumed**: ...` lines). Confirm which session this is, which
   flavor packs are active, what support level it runs at, and
   what era (for Mistborn). If the Session Metadata block has
   changed since the agent last saw it, the post-compression
   summary in the assistant's history is stale; the disk wins.

2. **Re-load the session's canonical data files.** Skim (do not
   re-read end-to-end unless the summary is clearly incomplete)
   each of:

   - `story.md` — the running fiction, paying special attention
     to the current scene.
   - `timeline.md` — beat-by-beat chronology. This is the
     fastest way to rebuild a sense of "where we are in the
     story."
   - `secrets.md` — GM-only file. Active Secrets, Burned
     Secrets, and GM Planning Notes. This is the file the
     compressor has the least reason to summarize well, and
     the file the table is most harmed by losing. Re-read it
     carefully.
   - `characters/*.md`, `locations/*.md`, `events/*.md` —
     dossiers for every entity referenced in the current
     scene. Do not pre-load the whole `characters/` folder;
     pick the ones the current beat is about to need.
   - `rolls/*.json` — only if the current beat is about to
     resolve a risky action whose audit trail matters.

   Per the append-only rule (see `ttrpg-bootstrap`'s
   "Append-Only Session Files" section), these reads are
   recovery reads, not in-flight edits. The agent does not
   rewrite them as part of a refresh. If a file is over 100
   lines and hard to skim, the recovery step is "queue a
   `/ttrpg-clean` for the next break" — not "edit the file
   in place right now."

3. **Re-load the operating rules.** The compression may have
   dropped the agent's recall of how to format Discord output,
   how to run the dice tool, how to handle turn order, and how
   to manage the secrets/print boundary. Re-load, in this
   exact order:

   a. `ttrpg-core` — the always-on common rules. Use
      `skill_view("ttrpg-core")`. The whitespace discipline,
      Discord formatting, multiplayer turn management, and
      dice display format all live here.
   b. The active setting pack — for a single-pack session,
      `skill_view("ttrpg-<pack>")`; for a native crossover,
      `skill_view` for both packs. Mistborn sessions also need
      `skill_view("ttrpg-mistborn", "resources/era_<n>.md")`
      for the era file the session metadata records.
   c. `ttrpg-bootstrap` — only if the recovery is happening at
      session-resume time and the agent needs to re-confirm
      the bootstrap procedure. In-flight mid-session refreshes
      do not need to re-load bootstrap.
   d. `ttrpg-clean` — only if a recovery read flagged a file
      that is over the 100-line budget or clearly full of
      stale entries. Otherwise skip; the compactor is for
      dedicated clean moments, not every refresh.

   The order matters because `ttrpg-core` is required reading
   for every turn (per `ttrpg-bootstrap`); the setting pack
   layers on top of it; bootstrap is the meta-skill that
   governs session lifecycle, not per-turn play.

4. **Cross-check the in-context summary against the disk.** The
   structured summary Hermes produced in Phase 3 of the
   compression algorithm uses a fixed template: `## Goal`,
   `## Constraints & Preferences`, `## Progress` (with `Done`,
   `In Progress`, `Blocked` subsections), `## Key Decisions`,
   `## Relevant Files`, `## Next Steps`, `## Critical Context`.
   Walk through that template against what the disk actually
   says. If the two disagree, the disk wins. Specifically:

   - The "Relevant Files" list in the summary may reference
     files that have since been moved, compacted, or replaced
     by `/ttrpg-clean`. Use the current on-disk layout, not
     the summary's file paths.
   - The "Progress → In Progress" section may be wrong about
     what is currently in flight. The current scene in
     `story.md` is the truth.
   - The "Next Steps" section may suggest moves the table has
     already made. The current beat in `story.md` / current
     timeline entry is the truth.
   - The "Critical Context" section may quote a value
     (a stat, a roll total, a deadline) that has since
     changed. The current dossier or roll is the truth.

5. **Re-anchor the active speaker.** In multiplayer sessions the
   agent must re-confirm whose turn it is from the most recent
   scene, not from the in-context summary. The
   `> **Up next: <player>**` handoff at the end of the last
   beat is the canonical pointer.

6. **Resume play with a single short opening line.** The
   recovery is internal; the table does not need a long
   "previously on..." recap. The right shape is one sentence
   in the GM voice that re-anchors the scene ("You are still
   in the cantina; Mira is mid-sentence.") and then the normal
   per-turn format. If the player asks for a recap, the
   `templates/session-summary.md` template is the right
   shape; do not improvise a recap from the compressed
   summary, since the disk is more accurate.

## What Refresh Must Not Do

These are hard rules. The whole point of refresh is that the
agent re-loads itself cleanly. Each of these failure modes
breaks the recovery.

- **Do not narrate the recovery.** The table does not need to
  see "Detected context compression; refreshing session." The
  refresh is an internal step that happens before the first
  prose line of the next beat. The only thing the player sees
  is the normal GM-voice opening of the resumed scene.
- **Do not paste `secrets.md` into chat.** Same rule as
  always. A refresh that paraphrases a secret as part of
  "re-anchoring" has leaked it. The compressed summary may
  already contain a stripped-down version of a secret; that
  is the compressor's problem, not a license to re-render the
  secret in Discord.
- **Do not rewrite session files as part of refresh.** Refresh
  reads; it does not write. The only sanctioned write paths
  are the per-turn append, `/ttrpg-clean`, and bootstrap.
  A refresh that "tidies up" `secrets.md` while it is at it
  has crossed into a clean, and a clean is its own skill.
- **Do not trust the in-context summary over the disk.** The
  summary is best-effort lossy compression; the disk is the
  canonical state. When they disagree, the disk wins,
  including about facts the summary is silently wrong about.
- **Do not re-load more packs than the session needs.** A
  single-pack session re-loads the single pack. A native
  crossover re-loads the two. Generic mode re-loads nothing
  setting-specific. A refresh that pulls in `ttrpg-pokemon`
  lore for a Cyberpunk session has contaminated the campaign.
- **Do not run `/ttrpg-refresh` and `/ttrpg-clean` in the same
  turn.** Refresh is a read; clean is a write. Mixing them in
  one turn means the agent is rewriting a session file it has
  not yet finished re-loading, which is exactly the stale-
  context bug refresh is meant to prevent.

## Detection Heuristics

The markers above are the canonical signals. In practice the
agent does not get a clean grep over its own context; it
notices compression when something feels wrong. These
heuristics are not strict rules, but they are the patterns
that have actually caught real compression events:

- The system prompt is suddenly much shorter than the agent
  remembers, or it contains a bracketed compaction note it
  has never seen before.
- An assistant turn in the recent history is dominated by a
  `## Goal / ## Progress / ## Relevant Files` structured
  summary instead of normal prose. That is the post-
  compression summary message.
- The agent reaches for a tool result (a file it supposedly
  read, a roll it supposedly saw) and the result in its
  context is the literal string
  `[Old tool output cleared to save context space]`. It
  cannot trust what that tool call returned; it has to
  re-run the read.
- The agent catches itself about to repeat a question the
  player already answered, or about to introduce a beat the
  timeline says already happened. The agent is guessing
  about state it has lost; refresh and the disk will tell
  the truth.
- The current player names an NPC, location, or secret the
  agent has no recollection of, even though the table
  clearly treats it as established. The disk has it;
  refresh brings it back.

When in doubt, refresh. The cost of an unnecessary refresh
is a few extra file reads and a slightly longer first
message of the next beat; the cost of a missed refresh is
the agent inventing canon to fill the gaps it cannot
remember.

## Verification

The skill is working correctly when all of the following are
true:

- The agent calls `/ttrpg-refresh` on its own initiative
  every time it sees a compression marker, a context-pressure
  warning, an obviously missing scene, or a pruned tool
  result — without waiting for the player to type it.
- The refresh's six steps run in order: identify session,
  re-load canonical files, re-load operating rules in
  core → pack → (bootstrap if resuming) → (clean if
  flagged) order, cross-check the in-context summary
  against the disk, re-anchor the active speaker, and
  resume with a single short opening line.
- The disk wins every disagreement between the in-context
  summary and the session files, including about the
  "Relevant Files" list, the "In Progress" section, the
  "Next Steps" section, and the "Critical Context" values.
- No `secrets.md` content reaches player-facing chat during
  or after a refresh.
- Refresh reads; it does not write. The only write the
  refresh turn produces is the normal per-turn append for
  the new beat, plus a one-line opening message.
- The next beat uses the same Discord formatting, the same
  dice card shape, and the same turn-handoff convention as
  every other beat — the rules from `ttrpg-core` are
  back in scope and being followed.
- After a refresh, the agent can name the active flavor
  pack(s), the current scene, the active player, the last
  rolled check, the most recent timeline entry, and any
  active secrets — all without inventing canon.

## Reference

- `ttrpg-bootstrap` - registers this skill, defines the
  append-only rule that recovery reads must respect, and
  names `/ttrpg-refresh` as the recovery loop that sits
  between compactions.
- `ttrpg-core` - the always-on common rules. Re-loaded
  first on every refresh, before the active setting pack.
- `ttrpg-clean` - the compactor. Refresh may flag files for
  `/ttrpg-clean`; it does not run the compactor itself.
- `ttrpg-cyberpunk`, `ttrpg-dnd`, `ttrpg-mistborn`,
  `ttrpg-pokemon`, `ttrpg-expanse` - the native flavor packs.
  Re-load the active session's pack(s) as part of step 3.
- `templates/secrets.md` - the shape of the GM-only file
  the agent re-loads most carefully during a refresh.
- `templates/session-summary.md` - the shape of an
  explicit recap, if the player asks for one after a
  refresh.
- Hermes compression guide -
  `https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching`
  - the upstream reference for the dual-compression
  system, the 4-phase algorithm, and the structured
  summary template the in-context summary message uses.
