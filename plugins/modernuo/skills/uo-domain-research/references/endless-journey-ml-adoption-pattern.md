# Endless Journey / Mondain's Legacy Adoption Report Pattern

Use this reference when the user needs a decision-grade UO report rather than a simple parity/gap summary, especially for Endless Journey (EJ), Mondain's Legacy (ML), storage, housing, account policy, or solo-friendly custom rules.

## Core Lesson

A report meant to support adoption decisions must explain **what to take, what not to take, and why**. Do not only say “feature X is implemented/missing.” The user needs to choose between canonical UO behavior, RebirthUO implementation state, and intentional custom shard policy.

## Recommended Report Shape

1. **Kurzfazit / Verdict**
   - State the useful truth in one paragraph.
   - Separate “content is reachable” from “practical play is blocked by storage/housing/multiplayer friction.”

2. **Decision framework**
   - Define decision labels: `Adopt`, `Adopt but flag`, `Customize`, `Defer`, `Needs live QA`.
   - Say whether the report is source-level, policy-level, or live-QA-level.

3. **Decision matrix**
   - Use columns:
     - `Area`
     - `Official/canonical rule`
     - `Current repo evidence`
     - `Recommendation`
     - `Why`
     - `Risk if unchanged`
     - `Custom option`

4. **Reachability honesty section**
   - What can truthfully be called “nearly complete” or “reachable.”
   - What is still not practical despite source/content access.

5. **Detailed recommendations**
   - One subsection per high-impact policy area.
   - Explain not just the rule, but the player impact and engineering risk.

6. **Profile proposals**
   - Keep strict-canonical and solo-friendly profiles separate.
   - Example shape:
     - `endless-journey-strict`: official EJ behavior.
     - `ej-solo-friendly`: account/key/resource lockers and capped solo helpers.
     - `ml-baseline`: pure ML boundary without EJ account restrictions.

7. **Implementation notes**
   - Prefer profile/config/feature flags over hardcoded policy.
   - Keep ML parity separate from EJ account-policy restrictions.
   - In ModernUO/RebirthUO, avoid `Projects/Server/` changes unless explicitly approved by repo instructions.

8. **Open decision IDs**
   - End with decision IDs so the next session can implement or ask targeted questions.
   - Example: `EJ-STORAGE-001`, `EJ-HOUSING-001`, `EJ-ARCANE-001`, `EJ-IP-001`.

## EJ / ML-Specific Guidance

### Content access vs practical blockers

Official EJ can grant broad content and skill access while still restricting storage, housing, vendors, and account/session behavior. Report these separately. Saying “ML is nearly reachable” is only honest if the report also calls out practical blockers like:

- 20/28-item bank limits.
- No house ownership/co-ownership.
- No mailbox, locked-down/secure container, or auction-safe placement.
- Weak or absent player economy on small shards.
- Arcane Circle requiring other qualified arcanists.

### Arcane Circle is a special blocker

Treat Arcane Circle as a gameplay gate, not just convenience. Official Spellweaving sources describe cooperative focus creation by the caster plus up to four arcanists within skill range. If local code also requires at least one other `PlayerMobile`, solo play is mechanically blocked unless the shard provides another solution.

Good custom options:

- Arcane-circle assistant NPC or circle controller.
- Requires Spellweaving unlock/quest context.
- Works only at defined public circles.
- Costs gold/resource/cooldown.
- Solo focus capped below full group strength.
- Real group casting remains best.

Bad custom option:

- Full strength 5/6 solo focus with no cost or gate. This erases the cooperative ML mechanic.

### Storage customizations

For solo-friendly shards, prefer specialized storage instead of simply raising the universal bank limit:

- Account/Inn Locker for bounded general storage.
- ML Key Locker for peerless/dungeon keys.
- Recipe Binder for learned/unlearned recipe scrolls.
- Resource Depot for stackable crafting resources.

This preserves the EJ idea of limited universal storage while removing ML-specific friction.

## Citation Rules

- Cite official UO pages inline where the claim appears.
- Cite local repo anchors with file:line ranges.
- For policy claims, use official UO.com first, then UOGuide/UO Stratics/Stratics Community Wiki as cross-checks.
- For implementation claims, cite `Distribution/Configuration/EraProfiles/*.json`, `Projects/UOContent/**`, `Projects/UOContent.Tests/**`, and `docs/*matrix*`/`*ledger*` documents.

## Output Style

If the user asks in German, write the report in German unless they specify otherwise. Keep code/repo artifact names in English. Use enough detail for a real decision: a terse bullet summary is not enough for adoption-policy work.
