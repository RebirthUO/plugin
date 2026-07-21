---
name: modernuo-codebase
description: Use when locating project ownership, repository instructions, source, configuration, data, build, or test anchors in a confirmed ModernUO-based checkout. Resolve the repository from project instructions and map the local layout before planning work. Do not use as official UO mechanics evidence or as authorization for issue, code, git, or GitHub mutation.
license: MIT
metadata:
  version: "1.1.0"
---

# ModernUO Codebase

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Map a confirmed ModernUO-based checkout to its owning projects, instructions,
source, data, and validation surfaces. This is read-only navigation guidance.

## Workflow

1. Confirm a ModernUO-based checkout with either a solution/project graph that names ModernUO, or two independent local anchors: a project/package/SDK pin and a ModernUO API source. Do not accept a lone source marker. If the checkout, root, instructions, or project graph cannot be confirmed, return `BLOCKED` with the smallest required path or artifact; do not infer it from a workstation path or remote.
2. Resolve the repository root and read every applicable `AGENTS.md` plus
   repository README, SDK/version pins, build props, solution files, and local
   developer documentation. Do not assume a workstation path or solution name.
3. When GitHub identity matters, use the exact repository declared by project
   instructions and verify it. Never infer a target repository from remotes or
   organization names.
4. Inventory projects and ownership from the actual solution/project graph.
   Distinguish engine, host, gameplay/content, tooling, tests, distribution
   output, and custom modules without relying on namespaces alone.
5. Search by API shape and live consumers as well as names. Trace
   registration/reachability, configuration/data, persistence, lifecycle,
   client presentation, and tests before calling a surface implemented.
6. Load a narrow subsystem skill only when an available skill's exact trigger applies. Otherwise inspect one current local precedent and keep the result within read-only navigation scope.
7. Return a file-level map with ownership, `path:line` anchors, risks, assumptions, confidence, unavailable evidence, and the
   narrowest honest build/test commands.

## Guardrails

- Local code proves repository behavior, not official UO mechanics or history.
- Do not hard-code project paths, branch names, solution names, or repository
  identities into reusable guidance.
- Treat generated/runtime distribution output according to repository
  instructions; do not edit generated files unless their generator owns the
  requested change.
- Trace thread, serialization, lifecycle, packet, gump, cliloc, and property
  contracts through their specialist skills.

## Output contract

Return these sections in order: `Outcome` (`MAPPED` or `BLOCKED`); `Read-Only Status` (`No files changed`); `Repository Evidence` (commit, instructions, and confirmation anchors); `Project Map`; `Reachability Anchors`; `Proposed Files and Narrow Skills`; `Validation` (command, result, or unavailable reason); and `Assumptions, Confidence, and Risks`. A `BLOCKED` result contains `Missing Evidence`, `Impact`, and `Smallest Resume Input`. Remain read-only.

## Verification

- Planned files belong to the reported projects at the reported revision.
- Commands target the owning build/test surface and label focused scope.
- Repository behavior is not presented as official UO evidence.
- Every material mapping claim has a local `path:line` anchor or is labeled unresolved.
- The output records every required section, read-only status, and unavailable command before delivery.
- Use `high` confidence only with complete confirmation anchors and completed relevant commands; use `medium` with verified partial evidence and named unavailable checks; use `low` only for `BLOCKED` or unresolved anchors.
