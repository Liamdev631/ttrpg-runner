# ttrpg-runner

`ttrpg-runner` is a [Hermes](https://hermes-agent.nousresearch.com) **plugin**
for running session-isolated tabletop RPG campaigns across multiple native
setting packs, with a story-aware context engine that survives compression.

As a plugin it ships:

- **Two bundled skills** loaded via `skill_view("ttrpg-runner:ttrpg-bootstrap")`
  and `skill_view("ttrpg-runner:ttrpg-recover")`:
  - `/ttrpg-bootstrap` - sets up a new session, loads the right flavor pack,
    walks the player through
    character creation, and opens the first scene.
  - `/ttrpg-recover` - runs the moment the context engine emits its
    "Session Data Update Required" bridge. The recover skill reads
    the data files the engine re-pasted into the working context,
    compares them against the recent transcript the engine kept
    verbatim, writes the updated files back to disk, and hands
    play back to `/ttrpg-bootstrap`.
- **One Python tool**:
  - `ttrpg_roll` - fair, auditable dice rolling.
  Everything else the agent needs (file reads/writes, listings, etc.) is
  already covered by Hermes' built-in filesystem and skill tools, so the
  plugin does not duplicate them. The post-compaction state is the
  session's data files themselves; the engine re-pastes them on the next
  compression and the recovery skill writes the changes back to disk.
- A custom **context engine** (`ttrpg-runner`) that replaces the built-in
  `ContextCompressor` with a story-aware variant. The engine:
  - Triggers at the same 50%-of-context threshold as the built-in default.
  - **Never pattern-matches** characters, locations, factions, or threads
    out of the transcript. The AI owns that choice via `/ttrpg-recover`.
  - **Re-pastes every data file from the active session folder**
    (`story.md`, `timeline.md`, `gm-notes.md`, `secrets.md`, plus the
    dossiers under `characters/`, `locations/`, `events/`, and `rolls/`)
    into the compressed context as system messages. The data files are
    the canonical state; the LLM reads them and writes the changes back
    to disk.
  - **Repastes the active pack's `PACK.md` files** in full into the
    compressed context, so the GM never loses the operating rules of the
    current setting across a compression boundary.
  - Emits a "Session Data Update Required" bridge message that points
    the LLM at the re-pasted data files and the recent transcript.
  - Keeps the last `protect_last_n` (default 12) user/assistant/tool
    turns verbatim so the immediate scene is preserved.
  - Tracks which packs are "active" by hooking `post_tool_call` and
    registering any `PACK.md` the GM reads under the
    `skill/ttrpg-bootstrap/flavorpacks/` tree.
- A `post_tool_call` audit hook (opt-in via `TTRPG_AUDIT_LOG=1`) for
  `ttrpg_roll` calls.
- A `pre_tool_call` safety lock (opt-in via `TTRPG_SAFETY_LOCK=1`) that
  refuses `ttrpg_*` tool calls when set.

## Native Support

`ttrpg-runner` natively supports five flavor packs:

- `cyberpunk`
- `dnd`
- `mistborn` (single pack with `era1` / `era2` sections selected by `mistborn_era`)
- `pokemon`
- `expanse`

The bootstrap skill tells players that any TTRPG is still possible even
when it is not one of the five native packs, but those unsupported games
run in a reduced-feature mode with no native pack references.

## Mistborn Layout

`mistborn` now loads as a single canonical pack document:

- Load `flavorpacks/mistborn/PACK.md`.
- Ask the table for `Era 1` or `Era 2` and record it in the Session Metadata block at the top of `story.md`.
- Use the matching era section inside the same `PACK.md` instead of loading a separate subpack file.

## What It Includes

- A `ttrpg-bootstrap` skill that handles session lifecycle, isolation,
  dice usage, and flavor-pack loading rules
- A companion `ttrpg-recover` skill that runs the post-compaction
  recovery pass
- An always-on `core` asset pack that carries the Discord-native
  markdown rules, whitespace discipline, multiplayer turn management,
  dice-and-roll interleaving, and roll display format the GM follows
  on every turn
- One plugin tool: `ttrpg_roll`
- Markdown templates for dossiers, secrets, and running session state
- Five native flavor packs under
  `plugins/ttrpg_runner/skill/ttrpg-bootstrap/flavorpacks/`
- A `mistborn` pack consolidated into one canonical `PACK.md`; the
  imported upstream source tree stays in
  `mistborn/references/` for when the GM needs the rules text
- No bundled seed libraries of reusable story ingredients; the system is
  designed to author fresh content instead
- No database bootstrap or searchable pack index; references are markdown
  files in the repo
- Any future externally curated reference material should be stored as
  markdown with source citations at the top
- Persistent per-session story storage with JSON session metadata plus
  markdown location, event, roll, and story logs
- Strict instructions to load only the active pack for the chosen setting

## Repository Layout

```text
plugins/
  ttrpg_runner/
    plugin.yaml                   # plugin manifest (name: ttrpg-runner)
    __init__.py                   # register(ctx) - wires tools, both skills, hooks, engine
    schemas.py                    # tool schemas (what the LLM sees)
    tools.py                      # tool handlers (what runs when called)
    lib.py                        # path constants, dice helpers, pack-pack detector
    context_engine.py             # TTRPGContextEngine (no pattern matching, re-pastes data files)
    skill/
      ttrpg-bootstrap/
        SKILL.md                  # /ttrpg-bootstrap - session bootstrap
        templates/
          character.md
          event.md
          location.md
          secrets.md
          session-summary.md
        flavorpacks/
          core/PACK.md  # always-on common rules and tips (Discord, dice, turn mgmt)
          cyberpunk/PACK.md
          dnd/PACK.md
          pokemon/PACK.md
          expanse/PACK.md
          mistborn/
            PACK.md # canonical Mistborn pack with Era 1 / Era 2 sections
            references/ # imported upstream source tree
              source-manifest.md
              Base Game/...
              Nobles - The Golden Mandate/...
              Skaa - Tin & Ash/...
              Terris - Wrought of Copper/...
      ttrpg-recover/
        SKILL.md # /ttrpg-recover - post-compaction recovery
README.md
```

The `core` flavor pack is the always-on asset pack: it carries the
setting-agnostic operating rules the GM follows every turn (Discord
output formatting, whitespace discipline, multiplayer turn management,
dice-and-roll interleaving, roll display format). The bootstrap skill
loads it before the first scene of any session, and the
`post_tool_call` hook registers it on the context engine so it gets
repasted into the working context after every compression boundary —
which is exactly what the `ttrpg-recover` skill needs to do its job
without re-reading the rule list from disk.

The directory is named `ttrpg_runner` (underscore) so multi-file Python
imports work, but the manifest's `name:` field is `ttrpg-runner` (hyphen)
to match the convention shown in the Hermes plugin guide. The skills are
loaded as `ttrpg-bootstrap` and `ttrpg-recover` (each with a hyphen) so
the GM types `/ttrpg-bootstrap` or `/ttrpg-recover` exactly as in the
skill files.

## Install In Hermes

Plugins are opt-in. After cloning this repo:

### User install (recommended)

```bash
# Symlink or copy the plugin into your personal plugins dir
ln -s "$(pwd)/plugins/ttrpg_runner" ~/.hermes/plugins/ttrpg-runner
```

Then enable it in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - ttrpg-runner

context:
  engine: "ttrpg-runner"   # optional: activate the story-aware compressor
```

Run `hermes plugins` to flip the toggle interactively, or:

```bash
hermes plugins enable ttrpg-runner
```

### Project-local install (dev)

```bash
ln -s "$(pwd)/plugins/ttrpg_runner" .hermes/plugins/ttrpg-runner
export HERMES_ENABLE_PROJECT_PLUGINS=true
hermes
```

### pip install (release)

Once the package is published, install via the plugin entry point:

```bash
pip install ttrpg-runner
hermes plugins enable ttrpg-runner
```

## Runtime Behavior

- A normal `/ttrpg-bootstrap <prompt>` call creates a new play session
  folder unless the player explicitly resumes one
- The session stores its own narrative state and dossiers under
  `~/.hermes/ttrpg-runner/sessions/<session-id>/`
- Native-pack references live in pack-local markdown files, so `cyberpunk`
  guidance never mixes with `mistborn`, `pokemon`, `dnd`, or `expanse`
- Unsupported games still work, but without native pack references
- When the context engine compresses, the GM sees a
  "Session Data Update Required" bridge in the working context; the
  next turn runs the `/ttrpg-recover` skill instead of the bootstrap
  skill, the GM reads the data files the engine re-pasted and the
  recent transcript, writes the updated files back to disk, then
  play resumes via `/ttrpg-bootstrap`
- Across every compression boundary, the active pack's `PACK.md` is repasted in full
  into the compressed context, just before the most recent N messages
- Active-pack tracking happens automatically: any `PACK.md` the GM
  reads under the `flavorpacks/` tree is registered on the engine via
  the `post_tool_call` hook, so the GM does not need a special tool
  to mark a pack as active

## Plugin Tools

| Tool | Purpose |
|---|---|
| `ttrpg_roll` | Generic dice expressions (`2d6+3`, `1d20`, `4d8-2`, `1d10+4+3+0`). Optional `seed` for reproducible rolls. |

For everything else the GM needs in a session - reading and writing
session files, listing sessions, normalizing pack names, recording
rolls - the agent uses Hermes' built-in filesystem and skill tools
directly. The skill folder under `skill/` ships the markdown
references, templates, and flavor packs the agent loads via the
bundled `/ttrpg-bootstrap` and `/ttrpg-recover` skills.

## Bundled Skills

| Skill | When it runs |
|---|---|
| `/ttrpg-bootstrap` | Normal play. New session, character creation, every turn until a compression boundary is detected. |
| `/ttrpg-recover` | Post-compaction only. Triggered by the "Session Data Update Required" bridge. Reads the re-pasted data files and the recent transcript, writes the updated files back to disk, then hands play back to `/ttrpg-bootstrap`. |

The bootstrap skill tells the GM when to expect a compression boundary
and what the recovery skill does. The recovery skill tells the GM how
to populate the state and which files to update.

## Context Engine

`TTRPGContextEngine` is a `ContextEngine` subclass. Compared with the
built-in `ContextCompressor`:

- Same 50%-of-context-window threshold (configurable)
- Compressed output structure: `[*head, *active_pack_packmd_messages, *session_file_messages, data_update_bridge, *tail]`
  - `head` is the first system message, preserved verbatim
  - `active_pack_packmd_messages` is one system message per active pack,
    each containing the full `PACK.md` content
  - `session_file_messages` is one system message per data file in the
    active session folder (`story.md`, `timeline.md`, `gm-notes.md`,
    `secrets.md`, and the dossiers under `characters/`, `locations/`,
    `events/`, and `rolls/`). The full file contents are re-pasted so
    the GM has the entire campaign state after compression.
  - `data_update_bridge` is the "Session Data Update Required" marker
    that tells the LLM to compare the re-pasted data files against the
    recent transcript and write the changes back to disk.
  - `tail` is the last `protect_last_n` (default 12) user/assistant/tool
    messages verbatim
- **No pattern matching.** The engine refuses to extract characters,
  locations, factions, or threads from the transcript. The state is
  the AI's to fill in and persist via `/ttrpg-recover` writing the
  updated data files back to disk.
- The first system message is always preserved
- `on_session_reset()` clears token counters, the focus topic, and the
  active-pack list
- `update_model()` recalculates the threshold when the host model changes
- `get_status()` exposes a self-describing dict for `/plugins` and logging,
  including `active_pack_count` and `active_pack_files`

Activate it with:

```yaml
context:
  engine: "ttrpg-runner"
```

or pick it in `hermes plugins` -> Provider Plugins -> Context Engine.

## Discord Output

- All player-facing output uses Discord-native markdown so messages render
  cleanly in chat
- `flavorpacks/core/PACK.md` (the always-on common-rules asset pack
  inside the bootstrap skill) is the canonical formatting reference for
  the agent, including the whitespace discipline rule
- Dice cards live in fenced code blocks, NPC speech in `>` block quotes,
  scene headers in `###` headings, ambient tags in `-#` subtext
- Each flavor pack `PACK.md` has a "Discord Rendering" section with
  setting-specific guidance

The session files themselves (under
`~/.hermes/ttrpg-runner/sessions/<session-id>/`) are the interface, and
the agent drives them with Hermes file tools.

## Configuration

Both keys are optional; defaults are shown.

| Key | Default | Description |
|---|---|---|
| `ttrpg_runner.base_dir` | `~/.hermes/ttrpg-runner` | Root directory for saved sessions |
| `ttrpg_runner.default_tone` | `adventurous` | Default session tone when the player does not specify one |

## Verification

The plugin is working correctly when all of the following are true:

- `hermes plugins list` shows `ttrpg-runner` as enabled
- `/plugins` shows `ttrpg-runner` with 1 tool, 2 hooks, and a context
  engine
- `skill_view("ttrpg-runner:ttrpg-bootstrap")` and
  `skill_view("ttrpg-runner:ttrpg-recover")` both resolve
- The agent can call `ttrpg_roll` for any dice expression
- A `/ttrpg-bootstrap` invocation loads the bootstrap skill and walks
  the player through setup
- The agent tells the player that `cyberpunk`, `dnd`, `mistborn`,
  `pokemon`, and `expanse` are natively supported
- For `mistborn`, the agent asks for `Era 1` or `Era 2`, records it in
  the Session Metadata block at the top of `story.md`, and loads the
  matching era file inside `mistborn/resources/`
- Unsupported TTRPGs are possible with reduced features
- Only the chosen native pack is loaded for a native game
- The active session folder contains `story.md`, `timeline.md`,
  `gm-notes.md`, `secrets.md`, and the `characters/`, `locations/`,
  `events/`, and `rolls/` directories
- The Session Metadata block at the top of `story.md` records the
  selected game, flavor packs, support level, and (when relevant)
  mistborn era
- After a compression boundary, the working context contains the
  "Session Data Update Required" bridge, the active pack's
  `PACK.md` content, the re-pasted session data files, and the
  last N messages
- `/ttrpg-recover` reads the re-pasted data files, compares them
  against the recent transcript, writes the updated files back to
  disk, and hands play back to `/ttrpg-bootstrap`
- Player-facing output uses Discord-native markdown
