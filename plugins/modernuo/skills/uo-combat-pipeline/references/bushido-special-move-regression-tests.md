# Bushido special-move regression test patterns

Session-derived patterns for RebirthUO/ModernUO Samurai Empire Bushido special-move parity work. Use these when implementing or reviewing issues around Counter Attack, Lightning Strike, Evasion, weapon abilities, and `BaseWeapon` hit/parry integration.

## Counter Attack parry integration

Goal: prove a prepared Counter Attack fires on the next successful parry and is then consumed.

Pattern:
- Create attacker/defender `PlayerMobile` fixtures with `PacketTestUtilities.CreateTestNetState()` and `DefaultMobileInit()`.
- Set `Core.Expansion = Expansion.SE`, deterministic `Core._now`, and `Timer.Init(0)`.
- Override `Mobile.SkillCheckDirectLocationHandler` so parry checks succeed deterministically.
- Equip the defender with a nested test `Katana` subclass that overrides `OnSwing(Mobile attacker, Mobile defender, double damageBonus = 1.0)` and records call count/arguments.
- Call `CounterAttack.StartCountering(defender)`.
- Drive the live path with `incomingWeapon.AbsorbDamageAOS(attacker, defender, damage)`.
- Assert damage absorbed to `0`, `OnSwing` called exactly once with defender as attacker and original attacker as defender, and `CounterAttack.IsCountering(defender)` is false after the first parry.
- Call the parry path a second time and assert no second counter swing, proving consumption.

Cleanup:
- `CounterAttack.StopCountering(defender)`.
- Delete weapons and mobiles.
- Detach/dispose `NetState` objects.
- Restore `Mobile.SkillCheckDirectLocationHandler`, `Core.Expansion`, `Core._now`, and `Timer.Init(0)`.

## Counter Attack active special-move carry-through

Goal: prove Counter Attack's parry-triggered counter swing uses an already active weapon ability, and prove the no-active-special path separately.

Pattern:
- Use a nested `TestCounterWeapon : Katana` whose `PrimaryAbility` returns a nested singleton `TestSpecialAbility : WeaponAbility`.
- `TestSpecialAbility.OnHit(...)` records hit count and attacker/defender arguments, then calls `ClearCurrentAbility(attacker)` to mimic normal ability consumption.
- Set `WeaponAbility.SetCurrentAbility(defender, TestSpecialAbility.Instance)` before `CounterAttack.StartCountering(defender)`.
- Drive `AbsorbDamageAOS(attacker, defender, damage)`.
- Assert the ability fired once, with defender as the ability attacker and original attacker as target, and that Counter Attack plus current weapon ability are cleared.
- Add a second test where `WeaponAbility.ClearCurrentAbility(defender)` is called before Counter Attack; assert no ability hit but Counter Attack is still consumed.

## Lightning Strike HCI cap tests

Goal: prove Lightning Strike's +50 hit chance bonus is applied through the normal `BaseWeapon.CheckHit` calculation and capped by the AoS hit chance increase cap.

Pattern:
- Use equal attacker/defender weapon skill values (e.g. 100.0 Swords each) for a stable baseline.
- Equip the attacker with a weapon whose `AccuracyLevel` is `WeaponAccuracyLevel.Supremely` to create a below-cap +10 HCI case.
- Capture the chance passed to the direct skill-check handler:
  ```csharp
  double? capturedChance = null;
  Mobile.SkillCheckDirectLocationHandler = (from, skill, chance) =>
  {
      if (ReferenceEquals(from, attacker) && skill == SkillName.Swords)
      {
          capturedChance = chance;
      }

      return true;
  };
  ```
- Baseline below cap: `attackerWeapon.CheckHit(attacker, defender)` should pass `0.55`.
- With `SpecialMove.SetCurrentMove(attacker, new LightningStrike())`, the +50 bonus plus +10 weapon accuracy would exceed cap; production cap should yield `0.725`.
- Prefer capturing the production skill-check chance over duplicating the hit chance formula in a pure formula test.

## Lightning Strike + Hit Lower Attack exception

Goal: prove Lightning Strike applies its full +50 bonus while the attacker is under Hit Lower Attack.

Pattern:
- Use equal 100.0 weapon skills and no weapon HCI for a stable baseline.
- Apply the live effect with `HitLower.ApplyAttack(attacker)`.
- Capture `BaseWeapon.CheckHit`'s direct skill-check chance as above.
- HLA-only expected chance: `0.375`.
- HLA + `SpecialMove.SetCurrentMove(attacker, new LightningStrike())` expected chance: `0.625`.
- Cleanup the HLA state by advancing time beyond `HitLower.AttackEffectDuration` and slicing timers before deleting fixtures:
  ```csharp
  if (HitLower.IsUnderAttackEffect(attacker))
  {
      Core._now = Core.Now + HitLower.AttackEffectDuration + TimeSpan.FromSeconds(1);
      Timer.Slice(8);
  }
  ```

## General fixture guidance

- These are `Projects/UOContent.Tests` sequential tests; use `[Collection("Sequential UOContent Tests")]` because they mutate global `Core`, `Timer`, `Mobile.SkillCheck*Handler`, special move, weapon ability, and static effect state.
- Set expansion explicitly (`Expansion.SE`) and restore it in `Dispose`.
- Use `--no-build --no-restore` focused test runs only after a successful restore/build.
- Keep production changes out of test-missing issues unless RED proves a real code gap.
