# Ninjitsu special-move test patterns

Session-derived patterns from RebirthUO Samurai Empire Ninjitsu parity tickets (#143-#149 range). Use these as examples when adding focused UOContent tests for Ninjitsu moves that touch global skill tables, special-move state, tracking bonuses, stealth checks, or timers.

## Lightweight formula / special-move tests

For tests that only need `Mobile.Skills`, mana, hidden state, or `SpecialMove.Table`, avoid full world bootstrap when possible:

```csharp
private static bool _skillsInfoConfigured;

private static Mobile CreateMobileWithNinjitsu(double ninjitsu)
{
    EnsureSkillsInfo();

    var mobile = (Mobile)RuntimeHelpers.GetUninitializedObject(typeof(Mobile));
    mobile.DefaultMobileInit();
    mobile.InitStats(100, 100, 100); // needed before setting Mana/ManaMax-sensitive state
    mobile.Skills.Ninjitsu.Base = ninjitsu;
    mobile.Mana = 100;
    return mobile;
}

private static void EnsureSkillsInfo()
{
    if (_skillsInfoConfigured)
    {
        return;
    }

    SkillsInfo.Configure();
    _skillsInfoConfigured = true;
}
```

Key pitfall: `DefaultMobileInit()` creates `Skills`, but `SkillInfo.Table` must be populated first for named skill access such as `Skills.Ninjitsu` or `Skills.Tracking`. If the test drives `Mobile.CheckSkill(...)` (Stealth/Hiding success checks), also initialize handlers with `SkillCheck.Initialize()`.

Use `[Collection("Sequential UOContent Tests")]` when tests touch global state such as `Core.Expansion`, `SkillsInfo.Configure()`, `SkillCheck.Initialize()`, `SpecialMove.Table`, `Tracking` state, or timer/action locks.

## Testing one-hit special moves

For moves like Focus Attack, Backstab, and Surprise Attack:

- Assert scalar helpers directly when possible (`GetDamageScalar`, `GetPropertyBonus`, or a small extracted helper like `CalculateDefensePenalty`).
- For one-hit reset behavior, seed `SpecialMove.Table[attacker] = move`, call `move.OnHit(...)`, then assert the table entry is gone. In `finally`, remove the entry directly if the test bypasses the public toggle pipeline.
- Set `Core.Expansion = Expansion.SE` in a `try/finally` when the move is SE-gated.

## Stealth and re-stealth checks

Order matters:

```csharp
mobile.Hidden = true;             // OnHiddenChanged resets AllowedStealthSteps
mobile.AllowedStealthSteps = 1;   // set after Hidden
mobile.Mana = 100;
```

For Backstab/Surprise Attack `OnBeforeSwing` tests:

- valid stealth state should return true,
- mana should decrease by `BaseMana`,
- `CanBeginAction<Stealth>()` should become false while the re-stealth lockout is active,
- cleanup with `attacker.EndAction<Stealth>()` in `finally`.

Expose timer durations as named properties when they are part of acceptance criteria (for example `RestalthLockoutDuration` and `DefensePenaltyDuration`) rather than reflection-peeking private timers.

## Tracking/Stalking distance bonus

`Tracking.AddInfo(attacker, defender)` captures the defender's current location and map. To test a distance bonus deterministically:

```csharp
attacker.MoveToWorld(new Point3D(100, 100, 0), Map.Internal);
defender.MoveToWorld(new Point3D(110, 100, 0), Map.Internal);
Tracking.AddInfo(attacker, defender);
defender.MoveToWorld(new Point3D(113, 104, 0), Map.Internal); // 5 tiles from tracked location
```

Then assert the expected contribution and call the move/helper a second time if you need to prove the tracking bonus is one-shot. Cleanup with `Tracking.ClearTrackingInfo(attacker)`.

## Shadowjump destination stealth checks

When a spell target pipeline is too expensive or fragile to simulate, extract the already-existing post-target behavior into a narrow public/static helper that preserves runtime behavior and enables focused tests. Example: `Shadowjump.CheckDestinationStealth(Mobile caster) => Stealth.OnUse(caster)`; `Target()` still calls the same path after moving the caster.

For pass/fail tests:

- success: high Hiding and Stealth, `Hidden=true`, `IsStealthing=true`; assert hidden remains, `IsStealthing` remains true, and `AllowedStealthSteps` is refreshed.
- failure: low Hiding (below `Stealth.HidingRequirement`) with Stealth high; assert `RevealingAction` clears `Hidden`, clears `IsStealthing`, and leaves no stealth steps.

## Reporting validation

When a broad filter fails due to the existing UOContent bootstrap issue `Path "Server.dll" is not an absolute path` from `TestServerInitializer` / `AssemblyHandler.LoadAssemblies(["Server.dll", "UOContent.dll"])`, do not claim broad suite green. Report the focused test result separately and document the broad filter as blocked by the harness/bootstrap issue.