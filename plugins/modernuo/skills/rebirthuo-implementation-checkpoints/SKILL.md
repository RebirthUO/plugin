---
name: rebirthuo-implementation-checkpoints
description: Use during RebirthUO implementation sessions when issue analysis exposes unresolved gameplay/product decisions or the user asks for a review, gap list, or decision matrix before continuing code work.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    related_skills:
    skill_group: rebirthuo
    skill_subgroup: agentic
    workflow_phase: implement
    workflow_tier: support
---
# RebirthUO Implementation Checkpoints

## Overview

Use this skill as a checkpoint inside RebirthUO issue implementation work. It exists for the class of tasks where the code path is known, but the implementation still contains product/gameplay decisions that can affect players: era gates, PvP/PvM balance, formula caps, context-menu UX, acquisition/loot source, tooltip behavior, adjacent fixes, test scope, or PR closure semantics.

The important lesson: when the user asks for `Review`, `was fehlt`, or a short decision matrix, stop the implementation stream and answer that request directly. Do not keep patching or testing in the same turn until the user approves a path.

## When to Use

- A `/rebirthuo-implement` issue produces unresolved design decisions before PR readiness.
- The user asks for `Review`, `was fehlt`, `kurze Matrix`, `was soll ich entscheiden`, or similar.
- A ticket is implementable but has multiple safe interpretations.
- A code change is partly done, but test/build/PR work should pause until product decisions are confirmed.

## Procedure

1. **Freeze the implementation state.** Check or summarize the current branch/worktree, changed files, build/test status, and known blockers. Do not continue coding while preparing the review.
2. **Separate done from undecided.** Mark which parts are already patched or validated, and which are still pending user/product choice.
3. **Build a compact decision matrix.** Include ID, topic, options, recommendation, risk if wrong, and default choice.
4. **Name player-loop side effects.** For UO changes, include PvP, PvM, economy/loot, era/ruleset, context-menu/client UX, and trust/rollback where relevant.
5. **Recommend a default path.** Give the user a single safe default such as `mach weiter mit Default`.
6. **Wait for approval before continuing.** The matrix is the deliverable for that turn unless the user explicitly authorizes continuing.

## Matrix Template

```markdown
## Entscheidungsmatrix

| ID | Thema | Option A | Option B | Empfehlung |
|---|---|---|---|---|
| D1 | <formula/cap/scope> | <choice> | <choice> | **A/B**, because <risk/evidence> |

## Default, wenn du "mach weiter" sagst

- D1: <default>
- D2: <default>
- Tests/PR: <default validation and PR handling>
```

## Pitfalls

- Do not treat a user's request for a review/matrix as permission to keep implementing. It is a steering instruction to pause and expose choices.
- Do not hide test state. If build passed but focused tests are blocked by an existing setup/baseline problem, say exactly that and avoid claiming suite-green.
- Do not overload the matrix with code internals. Lead with product choices and player-visible consequences.
- Do not create a PR before unresolved formula, era, UX, or loot/acquisition decisions are confirmed.

## Verification

The checkpoint worked if the next user can answer with a short approval (`mach weiter mit Default`) or pick individual decision IDs, and the implementation can then resume without rediscovering the same design questions.
