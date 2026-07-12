# Towns, Sigils, and Elections

Use this reference for faction-town ownership, offices, elections, sigil/monolith state, delayed actions, and transition verification.

## Town ownership and offices

Current anchors:

- `Projects/UOContent/Engines/Factions/Core/Town.cs`
- `Core/TownState.cs`
- `Definitions/TownDefinition.cs`
- `Instances/Towns/**`
- `Items/TownMonolith.cs`, `Items/StrongholdMonolith.cs`

`Town.Capture` changes owner, clears sheriff/finance offices, updates the town monolith, deletes existing faction guards/vendors, and rebuilds owner-dependent lists. Initial/changed/unowned transitions also affect income timing and faction rewards.

Treat capture as an aggregate transaction. After failure or restart, town owner, monolith faction, offices, guard/vendor registrations, silver/income timestamp, and region identity must agree.

`TownState.Sheriff` and `Finance` setters maintain back-references on `PlayerState`; never set only one side. Delayed gump/target actions must revalidate office holder, town owner, target membership/type, and current funds.

## Election state machine

Current `Election` transitions:

```text
Pending -> Campaign -> Election -> Pending
```

Candidate count can skip voting or return directly to pending. The state stores timestamps, candidates, and voters and runs a recurring slice timer. Candidate/voter removal also occurs when members leave.

For every election change, test:

- campaign-state and rank/membership candidate eligibility;
- maximum/duplicate candidates;
- voter membership, one-vote rule, candidate validity, and stale/deleted players;
- tie/winner/incumbent/no-candidate behavior according to current code;
- candidate/member removal during each phase;
- commander replacement and conflicting office cleanup;
- save/load at each phase boundary and one active timer.

Addresses, game time, skills, and kill points appear in voter audit data. Treat anti-mule policy and thresholds as security/official-policy claims; do not infer effective enforcement from unused helper methods.

Current voting checks phase and duplicate voter but does not revalidate faction membership or enforce account-level voting. Candidate rank and phase policy also reflects mixed historical eras. Preserve those as implementation facts and test stale/expelled voters and same-account characters before claiming an election security policy.

Fresh elections initialize their last-state timestamp to the minimum date, so the first timer slice can immediately advance state. Pin intended startup behavior with a deterministic test.

## Sigil state model

Current anchors:

- `Projects/UOContent/Engines/Factions/Items/Sigil.cs`
- `Items/BaseMonolith.cs`, `StrongholdMonolith.cs`, `TownMonolith.cs`
- `Projects/UOContent/Skills/Stealing.cs` for acquisition
- faction process/death/logout handlers in `Core/Faction.cs`

Model sigil state from durable fields:

- associated town;
- last monolith/home;
- carrier/parent;
- corrupting and corrupted faction;
- last-stolen, grace, corruption, and purification timestamps.

Derived states include home/available, carried, being corrupted at a matching stronghold monolith, corrupted, returned to town/purifying, and return-home recovery.

## Sigil invariants

- Ordinary lift is blocked; acquisition routes through Stealing and faction eligibility.
- A player cannot hold duplicate sigils.
- Transfer requires live same-faction players and a valid destination backpack.
- Stronghold placement requires matching faction and town monolith identity.
- Town placement requires the faction that completed corruption.
- Parent removal/deletion must clear carrier appearance and return the sigil to a valid monolith.
- Town capture, corruption/purification timestamps, monolith ownership, and displayed properties must agree after save/load.

Exact corruption, grace, return, purification, and ownership periods are official-evidence gated. Current constants prove implementation only.

Sigil carrier restrictions are distributed across travel, moongates, transformations, disguise, help/stuck, duel, death, and logout code. Audit every `Sigil.ExistsOn` consumer when changing carrier rules.

Sigil/monolith links serialize on both sides, while monolith load does not necessarily rebuild the relationship through the normal setter. Test stale or missing `LastMonolith`, deleted monoliths, lighting, carrier appearance, and return-home repair after restart.

## Failure and restart review

Test carrier death/logout/leave/kick, every travel/transformation restriction, full or deleted backpack, monolith deletion/replacement, wrong town/faction, cross-facet movement, duplicate target response, server save during each timer phase, restart after a period elapsed, and inability to return home. Ensure recovery does not clone or silently delete the only sigil.

## Verification evidence

If no focused Factions suite exists, create deterministic state-machine tests around timestamps and entity fixtures before relying on admin/client smoke checks. Report manual checks for monolith visuals, carrier hue, gump text, and world placement separately.
