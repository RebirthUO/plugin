---
name: modernuo-verification-guard
description: Use when an explicit post-edit guard requires a fresh, auditable ModernUO verification bundle beyond ordinary test output. Re-run scoped evidence from the exact worktree and prove temporary-file cleanup. Do not activate for normal test requests or treat ad-hoc evidence as CI.
version: 2.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    tags: [modernuo, verification, guard, evidence]
    related_skills:
      - modernuo-test-workflow
    skill_group: modernuo
    skill_subgroup: gate
    workflow_phase: implement
    workflow_tier: support
---

# ModernUO Verification Guard

## Boundary

Produce a new evidence bundle when an explicit guard rejects, cannot detect, or
requires evidence newer than prior logs. This does not authorize code, git, or
GitHub mutations.

## Workflow

1. Confirm the guard requirement, listed paths, exact worktree/root/branch/HEAD,
   authorization, and whether the change is working-tree, committed, pushed, or
   merged.
2. Create a verifier through the operating system's safe temp-file API. Use one
   runtime and path convention end to end; do not hard-code workstation paths.
3. Print evidence kind, repository root, branch/HEAD, and status before/after.
   Assert the actual root and every scoped path.
4. Check the correct delta: working-tree paths for uncommitted work or the exact
   commit/range and changed paths for committed work.
5. Compare local, verified remote, and PR heads only when that external state is
   authorized and relevant.
6. Run the owning build and focused behavior tests through
   `modernuo-test-workflow`; add broader tests only in proportion to risk.
7. Capture exit codes, remove verifier/output/scratch files even on failure, and
   prove cleanup. Report only the latest run.

## Guardrails

- Creating a verifier is not evidence; execute it.
- An empty working-tree diff does not prove a committed change.
- Do not kill a user's running process or alter git configuration to obtain a
  pass. Use isolated output when supported.
- A focused/ad-hoc pass is not broad-suite or CI evidence.
- Verify external scratch paths explicitly; repository status cannot see them.

## Output contract

Return evidence kind, verifier/removal state, worktree/HEAD, status before/after,
diff scope, relevant head equality, build/test commands and denominators,
required data, scratch cleanup, broad/CI state, and blockers.

## Verification

- The verifier ran against the intended root, revision, and paths.
- Required build/tests ran after the final edit.
- Cleanup left no verifier, output, or scratch residue.
- Scope labels match the evidence that actually ran.
