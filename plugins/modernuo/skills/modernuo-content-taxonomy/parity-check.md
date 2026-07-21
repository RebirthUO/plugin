# Parity Inventory

Read this reference only when the user explicitly requests parity, gaps,
implementation status, or a cross-domain inventory.

## Preconditions

1. Identify the official era/ruleset and the configured local profile.
2. Establish expected behavior through
   [uo-official-evidence](../uo-official-evidence/SKILL.md).
3. If official behavior or the target profile cannot be established, ask the
   user and stop instead of forcing a status.
4. Define the focus mechanic and direct dependencies. Keep other domains at
   summary level.

## Independent evidence axes

1. **Expected official behavior:** direct OSI/EA/Broadsword evidence for the
   named era/ruleset.
2. **Implementation state:** verified target-repository code, data,
   configuration, registration/reachability, tests, and merged work at a named
   revision.
3. **Discovery only:** community archives, emulator precedent, and client data
   within the limits defined by `uo-official-evidence`.

Repository implementation never precedes or defines expected official
behavior. Community/emulator agreement never upgrades a claim to official.

## Status vocabulary

- `Present`: official expected behavior is evidenced and the reachable
  implementation matches it.
- `Partial`: one or more required behavior, data, placement, reachability, or
  test surfaces are missing.
- `Gap`: official expected behavior is evidenced and no implementation is found.
- `Custom`: an explicit project policy differs from official behavior.
- `SourceLocked`: official expected behavior is established but implementation
  status is not yet assessed.
- `RuntimeBlocked`: implementation exists but registration, data, profile, or
  reachability prevents use.
- `Unverified`: official or implementation evidence is insufficient.

## Workflow

1. Build the era-scoped official behavior contract.
2. Inspect repository implementation and reachability at the named revision.
3. Deep-check only the focus: types/data, formulas, abilities, loot/rewards,
   access, spawns, era gates, client presentation, persistence/lifecycle, and
   tests as applicable.
4. Separate missing code from missing data/registration, disabled profile,
   unresolved official evidence, and intentional custom policy.
5. Cite every `Gap`, `Partial`, `RuntimeBlocked`, and `Custom` row. Preserve
   conflicts instead of selecting a default.
6. Re-scan the target branch for already merged implementation and stale paths.

## English output contract

```markdown
## Inventory

| Domain | Official expected behavior | Repository evidence | Discovery notes | Status | Confidence |
|---|---|---|---|---|---|
| World | ... | ... | ... | Present / Partial / Gap / Unverified | High / Medium / Low |
| Entity | ... | ... | ... | ... | ... |
| ItemSystem | ... | ... | ... | ... | ... |
| MobileSystem | ... | ... | ... | ... | ... |
| Progression | ... | ... | ... | ... | ... |
| EconomyCrafting | ... | ... | ... | ... |
| QuestNarrative | ... | ... | ... | ... |
| Encounter | ... | ... | ... | ... |
| ClientPresentation | ... | ... | ... | ... |

**Official era/ruleset:** ...
**Repository/profile/revision:** ...

## Gaps
- [Domain] Finding - official evidence, repository evidence, and impact.

## Partial or Runtime-Blocked
- [Domain] Finding - missing surface and evidence.

## Custom Deviations
- [Domain] Deviation - official value, custom value, and explicit authority.

## Focus Findings
- Classification, verified paths, and deep findings.

## Unresolved Research
- Official-source conflicts, missing implementation evidence, and questions.

## Issue Slice Options
- Offer independently actionable drafts on request; do not mutate a tracker
  without an explicit issue-creation request.
```

## Issue slicing

When requested, draft one issue per independent finding with official expected
behavior, verified actual state, impact, scope/non-goals, acceptance criteria,
validation, and open decisions. Tracker mutation belongs to
`modernuo-issue-create`.
> Every parity row must include `Official evidence`, `Repository evidence`, and
> `Discovery notes`. Community material is discovery-only and cannot determine a
> parity status; leave the status unresolved when official era-scoped evidence
> is unavailable.
