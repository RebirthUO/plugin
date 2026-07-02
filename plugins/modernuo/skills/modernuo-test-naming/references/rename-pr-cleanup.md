# Rename-Only Test Cleanup PR Workflow

Use this reference when normalizing RebirthUO/ModernUO test names after generated branches or AI-assisted work introduced noisy prefixes.

## Scope discipline

- Make rename-only changes: file names, class names, test method names, and direct references only.
- Do not change assertions, fixtures, setup, production code, or test behavior while cleaning names.
- Keep domain names when they are the tested object, e.g. `MLQuest*`, `MLPeerlessArtifactsTests`, source-reference hubs, or real helper/family names such as `MLSetArmor`.
- Remove era/batch labels when they are only context: `MondainsLegacy...`, `SamuraiEmpire...`, `Coverage`, `Smoke`, `Issue*`, `Publish*`, `Codex`, etc.

## Clean worktree pattern

1. Create the cleanup branch from `origin/live` in a separate worktree so existing user changes in the main working copy are not touched.
2. On Windows/MSYS worktrees, file mode changes can appear as false dirty state (`100755 => 100644`). Use `git -c core.filemode=false status/diff/add` for inspection and staging rather than committing mode-only noise.
3. Stage only the test project paths involved, for example:

```bash
git -c core.filemode=false add -A Projects/UOContent.Tests
```

4. Before committing, verify that no non-test files are staged:

```bash
git -c core.filemode=false diff --cached --name-only | grep -v '^Projects/UOContent.Tests/' || true
```

## Prefix verification script

After edits, scan file stems, class names, and xUnit methods. Allow known domain cases such as source-reference tests and `MLSetArmorTests`.

```bash
python - <<'PY'
import re
from pathlib import Path
root = Path('.').resolve()
tests = root / 'Projects' / 'UOContent.Tests'
hard = re.compile(r'^(Publish\d+|Pub\d+|P\d+|Issue\d+|Task\d+|Codex|Generated|Regression|AI)')
generic = re.compile(r'(Coverage|Smoke)')
method_prefix = re.compile(
    r'public\s+(?:static\s+)?(?:async\s+)?(?:void|Task|ValueTask)\s+'
    r'((?:MondainsLegacy|SamuraiEmpire|Publish\d+|Pub\d+|P\d+|Issue\d+|Task\d+|Codex|Generated|Regression|AI)[A-Za-z0-9_]*)\s*\('
)
remaining = []
for p in sorted(tests.rglob('*.cs')):
    rel = p.relative_to(root).as_posix()
    if hard.match(p.stem) or generic.search(p.stem):
        remaining.append(('file', rel, p.stem))
    text = p.read_text(encoding='utf-8-sig')
    for m in re.finditer(r'\bclass\s+([A-Za-z0-9_]+)', text):
        name = m.group(1)
        if hard.match(name) or generic.search(name):
            remaining.append(('class', rel, name))
    for m in method_prefix.finditer(text):
        name = m.group(1)
        if 'SourceReferenceTests.cs' in rel or rel.endswith('MLSetArmorTests.cs'):
            continue
        remaining.append(('method', rel, name))
print(len(remaining))
for row in remaining:
    print(row)
PY
```

Expected for a completed cleanup: `0` actionable findings.

## Validation

- Run `git -c core.filemode=false diff --cached --check` before commit.
- Run `dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1`.
- Run targeted renamed-class test filters in batches. Prefer targeted filters over relying only on a full suite when the repository has known static-state/order-sensitive tests.
- If an exploratory full `UOContent.Tests` run fails in unrelated order-sensitive static state after many passes, report it explicitly as exploratory and do not mix behavior fixes into the rename-only PR.

## PR completion

If the user asked for the PR to change or merge, local validation is not completion. Commit, push, create the PR, merge to the requested base, delete the branch, and verify the PR state and base head.
