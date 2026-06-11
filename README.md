# ttrpg-runner

`ttrpg-runner` is a [Hermes](https://hermes-agent.nousresearch.com) **plugin**
for running session-isolated tabletop RPG campaigns across multiple native
setting packs, with a story-aware context engine that survives compression.

As a plugin it ships:

- **Eight bundled skills** loaded via `skill_view("ttrpg-runner:<name>")`,
  each shipped as a first-class skill under
  `plugins/ttrpg_runner/skill/`:
  - `/ttrpg-bootstrap` - sets up a new session, loads the right flavor
    pack, walks the player through character creation, and opens the
    first scene.
  - `/ttrpg-recover` - runs the moment the context engine emits its
    "Session Data Update Required" bridge. The recover skill reads
    the data files the engine re-pasted into the working context,
    compares them against the recent transcript the engine kept
    verbatim, writes the updated files back to disk, and hands
    play back to `/ttrpg-bootstrap`.
  - `/ttrpg-core` - always-on common rules (Discord formatting,
    whitespace discipline, multiplayer turn management, dice-and-roll
    interleaving, roll display format). Loaded before the first scene
    of every session.
  - `/ttrpg-cyberpunk`, `/ttrpg-dnd`, `/ttrpg-mistborn`,
    `/ttrpg-pokemon`, `/ttrpg-expanse` - one skill per native flavor
    pack. `ttrpg-mistborn` ships with an `Era 1` / `Era 2` follow-up
    and pairs its base `SKILL.md` with exactly one era file from
    `resources/`.
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
  - **Repastes the active pack's `SKILL.md` files** in full into the
    compressed context, so the GM never loses the operating rules of the
    current setting across a compression boundary.
  - Emits a "Session Data Update Required" bridge message that points
    the LLM at the re-pasted data files and the recent transcript.
  - Keeps the last `protect_last_n` (default 12) user/assistant/tool
    turns verbatim so the immediate scene is preserved.
  - Tracks which packs are "active" by hooking `post_tool_call` and
    registering any `SKILL.md` the GM reads under one of the plugin's
    `ttrpg-<pack>/` skill directories.
- A `post_tool_call` audit hook (opt-in via `TTRPG_AUDIT_LOG=1`) for
  `ttrpg_roll` calls.
- A `pre_tool_call` safety lock (opt-in via `TTRPG_SAFETY_LOCK=1`) that
  refuses `ttrpg_*` tool calls when set.

## Native Support

`ttrpg-runner` natively supports five flavor packs:

- `cyberpunk` (`/ttrpg-cyberpunk`)
- `dnd` (`/ttrpg-dnd`)
- `mistborn` (`/ttrpg-mistborn`, with an `Era 1` / `Era 2` follow-up
  question for the era file)
- `pokemon` (`/ttrpg-pokemon`)
- `expanse` (`/ttrpg-expanse`)

The bootstrap skill tells players that any TTRPG is still possible even
when it is not one of the five native packs, but those unsupported games
run in a reduced-feature mode with no native pack references.

## Pack Skill Layout

Every flavor pack ships as its own first-class skill, so any future pack
(and any future era / subpack) follows the same pattern. The agent loads
packs through the standard `skill_view` tool:

- `skill_view("ttrpg-<pack>")` reads the base `SKILL.md` of the pack
- `skill_view("ttrpg-<pack>", "resources/<file>.md")` reads a specific
  reference inside the pack

Mistborn is the existing example of the `resources/` pattern. When the
player picks an era, the bootstrap skill loads the base `ttrpg-mistborn`
skill together with the matching era file in the same turn:

- `skill_view("ttrpg-mistborn")` (always-on Mistborn ruleset)
- `skill_view("ttrpg-mistborn", "resources/era_1.md")` for the
  Final Empire era, or
  `skill_view("ttrpg-mistborn", "resources/era_2.md")` for the
  industrial-era Scadrial.

The era choice is recorded in the Session Metadata block at the top of
`story.md`.

## What It Includes

- A `ttrpg-bootstrap` skill that handles session lifecycle, isolation,
  dice usage, and flavor-pack loading rules
- A companion `ttrpg-recover` skill that runs the post-compaction
  recovery pass
- An always-on `ttrpg-core` skill that carries the Discord-native
  markdown rules, whitespace discipline, multiplayer turn management,
  dice-and-roll interleaving, and roll display format the GM follows
  on every turn
- One plugin tool: `ttrpg_roll`
- Markdown templates for dossiers, secrets, and running session state
  (under `plugins/ttrpg_runner/skill/ttrpg-bootstrap/templates/`)
- Five native flavor-pack skills, one per supported setting, each
  living as its own first-class skill under
  `plugins/ttrpg_runner/skill/ttrpg-<pack>/`:
  `ttrpg-core`, `ttrpg-cyberpunk`, `ttrpg-dnd`, `ttrpg-mistborn`,
  `ttrpg-pokemon`, `ttrpg-expanse`
- A `ttrpg-mistborn/resources/` directory with one era file per
  Mistborn era (`era_1.md`, `era_2.md`), loaded by `skill_view` on
  demand after the player picks an era
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
    __init__.py                   # register(ctx) - wires tools, all skills, hooks, engine
    schemas.py                    # tool schemas (what the LLM sees)
    tools.py                      # tool handlers (what runs when called)
    lib.py                        # path constants, dice helpers, pack-skill detector
    context_engine.py             # TTRPGContextEngine (no pattern matching, re-pastes data files)
    skill/
      ttrpg-bootstrap/            # /ttrpg-bootstrap slash command
        SKILL.md
        templates/
          character.md
          event.md
          location.md
          secrets.md
          session-summary.md
      ttrpg-recover/              # /ttrpg-recover slash command
        SKILL.md
      ttrpg-core/                 # /ttrpg-core - always-on common rules
        SKILL.md
      ttrpg-cyberpunk/            # /ttrpg-cyberpunk
        SKILL.md
      ttrpg-dnd/                  # /ttrpg-dnd
        SKILL.md
      ttrpg-pokemon/              # /ttrpg-pokemon
        SKILL.md
      ttrpg-expanse/              # /ttrpg-expanse
        SKILL.md
      ttrpg-mistborn/             # /ttrpg-mistborn
        SKILL.md                  # base pack (always on once era is chosen)
        resources/
          era_1.md                # Era 1: Final Empire, Terris, Skaa, Heroes of the Trilogy
          era_2.md                # Era 2: Industrial Scadrial, Elendel, the Roughs, Nobles
README.md
```

The `ttrpg-core` skill is the always-on asset pack: it carries the
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
to match the convention shown in the Hermes plugin guide. Every skill
name is hyphenated (`ttrpg-bootstrap`, `ttrpg-recover`, `ttrpg-core`,
`ttrpg-mistborn`, ...) so the GM types `/ttrpg-bootstrap` or
`/ttrpg-mistborn` exactly as in the skill files.

## Install In Hermes

Plugins are opt-in. After cloning this repo:

### User install (recommended)

```bash
# Symlink or copy the plugin into your personal plugins dir
ln -s "$(pwd)/plugins/ttrpg_runner" ~/.hermes/plugins/ttrpg-runner

# Also link the bundled skills into the user's skills dir so they
# show up as slash commands. `ctx.register_skill` makes them opt-in
# for `skill_view(...)`, but the slash-command index only reads
# from `~/.hermes/skills/`.
for skill in ttrpg-bootstrap ttrpg-recover ttrpg-core ttrpg-cyberpunk \
             ttrpg-dnd ttrpg-mistborn ttrpg-pokemon ttrpg-expanse; do
  ln -s "$(pwd)/plugins/ttrpg_runner/skill/$skill" "$HOME/.hermes/skills/$skill"
done
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
for skill in ttrpg-bootstrap ttrpg-recover ttrpg-core ttrpg-cyberpunk \
             ttrpg-dnd ttrpg-mistborn ttrpg-pokemon ttrpg-expanse; do
  ln -s "$(pwd)/plugins/ttrpg_runner/skill/$skill" ".hermes/skills/$skill"
done
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
- Across every compression boundary, the active pack's `SKILL.md` is repasted in full
  into the compressed context, just before the most recent N messages
- Active-pack tracking happens automatically: any `SKILL.md` the GM
  reads under one of the plugin's `ttrpg-<pack>/` skill directories
  is registered on the engine via the `post_tool_call` hook, so the
  GM does not need a special tool to mark a pack as active

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
| `/ttrpg-core` | Loaded at the start of every session with `skill_view("ttrpg-core")`. Always-on common rules (Discord formatting, whitespace discipline, multiplayer turn management, dice-and-roll interleaving, roll display format). |
| `/ttrpg-cyberpunk`, `/ttrpg-dnd`, `/ttrpg-pokemon`, `/ttrpg-expanse` | One per native setting. Loaded with `skill_view("ttrpg-<pack>")` when the player names that setting. |
| `/ttrpg-mistborn` | Native Mistborn setting. Loaded with `skill_view("ttrpg-mistborn")`, then paired with `skill_view("ttrpg-mistborn", "resources/era_1.md")` or `resources/era_2.md` once the player picks an era. |

The bootstrap skill tells the GM when to expect a compression boundary
and what the recovery skill does. The recovery skill tells the GM how
to populate the state and which files to update.

## Context Engine

`TTRPGContextEngine` is a `ContextEngine` subclass. Compared with the
built-in `ContextCompressor`:

- Same 50%-of-context-window threshold (configurable)
- Compressed output structure: `[*head, *active_pack_messages, *session_file_messages, data_update_bridge, *tail]`
  - `head` is the first system message, preserved verbatim
  - `active_pack_messages` is one system message per active pack,
    each containing the full `SKILL.md` content
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
- `ttrpg-core` (the always-on common-rules skill shipped alongside
  the bootstrap skill) is the canonical formatting reference for
  the agent, including the whitespace discipline rule
- Dice cards live in fenced code blocks, NPC speech in `>` block quotes,
  scene headers in `###` headings, ambient tags in `-#` subtext
- Each flavor pack's `SKILL.md` has a "Discord Rendering" section with
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
  `skill_view("ttrpg-runner:ttrpg-recover")` both resolve, and
  the matching `/ttrpg-core`, `/ttrpg-cyberpunk`, `/ttrpg-dnd`,
  `/ttrpg-mistborn`, `/ttrpg-pokemon`, `/ttrpg-expanse` slash
  commands show up in the slash-command index
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
  `SKILL.md` content, the re-pasted session data files, and the
  last N messages
- `/ttrpg-recover` reads the re-pasted data files, compares them
  against the recent transcript, writes the updated files back to
  disk, and hands play back to `/ttrpg-bootstrap`
- Player-facing output uses Discord-native markdown
