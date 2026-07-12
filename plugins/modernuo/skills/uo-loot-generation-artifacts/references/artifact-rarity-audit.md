# Artifact Rarity Audit Notes

Use this reference when asked whether Artifact Rarity is implemented or
complete in the configured ModernUO-based repository.

## What to check

1. **Base display plumbing**
   - `Projects/UOContent/Items/Weapons/BaseWeapon.cs` should expose `public virtual int ArtifactRarity => 0;` and add `list.Add(1061078, ArtifactRarity)` when positive.
   - `Projects/UOContent/Items/Armor/BaseArmor.cs` should do the same; shields inherit through `BaseShield : BaseArmor`.
   - `Projects/UOContent/Items/Clothing/BaseClothing.cs` and `Projects/UOContent/Items/Jewels/BaseJewel.cs` should do the same.
   - Decoration artifacts may use a dedicated base such as `BaseDecorationArtifact` / `BaseDecorationContainerArtifact` with abstract `ArtifactRarity` and `ForceShowProperties`.

2. **Coverage, not just plumbing**
   - Search for `ArtifactRarity` and `1061078` separately. `ArtifactRarity` proves value assignment; `1061078` proves tooltip emission.
   - Count `public override int ArtifactRarity => N` by artifact family. Compare against expected era/content families rather than assuming every file under an `Artifacts` folder should have a rarity.
   - Check artifact-like families with no override (Tokuno lesser/greater, ML craftables, Champion replicas/decoratives/uniques, minor artifacts, peerless-style ML artifacts) and classify each as either intended no-rarity or missing parity evidence.

3. **Drop/use-site relevance**
   - Doom/AoS Demon Knight artifacts use `DemonKnight.ArtifactRarity10` / `ArtifactRarity11`; this is independent from tooltip display but is useful evidence that rarity tiers affect artifact selection/weighting.
   - Dye/turn-in systems can reference artifact type lists (`BasePigmentsOfTokuno` checks multiple artifact pools); do not treat tooltip-only implementation as complete economy/gameplay coverage.

4. **Tests to look for or add**
   - Positive case: an artifact with `ArtifactRarity > 0` emits cliloc `1061078` with the expected value.
   - Negative case: a normal item with `ArtifactRarity == 0` does not emit `1061078`.
   - Family coverage case: representative Doom/AoS weapon/armor/clothing/jewel/shield artifacts expose their expected rarity.
   - If no tests match `ArtifactRarity` or `1061078`, report the implementation as present but not fully regression-protected.

## Reporting pattern

Use a two-tier answer:

- **Narrow scope**: “yes” if base classes expose `ArtifactRarity` and tooltips emit cliloc `1061078` for positive values.
- **Full/parity scope**: “not sufficient yet” if there is no coverage matrix/tests or if major artifact families lack explicit intended-no-rarity documentation.

Always state the assumed era/ruleset. Artifact rarity is especially relevant to AoS/Doom/SE-era artifact systems and may not apply uniformly to every later or custom artifact family.
