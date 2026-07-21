# Weapon-Buff Spell Pattern

This is a repository-derived implementation reference for temporary weapon enchantment spells; it is not official gameplay evidence. Use it whenever
you implement or review a spell that buffs a `BaseWeapon` for a duration and must clean
up on disarm, weapon deletion, caster death, caster deletion, or timer expiry.

Before relying on a named path, hook, line, or behavior below, record the
consuming repository revision and confirm that anchor in its current source.

## Repository implementation examples

| Spell | School | Cleanup dict | Static helpers exposed |
|---|---|---|---|
| `Projects/UOContent/Spells/Necromancy/CurseWeapon.cs` | Necromancy | `Dictionary<BaseWeapon, ExpireTimer>` | None — uses `weapon.Cursed` flag |
| `Projects/UOContent/Spells/Chivalry/ConsecrateWeapon.cs` | Chivalry | `Dictionary<BaseWeapon, ExpireTimer>` | None — uses `weapon.Consecrated` flag |
| `Projects/UOContent/Spells/Spellweaving/ImmolatingWeapon.cs` | Spellweaving | `Dictionary<BaseWeapon, ImmolatingWeaponTimer>` | `IsImmolating(weapon)`, `GetImmolatingDamage(weapon)`, `DoEffect(weapon, target)`, `StopImmolating(weapon)` |
| `Projects/UOContent/Spells/Spellweaving/AttuneWeapon.cs` | Spellweaving | `Dictionary<Mobile, ExpireTimer>` (caster-keyed) | `IsAbsorbing(m)`, `StopAbsorbing(m, message)` |
| `Projects/UOContent/Spells/Mysticism/StoneFormSpell.cs` | Mysticism | `Dictionary<Mobile, ResistanceMod[]>` (caster-keyed) | `UnderEffect(m)`, `RemoveEffects(m)` |
| `Projects/UOContent/Spells/Necromancy/BloodOathSpell.cs` | Necromancy | `Dictionary<Mobile, ExpireTimer>` keyed by both participants | `RegisterOath`, `RemoveCurse`, `GetBloodOath` |

Note the design split:

- **Weapon-keyed dictionaries** (Curse, Consecrate, Immolate, Enchant) are right when
  the effect travels with the weapon — disarm/disarm cancels it.
- **Caster-keyed dictionaries** (Attune, StoneForm, BloodOath) are right when the effect
  lives on the caster and the weapon does not matter.

For SA `Enchant`, treat weapon-keyed state as a repository precedent only. Verify the target-era official mechanic separately before claiming that disarm cancellation is production behavior.

## Required `BaseWeapon` integration

The class `BaseWeapon` has two hook points every weapon-buff spell must use. Both are
**required** for a complete implementation. If you add a new weapon-buff spell and
forget to wire these, the buff will leak past disarm and weapon deletion.

`Projects/UOContent/Items/Weapons/BaseWeapon.cs`:

- **`OnRemoved(IEntity parent)`** (around line 1136) — fires when the weapon leaves a
  mobile's hand/armor. This is the disarm/unequip path. The existing
  `ImmolatingWeaponSpell.StopImmolating(this);` (line ~1171) and
  `ForceOfNature.Remove(m);` (line ~1172) are the canonical anchor — add your
  `MyWeaponBuffSpell.StopEffect(this);` adjacent to those lines.
- **`OnAfterDelete()`** — fires when the weapon is removed from the world. The
  `OnRemoved` path does not always fire on delete (e.g. dupe, internal relocation), so
  cleanup must be in `OnAfterDelete` as well. **`BaseWeapon` currently does not
  override `OnAfterDelete`**; you must add an override and call your `StopEffect` from
  there.

The existing `Cursed` and `Consecrated` flags are public auto-properties on `BaseWeapon`
and are reset by their own `ExpireTimer` ticks (not by `OnRemoved`). That works for
those two spells because the flag persists on the weapon after the caster disarms, but
the official Enchant wording says disarm cancels the effect — so Enchant must use the
dictionary-keyed pattern, not a `BaseWeapon` flag.

**Version and evidence override:** The preceding implementation descriptions are
repository discovery examples, not a portable requirement. Confirm every hook
and cleanup path in the consuming revision before adopting it. Do not treat the
reference's statement about any official wording as official evidence; obtain
the applicable era-scoped source separately or return `BLOCKED` for that claim.

## Source-generated cleanup for caster death/delete

The `ModernUO.CodeGeneratedEvents` source generator (in `Distribution/Assemblies/`,
referenced via `using ModernUO.CodeGeneratedEvents;`) wires `[OnEvent]`-annotated
static methods to existing `[GeneratedEvent]` static partial methods. For
player/creature death and deletion, the four canonical hooks are:

```csharp
using ModernUO.CodeGeneratedEvents;

[OnEvent(nameof(PlayerMobile.PlayerDeathEvent))]
[OnEvent(nameof(PlayerMobile.PlayerDeletedEvent))]
[OnEvent(nameof(BaseCreature.CreatureDeathEvent))]
[OnEvent(nameof(BaseCreature.CreatureDeletedEvent))]
public static void OnCasterRemoved(Mobile m) { /* remove rows where m was the caster */ }
```

The handler signature is `Mobile`, not the specific subclass. The generator dispatches
the `BaseCreature` events up to a `Mobile`-typed subscriber. The `BloodOathSpell`
`OnCurseEnds` is the reference implementation to copy.

If your buff is on a non-PlayerMobile / non-BaseCreature caster (rare, but possible for
staff-controlled mobs), those events will not fire. Add an additional safety net by
also clearing the dictionary on `World.Save` or by validating the caster is non-null
and not deleted in the `ExpireTimer` tick.

Do **not** subscribe to `EventSink.Logout` for weapon-buff cleanup. Logout is a
client-side event, not a server-side deletion — the player and weapon are still
in-world. The four `[OnEvent]` death/deletion hooks above are the correct way to break
a buff when the caster leaves the world.

## Hit-spell pipeline integration

`BaseWeapon` reads `AosWeaponAttributes.GetValue(attacker, AosWeaponAttribute.HitXxx)`
in its melee hit pipeline (around line 2191–2200 for the five hit-spell attributes).
The static `AosWeaponAttributes.GetValue(Mobile, AosWeaponAttribute)` iterates the
mobile's items and sums each weapon's permanent `WeaponAttributes[attr]`.

If your spell adds a **temporary** hit-spell chance, do NOT mutate the weapon's
`WeaponAttributes` (that would persist as a permanent property and survive weapon
trade, save/load, and `OnAfterDelete`). Instead:

1. Expose a static helper on your spell, e.g. `MySpell.GetExtraHitChance(weapon, attr)`.
2. Either:
   - Override `AosWeaponAttributes.GetValue(Mobile, AosWeaponAttribute)` (engine
     surface, not preferred — see `modernuo-code-audit`), or
   - Add the temporary value in the `BaseWeapon` hit-pipeline call sites directly
     (preferred — keeps the change scoped to `Projects/UOContent/Items/Weapons/BaseWeapon.cs`).
   The latter is what SA `Enchant` does: it adds the Enchant contribution in the
   `maChance`/`harmChance`/etc. expressions next to the existing
   `AosWeaponAttributes.GetValue(attacker, ...)` calls.

For Spell Channeling, the existing check is
`Attributes.SpellChanneling != 0` in `BaseWeapon.AllowEquippedCast(Mobile)` (line
~2957). To allow casting while holding a weapon with an Enchant that grants temporary
channeling, change that check to
`Attributes.SpellChanneling != 0 || EnchantSpell.ProvidesSpellChanneling(this)`.

## BuffIcon and StatMod

- `BuffIcon` is an enum with one entry per known buff (`BuffIcon.Enchant` already
  exists for SA Enchant). The icon is added/removed via
  `((PlayerMobile)caster).AddBuff(new BuffInfo(BuffIcon.X, titleCliloc, duration))`
  and `RemoveBuff(BuffIcon.X)`.
- The `-1 Faster Casting` portion of the Enchant buff is a `StatMod` of
  `StatType.CastSpeed` with value `-1`. **Verify that `StatType.CastSpeed` exists in
  this repo's `Projects/Server/Mobiles/Mods/StatMod.cs` before relying on it.** A
  previous Enchant implementation drafted in this repo assumed the name and the
  compile failed; if it does not exist, fall back to applying the faster-casting
  reduction through `AosAttribute.CastSpeed` on the caster, or by using
  `Caster.AddStatMod(new StatMod(StatType.Dex, ...))` with a comment that flags the
  pending engine change.
- Always suffix the `StatMod` name with the weapon's serial so the same caster can
  hold multiple enchanted weapons without collisions:
  `$"Enchant-{weapon.Serial}"`.

## Reagent / mana consumption

For self-targeting spells, call `CheckSequence()` inside `OnCast()` to consume
reagents and mana. The `CheckSequence()` call must be the gate on the actual effect
(perform the effect only when `CheckSequence()` returns true), and you must call
`FinishSequence()` regardless of success/failure so the spell pipeline clears.

`CheckSequence()` returns false and calls `DoFizzle()` if reagents are missing, mana
is insufficient, the caster is frozen, or the player is calmed. It also consumes
scroll charges when the source is a `SpellScroll` or `BaseWand`.

## Era gate

Register the spell in `Projects/UOContent/Spells/Initializer.cs` inside the matching
expansion block (`if (Core.SA) { ... }` for SA Mysticism). Mysticism and the
temporary-enchant effect are SA-only — never register spell 680 (Enchant) outside the
`Core.SA` guard.

## Test shape (UOContent.Tests)

`Projects/UOContent.Tests/Tests/Spells/Necromancy/BloodOathSpellTests.cs` is the
closest reference. Use:

- `[Collection("Sequential UOContent Tests")]` for any test that mutates
  `Core.Expansion`, global spell tables, timer state, or instantiates real `Mobile` /
  `BaseWeapon`.
- `var m = new Mobile(World.NewMobile); m.DefaultMobileInit();` to create a fixture
  mobile.
- For PlayerMobile-specific event tests, use `new PlayerMobile(World.NewMobile)` and
  call `PlayerMobile.PlayerDeletedEvent(m)` / `PlayerMobile.PlayerDeathEvent(m)` to
  trigger the source-generated event directly.
- For weapon fixtures, instantiate a real `BaseWeapon` (e.g. `new Katana()` or
  `Activator.CreateInstance(typeof(Katana))`) and equip it with
  `m.Weapon = weapon` (or use `BaseWeapon.OnAdded` to simulate equip).
- For timer-expiry tests, prefer direct `Timer.StartTimer`/slice manipulation over
  waiting on the real timer wheel — see the `modernuo-test-workflow` skill for the
  deterministic-test seam patterns.

## Common pitfalls

1. **Using `EventSink.Logout` for cleanup** — logout is not a world-removal event.
   Use the four `[OnEvent]` hooks instead.
2. **Mutating `weapon.WeaponAttributes[HitXxx]` to apply the temporary buff** — this
   persists the change forever and survives trade / save. Use a static helper on the
   spell that the `BaseWeapon` hit-pipeline call sites consult.
3. **Calling `Caster.Target = ...` for a self-targeting spell** — the cast pipeline
   waits for a target that never comes. Call `CheckSequence()` + `FinishSequence()`
   directly inside `OnCast()` instead.
4. **Forgetting `FinishSequence()`** — the caster's `Spell` slot stays set, the
   next cast is blocked, and the client shows a stuck cast bar.
5. **Keying the dictionary by `Mobile` for a weapon-buff spell** — the buff will
   survive disarm. Key by `BaseWeapon` so it follows the weapon.
6. **Setting `ClearHandsOnCast = true` (the default) for a weapon-buff spell** —
   `BaseWeapon.ClearHandsOnCast` runs in `Spell.Cast()` and disarms the caster
   before the effect can be applied. Override to `false`.
7. **Not wiring `BaseWeapon.OnRemoved` / `OnAfterDelete`** — the buff persists
   past disarm and weapon deletion, leaking the table entry and any `StatMod` /
   `BuffIcon` you applied.
8. **Using a public `BaseWeapon` flag for a new buff** — adds a property the
   weapon class must serialize, and forces a `MigrateFrom` for old saves. The
   dictionary-keyed pattern avoids both.
