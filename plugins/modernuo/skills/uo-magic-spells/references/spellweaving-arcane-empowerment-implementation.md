# Spellweaving Arcane Empowerment implementation pattern

Session-derived pattern from implementing RebirthUO issue #61. Use this as a concrete reference when adding or repairing ML Spellweaving buffs that affect spell damage/healing, summons, buff icons, and dispel resistance.

## Source and era anchors

- Treat Arcane Empowerment as ML Spellweaving content: register in the existing `Core.ML` Spellweaving block, not globally.
- Keep `ArcanistSpell` as the base so the ML-client gate, Arcanist quest context, Spellweaving skill check, mana/LMC scaling, cast focus snapshot, and `ClearHandsOnCast = false` behavior stay centralized.
- UO.com Spellweaving row values verified for Arcane Empowerment:
  - mantra `Aslavdra`
  - mana `30(50)`; existing Arcanist convention uses the parenthesized value as `RequiredMana`
  - cast time `4.0s`
  - required skill `24`
  - duration: `15 + max(1, Spellweaving.Fixed / 240) + 2 * FocusLevel` seconds
  - base spell-damage/healing: `Spellweaving.Fixed / 120` percent
  - focus: `+5%` healing/PvM damage per focus level, `+1%` damage-vs-player per focus level
  - summoned pet max HP: fixed `+10%`, not the same as the Spellweaving/focus damage bonus
  - caster-only AoE, no cooldown
- Source conflicts to preserve in issues/reviews: UO.com lists `4.0s` cast time while ServUO precedent uses `3.0s`; UOGuide's Arcane Empowerment page has an older/conflicting `+14% spell damage` focus-bonus line. Prefer current UO.com for player-facing mechanics unless the issue explicitly chooses ServUO compatibility, and document any deviation in tests/review notes.
- Publish anchor: focused research found UOGuide `Publish 34` as Mondain's Legacy support, but not a canonical UO.com Arcane Empowerment-specific publish note. State ML as the era gate and mark exact spell publish as unresolved unless a stronger source is found.

## Runtime effect shape

- Store effect state in a runtime-only static table keyed by caster; do not add serialized fields or save-format changes for temporary buff state.
- Recast should refresh/replace the old context and cancel the old timer; do not stack contexts.
- Use `Timer.StartTimer(duration, callback, out TimerExecutionToken)` and cancel the token in `StopEffect`.
- Remove state on timer expiry, recast, player/creature death/delete events, and logout. For logout, add a static `Initialize()` subscription to `EventSink.Logout` and guard it with an `_initialized` boolean so repeated test calls/server init do not double-subscribe.
- Use the existing `BuffIcon.ArcaneEmpowerment`; add/remove the buff when state starts/stops. Live client tooltip text still needs manual QA when cliloc args are not already proven.

## Hook placement

- Damage: hook the central spell-damage path (`SpellHelper.Damage`) after other central spell modifiers already present in the path and before the final `AOS.Damage` sink. Keep PvP focus bonus reduced so it does not inflate player-vs-player burst beyond the issue/source policy.
- Healing: hook `SpellHelper.Heal`, not `Mobile.Heal`, so only spell-healing is affected.
- Summoned/animated creature damage: use `BaseCreature.AlterMeleeDamageTo` and `AlterSpellDamageTo`; do not permanently mutate creature base damage fields.
- Summoned max HP: wrap `BaseCreature.HitsMax` via a lookup/scaler and refresh current Hits on apply/expire. Use the official fixed `+10%` HP rule.
- Dispel resistance: route `Dispel` and `MassDispel` through a helper such as `GetDispelDifficulty(BaseCreature)` so the existing dispel formula stays in one place except for the temporary difficulty lookup.

## Test coverage shape

Put focused tests in `Projects/UOContent.Tests/Tests/Spells/Spellweaving/` with `[Collection("Sequential UOContent Tests")]` because the tests touch `World`, `Timer`, `SpellRegistry`, `NetState`, ML quest context, and real `Mobile`/`BaseCreature` instances.

Cover at least:

- formula rows for duration, base bonus, PvM/healing focus bonus, and PvP focus bonus;
- registration/book path: spell ID `615`, `SpellweavingBook` slot/index, and scroll-created spell;
- `CheckCast` gates: missing ML client, missing Arcanist quest context, insufficient skill, insufficient mana, and valid ML client;
- runtime caster effect: spell damage, healing, recast refresh without stacking;
- summoned follower effect: `HitsMax`, current Hits refresh, outgoing melee/spell damage, dispel difficulty, and cleanup after stop;
- logout cleanup through `EventSink.InvokeLogout` so static runtime state cannot survive disconnected players.

## Validation pattern

For PR-ready validation on this class of change:

```bash
export MSBUILDDISABLENODEREUSE=1
export MODERNUO_TEST_DATA_DIR='C:/Program Files (x86)/Electronic Arts/Ultima Online Classic'
git diff --check -- <changed paths>
dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter 'FullyQualifiedName~ArcaneEmpowermentSpellTests' \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger 'console;verbosity=minimal'
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger 'console;verbosity=minimal'
```

If the Hermes post-edit guard fires after commit/push/PR, create a fresh `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script that validates the committed changed paths with `git diff --check HEAD~1..HEAD -- <paths>`, verifies local/remote/PR heads, builds the solution, runs the focused test filter, and deletes the script afterward. Report it as ad-hoc/focused verification, not broad suite green unless the script actually ran the broad suite.
