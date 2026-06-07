# ttrpg-runner

`ttrpg-runner` is a Hermes skill tap for running session-isolated tabletop RPG campaigns across multiple native setting packs.

It is packaged to work as either:

- a GitHub tap (`hermes skills tap add <owner>/<repo>`)
- a directly copied external skill directory (`skills/ttrpg-runner`)
- a local skill dropped into `~/.hermes/skills/<category>/ttrpg-runner/`

## Native Support

`ttrpg-runner` natively supports four flavor packs:

- `cyberpunk`
- `dnd`
- `pokemon`
- `expanse`

The skill should tell players that any TTRPG is still possible even when it is not one of the four native packs, but those unsupported games run in a reduced-feature mode with no native pack references.

## What It Includes

- A shared `SKILL.md` that handles session lifecycle, isolation, dice usage, and flavor-pack loading rules
- A Discord-native markdown reference so player-facing output reads cleanly in chat
- Shared Python helpers for fair dice rolling and lightweight session utilities
- Shared templates for dossiers and running session state
- Four native flavor packs under `skills/ttrpg-runner/flavorpacks/`
- No bundled seed libraries of reusable story ingredients; the system is designed to author fresh content instead
- No database bootstrap or searchable pack index; references are markdown files in the repo
- Any future externally curated reference material should be stored as markdown with source citations at the top
- Persistent per-session story storage with JSON character dossiers plus markdown location, event, roll, and story logs
- Strict instructions to load only the active pack for the chosen setting

## Repository Layout

```text
skills/
  ttrpg-runner/
    SKILL.md
    references/
      session-data-model.md
      discord-formatting.md
    templates/
    scripts/
    flavorpacks/
      cyberpunk/
      dnd/
      pokemon/
      expanse/
skills.sh.json
README.md
```

## Install In Hermes

### As a Tap

Publish this repository and then run:

```bash
hermes skills tap add <owner>/<repo>
hermes skills install <owner>/<repo>/ttrpg-runner
```

### As an External Skill Directory

Copy the `skills/` directory into a shared path such as `~/.agents/skills`, then add it to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

Hermes will discover `ttrpg-runner` automatically and expose it as `/ttrpg-runner`.

## Runtime Behavior

- A normal `/ttrpg-runner <prompt>` call creates a new play session folder unless the player explicitly resumes one
- The session stores its own narrative state and dossiers under `~/.hermes/ttrpg-runner/sessions/<session-id>/`
- Native-pack references live in pack-local markdown files, so `cyberpunk` guidance never mixes with `pokemon`, `dnd`, or `expanse`
- Unsupported games still work, but without native pack references

## Core Scripts

- `dice.py` - rolls generic dice and fast `1d10 + stat + skill + modifier` checks using Python's uniform `randint`
- `ttrpg_lib.py` - shared filesystem and session helpers used by the scripts above

## Discord Output

- All player-facing output uses Discord-native markdown so messages render cleanly in chat
- `references/discord-formatting.md` is the canonical formatting reference for the agent
- Dice cards live in fenced code blocks, NPC speech in `>` block quotes, scene headers in `###` headings, ambient tags in `-#` subtext
- Each flavor pack `PACK.md` has a "Discord Rendering" section with setting-specific guidance

The session files themselves (under `~/.hermes/ttrpg-runner/sessions/<session-id>/`) are the interface, and the agent drives them with Hermes file tools.
