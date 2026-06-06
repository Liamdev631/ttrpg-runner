# cyberpunk-runner

`cyberpunk-runner` is a Hermes skill tap for running session-isolated cyberpunk tabletop campaigns.
It is packaged to work as either:

- a GitHub tap (`hermes skills tap add <owner>/<repo>`)
- a directly copied external skill directory (`skills/cyberpunk-runner`)
- a local skill dropped into `~/.hermes/skills/<category>/cyberpunk-runner/`

> **Model Recommendation:** We strongly recommend running this skill against an **uncensored model**. Cyberpunk is brutal — the fiction leans on graphic violence, hard drugs, sexual content, corpo cruelty, and moral rot, and a heavily filtered model will sand the edges off the genre until the campaign stops feeling like cyberpunk. The skill is designed to play that material straight; pairing it with a sanitized model will produce muted, repetitive, and frankly boring sessions.

## What It Includes

- A Hermes-native `SKILL.md` with progressive-disclosure references and configuration settings
- Standard-library Python tools for setup, database search, scene oracles, dice rolls, and session management
- A local searchable SQLite knowledge base built from bundled public/open cyberpunk data packs
- An optional internet enrichment pass that pulls public genre summaries from Wikipedia
- Persistent per-session story storage with JSON character dossiers plus markdown location, event, roll, and story logs
- Bootstrap guidance for solo play or multi-player Discord sessions, including per-user character mapping and Discord troubleshooting notes
- Session isolation rules so each invocation starts a fresh play archive unless the user explicitly resumes one

## Hermes Features Used

This repository is designed specifically around the Hermes skills system documented at:
<https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>

It uses Hermes-specific features including:

- `SKILL.md` frontmatter with `metadata.hermes.category`, tags, and config settings
- Progressive disclosure via `references/`, `templates/`, `scripts/`, and `assets/`
- Tap-compatible repository layout under `skills/`
- Optional `skills.sh.json` groupings for better Skills Hub categorization
- Slash-command-friendly instructions for `/cyberpunk-runner`

## Repository Layout

```text
skills/
  cyberpunk-runner/
    SKILL.md
    references/
    templates/
    scripts/
    assets/
skills.sh.json
README.md
```

## Install In Hermes

### As a Tap

Publish this repository and then run:

```bash
hermes skills tap add <owner>/<repo>
hermes skills install <owner>/<repo>/cyberpunk-runner
```

### As an External Skill Directory

Copy the `skills/` directory into a shared path such as `~/.agents/skills`, then add it to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

Hermes will discover `cyberpunk-runner` automatically and expose it as `/cyberpunk-runner`.

## Runtime Behavior

The skill is intentionally session-centric:

- A normal `/cyberpunk-runner <prompt>` call creates a new play session folder
- The session stores its own narrative state and dossiers under `~/.hermes/cyberpunk-runner/sessions/<session-id>/`
- In Discord, the skill can map multiple human players to their own character files inside the same session
- The agent is instructed to use only the active session's files unless the player explicitly asks to resume a prior session

Hermes skills do not currently provide a documented way for third-party skills to open a brand new Hermes chat thread programmatically. To stay compliant with Hermes as documented, this skill implements a fresh isolated *play session* on invocation, with dedicated storage and strict context-scoping rules.

## Core Scripts

The skill exposes a small set of one-shot Python helpers. **There is no session controller script** — Hermes reads and writes the active session's files directly with its own file tools, treating the session folder as the API.

- `bootstrap_sources.py` — builds or refreshes the cyberpunk knowledge database
- `db_search.py` — searches the knowledge database for tone, texture, and reference material
- `dice.py` — rolls generic dice and cyberpunk-style action checks
- `cyberpunk_lib.py` — shared utilities used by the scripts above

The session files themselves (under `~/.hermes/cyberpunk-runner/sessions/<session-id>/`) are the interface, and the agent drives them with the Hermes file tools.

## Data Model

Each play session contains:

- `session.json`: metadata, clocks, open threads, Discord user registry, party ties, and current situation
- `story.md`: running fiction log
- `timeline.md`: concise event chronology
- `gm-notes.md`: hidden planning notes and stakes
- `characters/`: one JSON dossier per important character (players and NPCs); schema in `templates/character.json`
- `locations/`: one markdown dossier per important location
- `events/`: one markdown dossier per major event or mission beat
- `rolls/`: optional dice result logs

## Design Notes

- The skill is system-agnostic and genre-first rather than a verbatim implementation of any proprietary tabletop rulebook
- Seed data is original/openly shareable and intended for improvisational play
- Optional public internet enrichment stays additive and never blocks play if the network is unavailable
- All Python tooling uses the standard library only for easy Hermes-side execution
