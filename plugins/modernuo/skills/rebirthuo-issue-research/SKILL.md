---
name: rebirthuo-issue-research
description: Autonomously research, review, and make an existing RebirthUO issue implementation-ready. Exhaust current and historical official OSI/EA/Broadsword searches, infer era when evidence permits, use relevant research and code-domain skills, retry failed searches through materially different routes, compare the verified repository, and rewrite the issue in place. Ask only for a genuine product or custom-policy decision after evidence exhaustion. Do not implement or silently substitute emulator behavior.
license: MIT
metadata:
  version: "4.0.2"
---

# RebirthUO Issue Research

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Boundary

Own autonomous research and readiness. Official OSI/EA/Broadsword material is
the only gameplay authority. Repository, client, emulator, archive, and
community evidence remain separately labeled and never fill an official claim.

## Workflow

1. Verify the exact repository from applicable `AGENTS.md`, then load
   [the research contract](references/research-contract.md),
   [publication rules](references/issue-publication.md), and
   [uo-official-evidence](../uo-official-evidence/SKILL.md).
   If applicable instructions do not declare one unambiguous repository, stop
   with `RESEARCH_REPOSITORY_BLOCKED`. Never infer from cwd, remotes,
   organization, issue number, neighboring projects, documentation, or memory.
2. Capture the live issue, comments, labels, linked work, timestamp, digest, and
   any `IntakePacket`; build one claim per ledger row.
   Require one issue URL or number bound to the verified repository. Missing,
   conflicting, multiple, inaccessible, or cross-repository locators return
   `ISSUE_INPUT_BLOCKED` with candidates/evidence and no mutation.
3. Run the contract's exhaustion protocol. Infer era/publish from issue facts,
   official chronology, repository gates, and
   `uo-publish-expansion-mapping`; expand aliases and neighboring official
   pages; retry misses through materially different queries/source routes.
4. Invoke relevant RebirthUO/ModernUO codebase and domain skills to inspect
   implementation, reachability, data, configuration, persistence, lifecycle,
   client surfaces, and tests. Keep this evidence separate from official truth.
   Select only skills whose descriptions explicitly own an implicated surface;
   record their names and outputs. If none is available, inspect the verified
   repository directly and record `domain_skill: unavailable`; never reduce the
   official-evidence or readiness gates.
5. Reconcile conflicts and audit every readiness row, acceptance boundary,
   non-goal, player/economy/security impact, rollback concern, and test oracle.
6. Ask only after recorded exhaustion leaves a product decision. Offer focused
   supported choices: narrow scope, provide a direct official source, or adopt
   a visibly labeled custom policy. Never present emulator behavior as a default.
7. After an answer, re-read the issue, invalidate only affected claims, rerun
   their research and completeness checks, then continue autonomously.
8. Rewrite the issue body in its existing format, remove obsolete/resolved
   scaffolding, then publish only when the user explicitly requested an issue
   update or the full workflow supplied scoped publication authority. Otherwise
   return `AUTHORIZATION_REQUIRED` with the proposed body and label action.
   After authorized publication, apply only live-verified, issue-specifically
   justified existing labels add-only alongside the `blocked` readiness toggle,
   read back every mutation, and return implementation readiness `READY` only
   at that revision with no blocker. Never create, remove, rename, or
   bulk-synchronize labels.

## Output Contract

Return the contract's `ResearchPacket` with search-attempt ledger, era inference,
official and implementation evidence, readiness matrix, policy decisions,
calibrated claim and packet confidence, selected-label rationale and truthful
publication read-back,
`execution_state`, and nullable `implementation_readiness`. A blocked packet
has stable focused questions and exact resume claim IDs. Only
`execution_state: COMPLETE` with `implementation_readiness: READY` may hand off
to `rebirthuo-issue-implement`.

## Verification

- No evidence-unavailable result lacks materially different recorded attempts.
- Era was inferred when evidence permitted; ambiguity is tied to product intent.
- Every official claim is cited or remains explicitly unresolved.
- Publication is format-preserving, relevant labels are add-only and read back,
  and the `blocked` label matches readiness.
- Implementation readiness `READY` has no unresolved marker, question, blocker,
  or stale issue revision and requires publication state `succeeded`; partial
  or failed publication uses execution state `PUBLICATION_BLOCKED`.
