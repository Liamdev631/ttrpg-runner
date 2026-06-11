# ttrpg-runner workflow

A short tour of how the `ttrpg-runner` Hermes plugin runs an isolated
TTRPG session that survives context compression. For full operating
instructions, see the per-skill manuals:

- [ttrpg-bootstrap/SKILL.md](../plugins/ttrpg_runner/skill/ttrpg-bootstrap/SKILL.md)
- [ttrpg-recover/SKILL.md](../plugins/ttrpg_runner/skill/ttrpg-recover/SKILL.md)

## Components

The plugin lives at `plugins/ttrpg_runner/`:

- **`plugin.yaml`** — manifest: one tool (`ttrpg_roll`), two
  skills (`ttrpg-bootstrap`, `ttrpg-recover`), two hooks, and a
  custom context engine.
- **`__init__.py`** — `register(ctx)` wires tools, skills, the
  engine, and the hooks.
- **`lib.py`** — path constants, the dice parser, the flavor-pack
  and session-directory detectors.
- **`schemas.py` / `tools.py`** — JSON schema and handler for
  the one tool.
- **`context_engine.py`** — `TTRPGContextEngine`, a `ContextEngine`
  subclass that re-pastes session data files after compression.
- **`skill/ttrpg-bootstrap/`** — bootstrap skill, plus
   `templates/`, and `flavorpacks/`
  (`core` always-on, plus the five native settings
  `cyberpunk`, `dnd`, `pokemon`, `expanse`, `mistborn`).
- **`skill/ttrpg-recover/`** — the post-compaction recovery
  skill.

Every play session is a fresh directory under `ttrpg_runner.base_dir`
(default `~/.hermes/ttrpg-runner/sessions/<session-id>/`):

```text
<session-id>/
  story.md            # running fiction + Session Metadata header
  timeline.md         # beat-by-beat chronology
  gm-notes.md         # hidden planning
  secrets.md          # GM-only truths (seeded from template)
  characters/         # markdown dossiers
  locations/
  events/
  rolls/              # JSON dice audit trail
```

There is no `session.json`. The Session Metadata block at the top
of `story.md` records the active game, flavor packs, support
level, and (when relevant) mistborn era. The other data files are
the canonical state; the engine re-pastes them after every
compression.

## The two skills

**`/ttrpg-bootstrap`** — session setup and runtime manual. The
GM picks a setting (one of the five native packs, a native
crossover, or reduced-feature generic mode), writes the Session
Metadata header in `story.md`, reads the always-on
`flavorpacks/core/PACK.md` asset pack (Discord formatting,
whitespace discipline, multiplayer turn management, dice-and-roll
interleaving, roll display format), and reads the active pack's
`PACK.md` (and the matching `mistborn/resources/mistborn_era_{1,2}.md`
for mistborn). Each turn: skim `story.md` and `timeline.md`, use
`ttrpg_roll` for risky actions, format Discord-native output, write
state changes back to the data files.

**`/ttrpg-recover`** — the post-compaction fix-up. Runs once
after the engine emits a `## Session Data Update Required` bridge
message. Reads the recent transcript the engine kept verbatim,
compares it against the data files the engine re-pasted, writes
the changes back to disk, and hands play back to
`/ttrpg-bootstrap`.

## The tool

- **`ttrpg_roll(expression, seed?)`** — fair dice. `1d20+5`,
  `3d6`, etc. Optional seed for reproducible audit. The plugin
  only ships this one tool; everything else the GM needs is
  covered by Hermes' built-in filesystem and skill tools.

## The context engine

`TTRPGContextEngine` is opt-in via `context.engine: "ttrpg-runner"`
in `config.yaml`. Threshold defaults to 50% of the context window.

**Active pack tracking.** The engine never pattern-matches the
transcript. The `post_tool_call` hook watches every file read;
any `PACK.md` under `skill/ttrpg-bootstrap/flavorpacks/` is
registered as an active pack, and any path inside a
`sessions/<id>/` directory registers the active session folder.

**`compress()`** rebuilds the message list in four steps:

1. Keep the first system message verbatim.
2. Repaste every tracked `PACK.md` from disk, in load order, as
   system messages (`## Active Flavor Pack: <label>`).
3. Re-paste every data file from the active session folder
   (`story.md`, `timeline.md`, `gm-notes.md`, `secrets.md`, plus
   the dossiers under `characters/`, `locations/`, `events/`, and
   `rolls/`) as system messages (`## Session File: <rel>`).
4. Emit a "Session Data Update Required" bridge system message
   that points the LLM at the re-pasted files and the recent
   transcript, and append the last `protect_last_n` (default 12)
   user / assistant / tool messages verbatim.

The data files are the canonical state. The engine never
summarises them, never pattern-matches them, never edits them —
it just routes them back into the working context so the LLM has
the full campaign state to work with after compression.

## The hooks

- **`pre_tool_call`** — when `TTRPG_SAFETY_LOCK=1`, refuses any
  `ttrpg_*` tool call. Otherwise a no-op.
- **`post_tool_call`** — three jobs:
  1. Audit-log `ttrpg_*` results when `TTRPG_AUDIT_LOG=1`.
  2. Register any `flavorpacks/<pack>/PACK.md` read as an active
     pack on the engine.
  3. Register any path inside a `sessions/<id>/` directory as
     the active session folder on the engine.

## End-to-end

**Bootstrap.** Player runs `/ttrpg-bootstrap`. Skill asks for
solo/multiplayer, then the setting (and Era 1 or 2 for mistborn).
reates the session folder, seeds the data files, writes the
Session Metadata block in `story.md`. Reads
`flavorpacks/core/PACK.md` (the always-on common-rules asset pack)
and the active pack `PACK.md` (and mistborn era file). The
`post_tool_call` hook registers both packs on the engine. Player
runs through character creation and authorizes play. Skill opens
the first scene.

**Run a turn.** Skim `story.md` (metadata header + current scene)
and `timeline.md`. For risky actions, call `ttrpg_roll`. Consult
the active pack references when needed. Compose the response in
Discord-native markdown. Write state changes back to the relevant
data file. End with `> **Up next: <player name>**` for
multiplayer rotation.

**Compression boundary.** Token usage crosses the threshold.
`engine.compress()` rebuilds the message list (head, pack repaste,
session files, bridge, tail). The bridge message lands as the
most recent system message. The next GM turn sees it and routes
through `/ttrpg-recover`.

**Recovery.** `/ttrpg-recover` confirms the `## Session Data
Update Required` bridge marker. The engine has already re-pasted
the data files into the working context, so the GM reads them and
the recent transcript the engine kept verbatim. For each data
file, the GM decides whether the new transcript requires a change
and writes the new contents back to disk. The metadata block at
the top of `story.md` is preserved across the recovery. A
one-line entry is appended to `timeline.md` noting the recovery
timestamp. Play hands back to `/ttrpg-bootstrap` at the "Run the
game" step.

## Configuration

Plugin config under `metadata.hermes.config`:
`ttrpg_runner.base_dir` (default `~/.hermes/ttrpg-runner`) and
`ttrpg_runner.default_tone` (default `adventurous`).

Context engine reads `context.context_length` (default 200,000) and
`context.threshold_ratio` (default 0.5); `compression.*` keys are
also honoured, with `context.*` taking precedence.

Env-var trip-wires: `TTRPG_AUDIT_LOG=1` enables the audit log;
`TTRPG_SAFETY_LOCK=1` blocks all `ttrpg_*` tool calls.

## Invariants

- The data files inside the active session folder are the only
  authoritative memory. There is no `session.json` mirror.
- The engine never pattern-matches characters, locations,
  factions, or threads. The AI owns that choice through
  `/ttrpg-recover`, which reads the recent transcript and updates
  the data files.
- The protected tail is preserved verbatim; the engine never
  summarises.
- `secrets.md` is never re-pasted into player chat; nothing
  inside it is moved into a shared file by the recovery skill.
- Single setting per session unless the player explicitly asks
  for a native crossover.
- Character sheets are markdown; nothing in JSON.
- A pack's own references are only valid while that pack is
  active — including in a crossover.

## Future direction

The `load_ttrpg_context_files(session_id)` tool is currently a
read-only convenience over the list the `post_tool_call` hook
maintains; the bootstrap skill never has to write to it by hand.
When (or if) a real implementation lands, it will simply expose
the engine's existing auto-built list — there is no plan for a
manual `register_*` counterpart, since the hook already covers
that ground.
