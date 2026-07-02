---
name: rebirthuo-online-triage-verification
description: Use when taking RebirthUO GitHub issues with the `Triage required` label and verifying them online before promotion to `Human Review`. Enforces approved-source-only UO evidence (`uo.com`, `uoguide.com`, `uo.stratics.com`) and blocks promotion unless both review completeness and confidence are 100%.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [rebirthuo, modernuo, github, triage, human-review, uo-sources, verification]
    related_skills: [triage-to-human-review, modernuo-ticket-triage, github-issues, uo-domain-research, uo-modernuo-workflow, modernuo-era-parity-check]
---

# RebirthUO Online Triage Verification

## Overview

Use this skill as the hard online evidence gate for RebirthUO issues that currently carry `Triage required`. The goal is not merely to summarize an issue; the goal is to prove, from approved Ultima Online sources and current repository evidence, that the ticket can safely move to `Human Review` with a complete implementation handoff.

`Human Review` means the issue has a source-backed, implementation-ready triage comment and no unresolved canonical-behavior uncertainty. A ticket can only be promoted when both of these are true:

1. **Review completeness: 100%** — every claim needed for the proposed implementation is verified, sourced, repo-anchored, and represented in the comment.
2. **Confidence: 100%** — approved online sources and repo evidence are sufficient and non-conflicting for the issue's target era/ruleset.

If either value is below 100%, keep the issue in `Triage required` and report the exact blocker instead of posting a weak plan or setting `Human Review`.

## When to Use

- User asks to take `Triage required` RebirthUO tickets and verify them online.
- User asks whether a ticket can move to `Human Review`.
- User asks for source-locked triage, 100% confidence triage, or online verification for RebirthUO/ModernUO issues.
- User asks to process a queue of RebirthUO issues before human review.

Don't use for:

- Implementing code after a ticket is approved. Use implementation and ModernUO code skills for that.
- PR code review. Use `github-code-review` / `modernuo-code-audit`.
- Custom shard design decisions where the user explicitly chooses behavior different from canonical UO; such issues can be planned, but not marked `100%` canonical confidence unless the custom policy is explicitly documented by the user.

## Required Companion Skills

Load these before doing substantive work:

1. `triage-to-human-review` for the #73-style German implementation-plan comment and safe label transition sequence.
2. `modernuo-ticket-triage` for issue intake, evidence tables, confidence labels, and source/repo distinction.
3. `github-issues` for GitHub reads/writes when issue operations are needed.
4. `uo-domain-research` for approved UO source triangulation.
5. `uo-modernuo-workflow` and a domain-specific ModernUO/UO skill when the owning subsystem is clear.
6. `modernuo-era-parity-check` whenever the issue mentions publish, expansion, era, facet, profile, or historical behavior.

Completion criterion: the final issue decision can name the loaded triage/source/repo skills that governed it.

## Approved Online Sources

Only the following online source families can contribute to the `100% confidence` gate:

| Tier | Valid domains | Use |
|---|---|---|
| Official | `uo.com` | Official UO wiki pages, official publish notes, official feature pages, current official wording. |
| Canonical community | `uoguide.com`, `www.uoguide.com` | Mechanics tables, historical player-facing data, item/skill/spell/monster pages, expansion summaries. |
| Canonical legacy community | `uo.stratics.com` | Legacy Stratics guides, feature pages, publish-era writeups, mechanics explanations. |

Hard rules:

- Do not count memory, generated summaries, private shard wikis, random forums, emulator code, Discord/Telegram excerpts, or likely-but-unopened URLs toward `100% confidence`.
- Do not count a search-result snippet as evidence. Fetch/open the page or use a saved copy produced by a real fetch.
- Do not cite a remembered page. A URL only counts after it resolves and the relevant claim is visible in the fetched content.
- Repository evidence is mandatory for implementation planning, but repo code alone does not prove canonical UO behavior unless the issue is explicitly repo-only.
- If approved sources disagree, mark `source-conflict`; confidence is not 100% until the target era/ruleset decision resolves the conflict.
- If an approved source lacks a needed value (timer, probability, formula, coordinate, property, era gate), the issue remains `Triage required` with an `open-research` blocker.

Completion criterion: every gameplay claim in the triage comment has at least one approved-source citation or is explicitly marked as repo-only/user-policy and excluded from the 100% canonical gate.

## Per-Issue Workflow

### 1. Read the GitHub issue state

Use GitHub as the source of current tracker state:

```bash
gh issue view <N> --repo RebirthUO/service --json number,title,url,state,labels,body,comments,updatedAt
```

Capture:

- Issue number, title, and URL.
- Current labels, especially `Triage required` and `Human Review`.
- Body claims, acceptance criteria, screenshots, linked source URLs, and comments.
- Existing `## Konkretisierter Implementierungsplan` comments.

Completion criterion: you can say whether the ticket needs a new plan, an upgraded plan, label-only verification, or must remain blocked.

### 2. Define era/ruleset and issue domain

Before web research, state the measurement target:

- Publish base or expansion (`T2A`, `Renaissance`, `AoS`, `SE`, `ML`, `SA`, `ToL`, modern, or custom).
- Emulator/repo baseline (`RebirthUO/service`, usually `origin/live`).
- Client/profile assumptions if the behavior is client-, expansion-, or account-policy-dependent.
- Domain: combat, magic, skill, item property, loot, crafting, housing, world/region, monster, quest, UI/gump, persistence, networking, economy, PvP/PvM balance, or documentation/test gap.

Completion criterion: the plan names the era/ruleset assumption and does not silently apply modern-UO evidence to a historical shard profile.

### 3. Fetch approved online evidence

Search/fetch only enough pages to prove the ticket's target claim. Prefer direct pages from approved domains. Record the exact claim each source proves.

Recommended pattern:

1. Try `uo.com` for official current/publish behavior.
2. Try `uoguide.com` for mechanics tables and historic/player-facing pages.
3. Try `uo.stratics.com` for legacy mechanics, era-specific feature pages, or publish-era detail.
4. If the issue supplies source links, fetch them and classify them; approved-domain links may count, other links are breadcrumbs only.

For each relevant page, capture:

- URL actually fetched.
- Page title or stable heading when visible.
- The exact mechanic/data proven.
- Any publish/date/era wording.
- Any missing value or ambiguity.

Completion criterion: no external claim in the comment relies on un-fetched or non-approved online material.

### 4. Verify repository anchors

Use the current target base, preferably `origin/live`, for repo claims. Search the smallest likely owner surfaces:

- `Projects/UOContent/` for gameplay/content.
- `Projects/UOContent.Tests/` and `Projects/Tests/` for test coverage.
- `Projects/Server/` only for engine-level ownership; do not recommend editing it without a specific engine reason.
- `Distribution/Data/` and `Distribution/Configuration/` for spawns, regions, expansions, era profiles, and data-driven behavior.
- `docs/` and `dev-docs/` for matrices, ledgers, source references, and plans.

Use exact file paths and line ranges when possible. If the issue cites a path absent from `origin/live`, record it as issue-supplied/missing rather than inventing the file.

Completion criterion: every repo claim has a path/line, exact search result, or explicit `open-research` blocker.

### 5. Compute the promotion gate

Use this strict gate before posting or changing labels:

| Gate item | Pass condition | Failure label |
|---|---|---|
| Approved online source exists | Each canonical UO behavior needed by the ticket is proven by `uo.com`, `uoguide.com`, or `uo.stratics.com`. | `open-research` / `unverified-source` |
| Source conflict absent | Approved sources do not disagree for the selected era/ruleset, or the issue explicitly targets the resolved era. | `source-conflict` |
| Era/ruleset measured | Publish/expansion/profile impact is named and the expected gate is clear. | `open-research` / `source-conflict` |
| Repo anchor verified | Owning files/tests/data/docs are found or missing paths are explicitly documented. | `open-research` |
| Implementation plan complete | The #73 German plan sections are complete and concrete. | `incomplete-review` |
| Tests/validation identified | Focused and broader test/manual QA paths are named. | `incomplete-review` |
| Risk side effects named | PvP/PvM/economy/housing/save/client/performance risks are addressed when applicable. | `incomplete-review` |
| No unresolved blocker | No `needs-runtime`, `open-research`, `source-conflict`, or `unverified-source` remains for the promotion decision. | matching blocker |

Set:

- **Review completeness = 100%** only if all plan, repo-anchor, acceptance, test, and risk sections are complete.
- **Confidence = 100%** only if approved sources and repo evidence are sufficient, fetched, non-conflicting, and era/ruleset-aligned.

Any unresolved blocker means **do not move to `Human Review`**.

Completion criterion: the decision includes `Review completeness: 100%` and `Confidence: 100%`, or a concrete blocker explaining why promotion is refused.

## Human Review Promotion Contract

`Human Review` is allowed only after all of the following are true:

- [ ] Issue still exists and is open.
- [ ] Issue has or will receive a complete `## Konkretisierter Implementierungsplan` comment.
- [ ] Approved online sources (`uo.com`, `uoguide.com`, `uo.stratics.com`) verify every canonical gameplay claim required by the issue.
- [ ] Repo anchors on the target base verify current implementation surfaces.
- [ ] Era/ruleset assumptions are explicit.
- [ ] `Review completeness: 100%`.
- [ ] `Confidence: 100%`.
- [ ] No `open-research`, `source-conflict`, `unverified-source`, `needs-runtime`, or `incomplete-review` blocker remains.
- [ ] User authorized GitHub side effects if posting/commenting/labeling is required.

Safe sequence, after authorization:

```bash
cat > /tmp/rebirthuo-triage-<N>.md <<'EOF'
<full verified German #73-style plan>
EOF

gh issue comment <N> --repo RebirthUO/service --body-file /tmp/rebirthuo-triage-<N>.md
gh issue edit <N> --repo RebirthUO/service --add-label "Human Review" --remove-label "Triage required"
gh issue view <N> --repo RebirthUO/service --json labels,comments --jq '{labels:[.labels[].name], lastComment:.comments[-1].body[0:120]}'
```

Completion criterion: GitHub is queried after the mutation and confirms the comment and label state.

## Required Comment Addendum

When drafting or posting the #73-style German implementation plan, include a compact gate summary near the end, usually before `### Risiken / Hinweise fuer den Implementierer` or after it:

```markdown
### Verifikations-Gate
- Review-Vollstaendigkeit: 100%
- Confidence: 100%
- Zugelassene Online-Quellen: <uo.com/uoguide.com/uo.stratics.com URLs with exact claims>
- Repo-Basis: <branch/base, e.g. origin/live>
- Blocker: keine
```

If the issue cannot pass, do not post a promotion-ready comment. Report a blocker summary instead:

```markdown
### Verifikations-Gate
- Review-Vollstaendigkeit: <0-99>%
- Confidence: <0-99>%
- Blocker: <open-research/source-conflict/unverified-source/needs-runtime/incomplete-review>
- Naechster Nachweis: <exact approved-source lookup, repo check, runtime QA, or user era decision needed>
```

## Batch Queue Workflow

For a queue of `Triage required` issues:

1. Export the queue from GitHub:

```bash
gh issue list --repo RebirthUO/service --state open --label "Triage required" --limit 300 \
  --json number,title,url,body,comments,labels,updatedAt > /tmp/rebirthuo-triage-required.json
```

2. Build a manifest with one row per issue:
   - `promote` only when the issue reaches 100% review and 100% confidence.
   - `comment-only` when a complete evidence summary is useful but a blocker remains; do not remove `Triage required`.
   - `label-only` only when a verified complete plan already exists and the gate is independently rechecked.
   - `blocked` when approved-source or repo evidence is missing/conflicting.

3. Process small domain batches so source assumptions remain coherent.
4. For each issue, fetch approved online evidence and repo anchors independently; do not reuse one issue's evidence for another unless the exact same source claim applies.
5. For UOGuide monster pages, prefer the MediaWiki raw endpoint (`https://www.uoguide.com/index.php?title=<Title>&action=raw`) and parse `{{Creatures ...}}` fields instead of relying on snippets. Retry title variants such as hyphen/space/case changes (`RaiJu` -> `Rai-Ju`) before marking an approved-source miss.
6. Treat issue-cited repo documents as issue-supplied until verified on the target base. If an issue points to `dev-docs/parity/...` but `origin/live` lacks it, cite the issue as context and use current repo anchors plus online sources for the gate; do not invent or recreate the doc by default.
7. Split the manifest by action class:
   - `promote` only when review and confidence are both 100%.
   - `comment-only` when a useful blocker comment should be posted but the issue must remain `Triage required`.
   - `no-op/closure candidate` when approved sources and repo evidence show no confirmed gameplay delta; this can be promoted if the comment clearly asks human review to accept/close the no-op and the gate is 100%.
8. Post and promote atomically only for `promote` rows: comment first, label second, verify third.
9. Final verification must query GitHub, not local manifest state.

Completion criterion: final report lists issue numbers promoted, label-only verified, comment-only/not promoted, blocked, and the GitHub-verified remaining `Triage required` count.

## Common Pitfalls

1. **Treating `Human Review` as progress.** It is not a progress marker. It is only allowed after 100% review completeness and 100% confidence.

2. **Counting repo code as online UO proof.** Repo code proves current implementation, not canonical UO behavior. Use approved online sources for gameplay claims.

3. **Counting non-approved sources.** Forums, private shard wikis, emulator code, and generated summaries can guide searches but cannot satisfy the gate.

4. **Ignoring era drift.** Modern `uo.com` behavior may not match an AoS/SE/ML target. If the issue is era-scoped, confirm the publish/era boundary or block promotion.

5. **Posting a strong-looking plan with weak evidence.** A polished #73 comment still fails if the sources do not prove the mechanic.

6. **Promoting with runtime-only unknowns.** If the decisive proof requires live server/client QA and it has not been run, confidence is not 100%.

7. **Duplicate comments.** If a complete verified plan already exists, prefer `label-only` verification rather than appending another full comment.

8. **Silent source conflict resolution.** Do not choose between conflicting approved sources without stating the era/ruleset reason or asking for a maintainer decision.

## Verification Checklist

- [ ] Required companion skills loaded.
- [ ] GitHub issue body/comments/labels read from the live issue.
- [ ] Era/ruleset/publish/profile assumption stated.
- [ ] Approved online sources fetched from `uo.com`, `uoguide.com`, or `uo.stratics.com`.
- [ ] Each approved source is mapped to the exact claim it proves.
- [ ] Non-approved sources, if seen, are excluded from the 100% confidence gate.
- [ ] Repo anchors are verified against the target base with path/line or exact search evidence.
- [ ] `Review completeness` and `Confidence` are explicitly scored.
- [ ] No promotion unless both scores are 100% and no blocker remains.
- [ ] GitHub side effects are authorized before posting or label changes.
- [ ] After any label/comment mutation, GitHub is queried again to verify the result.
