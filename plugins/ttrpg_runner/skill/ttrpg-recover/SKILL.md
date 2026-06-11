---
name: ttrpg-recover
description: Recover a ttrpg-runner session immediately after the context engine has compressed the conversation. Reads the data files re-pasted by the engine, compares them against the recent transcript, updates the data files to reflect what just happened, and hands play back to the GM.
version: 3.0.0
author: OpenAI
platforms: [linux, macos, windows]
---

# TTRPG Recover

Run this skill the moment a "Session Data Update Required" bridge
message appears in the working context. That marker is emitted by
the `ttrpg-runner` context engine when the host framework crosses
its token threshold. The engine has already re-pasted every active
session data file into the working context and kept the most recent
`protect_last_n` user / assistant / tool messages verbatim. This
skill tells the GM what to do with that re-pasted state and the
recent transcript.

The recovery skill is the only skill that should run between the
compression event and the next normal player-facing turn. After it
finishes, hand play back to `ttrpg-bootstrap` for the next beat.

## When To Invoke

Invoke `/ttrpg-recover` automatically when **all** of the following
are true:

- The conversation contains a system message whose body starts
  with `## Session Data Update Required`.
- An active session folder exists on disk under
  `ttrpg_runner.base_dir` (default
  `~/.hermes/ttrpg-runner/sessions/<session-id>/`).
- The session folder still contains the data files the engine
  re-pasted (story, timeline, characters, locations, events, and so
  on).

If any of those conditions fail, stay in `ttrpg-bootstrap` and
continue normal play. The recovery skill is not a free-form tool —
it is a one-shot fix-up that runs after a real compression
boundary, and only then.

## What The Engine Already Did

Before this skill runs, the `ttrpg-runner` context engine has
already done three things:

1. **Kept the first system message verbatim.** The GM's core
   instructions are still on top.
2. **Re-pasted the active pack's `SKILL.md` files** into the
   compressed context, in full, in load order. The agent still has
   the operating rules of the active setting without needing a
   fresh file read.
3. **Re-pasted every data file from the active session folder**
   into the compressed context as system messages, in the order
   `story.md`, `timeline.md`, `gm-notes.md`, `secrets.md`, then the
   dossiers under `characters/`, `locations/`, `events/`, and
   `rolls/`. These re-pasted files are the canonical state; the GM
   reads them, not the disk, for the rest of the recovery turn.
4. **Appended a "Session Data Update Required" bridge message** and
   the last `protect_last_n` user / assistant / tool messages
   verbatim so the immediate scene is preserved.

The bridge message is the only marker the recovery skill looks for.
The data files are the source of truth; the transcript is the
input the LLM must compare them against.

## Recovery Procedure

1. **Confirm the bridge marker is present.** The most recent
   system message should open with `## Session Data Update
   Required`. If it does not, leave this skill and return to
   `ttrpg-bootstrap`.

2. **Identify the active session folder.** Read the Session
   Metadata block at the top of the re-pasted `story.md` (or, if
   `story.md` is missing, infer the folder from the path the
   engine reported in the bridge message). Do not list other
   sessions; the active session is the only one this recovery
   touches.

3. **Read the recent transcript.** The bridge message is followed
   by the last `protect_last_n` (default 12) user / assistant /
   tool messages, verbatim. The GM's job is to read the transcript
   tail and decide what the data files need to look like after the
   beats that just happened.

4. **Compare the re-pasted data files against the transcript.**
   The engine has re-pasted `story.md`, `timeline.md`, `gm-notes.md`,
   `secrets.md`, and every dossier under `characters/`,
   `locations/`, `events/`, and `rolls/`. For each one, decide:
   - Is the file still accurate after the recent transcript?
   - Which beats should be added, which should be updated, which
     are now stale and should be removed or annotated?
   - Are there new characters, locations, events, or rolls to
     create (and which dossier `slug` to give them)?

   Only act on facts the transcript proves. Do not invent
   characters, locations, factions, or threads that are not
   visible in the recent transcript or in the re-pasted files. Do
   not copy `secrets.md` content into `story.md`, `timeline.md`,
   or any dossier — secrets are GM-only.

5. **Write the updated data files back to disk.** For each file
   that needs to change, use the host's filesystem tools to
   replace its contents. The re-pasted versions in the working
   context are the *current* contents; the GM is writing the
   *new* contents, with the changes the transcript just
   established. Do not add a parallel `session.json` mirror — the
   data files are the canonical state, the engine does not reload
   a JSON mirror, and a mirror would only drift.

   In particular:
   - `story.md` — keep the Session Metadata block at the top
     intact; append the latest scene recap; do not erase prior
     scenes, only fold them into the running fiction.
   - `timeline.md` — append a one-line entry noting `state
     recovered after compression at <ISO timestamp>` and any
     beats established during the protected tail.
   - `gm-notes.md` — update hidden planning, stakes, and hooks.
   - `secrets.md` — record new GM-only truths. Never print this
     file's contents in player chat.
   - `characters/<slug>.md`, `locations/<slug>.md`,
     `events/<slug>.md` — create new dossiers for new entities
     (using `templates/character.md`, `templates/location.md`,
     `templates/event.md` as the starting shape) and update
     existing ones for facts the transcript just established.
   - `rolls/<stamp>-<label>.json` — record any important dice
     calls from the protected tail so the audit trail is current.

6. **Confirm the writes.** Re-read the data files you just
   changed and confirm they match what you intended. The
   post-compaction turn should continue from the freshly written
   files, not from a stale in-memory guess.

7. **Hand play back to `ttrpg-bootstrap`.** Resume the bootstrap
   skill's Procedure step 8 ("Run the game by editing the active
   session's files"). Compose the next player-facing response
   using the freshly written data files and the recent transcript.
   Do not announce that recovery happened; just continue the
   scene.

## What The Engine Will Not Do

The engine's deliberate scope — the things this skill should never
try to delegate back to the engine — is:

- No regex-based extraction of names, places, or factions. The AI
  owns the choice of "what just happened" by reading the
  transcript.
- No automatic summary of the recent transcript. The running
  fiction in `story.md` is the GM's voice, not the engine's; the
  engine only preserves the verbatim tail.
- No "soft reveal" of `secrets.md` content into other data files.
  If a secret is currently in play, it stays in `secrets.md`; the
  other data files only carry what the table already knows.
- No JSON mirror. There is no `session.json > state_snapshot`.
  The data files are the state.

## Pitfalls

- Do not invoke `/ttrpg-recover` outside of a real compression
  boundary. If the marker is missing, the engine did not
  compress; stay in `ttrpg-bootstrap`.
- Do not invent characters, locations, factions, or threads that
  are not visible in the recent transcript or in the re-pasted
  data files. The point of the AI-owned update is that it is
  faithful to what just happened.
- Do not copy a `secrets.md` entry into `story.md`, `timeline.md`,
  or any dossier. Secrets are GM-only; the shared data files
  must not carry them.
- Do not delete or rewrite the `ttrpg-bootstrap` procedure while
  running recovery. Recovery borrows the bootstrap procedure only
  at the end (step 7) to resume play.
- Do not update the data files from rules docs or pack lore. The
  files describe the current campaign state, not the setting in
  general.
- Do not skip writing the updates back to disk in step 5. The
  next compression event will re-paste whatever is on disk; if
  the data files still carry the pre-compression state, the
  engine will hand the GM stale facts and the LLM will be unable
  to tell the difference.
- Do not introduce a `session.json` mirror. The data files are
  the canonical state.

## Verification

The recovery skill is working correctly when all of the following
are true:

- The bridge marker (`## Session Data Update Required`) is
  present, and the GM re-reads the recent transcript the engine
  kept verbatim.
- The Session Metadata block at the top of `story.md` still
  records the active game, packs, support level, and (when
  relevant) mistborn era. The metadata is preserved across the
  recovery.
- The re-pasted data files have been compared against the recent
  transcript and the changes have been written back to disk.
- No fact appears in `story.md`, `timeline.md`, `gm-notes.md`, or
  any dossier that the recent transcript or the previous
  re-pasted state did not establish.
- `secrets.md` content is still GM-only. Nothing from it was
  moved into a shared file.
- `timeline.md` has a one-line entry recording the recovery
  timestamp.
- The next player-facing turn is composed in the
  `ttrpg-bootstrap` procedure, not in this one.
