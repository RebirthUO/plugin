# Reusable Property PR Scope Correction

Use this when an item-property PR proposes a named artifact/item but the intended deliverable is the reusable property and mechanic first.

## Required discovery

1. Inspect the live PR's base/head, changed files, commits, and linked issue.
2. Search the current base for the property, mechanic, tests, and any prior PR that already merged them.
3. Compare the requested scope with the actual three-dot PR diff, not only the branch's commit history.
4. Check whether a predecessor PR already merged the reusable implementation. If so, do not duplicate or revert it merely to make the follow-up PR appear to contain production code.

## Safe scope correction

When the reusable property/mechanic is already in the base and the concrete artifact is premature:

- Remove the named item class and artifact-specific tests.
- Remove artifact-only tooltip, context-menu, buff, lifecycle, negative-property, serialization, and distribution changes.
- Keep or add tests against an existing compatible item (`Katana`, armor, shield, etc.) that carries the generic property.
- Preserve the generic property/mechanic in the base; do not force a redundant production diff.
- Update the PR title/body to say explicitly that the artifact is deferred and why the resulting net diff may be test-only.
- Do not close the related issue automatically if the deferred artifact is still outstanding.

## Verification

Verify all of the following before pushing:

- The three-dot PR diff contains no named artifact/item or distribution files.
- No stale artifact symbol remains in the committed tree.
- Generic storage, tooltip, mechanic, and central hook tests use an ordinary existing item fixture.
- PR head equals the pushed remote head.
- Report focused tests separately from broad-suite results; GitHub may report no checks for the branch.

This is a scope correction, not permission to change the gameplay formula. Preserve the already-reviewed era/ruleset and mechanic decisions unless the user explicitly changes them.
