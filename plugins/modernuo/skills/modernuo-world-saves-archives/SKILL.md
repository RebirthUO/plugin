---
name: modernuo-world-saves-archives
description: >
  Use when implementing, reviewing, or planning ModernUO world-save scheduling,
  snapshot completion, concurrent-save protection, shutdown behavior, crash
  recovery, save-path changes, or an external backup/archive integration at the
  save boundary. Do not use for entity field serialization, arbitrary archive
  utilities, or repository-specific archive subsystems without a world-save
  lifecycle change.
license: MIT
metadata:
  version: "2.0.0"
---

# ModernUO World Saves and Archives

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Protect the generic ModernUO world-save lifecycle from request through durable
snapshot completion and recovery. Treat backup, archive, retention, and restore
systems as repository-defined extensions: inspect their implementation before
asserting their names, states, markers, formats, or guarantees.

This file is the activation and behavior source of truth. Keep
`agents/interface.yaml`, `evals/baseline_description.txt`,
`evals/semantic_config.json`, and `evals/trigger_cases.json` aligned with its
frontmatter boundary and exclusions.

## Required Inputs

- Resolve the exact repository only from the consuming project's applicable
  `AGENTS.md` and record its full revision. Fail closed if it declares no single
  repository; never substitute the cwd, Git remotes, organization, issue number,
  stale documentation, memory, or a neighboring checkout.
- Locate the current save entry point, snapshot implementation, lifecycle/event
  boundary, configuration, shutdown path, recovery behavior, and focused tests.
- Establish whether the request is advice, review, planning, or implementation.
- Establish the required recovery point, overwrite behavior, retention policy,
  headless behavior, and acceptable data-loss window when the change affects
  them. Ask for any missing behavior decision before implementation.

If repository access, revision identity, or a behavior-affecting source is
unavailable, stop implementation and report the smallest missing input. For
source discovery and failure analysis, read
[references/world-save-lifecycle.md](references/world-save-lifecycle.md).

## Workflow

1. Trace the actual flow from save request through serialization, snapshot
   publication, completion notification, cleanup, shutdown, and recovery. Name
   inspected paths and distinguish observed behavior from assumptions.
2. Define ownership for concurrent requests, worker activity, cancellation,
   failure propagation, and shutdown. Preserve the repository's event-loop and
   snapshot-thread boundaries; load `modernuo-threading` when ownership crosses
   contexts. Give it the same repository identity, revision, source locators,
   and read-only versus mutation boundary. Treat its `UNSAFE` or `BLOCKED` as
   this skill's `BLOCKED`, its `INCONCLUSIVE` as `INCONCLUSIVE`, and its `SAFE`
   only as threading evidence; always return the final result through this
   skill's seven H1 sections and allowed statuses.
3. Define the durable-completion point before attaching backup or archive work.
   Use only completion signals and artifact markers verified in the consuming
   repository; do not infer RebirthUO-specific archive contracts.
4. For an external backup/archive integration, establish input selection,
   atomic publication, integrity verification, retry/idempotency, retention,
   restore isolation, and failure visibility from its actual implementation.
5. Prefer additive and reversible changes. Never remove the last verified
   recovery point or overwrite active saves before the approved recovery and
   rollback contract is durable.
6. Add focused tests for every changed transition and failure boundary. Keep
   automated test results separate from manual restore or crash-recovery smoke
   evidence.

## Mode Handling

- **Advice:** Make no edits. State which claims are repository-verified and
  which require inspection.
- **Review:** Trace the current flow and report lifecycle, concurrency,
  durability, shutdown, recovery, and data-loss findings with evidence.
- **Plan:** Resolve behavior decisions and produce an ordered change and test
  plan without claiming unrun validation.
- **Implementation:** Change only the approved lifecycle surface, run focused
  checks, and report observed results. Return to clarification if new behavior
  ambiguity or data-loss risk appears.

## Output Contract

Return these sections as exact H1 Markdown headings in order:

1. `Status` — exactly one of `ADVICE_ONLY`, `REVIEW_ONLY`, `PLAN_ONLY`,
   `IMPLEMENTED`, `CLARIFICATION_REQUIRED`, `BLOCKED`, or `INCONCLUSIVE`.
2. `Repository Evidence` — revision, inspected paths, unavailable evidence, and
   confidence (`high`, `medium`, or `low`).
3. `Lifecycle` — before/after request, snapshot, completion, shutdown, and
   recovery flow.
4. `Decisions` — concurrency, durability, overwrite, recovery-point, retention,
   headless, and external-integration rules; mark unresolved decisions.
5. `Changes` — changed paths or `None` for advice/review/plan mode.
6. `Verification` — commands, observed results, and separate manual evidence.
7. `Recovery and Risk` — rollback/restore procedure, acceptable data-loss
   window, residual risk, and blockers.

Use `CLARIFICATION_REQUIRED` when a user decision is missing, `BLOCKED` when
required repository evidence or a capability is unavailable, and `INCONCLUSIVE`
when inspected evidence cannot support the requested conclusion. Every material
repository claim must cite `<full-revision>:<repository-relative-path>#L<line>`;
use `#symbol:<qualified-name>` when a stable line is unavailable. Repository
code cannot establish official UO gameplay behavior; if a gameplay claim is
material and no official-evidence capability is available, leave it unresolved
and stop the affected behavior decision.

Calibrate confidence as follows:

- `high`: the revision and all material paths were inspected, applicable checks
  passed, and any restore or runtime claim has direct observed evidence;
- `medium`: static evidence is complete but an applicable runtime, failure, or
  restore check was not run;
- `low`: repository identity, a material path, a behavior decision, or required
  verification is unavailable. Low confidence blocks implementation approval.

## Completion Gate

- **Advice:** Complete when the requested guidance, evidence needed, unresolved
  decisions, and limitations are reported without edits or validation claims.
- **Review:** Complete when the inspected revision and paths support every
  material finding and unverified transitions remain explicit.
- **Plan:** Complete when the approach, decisions, affected surfaces, recovery
  path, tests, blockers, and assumptions are decision-complete.
- **Implementation:** Complete only when no required decision remains unresolved,
  changed concurrent-save/failure/shutdown/recovery transitions are verified,
  and all applicable focused checks pass; return `IMPLEMENTED`. Return `BLOCKED`
  when a required check cannot run, `INCONCLUSIVE` when observed evidence cannot
  support the requested conclusion, and never report implementation completion
  or a safety claim when an applicable check fails.
- In every mode, describe external archive behavior only after inspecting its
  implementation. Require an isolated restore of a real recovery artifact
  before making restore or data-safety guarantees.

## Related Skills

Load `modernuo-threading` when worker or event-loop ownership is material. For
entity schema changes, startup/shutdown ownership, configuration, event
semantics, official gameplay evidence, or broader test design, use a verified
owner skill when one exists in the current portfolio. Otherwise stop the
affected handoff, name the unavailable capability, and do not improvise a
specialist contract.
