# Official Evidence Policy

The plugin uses two independent evidence axes. They must never be collapsed.

## Official gameplay truth

| Class | Allowed use |
|---|---|
| Official current | UO.com/Broadsword pages for current production-server behavior |
| Official historical | Official OSI/EA/Broadsword publish notes, update pages, design documents, or preserved official material for the named time |
| Unresolved | No direct official support, incomplete wording, or conflicting official material |

Only official current or official historical evidence establishes expected
gameplay. Match the source to the requested era/ruleset. A current wiki page
does not prove launch behavior, and a launch note does not prove current
behavior after later fixes.

## Discovery and implementation evidence

| Class | What it may prove | What it may not prove |
|---|---|---|
| Community discovery | Search terms, citations to locate, historical leads | Official mechanics, formulas, chronology, or restrictions |
| Community archive | What a community page claimed at a date | Official authority |
| Client evidence | Cliloc text, art, packet, TileData, or client-visible schema directly observed | Server-side mechanics not encoded by that artifact |
| Engine precedent | How ModernUO, ServUO, RunUO, or another emulator implemented a feature | OSI/EA behavior |
| Repository evidence | Current target code, data, config, registration, tests, and reachability | Official behavior or history |
| Custom policy | An explicit user/maintainer decision for this project | Official parity |

UOGuide, Stratics, forums, UOAlive, freeshards, ServUO, RunUO, ModernUO, local
code, and memory are never official gameplay sources. They may be useful only
within the allowed columns above.

## Claim record

```yaml
claim:
  id: C1
  statement: exact claim
  target: official-current | official-historical
  era_or_publish: exact scope
  official:
    status: verified | conflicting | unavailable
    url: exact URL
    page_title: exact title
    checked_at: ISO-8601
    support: exact finding or concise quotation
    revisions: []
  discovery:
    sources: []
    purpose: locate-official-material | expose-conflict
  implementation:
    repository: owner/repository
    revision: exact revision
    paths: []
    status: match | partial | absent | custom | unreachable
  resolution: official-wins | custom-policy | unresolved
```

## Reconciliation

1. Compare official sources only within the same time/ruleset scope.
2. Prefer the later official correction for later behavior while preserving the
   older official statement for its valid period.
3. Do not average conflicts or select the value shared by most emulators.
4. An explicit custom decision may authorize a deviation, but the output labels
   it `custom` and preserves the official expected value.
5. If official evidence cannot settle a behavior-changing claim, stop and ask
   the user whether to postpone the work or explicitly choose a custom policy.

## Staleness rules

- Record source check date and target branch/revision.
- Avoid reusable file-line anchors; use stable paths and symbols, then re-locate.
- Do not store statements that a feature is currently live without a revision
  and reachability check.
- Re-verify URLs, issue state, repository paths, cliloc values, and
  implementation status at use time.
