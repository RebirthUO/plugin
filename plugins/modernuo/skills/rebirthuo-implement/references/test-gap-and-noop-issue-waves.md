# RebirthUO test-gap and no-op implementation waves

Use this reference when `/rebirthuo-implement` is processing Human Review issues whose acceptance criteria are clear but mostly test-focused.

## When a test-only PR is valid

A PR with no gameplay/product code changes is still a valid implementation when the issue explicitly asks for missing regression coverage, such as:

- artifact construction/property tests
- season-table membership tests
- charge/palette tests
- turn-in guard tests
- source-lock tests that freeze existing behavior

The PR must still add real durable coverage. Do not present a comment-only, PR-body-only, TODO-removal-only, or doc-only change as implementation.

## No-op / already-satisfied issues

If investigation shows `origin/live` already satisfies the issue:

1. Verify the relevant files and tests on a clean worktree or detached temp worktree from `origin/live`.
2. Run the focused test filter for the existing coverage.
3. Post an issue comment instead of opening a duplicate PR.
4. Include repo anchors, exact validation commands/results, and a clear `already fulfilled / no-op closure candidate` decision.

Example shape:

```markdown
## Implementierungsprüfung: bereits erfüllt / No-Op-Kandidat

### Kurzfassung
#NNN ist auf `origin/live` bereits durch vorhandene Tests erfüllt. Ich öffne keinen neuen PR, weil ein Kommentar- oder Duplikat-PR keine zusätzliche Implementierung liefern würde.

### Repo-Anker
- `path:line-range` — what is already tested/implemented.

### Verifikation
- `dotnet build ...` — passed.
- `dotnet test ... --filter "FullyQualifiedName~ExistingTests"` — passed.

### Entscheidung
- Kein Code-Change nötig.
- Empfehlung: Issue als erledigten Audit-No-Op/Closure-Kandidaten schließen oder mit dem vorhandenen Testanker verknüpfen.
```

## Multi-issue wave discipline

For adjacent test-gap issues in the same subsystem:

- Keep one issue per branch and PR unless explicitly asked to combine.
- Prefer new focused test files when several open PRs would otherwise edit the same hot test file and create avoidable merge conflicts.
- Still cite the exact source arrays/classes and player/economy side effects in every PR body.
- Verify the GitHub closing reference after PR creation. Sometimes the first `gh pr view` returns `closingIssues: []` before GitHub indexes the body; re-query before changing anything. If a later read shows the closing issue, no fix is needed.

## Broad-suite reporting

If broad `UOContent.Tests` is red on the issue branch, compare against a clean `origin/live` baseline before calling it a regression. Report:

- focused tests and subsystem filter as pass/fail
- root build result
- broad suite attempted, but baseline-blocked, with failure counts and first clusters
- never call focused or subsystem-filter green results “suite green”
