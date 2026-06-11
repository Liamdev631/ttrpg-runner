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

If a change would otherwise leave a stub, a fallback, or a
"compatibility" alias behind, remove it before merging.
