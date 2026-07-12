---
name: modernuo-codebase
description: Use when locating project ownership, repository instructions, source, configuration, data, build, or test anchors in a confirmed ModernUO-based checkout. Resolve the repository from project instructions and map the local layout before planning work. Do not use as official UO mechanics evidence or as authorization for issue, code, git, or GitHub mutation.
version: 1.0.0
author: RebirthUO
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, codebase, navigation, dotnet]
    related_skills:
      - modernuo-code-audit
      - modernuo-test-workflow
---

# ModernUO Codebase

## Boundary

Map a confirmed ModernUO-based checkout to its owning projects, instructions,
source, data, and validation surfaces. This is read-only navigation guidance.

## Workflow

1. Resolve the repository root and read every applicable `AGENTS.md` plus
   repository README, SDK/version pins, build props, solution files, and local
   developer documentation. Do not assume a workstation path or solution name.
2. When GitHub identity matters, use the exact repository declared by project
   instructions and verify it. Never infer a target repository from remotes or
   organization names.
3. Inventory projects and ownership from the actual solution/project graph.
   Distinguish engine, host, gameplay/content, tooling, tests, distribution
   output, and custom modules without relying on namespaces alone.
4. Search by API shape and live consumers as well as names. Trace
   registration/reachability, configuration/data, persistence, lifecycle,
   client presentation, and tests before calling a surface implemented.
5. Load the narrow subsystem skill and inspect at least one current local
   precedent before proposing files or commands.
6. Return a file-level map with ownership, anchors, risks, assumptions, and the
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

Return repository/commit, instruction files, project map, source and
reachability anchors, proposed files, narrow skills, risks, validation commands,
assumptions, and read-only status.

## Verification

- Planned files belong to the reported projects at the reported revision.
- Commands target the owning build/test surface and label focused scope.
- Repository behavior is not presented as official UO evidence.
