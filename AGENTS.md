# ttrpg-runner agent rules

## No legacy or stub systems

**Always remove legacy and stub systems immediately. Backwards
compatibility is not a goal of this project.**

When working on `ttrpg-runner`:

- **Delete, do not preserve.** A legacy directory, module, function,
  class, configuration key, or documentation section is removed in
  the same change that supersedes it. There is no deprecation
  window, no fallback path, and no "for archival" twin.
- **No stub code.** Do not add placeholder classes, mock imports,
  defensive fallbacks, or `try/except` shims around host APIs to
  keep the module loadable in isolation. The plugin depends on
  Hermes at runtime; type-check convenience classes, ABC
  re-definitions, and "minimal stub mirroring" helpers are out.
- **Strip every reference.** A legacy or stub feature must not
  appear in `README.md`, `SKILL.md`, repository-layout diagrams,
  comments, or docstrings once it is gone. Search the whole
  codebase for the old name and remove every mention, including
  narrative references such as "the old `references/` directory" or
  "the legacy `mistborn/era1/` subfolders."
- **Single source of truth.** Always-on rules live in exactly one
  place (e.g. `flavorpacks/core/PACK.md`). Do not maintain a
  secondary copy under a different path; if the secondary copy is
  abandoned, delete it.
- **In-fiction word "legacy" is allowed.** Flavor text inside a
  pack's `PACK.md` or era file (e.g. "house legacy", "legacy of the
  old world") is TTRPG content, not legacy code, and stays.

If a change would otherwise leave a stub, a fallback, or a
"compatibility" alias behind, remove it before merging.
