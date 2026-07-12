---
name: uo-living-world-review
description: Use when reviewing UO/RebirthUO changes for era/ruleset, facet/map, player-loop, economy, housing, PvP/PvM, trust, and source-evidence side effects before code or policy recommendations.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    skill_group: uo
    skill_subgroup: gate
    workflow_phase: none
    workflow_tier: support
    tags:
    - UltimaOnline
    - RebirthUO
    - Product
    - Parity
    related_skills:
    - uo-product-model
    - uo-era-product-timeline
    - uo-era-publish-source-gate
    - uo-modernuo-workflow
license: MIT
---
# UO Living-World Review

## Overview

Use this skill to keep Ultima Online and RebirthUO work grounded in the game as a living product: era, map, loops, trust, economy, and player consequences. It does not replace code-domain skills or parity research; it is the first-pass gate that decides what must be verified before code, triage, balance, or documentation work proceeds. It uses Hermes tools only and depends on source-backed UO evidence rather than memory or unsupported product claims.

## When to Use

- The user asks about Ultima Online, RebirthUO, ModernUO, shard rules, era parity, content, mechanics, or balance.
- A task may affect gameplay, maps, housing, vendors, economy, PvP, PvM, progression, social systems, or player trust.
- A code change looks small but could alter risk, reward, storage, travel, loot, skill gain, insurance, murder/criminal behavior, or housing memory.
- The user asks to check, audit, verify, triage, plan, implement, or explain a UO feature.
- A claim sounds like product knowledge but lacks UO.com, UOGuide, Stratics, issue, or repo evidence.

## Prerequisites

- No credentials or environment variables are required.
- Local RebirthUO repo when available: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`.
- Trusted source tiers: UO.com first for current official wording, UOGuide for mechanics/history tables, Stratics for era context, then issue-supplied evidence and repo anchors.
- Load narrower UO or ModernUO skills with `skill_view` after this gate identifies the domain, such as combat, housing, crafting, era parity, serialization, gumps, or tests.

## How to Run

Invoke this skill at the start of the UO task through `skill_view`, then gather source and repo evidence before recommending behavior. Use `web_extract` or `browser_navigate` for UO.com, UOGuide, and Stratics pages; use `search_files` and `read_file` for repo anchors; use `terminal` only for git, build, test, or runtime checks. If the current tools cannot fetch a source, say which source was unavailable and mark the claim as unresolved instead of filling the gap from memory.

## Quick Reference

- `https://uo.com/`
- `https://uo.com/wiki/ultima-online-wiki/`
- `https://www.uoguide.com/`
- `https://uo.stratics.com/`
- `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service`
- `Distribution/Data/expansions.json`
- `Distribution/Data/map-definitions.json`
- `Projects/Server/ExpansionInfo.cs`
- `Projects/Server/Main.cs`
- `Projects/UOContent/Misc/Notoriety.cs`
- `Projects/UOContent/Multis/Houses/BaseHouse.cs`
- `Projects/UOContent/Engines/Craft/Core/CraftSystem.cs`

## Procedure

1. **State the assumption frame.** Write the assumed shard/ruleset, era or expansion, facet/map, and whether the task is canonical parity or custom shard policy. The step is done only when unknowns are explicitly labeled instead of silently guessed.

2. **Identify the player loops.** Classify the feature into progression, PvM, PvP, economy/crafting/vendors, housing/storage/IDOC, travel/maps, social/guilds, events, or client presentation. The step is done only when at least one affected loop and one possibly unaffected loop are named.

3. **Pull product evidence first.** Use `web_extract` or `browser_navigate` for UO.com, UOGuide, or Stratics before treating a product claim as canonical. The step is done only when the answer can cite a URL or says `Needs source confirmation` for the missing value.

4. **Map to repo evidence second.** Use `search_files` for symbols, data names, feature flags, and content folders, then use `read_file` to inspect the smallest file range that proves the local behavior. The step is done only when the answer has concrete repo anchors such as file paths, classes, methods, data files, or line ranges.

5. **Check side effects before proposing a fix.** For each change, fill this row: era/ruleset, facet/map, benefited player loop, harmed or stressed player loop, economy faucet/sink/storage impact, PvP counterplay impact, PvM risk/reward impact, housing/trust impact, save/client compatibility, and exploit or bot risk. The step is done only when the side-effect row is present or explicitly not applicable.

6. **Separate canonical, repo, and custom.** Use `Canonical` for UO.com/UOGuide/Stratics-backed behavior, `Repo evidence` for what RebirthUO currently does, `Issue-supplied` for GitHub issue evidence, and `Custom policy` for shard decisions. The step is done only when the final wording does not present repo-only or issue-only evidence as official UO truth.

7. **Choose the smallest safe action.** Prefer evidence gathering, a focused test, a reversible config change, or a narrow code change before broad balance rewrites. The step is done only when rollback, validation, and monitoring are described for live-impacting changes.

8. **Verify before finalizing.** For code or docs, run the relevant `terminal` build/test/checks or use `search_files` and `read_file` to prove the referenced anchors exist. For research-only answers, verify every external claim has a source URL or is marked unresolved. The step is done only when the final answer includes real verification output or a clear blocker.

9. **Learn incrementally.** When the task produces reusable domain knowledge, improve a focused skill with `skill_manage` rather than bloating this gate. The step is done only when the new learning is either saved to a skill or intentionally skipped as task-specific.

## Pitfalls

- Do not answer UO mechanics from memory when a UO.com, UOGuide, Stratics, issue, or repo source can be checked.
- Do not assume live UO, pre-AoS, Renaissance, AoS, SE, ML, SA, ToL, EJ, or custom RebirthUO rules are interchangeable.
- Do not treat a class existing in the repo as proof that a feature is live; check registration, era gates, config, data, map access, spawns, and tests.
- Do not reduce Felucca to PvP only or Trammel to safety only; both affect resources, travel, stealing, fields, guards, vendors, and player social patterns.
- Do not make housing or storage changes casually; they affect trust, memory, vendors, IDOCs, economy, and long-term shard identity.
- Do not balance from one anecdote; separate logs, reproduction, source behavior, player skill, gear, group size, and counterplay.
- Do not hide uncertainty. Use `Needs source confirmation`, `Repo evidence only`, or `Custom policy decision needed` when evidence is incomplete.
- Do not let a /learn round become a broad encyclopedia. Save one reusable decision pattern or mechanic boundary at a time.

## Verification

The skill worked if a UO/RebirthUO answer begins with era/ruleset, facet/map, player loops, side effects, source URLs, repo anchors, and explicit unknowns before any code or policy recommendation.
