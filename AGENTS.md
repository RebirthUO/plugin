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
- Keep every member skill valid against the Agent Skills format and the Yao
  production boundary: lean `SKILL.md`, conditional references, aligned
  `agents/interface.yaml`, `manifest.json`, and trigger smoke evals.
- After skill edits, run this maintenance sequence from the repository root:

  ```powershell
  python scripts/prepare-yao-portfolio.py
  python scripts/generate-skill-catalog.py
  python scripts/verify-skill-portfolio.py
  python scripts/run-yao-portfolio.py --yao-root <path-to-yao-meta-skill> --extended
  ```

- Synchronize to a Hermes profile only after the gates pass. Preview the exact
  target first:

  ```powershell
  python scripts/sync-plugin-to-hermes.py --hermes-root <profile-skills> --dry-run
  ```
- GitHub-mutating skills must fail closed when the exact repository cannot be
  resolved from the consuming project's applicable `AGENTS.md`. Do not infer or
  substitute a repository from the cwd, git remotes, organization name, stale
  documentation, issue number, or a neighboring project.
- Official OSI/EA/Broadsword material is the only gameplay authority.
  Community, client, emulator, and repository evidence must remain separately
  labeled and may not fill an unresolved official claim.
