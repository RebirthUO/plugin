---
name: modernuo-ticket-triage
description: Use when asked to triage a ModernUO/RebirthUO GitHub issue, ticket, bug report, feature request, or pasted issue text into a source-backed implementation plan. Trigger for requests like "triage this issue", "turn this GitHub ticket into an implementation plan", "research this UO bug ticket", or "what should we do for issue 123"; requires explicit rationale for needed code changes, maps publish/era claims to a measurement target, and only cites information verified in the repo or on the internet.
---

# ModernUO Ticket Triage

Use this skill to turn one GitHub issue or ticket into a decision-ready implementation plan. The job is to connect the issue's claim to canonical Ultima Online sources, current ModernUO/RebirthUO source evidence, risks, acceptance criteria, and tests.

Do not create GitHub comments, labels, branches, commits, issues, or PRs unless the user explicitly asks for that write action. By default, recommend tracker actions only.

## Required Input

Require one issue before starting:

- GitHub issue URL or issue number.
- Pasted issue text, comments, labels, and screenshots if GitHub access is unavailable.
- Optional target era, expansion, shard profile, or user-provided source URLs.

If the issue number is ambiguous because the repository is unknown, ask for the repository or issue URL. If multiple issues are provided, produce one plan per issue and keep each issue independently actionable.

## Intake Workflow

1. Capture the issue title, URL or identifier, labels, current body, linked comments, linked PRs, and any user-provided constraints.
2. Restate the issue as a small implementation goal and list current ambiguity.
3. Identify the likely domain: era parity, content taxonomy, skill/spell/item parity, bug, migration, source-data correction, test gap, or operator workflow.
4. Select companion skills:
   - Use `uo-domain-research` for UO source triangulation.
   - Use `modernuo-era-parity-check` when the issue is era-scoped, content parity, or any source says a publish introduced, removed, or changed the behavior.
   - Read `references/publish-era-measurement.md` when the issue mentions a publish, era, expansion, publish note, or Endless Journey.
   - Use `modernuo-code-audit` expectations when the plan implies `.cs` changes.
   - Use named skill, spell, item-property, combat, crafting, loot, quest, housing, region, gump, timer, serialization, networking, or migration skills when the owning subsystem is clear.
5. Gather source evidence before proposing code. Distinguish cited facts, repo facts, and inference. Only cite information that was found in the repository, fetched from the internet, or supplied directly in the issue.
6. If a source cites a publish number, publish note, era, expansion, or profile, map it to the measurement target first. Do not plan a global behavior change until the era/profile impact is described.
7. Search the repository for owning code, docs, tests, data files, era profiles, and previous plans.
8. Produce a Markdown implementation plan. Do not include patches unless the user asks for implementation.

## Source Trust Policy

Broad research is allowed, but every source must carry a trust tier. Never let a private shard wiki or emulator implementation silently become canonical UO behavior.

| Tier | Sources | Use |
|---|---|---|
| `official` | `uo.com/wiki`, official publish notes, official UO pages | Strongest source for live official behavior, publish scope, current pages, and official wording. |
| `canonical-community` | `www.uoguide.com`, legacy `uo.stratics.com`, `wiki.stratics.com` | Strong source for mechanics tables, historical behavior, player-facing names, older feature writeups, and practical details. |
| `repo` | Current ModernUO/RebirthUO source, docs, tests, data, era profiles | Source of truth for what the repo currently does. Use file paths and line numbers when possible. |
| `issue-supplied` | GitHub issue body, issue comments, pasted ticket text, user-provided screenshots or notes | Valid input context, but not proof of canonical UO behavior until corroborated by repo or internet evidence. |
| `secondary` | UO Herald archives, reputable guides, RunUO or ServUO discussions, emulator code | Useful for leads, implementation comparisons, and historical context. Verify before treating as target behavior. |
| `unverified` | Private shard wikis, forums, Discord excerpts, random blogs, generated summaries | Breadcrumbs only unless the user explicitly chooses custom shard behavior. |

When sources conflict, mark the row `source-conflict` and recommend a decision instead of choosing silently. When only non-authoritative sources exist, mark the evidence `unverified-source`.

## Evidence Existence Rule

Only reference information that exists in the current repository, in fetched internet sources, or in the issue content provided by the user.

- Verify every file path, symbol, test, doc, issue, URL, publish note, table, and quoted mechanic before citing it as evidence.
- For repository evidence, cite an existing path and line number when possible, or an exact search result when line numbers are not available.
- For internet evidence, cite the URL that was actually fetched or opened. Do not cite remembered URLs, generated URL patterns, or likely page names as evidence until they resolve.
- For user-provided issue text, label it as `issue-supplied` rather than external source evidence.
- If a source, file, or fact cannot be verified, do not include it as a factual citation. Put it in `Open Questions` or `Open Research` with the exact lookup needed.
- Do not infer that a publish, mechanic, class, test, or repo document exists because a similar one exists elsewhere. Search first, then cite.

## Publish and Era Measurement Rule

If information is era-based, use that era, publish, or profile as the measurement target. If a publish introduced, removed, rebalanced, or otherwise changed the behavior in the issue, the applicable era is an era check:

- Identify the publish number, date when available, source URL, and behavior change.
- Map the publish to the active UO era or expansion boundary using repo era docs, UOGuide expansion data, official publish notes, or existing era matrices.
- Treat the change as era/profile scoped until proven global. Name the measurement target and expected gate, such as `Core.SE`, `Core.ML`, `Core.SA`, `Core.TOL`, `Expansion`, or an EraProfile.
- Add `modernuo-era-parity-check` to the companion skill list and include a `Publish / Era Check` section in the plan.
- Use `references/publish-era-measurement.md` as the local mapping guide before assigning a publish to an era.
- If the publish falls between named expansions or the repo lacks the corresponding era gate, mark the issue `source-conflict` or `open-research` and recommend the exact decision or source lookup needed.
- Treat Endless Journey as a profile/account-policy measurement, not as a normal content-era measurement, unless a verified source and repo evidence show the behavior is a true expansion/content gate.

## Repository Investigation

Use issue keywords and normalized UO names to search the repo. Prefer `rg` and inspect the smallest useful set of files.

Start with these surfaces:

- `Projects/Server/` for engine behavior, expansion gates, serialization, networking, accounts, world state, and core services.
- `Projects/UOContent/` for game content, mobiles, items, spells, skills, gumps, quests, crafting, loot, regions, events, and systems.
- `Projects/UOContent.Tests/` and `Projects/Tests/` for regression coverage.
- `Distribution/Data/` and `Distribution/Configuration/` for JSON, CFG, era profiles, maps, regions, assemblies, spawns, and runtime config.
- `docs/` and `dev-docs/` for era matrices, implementation plans, source references, and coding standards.

Useful searches:

```bash
rg -n "IssueKeyword|UOName|ModernUOType|Core\.(AOS|SE|ML|SA|HS|TOL|EJ)|Expansion\." Projects Distribution docs dev-docs
rg -n "TODO|SourceLocked|Partial|Gap|RuntimeBlocked|Unverified|Needs runtime|Needs live QA" Projects Distribution docs dev-docs
rg --files Projects/UOContent Projects/UOContent.Tests Distribution docs dev-docs
```

For GitHub issue bodies, preserve important user claims, reproduction steps, acceptance criteria, screenshots, and linked evidence. Do not copy long issue comments into the final plan; summarize them and link or cite the issue.

## Confidence Labels

Use these labels exactly:

- `confirmed` - canonical or user-approved source and repo evidence agree enough to act.
- `source-conflict` - sources disagree or target era/profile changes the answer.
- `repo-only` - repo evidence is clear, but external expected behavior is missing or unnecessary.
- `needs-runtime` - source and code imply a behavior, but the decisive check requires running the server/client or live QA.
- `open-research` - evidence is insufficient after reasonable source and repo checks.
- `unverified-source` - the only external support is secondary, shard-specific, forum-based, or otherwise non-authoritative.

Do not leave a final row as "needs confirmation". Convert it into one of the labels above and give the next validation step.

## Implementation Plan Format

Produce one Markdown plan per issue using this structure:

```markdown
# Implementation Plan: {Issue Title}

| Field | Value |
|---|---|
| Issue | {URL or identifier} |
| Target area | {subsystem/domain} |
| Target era/profile | {era/profile or "not specified"} |
| Measurement | {era, publish, profile, or "repo-only"} |
| Confidence | {confirmed/source-conflict/repo-only/needs-runtime/open-research/unverified-source} |
| Risk | {save compatibility, client behavior, performance, economy, security, era parity, PvM, PvP, crafting economy, operator workflow, or test coverage} |

## Goal

{One paragraph describing what the implementation should accomplish.}

## Current Ambiguity

- {Ambiguity ID}: {unclear source, missing era, source conflict, runtime-only behavior, or user policy decision}

## Source Evidence

| Tier | Source | Claim | Confidence |
|---|---|---|---|
| official | {URL} | {expected behavior} | {label} |
| canonical-community | {URL} | {mechanic or historical detail} | {label} |
| issue-supplied | {issue URL, comment, or pasted text reference} | {user claim or repro detail} | {label} |
| secondary | {URL or repo comparison} | {lead or comparison} | unverified-source |

## Repository Evidence

| Area | Evidence | Meaning |
|---|---|---|
| {system} | `{path}:{line}` or exact search result | {what the repo currently does} |

## Expected vs Actual

| Behavior | Expected | Current Repo Evidence | Delta | Validation |
|---|---|---|---|---|
| {behavior} | {cited target} | {path/search/test evidence} | {concrete mismatch or no delta found} | {label} |

## Publish / Era Check

| Publish or Source Change | Measurement | Era/Profile Impact | Expected Gate | Repository Evidence | Decision |
|---|---|---|---|---|---|
| {publish, date, or source claim} | {era, publish range, or profile} | {which era/profile should receive the behavior} | `{Core.X}` / `{Expansion}` / `{EraProfile}` / `none` | `{path}:{line}` or search result | {apply behind gate, global because pre-existing, block on decision, or open-research} |

## Code Change Plan

| Change | Files / Owners | Reason | Evidence | Risk |
|---|---|---|---|---|
| {small code/data/doc/test change} | `{path}` or owning subsystem | {why the change is necessary} | {verified source row, repo evidence, or expected-vs-actual delta} | {risk and mitigation} |

## Recommended Implementation

1. {Smallest first code/doc/data step}
2. {Next step}
3. {Test or validation step}

## Acceptance Criteria

- {Observable condition}
- {Source-backed parity condition}
- {Regression or runtime validation condition}

## Test Plan

- {Unit/integration/manual test}
- {Build or targeted test command if known}
- {Manual QA scenario if needed}

## Tracker Recommendations

- Labels: {recommended labels only}
- Slice: {single issue, split into N issues, or block on decision}
- Comment draft: {optional summary only, do not post unless asked}

## Open Questions

- TTR-1: {only if evidence is genuinely missing or user policy is required}
```

Omit empty sections only when they do not apply. Keep `Source Evidence`, `Repository Evidence`, `Expected vs Actual`, `Code Change Plan`, `Recommended Implementation`, `Acceptance Criteria`, and `Test Plan` whenever the issue implies code or data changes. Keep `Publish / Era Check` whenever a source mentions a publish, publish-note behavior change, era boundary, expansion, or EraProfile.

## Planning Rules

- Prefer the smallest implementation that resolves the issue and preserves existing era/profile behavior.
- Separate official parity from custom shard policy. If the issue asks for a custom RebirthUO choice, state the official behavior first, then the custom recommendation.
- When code changes are necessary, describe each change with the owning file or subsystem, the reason it is necessary, the verified source/repo evidence that justifies it, and the risk it carries. Do not hide code work inside vague steps like "fix behavior".
- If a publish introduced the target behavior, treat that publish's measured era/profile as part of the acceptance criteria. The plan must say whether the implementation is gated, already global, intentionally custom, or blocked on an era decision.
- If a ticket or source maps a publish to an era but verified sources disagree, do not smooth it over. Mark `source-conflict`, cite the verified publish/date evidence, and keep the measurement at the verified publish/era boundary.
- If evidence is remembered, inferred, conventional, or likely but not found in the repo, on the internet, or in issue-supplied text, do not cite it. Record it as `open-research` with the lookup required.
- Do not bundle unrelated deltas. If the issue reveals separate problems, recommend slicing them into independent follow-up issues.
- Treat tests as part of the plan, not an afterthought. Name the likely test project or manual QA path when known.
- Flag risks that need extra care: save compatibility, client packets, world saves, timers, spawn density, loot economy, PvP balance, crafting economy, and player-visible era parity.
- When `.cs` changes are likely, mention that `modernuo-code-audit` should be applied after implementation.
- If a source table is too large or web summaries hide row data, recommend local HTML fetch and parsing rather than hand-copying summarized tables.

## Related Skills

- `uo-domain-research` for source triangulation and UO mechanics research.
- `modernuo-era-parity-check` for era-scoped parity reports.
- `modernuo-content-taxonomy` for classifying content work into implementation domains.
- `modernuo-code-audit` for reviewing C# implementation risks.
- `modernuo-skill-parity-check`, `modernuo-spell-parity-check`, and `modernuo-item-property-parity-check` for named single-subject parity issues.
