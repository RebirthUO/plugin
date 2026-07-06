# ModernUO Plugin Sync Verification

Use this reference when synchronizing `plugins/modernuo/skills/` from the active Hermes profile.

## Selection rule

Select skills from the active profile skills tree by skill name plus frontmatter scope, not by arbitrary body text. A good scope regex covers names/frontmatter that explicitly reference:

- `uo`
- `ultima-online` / `ultima online`
- `modernuo`
- `rebirthuo`
- `runuo`
- `servuo`
- `sphere`
- `pol`
- `uoguide`
- `stratics`

Avoid using full body text as the selector. Body examples and related-skill prose can pull in general skills that are not actually UO/ModernUO/RebirthUO class skills.

## Sync checklist

1. Enumerate every `SKILL.md` under the active profile skills tree, not only `software-development/`.
2. Parse each `SKILL.md` frontmatter enough to get `name`, `description`, and metadata/tags when present.
3. Build the selected set from name/frontmatter scope.
4. Remove plugin skill directories whose directory name is not in the selected set.
5. Copy each selected source skill directory wholesale into `plugins/modernuo/skills/<skill-name>/`, including support files under `references/`, `templates/`, `scripts/`, and any peer support directories already present in Hermes.
6. Bump the plugin version in every plugin manifest required by `AGENTS.md`; update README and CHANGELOG.
7. Verify selected source set equals plugin directory set.
8. Verify every copied file has identical relative path and SHA-256 hash between source and plugin.
9. Verify README/CHANGELOG mention the current sync contract and version.
10. Delete any OS-temp verifier script after it passes.

## Ad-hoc verifier pattern

When no canonical plugin validator exists, create an OS-temp `hermes-verify-modernuo-sync.py` and label it as ad-hoc verification. It should assert:

- all JSON manifests parse;
- plugin versions match the requested version;
- Codex manifest still points `skills` at `./skills/`;
- README contains `Skill Sync Contract` and newly relevant workflow terms;
- CHANGELOG contains the current version/date entry;
- selected source skill names exactly equal plugin skill directory names;
- every selected source skill directory and plugin copy have identical relative file sets and SHA-256 hashes;
- every plugin `SKILL.md` has frontmatter, `name`, `description`, and non-empty body.

If a verifier fails because a copied directory lacks a source support file, resync whole directories rather than hand-copying individual missing files. This preserves the 1:1 contract.
