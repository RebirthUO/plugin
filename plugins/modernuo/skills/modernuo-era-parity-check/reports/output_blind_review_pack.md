# Output Blind A/B Review Pack

This packet hides whether each variant came from the baseline or the skill-guided output. Use the separate answer key only after review.

- Pairs: `2`
- Seed: `yao-output-eval-blind-v1`
- Answer key separate: `True`

## Case: monster_delta_required

Prompt: Run a Samurai Empire monster parity excerpt for Yomotsu Elder.

Rubric:
- `has_expected` (2.0): Risk rows include expected behavior.
- `has_modernuo_evidence` (2.0): Risk rows include path-backed ModernUO evidence.
- `has_delta_matrix` (2.0): Risk rows include a Delta Matrix.
- `reject_confirmation_only` (1.0): Final risk rows must not rely on confirmation-only wording.

### Variant A

| Name | State | Issue | Recommendation |
|---|---|---|---|
| Yomotsu_Elder | Partial | Needs confirmation; missing Axe Throw | Verify later |

### Variant B

## Entity / System Detail

| Name | State | Era | Source | Expected | ModernUO Evidence | Delta | Validation | Impact | Accuracy % | Recommendation |
|---|---|---|---|---|---|---|---|---|---:|---|
| Yomotsu_Elder | Partial | Samurai Empire | https://www.uoguide.com/Yomotsu_Elder | UOGuide creature table plus Axe Throw special | `Projects/UOContent/Mobiles/Monsters/SE/YomotsuElder.cs:88` has TODO for Axe Throw and no ability hook | Missing ability hook | confirmed | PvM balance / era parity | 65% | Implement or intentionally defer Axe Throw; add parity test |

## Delta Matrix

| Aspect | Name | Field | Expected | ModernUO Evidence | Delta | Validation |
|---|---|---|---|---|---|---|
| Monsters | Yomotsu_Elder | Ability | Axe Throw special | `YomotsuElder.cs:88` TODO / no hook | Missing ability hook | confirmed |

## Case: crafting_research_required

Prompt: Report an unclear Samurai Empire crafting discrepancy.

Rubric:
- `open_research` (2.0): Unresolved crafting claims move to Open Research with checked sources.
- `crafting_delta_status` (2.0): Crafting uncertainty is represented as open-research, not a final partial claim.
- `reject_confirmation_only` (1.0): Confirmation-only crafting issue wording is forbidden.

### Variant A

| Name | State | Issue | Recommendation |
|---|---|---|---|
| Bokuto | Partial | Crafting needs confirmation | Confirm crafting |

### Variant B

## Open Research

- EPC-OR-1: Bokuto crafting skill requirement differs across available notes - Checked: UO.com crafting index, UOGuide Bokuto page, `Projects/UOContent/Engines/Craft/DefBlacksmithy.cs`, `Projects/UOContent/Engines/Craft/DefCarpentry.cs` - Missing evidence: exact OSI-era recipe skill and resource count - Next step: verify source table or runtime craft menu for Samurai Empire profile

## Delta Matrix

| Aspect | Name | Field | Expected | ModernUO Evidence | Delta | Validation |
|---|---|---|---|---|---|---|
| Crafting | Bokuto | Recipe requirement | Source conflict; exact OSI-era requirement not confirmed | Craft definitions checked; no final source-backed mismatch yet | No confirmed delta; moved to Open Research | open-research |
