---
name: ttrpg-clean
description: Compactor for ttrpg-runner session files. The only sanctioned read-modify-write path for session data. Opens each session file, merges redundant entries, drops resolved and stale items, and rewrites the file under 100 lines.
version: 1.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# TTRPG Clean

The compactor skill for `ttrpg-runner` session files. Session data
files (`story.md`, `timeline.md`, `secrets.md`, the `characters/`,
`locations/`, and `events/` dossiers) are **append-only** during
play — the GM never opens, reads, edits, and saves them in the
middle of a turn. They grow. Eventually they get long. That is
what this skill is for.

`/ttrpg-clean` is the only sanctioned read-modify-write path for
session data. When the player or the GM runs it, the LLM opens
each session file, merges redundant entries, drops resolved and
stale items, and rewrites the file at or under 100 lines. Play
resumes against the compacted file as if nothing happened.

## Why It Exists

`/ttrpg-bootstrap` declares the data files append-only. The rule
is what makes per-turn writes O(1): the GM skims, appends one
new beat, closes the file. No full re-read, no line-level
diff-and-patch, no risk of clobbering a fact the table has
already accepted as canon.

The tradeoff is that append-only files grow. A long campaign
will eventually produce a `timeline.md` that no longer fits in
the working context, a `secrets.md` full of fired-and-archived
twists, a `story.md` with every scene of the campaign in it.

`/ttrpg-clean` is the off-turn that fixes that. It is the only
moment a session file is read, summarized, deduplicated, and
rewritten. The LLM does the work; the table does not see it.
When the compactor is done, the file is the same campaign, the
same canon, the same secrets — just smaller and easier to
re-skim on the next turn.

## When To Run It

Run `/ttrpg-clean` when any of these is true:

- A session file is approaching a size that is painful to skim
  in one read (rough rule of thumb: more than 100 lines, or
  larger than the working context can comfortably hold).
- A `secrets.md` has accumulated multiple `Burned Secrets` that
  no longer need to dominate the file.
- A `timeline.md` has more than one campaign-arc of beats and
  the early beats are no longer load-bearing.
- A character/location/event dossier has grown past the point
  where the most recent beat is what the table actually needs.
- The player explicitly asks for a clean.

Do not run `/ttrpg-clean` mid-scene. Pause between beats (at a
hard scene break, at the end of a session, or right before the
next session resumes). The compactor replaces file contents; if
the in-flight beat is still being narrated, narrate it first,
append it, *then* clean.

## What It Touches

`/ttrpg-clean` compacts the **active session** only. It never
touches another session's folder, never touches a flavor pack's
`SKILL.md`, never touches the plugin's `tools.py` or `lib.py`.

The files it compacts, in order:

1. `timeline.md` — the most natural first target. It is a
   chronological log and a chron log is the easiest thing to
   compact: drop stale beats, merge adjacent beats that
   describe the same moment, and keep the load-bearing plot
   turns.
2. `story.md` — running fiction. The Session Metadata block at
   the top is preserved verbatim. The running fiction is
   compacted by keeping the most recent beat in full, the
   most recent few scenes in moderate detail, and older
   scenes as a one-line "previously" recap at the end of the
   file (or as a hand-off into a new `events/<slug>.md`).
3. `secrets.md` — both `Active Secrets` and `GM Planning
   Notes` are deduplicated and merged; `Burned Secrets` are
   collapsed to a single-line-per-entry appendix.
4. `characters/<slug>.md`, `locations/<slug>.md`,
   `events/<slug>.md` — one entity per file. Compact each
   dossier by keeping the canonical header (Stats, Inventory,
   Hooks, etc.) and moving long `Session Notes` to a
   condensed form. Outdated stats are merged with their
   current values; superseded lore is dropped.

`rolls/<stamp>-<label>.json` files are **not** compacted.
They are an append-only audit trail; once a roll is recorded
it stays recorded. `/ttrpg-clean` does not open, merge, or
delete roll files.

## The Compaction Procedure

The procedure is the same on every clean. The model follows it
in order; the order matters.

1. **Identify the active session.** Read the Session Metadata
   block at the top of `story.md` to confirm the session is
   real and you are looking at the right folder. If the
   player named a session explicitly, use that one. If the
   player did not name one, ask before opening any folder.

2. **Enumerate the files in scope.** Walk the session folder
   and list every file `/ttrpg-clean` will touch. Show the
   list to the player (one line per file) so they know what
   is about to be rewritten.

3. **Open one file at a time.** For each file in the order
   above:

   a. **Read it in full.** This is the only sanctioned
      read step. Use Hermes's file tools to open the file
      end-to-end. Do not skim. The compactor must see every
      entry before it can decide what to merge or drop.

   b. **Classify each entry.** For every beat, secret,
      planning note, or dossier field, mark it with one of:

      - `keep` — still load-bearing. Move it into the
        compacted file as-is (or with a small merge if a
        near-duplicate is also `keep`).
      - `merge` — a near-duplicate of a `keep` entry. Fold
        its unique information into the `keep` entry and
        drop the duplicate.
      - `drop` — superseded by a newer entry, no longer
        relevant, or fully resolved and already archived.
      - `archive` — resolved / no longer active, but worth
        keeping a one-line note of. Move to the file's
        archive appendix.

   c. **Rewrite the file.** Produce a new full-file rewrite
      that contains:

      - The file's required header block (banner for
        `secrets.md`, Session Metadata for `story.md`, the
        `templates/<thing>.md` shape for dossiers).
      - All `keep` and `merge`d entries, in their original
        order, deduplicated.
      - A short `Archive` appendix of one-line `archive`
        entries at the end.
      - Nothing else. No scratch reasoning, no notes-to-self,
        no commentary.

   d. **Verify the line count.** If the rewrite is over 100
      lines, compact again: re-classify the longest entries,
      merge more aggressively, move older beats to the
      archive. Iterate until the file is at or under 100
      lines. The line budget is load-bearing — it is what
      keeps the next turn's skim fast.

   e. **Save the file.** Hermes writes the new contents over
      the old. The old version is not preserved; the
      compacted file is the new canonical state. (This is
      the only sanctioned read-modify-write, and the rule is
      "save in place"; the player does not get a backup
      folder, an undo, or a `*.bak` twin. Per the project
      rules there is no deprecation window and no
      "for archival" copy.)

4. **Report.** After all files are rewritten, tell the player
   what was compacted: which files, how many entries merged,
   how many dropped, and the new line counts. Do not paste
   the new contents into chat — the player can open the
   files.

5. **Resume play.** The next turn proceeds as normal. Skim,
   append, close.

## Compaction Rules Per File

These rules apply during the classification step above.

### `timeline.md`

- `keep` a beat only if it changed the campaign's state
  (location shift, NPC introduced, secret fired, mission
  started or ended, clock ticked).
- `merge` adjacent beats that describe the same moment (e.g.
  "Mira enters the cantina" + "Mira orders a drink" → one
  beat).
- `drop` pure flavor beats that did not move the campaign.
  Flavor belongs in `story.md`, not in the timeline.
- `archive` campaign-arc-level turning points that the table
  still references ("the night the cantina burned") into a
  one-line appendix at the bottom.

### `story.md`

- Preserve the Session Metadata block at the top, byte-for-byte.
- `keep` the current scene and the immediately preceding scene
  in full prose.
- `merge` older adjacent scenes into a single condensed beat
  per scene (one short paragraph).
- `drop` exact duplicate descriptions of the same moment
  across scenes.
- `archive` the original prose of any merged scene as a
  one-line "previously" line in the new events dossier for
  that scene, if one does not already exist. Otherwise drop
  the old prose; the timeline still has the beat.

### `secrets.md`

- Preserve the GM-only banner verbatim.
- `keep` every entry in `Active Secrets` that is still
  `dormant`, `active`, or `about_to_fire`.
- `merge` two secrets that are the same twist described two
  different ways. Keep the entry with the most complete
  fields; absorb the other entry's unique information into
  it.
- `move to Burned Secrets` any secret that fired or resolved
  during play but was never archived.
- `drop` nothing in `Active Secrets` — a secret is either
  `keep` or it moves to `Burned Secrets`. There is no
  "deleted a secret without a trace" path.
- For `GM Planning Notes`, `keep` the open clocks with
  current progress, the active stakes, and the live hooks.
  `merge` near-duplicate planning notes. `drop` planning
  notes whose trigger has passed and whose fallback is
  irrelevant. `archive` planning notes for hooks that the
  table already bypassed, in case the GM wants to recycle
  the beat later.

### `characters/<slug>.md`, `locations/<slug>.md`, `events/<slug>.md`

- Preserve the entity's canonical header (Name, Slug, Kind /
  Type / Event Type, etc.) verbatim.
- `keep` the most recent canonical fields (Stats, Inventory,
  Status, First Impression, Sensory Details, What Happened).
- `merge` duplicate entries in the `Session Notes` section
  into a single "current state" line per session.
- `drop` session notes whose fact is already represented in a
  canonical field above (e.g. "Mira picked up the pistol" is
  redundant once `Signature Gear: pistol` is set).
- `archive` older session notes as dated one-liners at the
  bottom of the dossier, so the GM can still trace how the
  character got here.

## What The Compactor Must Not Do

These are hard rules. Violating any of them means the clean
failed and must be re-run.

- **Do not edit a session file in place outside `/ttrpg-clean`.**
  The whole point of this skill is that in-flight turns do
  *not* read-modify-write session files. If a turn needs
  history rewritten, the turn should describe the desired
  state to the player and queue the rewrite for the next
  `/ttrpg-clean`.
- **Do not touch `rolls/`.** Dice audit files are append-only
  forever. Cleaning them would be a soft deletion of campaign
  history.
- **Do not touch the Session Metadata block in `story.md`.**
  It is the identity record. A clean that bumps the metadata
  is a clean that broke the session.
- **Do not touch another session's folder.** The compactor is
  always scoped to the active session. Cross-session rewrites
  are a session-isolation violation.
- **Do not invent canon to fill space.** A clean that adds
  new beats, new secrets, or new NPCs to a file is not a
  clean. If a section is empty, leave it empty (or restore
  it to its template shape).
- **Do not paste `secrets.md` into player-facing chat.** The
  compactor reads the file, summarizes the work it did, and
  stops. The compacted file is for the GM. A "before / after"
  snippet of a secret in chat is a leak.
- **Do not produce a `*.bak` or `*.prev` twin.** The old file
  contents are gone after the clean. Per the project rules,
  there is no deprecation window and no archival copy. The
  campaign is supposed to live in its current canonical
  files, not in a graveyard of superseded snapshots.
- **Do not exceed 100 lines.** If a file is still over 100
  lines after a compaction pass, compact again. The line
  budget is the point.

## Verification

The skill is working correctly when all of the following are
true:

- `/ttrpg-clean` is only ever invoked between beats, not in
  the middle of a scene.
- The compactor reads each file in scope in full before
  rewriting it.
- The rewrite preserves required headers (Session Metadata
  in `story.md`, the GM-only banner in `secrets.md`, the
  entity headers in dossiers).
- The rewrite is at or under 100 lines per file.
- `rolls/` files are untouched.
- No new canon is invented during the clean.
- No `secrets.md` content reaches player-facing chat.
- The player is told which files were compacted and the new
  line counts, but is not shown the new contents in chat.
- The next turn after a clean reads the compacted file
  normally and proceeds as if nothing changed.

## Reference

- `ttrpg-bootstrap` - declares the append-only rule and
  registers this skill as the only sanctioned read-modify-write
  path. See "Append-Only Session Files" in `ttrpg-bootstrap`.
- `ttrpg-core` - common-rules pack. Load once at the start of
  the session per `ttrpg-bootstrap`; the compactor inherits
  the same Discord formatting rules for any chat-side report
  it issues.
- `templates/secrets.md` - the shape every fresh `secrets.md`
  is seeded from. The compactor rewrites `secrets.md` back to
  this shape (with merged and archived entries).
- `templates/character.md`, `templates/location.md`,
  `templates/event.md` - the canonical shapes for dossiers.
  The compactor rewrites each dossier back to its template
  shape (with merged and archived entries).
