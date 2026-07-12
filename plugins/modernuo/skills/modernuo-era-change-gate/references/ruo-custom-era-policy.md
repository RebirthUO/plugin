# RebirthUO custom era / RUO expansion policy notes

Use this when a RebirthUO request asks whether to introduce a custom expansion/era after `Endless Journey` (named `RebirthUO`, with `RUO` as the existing content-layer/code shorthand where appropriate) to separate shard-specific behavior from ModernUO/UOContent/Server base code.

## Current policy direction

Treat `RebirthUO` as a **real RebirthUO custom ruleset era after `EJ`** when maintainers explicitly want shard-specific player mechanics, balancing, or global rules to diverge from official ModernUO/UOContent behavior. `RUO` remains the established content-layer shorthand in `RUOContent` and may be used as code shorthand only by explicit maintainer choice.

Do **not** treat a new expansion enum as a harmless code-ownership marker. In ModernUO/RebirthUO, an `Expansion` value is a global ruleset/client-feature/housing/data contract. The RebirthUO Core gate (currently discussed as `Core.RUO`) is appropriate for runtime ruleset gates, not as a replacement for comments, `#region`, or ownership labeling.

## Ownership separation still comes first

For code ownership and updateability, prefer the existing content-layer boundary first:

- `Distribution/Data/assemblies.json` loads `UOContent.dll` before `RUOContent.dll`.
- `Projects/RUOContent/RUOContent.csproj` is the RebirthUO-specific assembly above `Server` and `UOContent`.
- `Projects/RUOContent/Misc/RUOContentLayer.cs` marks that layer.

Use the RebirthUO Core gate only when behavior really depends on the RebirthUO ruleset. Upstream-fixable ModernUO/UOContent improvements should stay neutral and should not be hidden behind a RebirthUO gate merely because RebirthUO discovered them.

## Player-facing gates

`Core.RUO` may gate player mechanics and balancing changes when all of these are true:

1. The behavior is intentionally RebirthUO-specific custom policy, not official era parity.
2. PvP, PvM, economy, housing/storage, new-player, and exploit/bot side effects are named in the issue or PR.
3. The official era behavior remains legible; avoid silently redefining `EJ`, `TOL`, `SA`, or `AOS` behavior.
4. The branch is small and searchable, avoiding broad `#region` blocks or scattered implicit custom changes.

Tooling and diagnostics should generally prefer AccessLevel, configuration, and neutral hooks. They need `Core.RUO` only when the diagnostic behavior itself changes with the ruleset.

## Initial RebirthUO flag policy

When first introducing the RebirthUO expansion row, start with no intentional client-facing deviation from `EJ`:

- `RequiredClient`: same as EJ unless separately reviewed.
- `ClientFlags`: same as EJ / no new flag.
- `FeatureFlags`: same as EJ; do not invent new feature bits without a client contract.
- `CharacterListFlags`: same as EJ.
- `HousingFlags`: same as EJ.
- `MobileStatusVersion`: same as EJ.
- `MapSelectionFlags`: same as EJ; compare `Distribution/Data/expansions.json` with `Distribution/Configuration/expansion.json` before copying because local data/config rows can differ.

Future RebirthUO-specific flags or rules belong in separate review tickets with migration and test plans.

## Generic hooks for RUOContent tools

If base pipelines need to support RUO-specific tools such as `MechanicsTestDummy`, prefer neutral hooks/interfaces/events in `UOContent`/`Server` rather than direct references to RUO types from base assemblies. Do not rely on `partial` classes in `RUOContent` to extend `UOContent`/`Server` classes: partial declarations merge only inside the same compilation/assembly, and duplicate full type names across assemblies are a type lookup/serialization risk.

Good hook shape:

- No `RUO`, `RebirthUO`, or `MechanicsTestDummy` names in base API unless the API itself is shard-specific.
- No dependency from `Projects/UOContent/` or `Projects/Server/` to `Projects/RUOContent/`.
- Zero-cost/no-op when no diagnostic sink is registered, especially in combat hot paths.
- Domain names describe the observable pipeline: weapon hit, damage, proc chance, proc result, formula context, etc.
- Useful to ModernUO upstream, tests, or other shards, not only to one RebirthUO mobile.

## Repo anchors to inspect

- `Projects/Server/ExpansionInfo.cs` — `Expansion` enum, `FeatureFlags`, `CharacterListFlags`, `HousingFlags`, static table load, `GetEraFolder` fallback behavior, `GetInfo` index handling.
- `Projects/Server/Main.cs` — `Core.Expansion` and ordinal `Core.*` convenience gates.
- `Distribution/Data/expansions.json` — expansion table loaded at server startup.
- `Distribution/Configuration/expansion.json` — active shard expansion config.
- `Distribution/Data/assemblies.json` — assembly load order.
- `Projects/RUOContent/RUOContent.csproj` — RUO-specific content layer.
- `Projects/RUOContent/Misc/RUOContentLayer.cs` — layer marker.
- `Projects/RUOContent/Mobiles/Special/MechanicsTestDummy.cs` — RUOContent staff/mechanics tooling example.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs` — example combat pipeline where diagnostic hooks must stay generic and low-overhead.

## Review framing

Classify the source status as `Custom policy` plus `Repo evidence`; this is usually not a UO.com parity question unless a concrete official mechanic is being gated.

Ask/record these decision points:

1. Is `RebirthUO` intended as a real global ruleset era or only a code ownership marker? Current direction: real custom ruleset era.
2. If real era: may the RebirthUO Core gate (`Core.RUO` if that shorthand is chosen) gate player-facing mechanics? Current direction: yes, for intentional RebirthUO balancing/ruleset deviations with side-effect review.
3. Which client, feature, housing, map-selection, mobile-status, and config flags intentionally differ from EJ? Current direction: initially none.
4. How will future official post-EJ expansion/content names avoid enum ordinal/name conflict?
5. If a change is only for diagnostics/tooling, what neutral hooks/interfaces are needed so RUOContent can observe/extend base pipelines without base assemblies depending on RUOContent?
6. Where will the architecture rule be documented so contributors do not misuse `Core.RUO` as a mere marker?

## Acceptance/risk checklist

- A new RebirthUO expansion/era is a `Projects/Server/` change and needs explicit maintainer approval.
- Existing `Core.AOS`/`Core.SA`/`Core.TOL`/`Core.EJ` checks that compare by ordinal remain true in a post-EJ custom era; review for accidental behavior inheritance.
- `expansions.json` and `expansion.json` must stay synchronized with enum ordinals if a new era is introduced.
- `FeatureFlags`, `CharacterListFlags`, `HousingFlags`, map-selection flags, required client, and mobile-status version must be explicit, initially matching EJ unless separately reviewed.
- Era-folder fallback (`GetEraFolder`) should be considered for new folder names and data lookup behavior.
- Public/player communication should call custom RebirthUO behavior shard policy, not official UO era parity.
- Every player-facing RebirthUO Core gate should name PvP/PvM/economy/housing/new-player side effects.
- Generic diagnostic hooks in combat or item hot paths must avoid allocations and RUOContent dependencies.
