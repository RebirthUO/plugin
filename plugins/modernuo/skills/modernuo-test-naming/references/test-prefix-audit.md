# Test Prefix Audit Checklist

Use this reference when reviewing a ModernUO-based repository's test names for AI-generated
or source-of-work prefixes.

## What to scan

- File stems under test projects (`*Tests.cs`).
- Test class names.
- xUnit method names (`[Fact]`, `[Theory]`, `MemberData`, `InlineData`).

## High-confidence noise

Flag these when they prefix file/class/method names:

- `Publish\d+`, `Pub\d+`, `P\d+`
- `Issue\d+`, `Task\d+`, branch slugs, `Codex`
- `Generated`, `Regression`, `AI`

If these scan to zero, say that explicitly; it gives the user confidence that
old PR/ticket labels are gone.

## Soft candidates

Flag for human review, not automatic certainty:

- `Coverage` or `Smoke` in suite names. These usually describe a batch, not the
  tested object. Suggested shape: `{System}Tests` or `{ContentArea}Tests`.
- Era words such as `MondainsLegacy`, `SamuraiEmpire`, `ML`, `SE` when they are
  only setup context.

## Era/domain decision rule

Keep era/domain names when they are the tested object or stable domain:

- `MLQuest*`
- `MLPeerlessArtifactsTests`
- `MondainsLegacySourceReferenceTests`
- `SamuraiEmpireSourceReferenceTests`
- Real production helpers such as `MondainsLegacySetArmor` when the test is
  specifically about that helper/family.

Flag era names when the class already names the object and the method starts
with redundant era context, for example:

- `DisarmAbilityTests.MondainsLegacyDisarm...` -> `Disarm...`
- `ParrotContentTests.MondainsLegacyCreatures...` -> `Creatures...`
- `BaseWeaponMondainsLegacyPropertyTests.MondainsLegacyQuiver...` ->
  `Quiver...`

## Report shape

Group findings by confidence:

1. Hard source-of-work prefixes.
2. High-confidence method-prefix cleanup.
3. Generic `Coverage` / `Smoke` suite names.
4. Ambiguous era-prefix class names requiring review.

For each row include file path, line, current name, suggested name, and why it is
or is not certain. Avoid editing unless the user asked to normalize/clean up.
