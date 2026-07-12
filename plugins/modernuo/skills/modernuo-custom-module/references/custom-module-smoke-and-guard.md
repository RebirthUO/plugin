# Custom Module Smoke Tests and Post-Commit Guard

Use this when a ModernUO-based custom content module change requires fresh
post-edit verification evidence on its changed paths.

## Minimal no-op module marker

For an infrastructure-only module PR that must not change gameplay, add a tiny marker type rather than placeholder content:

```csharp
using System.Reflection;

namespace Server;

public static class RUOContentLayer
{
    public const string AssemblyName = "RUOContent";

    public static Assembly BaseContentAssembly => typeof(SkillsInfo).Assembly;
}
```

This proves the custom layer assembly exists and can reference `UOContent` without introducing items, mobiles, commands, serialization, timers, or gameplay side effects.

## Smoke-test coverage

A focused module smoke suite should validate the real runtime boundary, not only that the test project compiles:

- `Distribution/Data/assemblies.json` exactly lists base content before custom content, e.g. `["UOContent.dll", "RUOContent.dll"]`.
- `AssemblyHandler.LoadAssemblies(["UOContent.dll", "RUOContent.dll"])` loads assemblies in that order.
- The marker type's assembly name is the custom module name.
- The marker's base-content assembly is `UOContent`.

Keep the fixture lightweight: set `Core.ApplicationAssembly`, load mocked `ServerConfiguration`, add `Core.BaseDirectory` to `ServerConfiguration.AssemblyDirectories` if missing, then call `AssemblyHandler.LoadAssemblies(...)`. Do not boot the world or client-data-dependent UOContent fixture for a pure assembly-load smoke test.

## Post-commit Hermes guard script shape

When the branch is already committed and pushed, validate the committed delta rather than an empty worktree diff. Create a temporary script through the OS temp directory (for example, `tempfile.mkstemp(prefix="hermes-verify-", suffix=".sh")`), run it, then remove it. If Hermes repeats the guard after a successful run, treat it as a request for a **fresh evidence bundle**: create a new `hermes-verify-*` script and rerun the committed-path checks with a visible timestamp.

The script should print:

- UTC run timestamp (especially for repeated guard prompts)
- repo path, branch, local head
- remote branch head, and assert it equals local head
- PR head, and assert it equals local head when a PR exists
- `git status --short --branch --untracked-files=all`
- `git diff --check HEAD~1..HEAD -- <changed paths>`
- `git diff --stat HEAD~1..HEAD -- <changed paths>`
- PR check summary (`gh pr view ... --json statusCheckRollup`) when the PR is already open

Then run the focused verification for the module:

```bash
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
for f in Distribution/Assemblies/RUOContent.dll Distribution/Assemblies/RUOContent.deps.json; do
    test -f "$f"
    wc -c < "$f"
done
python - <<'PY'
import json
from pathlib import Path
actual = json.loads(Path('Distribution/Data/assemblies.json').read_text(encoding='utf-8'))
assert actual == ['UOContent.dll', 'RUOContent.dll'], actual
PY
dotnet test Projects/RUOContent.Tests/RUOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity minimal \
  --logger "console;verbosity=minimal"
```

Report this explicitly as **ad-hoc/focused verification**, not broad suite-green. If a broad solution test was attempted and failed because unrelated UO client data or culture setup is missing, keep that separate from the focused custom-module verification.
