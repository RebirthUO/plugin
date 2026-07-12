---
name: modernuo-skill-discovery
description: >
  Use when auditing or curating ModernUO skill-library coverage against current
  repository patterns, installed skills, developer docs, and source domains.
  Prefer evidence-backed patches to existing skills; do not create, merge,
  rename, or delete skills unless the request explicitly authorizes it.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: meta
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, skills, discovery, coverage, learning]
    related_skills:
      - modernuo-codebase
      - modernuo-code-audit
      - modernuo-content-patterns
      - modernuo-lifecycle-cleanup
      - modernuo-performance-hot-paths
      - modernuo-test-workflow
---

# ModernUO Skill Discovery

## Boundary

Determine which recurring ModernUO jobs are covered, partial, duplicated, or
missing, and improve the smallest durable skill surface. This skill is read-only
unless the user asks for edits. It does not authorize repository or GitHub
mutation, nor speculative skill creation.

## Workflow

1. Inventory every skill source exposed by the runtime and repository. Verify
   each `SKILL.md` exists; record name, location, source type, description,
   metadata, references, and tool/vendor coupling.
2. Run a mechanical audit for YAML/frontmatter, description length and trigger
   quality, broken links/related skills, context size, mojibake, absolute local
   paths, and unused resources.
3. Read repository instructions, developer docs, and representative/high-risk
   source domains. Extract recurring APIs, lifecycle rules, failure modes,
   verification practices, and near-neighbor boundaries.
4. Compare by meaning, not filenames, and apply the coverage labels in the
   reference.
5. Patch an existing class-level skill when a sharper trigger, workflow,
   reference, or self-check closes the gap. Propose a new skill only for a
   distinct reusable job with evidence and an output contract.
6. Re-run scoped YAML/link/context checks and inspect representative edited
   skills through the runtime when available.

## Guardrails

- Use only installed/exposed skills and existing files; never treat a cached but
  unavailable package as installed.
- Keep entrypoints lean; defer detail, deterministic logic, and evidence only to
  task-authorized resources.
- Require recurring evidence, distinct boundaries, and route value before calling
  a skill missing.
- Preserve owner/project metadata and high-risk gotchas during curation.
- Report global/non-scoped issues without editing them.

## Output Contract

For an audit, return inventory counts, coverage matrix, evidence paths, existing
skills to update, proposed gaps with priority/confidence, and not-recommended
duplicates. For implementation, return touched skills/references, trigger and
boundary changes, checks run, and residual issues; explicitly list destructive
actions not taken.

## Verification

- Every changed description begins with a concrete recurring job and excludes
  plausible near neighbors.
- Every changed skill contains an executable workflow, output contract,
  verification/self-check, and conditional reference routing.
- YAML parses, descriptions meet the runtime limit, local links resolve, initial
  context stays within the selected budget, and no absolute host path/mojibake
  remains in scope.
- Sample route cases distinguish each edited skill from adjacent skills.

## Reference Routing

- Read [coverage audit labels, priorities, scan queries, and report shape](references/coverage-audit.md)
  when running a full library audit or proposing gaps.
- Load the active skill-authoring/meta-skill only when the user requests content
  changes or a new reusable package.
- Read repository `AGENTS.md`, plugin metadata, and current source/docs before
  treating local conventions as authoritative.
