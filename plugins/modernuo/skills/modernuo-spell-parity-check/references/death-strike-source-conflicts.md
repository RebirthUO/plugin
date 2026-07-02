# Death Strike Source-Conflict Notes

Use this when auditing or implementing the Ninjitsu `Death Strike` formula in ModernUO/RebirthUO. It records the durable source conflict found while reviewing RebirthUO PRs #203/#204 (June 2026), but the guidance is class-level: do not silently treat one source as decisive when Death Strike wording differs by source era and implementation lineage.

## Confirmed Shape

Multiple source tiers agree on the broad mechanic:

- `Death Strike` is Ninjitsu delayed/direct damage.
- The trigger is movement threshold or timer expiry.
- Damage depends on attacker Ninjitsu, movement, tracking/stalking distance, and Hiding/Stealth scaling.
- Ranged weapons deal half Death Strike damage.
- PvP damage is capped.

## Attacker vs Target Hiding/Stealth Conflict

| Source | Claim | Confidence / Use |
|---|---|---|
| UO.com current Ninjitsu page | Damage uses attacker Ninjitsu, **average of the target's Hiding/Stealth**, tracked tiles; PvP capped at 50%. | Official/current wording, but conflicts with older community docs and emulator lineage. Treat as `source-conflict` unless the shard intentionally tracks current official wording. |
| UOGuide Death Strike raw | Damage uses attacker's Ninjitsu, Hiding, and Stealth, plus tracking state; PvP cap is 50. | Canonical-community wording; supports attacker-side skills. |
| UOGuide Ninjitsu raw | Damage uses target movement steps and the **Ninja's** Hiding/Stealth average; ranged weapons do half damage. | Canonical-community wording; supports attacker-side skills. |
| UO.com Publish 46 | Damage scales based on average Hiding/Stealth from 30% to 100%, ranged half, cap lowered to 60. | Official publish note confirms the 30%-100% scalar and ranged/cap changes but does not identify attacker vs target. |
| RunUO / ServUO / ModernUO lineage | ML formula uses **attacker** Hiding + Stealth for the scalar. | Repo/secondary implementation lineage; useful corroboration but not official by itself. |

### Practical Rule

When changing Death Strike formula code/tests:

1. Mark attacker-vs-target Hiding/Stealth as `source-conflict` if both UO.com current wording and UOGuide/emulator lineage matter to the target era.
2. Do **not** rename helpers/tests to `targetHiding` / `targetStealth` unless the project has explicitly chosen current UO.com wording over UOGuide + RunUO/ServUO lineage.
3. If choosing attacker skills, cite UOGuide Ninjitsu/Death Strike and the existing implementation lineage; if choosing target skills, cite UO.com current Ninjitsu and record the divergence.

## PvP Cap Conflict

| Source | Claim | Confidence / Use |
|---|---|---|
| UO.com current Ninjitsu page | `Damage in pvp capped at 50%`. | Ambiguous: could mean 50 damage or 50% of some target value. Do not assume `HitsMax / 2` without a policy decision. |
| UOGuide Death Strike raw | `The damage is capped at 50 for PvP`. | Clear fixed 50 damage cap. |
| UO.com Publish 69 | `Death strike damage capped at 50 verses players`. | Clear fixed 50 damage cap in publish note. |
| ServUO master lineage | Caps player-vs-player Death Strike damage at fixed `50`. | Secondary implementation support for fixed cap. |

### Practical Rule

Default to a **fixed 50 PvP damage cap** unless the issue/era profile explicitly chooses the current UO.com `50%` wording as a custom/current-official policy. If implementing a `HitsMax / 2` cap, add tests above and below 100 `HitsMax` so the policy difference is visible:

- `HitsMax = 80`: half-HP cap = 40, fixed cap = 50.
- `HitsMax = 100`: both equal 50.
- `HitsMax = 120`: half-HP cap = 60, fixed cap = 50.

### Rebase / Review Pitfall

When rebasing a Death Strike cap PR after a sibling formula PR has merged, inspect the combined runtime path, not just whether conflicts are additive. A branch that adds `ApplyPvpDamageCap(target.HitsMax / 2)` on top of a base that already applies `GetMlDirectDamage(... useFixedPvpCap: Core.HS)` can silently create a mixed rule: `min(fixed 50, target.HitsMax / 2)` on HS/current ML while also applying the half-Hits cap to non-HS ML or legacy physical paths. That is a source-policy change and should be reviewed as `changes requested` unless the issue/era profile explicitly chooses the half-Hits interpretation and defines which `Core.*` eras it applies to.

Tests with a 100 HP defender are insufficient because fixed 50 and half-Hits both equal 50. Require differentiating cases above and below 100 HP plus a runtime/order assertion when both fixed-cap and post-helper cap paths can compose.

## Source URLs

- UO.com Ninjitsu: https://uo.com/wiki/ultima-online-wiki/skills/ninjitsu/
- UOGuide Death Strike raw: https://www.uoguide.com/index.php?title=Death_Strike&action=raw
- UOGuide Ninjitsu raw: https://www.uoguide.com/index.php?title=Ninjitsu&action=raw
- UO.com Publish 46: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2007-2/publish-46-9th-august/
- UO.com Publish 69: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2010-2/publish-69-16th-december/
