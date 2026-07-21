# Repository Instructions

- For every plugin change, automatically bump the plugin version in the
  corresponding `.codex-plugin/plugin.json` before finishing the work. Use
  semantic versioning: patch for fixes and documentation-only updates, minor
  for new skills or behavior, and major for breaking changes.
- Every plugin change must include a `README.md` that documents the plugin's
  purpose, contents, and usage.
- Every plugin change must include a `CHANGELOG.md` entry describing the
  notable changes for the updated version.
- Treat `plugins/modernuo/skills/` in this checkout as the reviewed source.
  Never hand-edit the installed Codex plugin cache.
- Keep every member skill valid against the Agent Skills format: lean
  `SKILL.md`, conditional references, aligned
  `agents/interface.yaml`, `manifest.json`, and trigger smoke evals.
- Maintain every skill, adapter metadata file, and evaluation contract in
  English. Make implicit triggering depend on user intent in any language;
  include representative multilingual positive fixtures for new skills without
  requiring a portfolio-wide fixture rewrite in every individual change.
- Do not add or maintain Hermes-specific metadata. Continue to maintain version
  metadata and bump the plugin version as required above.
- After skill edits, run the current runtime validator from the repository root:

  ```powershell
  python C:\path\to\skill-creator\scripts\quick_validate.py plugins\modernuo\skills\<skill-name>
  ```

- Also parse changed JSON/YAML metadata, inspect trigger fixtures and referenced
  resources, and run `git diff --check`. Do not substitute the retired
  preparation, catalog, Yao, or Hermes sequence for these skill-local gates.
- GitHub-mutating skills must fail closed when the exact repository cannot be
  resolved from the consuming project's applicable `AGENTS.md`. Do not infer or
  substitute a repository from the cwd, git remotes, organization name, stale
  documentation, issue number, or a neighboring project.
- Official OSI/EA/Broadsword material is the only gameplay authority.
  Community, client, emulator, and repository evidence must remain separately
  labeled and may not fill an unresolved official claim.
