---
name: "uo-domain-research"
description: "Use when authoring or extending Ultima Online domain knowledge for ModernUO/RebirthUO skills - the workflow for triangulating UO game-mechanics documentation (UOGuide, UO Stratics, uo.com wiki) with the actual repo source (Projects/Server, Projects/UOContent, Distribution/Data, dev-docs, docs/) to produce a class-level UO skill. Use when the user asks for a new UO skill, wants to expand an existing one, or wants to audit a mechanic against canonical UO behavior."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Crome696"
---

# UO Domain Research

## Overview

This umbrella captures the workflow for turning Ultima Online game-design knowledge into ModernUO/RebirthUO skills. The pattern is to triangulate three sources:

1. **UO community documentation** (UOGuide, UO Stratics, uo.com wiki) for the canonical game-mechanics answer ("how does Magic Arrow actually work?", "what are the 7 facets?", "what does Publish 96 change about special moves?").
2. **The actual repo source** (`Projects/Server/`, `Projects/UOContent/`, `Distribution/Data/`, `dev-docs/`, `docs/`) for what ModernUO/RebirthUO has actually implemented and how (which file owns the swing lifecycle, which class registers the 8th-circle summons, which `Region.OnBeginSpellCast` blocks Recall).
3. **In-repo matrix documents** (`docs/mondains-legacy-content-matrix.md`, `docs/server-engine-knowledge-base.md`, the era-analysis tickets, the item-properties-completion plan) which bridge the gap between canonical UO behavior and the current source-level baseline.

The output is a class-level `SKILL.md` that names the engine anchors (file:line, class, method), references the canonical game behavior with a citation, and links to a `references/` support file when the session has pulled longer per-topic detail that would otherwise bloat the main skill.

## When to Use

- Authoring a new UO skill (`uo-*` umbrella) from a domain topic the user names ("skills", "combat", "magic", "world", "crafting", "housing", "pets", "loot").
- Extending an existing UO skill with a mechanic the user calls out ("add the SA-era Mysticism school to `uo-magic-spells`", "add the Quiver of Rage to `uo-combat-pipeline`").
- Auditing whether a ModernUO/RebirthUO behavior matches canonical UO behavior ("does our slayer check match the official table?").
- Building a parity matrix that combines a community source-of-truth with the repo's current implementation status.

Don't use for:

- Pure skill-schema questions (use `hermes-skill-creator`).
- Writing skills about a non-UO topic (this umbrella is UO-specific; for a different game, build a parallel umbrella).
- Per-skill session-specific work (e.g. "add a single spell to Necromancy") - that is a per-skill update, not an umbrella expansion.

## Procedure

The recommended shape of a UO-domain research session is five phases. Each phase has a concrete deliverable; do not skip.

### Phase 1: Define the Domain Boundary

Before touching any source, write a one-paragraph answer to:

- What game-mechanics concept does this skill cover?
- What is the canonical UO name (the name a player would search for on UOGuide)?
- What is the engine anchor (the file:class:method in the repo)?
- What era boundary is the focus (pre-AoS, AoS, SE, ML, SA, ToL, EJ)?
- What is the minimum viable output (3 sections, 5 sections, full coverage)?

If you cannot answer 1-4 cleanly, the domain is too broad - split it before you start. Common splits: "magic" splits into "schools and their spells" vs "the cast pipeline"; "combat" splits into "the swing lifecycle" vs "damage formulas" vs "weapon abilities". The class-level umbrella should be the smallest natural unit, not a kitchen-sink "everything UO" skill.

### Phase 2: Pull the Canonical UO Source

Use `web_extract` and `web_search` to pull from the three trusted UO sources, in this priority:

1. **`uoguide.com`** - the most reliable for spell tables, item property tables, skill taxonomies, race abilities. Start here for almost every mechanic.
2. **`uo.stratics.com`** - the original UO-era feature spotlights (e.g. the AoS Combat Changes page is a primary source for the AoS damage formula). Best for "how was this introduced and what changed in which publish".
3. **`uo.com/wiki/...`** - the official Broadsword wiki, currently active, best for the canonical per-spell and per-skill pages.

For each mechanic, capture:

- The page URL (cite it in the skill's "Related Skills" or in the `references/` support file).
- The exact mechanic the source confirms (e.g. "Publish 96 changed special-move Tactics requirement from 70 to 30 for primary").
- The version date (UOGuide pages carry a "last modified" date in the body; use it to date the citation).
- The source-of-truth version of the data (per-spell mana cost, per-race bonus, per-facet rule).

Limit to the top 5-10 URLs per research session. Citing more is fine; citing fewer is also fine; the goal is to have a defensible source-of-truth for every claim, not exhaustive coverage.

When the web tool returns summarized or truncated content, **do not invent the missing data**. Note the gap and find a better source or flag it in the skill's "Verification" section.

### Phase 3: Map to the Repo Source

For every canonical claim, find the engine anchor. The three search surfaces:

1. **`Projects/Server/`** - engine-core (Item, Mobile, Map, Region, World, Timer, NetState, Serialization). Use `search_files` and `read_file` to find the class and method.
2. **`Projects/UOContent/`** - content scripts (BaseWeapon, BaseArmor, AOS, CraftSystem, Spell subclasses, regions, dungeons). The class hierarchy and the `Def*.cs` registration files are the canonical place to look.
3. **`Distribution/` and `docs/`** - declarative data (map-definitions.json, regions.json, expansions.json, era profiles, monster spawns) and the in-repo matrix documents (mondains-legacy-content-matrix.md, server-engine-knowledge-base.md, era-analysis-tickets.md).

For each engine anchor, capture:

- File path and the relevant `line:col` (or the method signature, which is more readable in prose).
- The class name and the role of the class (one sentence).
- The hook that content uses to interact with the engine (e.g. `Region.OnBeginSpellCast` for travel blocks).
- The era-gate name (e.g. `Core.AOS`, `Core.ML`, `Core.SA`) when the behavior is conditional.

### Fast Recipe: Answering “What Is Still Open?” for an Era Implementation

When the user asks a short follow-up like “what is open?”, “what remains?”, or “what’s left?” after an era implementation/audit discussion, assume they mean **the current era implementation backlog**, not operating-system windows, ports, or generic process state. Do not jump to system-state inspection unless they explicitly ask about the machine.

Use this order:

1. **Recall the active implementation context** with `session_search` if the current chat does not contain the plan/matrix path. Search for the era name plus terms like `implementation plan`, `missing`, `backlog`, or the key mechanics (`Samurai Empire`, `Tokuno`, `Bushido`, `Ninjitsu`).
2. **Read the era matrix first** (`era_<era>.md`, e.g. `era_samurai_empire.md`). The `Known Missing or Inaccurate Backlog` table is the authoritative “open work” answer after implementation begins.
3. **Read the plan second** (`.hermes/plans/*<era>*missing-implementation-plan.md`) to map matrix rows back to task numbers and intended execution order.
4. **Check repo state** (`git status`, `git diff --stat`) to distinguish already-applied-but-uncommitted implementation from genuinely untouched tasks. A row can be “implemented” in the matrix while still uncommitted in git.
5. **Check reports** under `.hermes/reports/` for audit-only slices, especially when the remaining work says “compare”, “validate”, or “manual QA”. These often explain why a row is still Partial.
6. **Separate buckets in the answer:**
   - implemented code/tests but still needs live/manual validation;
   - still Partial because source/property/data parity is incomplete;
   - environment/test-run blockers that prevent local verification;
   - intentionally deferred/out-of-scope follow-ups.
7. **If running tests**, report real output and classify failures. Do not call a feature broken when the test failure is caused by an environment/data prerequisite such as missing client data files.

This pattern is specifically useful for Samurai Empire/Tokuno, Mondain’s Legacy, Endless Journey, and other era matrix work where “open” means “remaining implementation/parity backlog”.

### Fast Recipe: Answering “Is Era X Implemented / Activated?”

When the user asks whether an era such as Endless Journey is implemented and how it was activated, treat it as a source-level activation audit, not a full parity report. Check these anchors in order and separate **core expansion activation** from **profile/policy activation**:

1. **Core enum and era predicates**: `Projects/Server/ExpansionInfo.cs` for `Expansion.<Era>`, feature/client/housing flag aliases, and `ExpansionInfo.Table`; `Projects/Server/Main.cs` for `Core.<Era> => Expansion >= Expansion.<Era>`.
2. **Runtime activation file**: `Distribution/Configuration/expansion.json` is the active runtime config. If it has `Id: 11`, `Name: "Endless Journey"`, and `SupportedFeatures.EJ: true`, then EJ is the configured core expansion.
3. **Canonical metadata**: `Distribution/Data/expansions.json` is the source table for the expansion entry (`RequiredClient`, supported features, character-list flags, housing flags, map selection). Compare the runtime config to this entry when in doubt.
4. **Startup load path**: `ExpansionInfo.LoadConfiguration()` reads `Configuration/expansion.json`; `ServerConfiguration.Load()` assigns `Core.Expansion = currentExpansion`. If the file is missing, `ExpansionConfigurationPrompts.GetExpansion()` selects an expansion and `ExpansionInfo.SaveConfiguration()` writes it.
5. **Era profile layer**: inspect `Distribution/Configuration/EraProfiles/<profile>.json`, `EraProfileManager.Create<Profile>()`, `EraProfileCommands.Configure()`, and `FeatureFlagAdminGump` if the profile can be listed/applied from admin UI. Check `Distribution/Configuration/EraProfiles/active-profile.json`; if it does not exist, the profile exists but is not currently marked active.
6. **Policy completeness**: search for account-policy terms (`TrialAccount`, `LiveAccount`, bank/storage limits, house placement/ownership, IP limits). Do not claim “full EJ implemented” unless those runtime account/storage/housing controls exist. It is usually safer to say “expansion/profile foundation implemented; official EJ account policy still partial” when only expansion flags and profiles exist.

The skill body should cite the engine anchor with the file:line convention used elsewhere in the repo (e.g. `Projects/UOContent/Misc/AOS.cs:37-246`). Cite the *smallest* range that contains the behavior; do not paste large blocks.

### Phase 4: Reconcile Canonical vs Repo

Every claim in the final skill should answer both:

- **What does UO say?** (canonical)
- **What does the repo actually do?** (engine)

When the two diverge, the skill must say so explicitly. The common divergence modes:

- **Pre-AoS path still present**: ModernUO keeps the pre-AoS damage path behind `if (!Core.AOS)`. The skill should describe the pre-AoS path and the AoS path side-by-side.
- **Era-gated but implemented in full**: e.g. ML Spellweaving is registered conditionally in `Initializer.Configure()`. The skill should mention the registration gate.
- **Out of scope by parity choice**: e.g. the ML/SA content matrix documents that some ML monster profiles are "Partial" or "Needs verification". Cite the matrix status, do not claim parity you have not verified.
- **ML content matrix tickets**: `docs/mondains-legacy-content-matrix.md` and `docs/mondains-legacy-crafting-matrix.md` are the source-of-truth for "what is currently implemented vs. the parity target". When a skill documents an ML/SA mechanic, it should cite the matrix's "Status" column for the relevant area.

### Phase 5: Shape Decision/Adoption Reports When the User Must Choose

When the user asks for a report because they need to decide what to adopt, keep, defer, or customize, do **not** stop at a feature-gap summary. Produce a decision-grade report with explicit rationale:

1. Start with a short verdict that separates **content access** from **practical blockers**.
2. Add a decision matrix with columns like `Area`, `Official/canonical rule`, `Current repo evidence`, `Recommendation`, `Why`, `Risk if unchanged`, and `Custom option`.
3. Use direct recommendation verbs: `Adopt`, `Adopt but flag`, `Customize`, `Defer`, `Needs live QA`.
4. Explain the “why” for each row so the user can decide what to carry forward, not just see what exists.
5. Separate strict-canonical profiles from solo-/small-shard-friendly profiles when official UO behavior creates multiplayer, storage, housing, or economy friction.
6. Cite official UO sources inline at the point of the claim and cite local repo anchors with file:line ranges.
7. End with open decision IDs and recommended order of decisions before implementation.

For the Endless Journey / Mondain's Legacy storage, housing, and Arcane Circle decision pattern, see `references/endless-journey-ml-adoption-pattern.md`.

When the user asks for a player-facing 100% completion guide, produce a real Markdown artifact under `docs/` and generate long checklists from source data rather than hand-maintaining them in chat. For the EJ/ML pattern, use `references/endless-journey-ml-no-housing.md`: parse `MLQuests.cfg`, walk the ML monster/item folders, parse `MLPeerlessArtifacts.cs`, include Pre-ML baseline families when requested, and run a coverage script before finalizing.

### Phase 6: Shape the SKILL.md

The class-level skill should follow the same shape as the other UO skills in the library:

1. **Frontmatter** with `name`, `description` (≤ 1024 chars, starts with "Use when..."), `version`, `author`, `license`, `platforms`, `metadata.hermes.tags`, `metadata.hermes.category: software-development`, and the `metadata.cromesdk.sync.*` block (marker, owner, plugin-allowed, cat-source, cat-target) and the three required tags (`cromesdk-personal-skill`, `cromesdk-sync-managed`, `plugin-allowed`). The `related_skills` field should list the UO siblings in the umbrella and the non-UO skills the skill depends on.
2. **Overview** (1-2 paragraphs) that names the engine anchor, the canonical UO concept, and the boundary the skill covers.
3. **When to Use** with bulleted triggers and "Don't use for" counter-triggers.
4. **Body** that reads like a developer reference: tables for taxonomies, code-snippet references for engine anchors, prose for the per-mechanic flow. Each major section should have an "engine anchor" + "canonical UO behavior" pair.
5. **Common Pitfalls** with numbered, engine-specific traps (e.g. "calling `Mobile.Damage` directly on an AoS+ shard").
6. **Common Recipes** with short C# snippets that match the existing skills' style.
7. **Verification Checklist** with checkboxes.
8. **Related Skills** with the local `uo-*` siblings and a "for offline reference" list of the canonical UO URLs pulled in Phase 2.

When the session produces primary research that another session will benefit from (e.g. the per-spell mana/skill table for Magery, the per-facet travel rules, the per-race bonus table), put it in a `references/<topic>.md` support file and link it from the SKILL.md. The umbrella's `references/` directory is the right place for shared research banks that span multiple UO skills.

### Phase 6 (when the task is "audit N items"): Bulk extraction + master-list parse

When the user asks for a parity audit over a *set* of similar items (every weapon, every spell, every monster), do not iterate one `read_file` + one `web_extract` per item. The bulk-extraction recipe below converts a 4-hour task into ~15 minutes:

1. **Find the code pattern once.** Open one representative file (e.g. `Axes/Axe.cs`) and identify the override properties you need (`AosMinDamage`, `AosMaxDamage`, `MlSpeed`, etc.). Note the exact regex pattern; a single `r'public\s+override\s+int\s+AosMinDamage\s*=>\s*(\d+)\s*;'` per stat is enough.
2. **Extract every file in one `execute_code` script.** `Path.rglob("*.cs")` over the relevant folder, read each file once, run all the regexes, dump to JSON. Skip base classes (`name.startswith("Base")`) and helper directories (`Abilities/`, `Artifacts/` if not the target). For 100-200 files this is sub-second.
3. **Find the canonical master list.** For weapons, it's `uo.com/wiki/ultima-online-wiki/items/weapons/` (one table, 126 standard weapons, all stats). For other subsystems, look for a single-page table on `uo.com/wiki/...` or `uoguide.com/...` that lists the whole category.
4. **Parse the master list with `curl` + regex.** `curl -sL -A "Mozilla/5.0" <url> -o /tmp/x.html` then regex-parse the `<table>...</table>`. Section headers often appear as `colspan=N` cells with the category name; data rows are uniform cell counts.
5. **Match by normalized name + ItemID fallback.** `normalize(name) = lowercase + strip non-alnum + collapse spaces`. For ambiguous matches, the C# `[Flippable(0xF49, 0xF4a)]` and `: base(0xF49)` item IDs are a robust secondary key — UOGuide and Stratics always carry the art ID.
6. **Generate per-item source URLs from the class name.** See `references/uo-master-list-extraction.md` for the UOGuide and Stratics URL patterns; this lets you cover 100+ items in one script without a single `web_search`.
7. **Diff + report in markdown.** Sort by category, group by source folder, emit per-category tables + a master diff table + an "unmatched" table. Cite the engine anchor (`file:line`) for any non-trivial code extraction so the next session can verify.

This pattern produced the `Projects/UOContent/Items/Weapons/weapons.md` parity audit in this repo (June 2026): 168 weapons, 85 matched against UO.com, 66 with measurable diffs, in one session.

## Pitfalls

1. **Inverting the order (repo first, web second).** The web sources are what UO actually does; the repo is one implementation of it. A skill built repo-first will encode ModernUO-specific quirks as if they were canonical. Pull the canonical source first, then map to the repo.
2. **Skipping the era gate.** Every pre-AoS, AoS, SE, ML, SA, ToL behavior in UO has a `Core.<Era>` or `RequiredExpansion` check. If the skill claims a behavior without naming the gate, the next session will not know when to apply it.
3. **Record authoritative values and unknowns separately.** When resolving implementation questions from web sources, distinguish values actually sourced from approved tiers from values still unknown. Use non-priority shard wikis only as search breadcrumbs, never as implementation authority. If UO.com/UOGuide/Stratics do not provide an exact timer, probability, coordinate, or mechanic, write `Needs source confirmation` rather than inventing a conservative project policy constant. For example, a source-locked plan may record `Prism ticket = 10,000 gp / 12 hours` from UO.com and `Dread Horn key pieces = 7 days; Essence of Wind = 10 minutes` from UOGuide, while leaving other peerless key durations unresolved until an approved source or explicit user policy decision exists.
4. **Citing a generic UO summary (e.g. "there are 58 skills") as the only source.** Cite the specific UOGuide page or Stratics article. A vague citation is a self-imposed constraint that bites the next session.
4. **Citing the repo without the line number.** `Projects/UOContent/Misc/AOS.cs:37-246` is verifiable; `AOS.Damage in AOS.cs` is not. Always include the line range.
5. **Building a 30 KB SKILL.md that should have been a 12 KB SKILL.md plus a 18 KB references file.** The target shape is class-level SKILL.md + session-specific `references/`. If the body is bloating, split.
6. **Treating "WARN related skill X not in local set" from the validation script as a hard failure.** The script is a sanity check; if a related skill is intentionally external (e.g. a docs file, a web URL), prefix the entry so the check skips it (`www.uoguide.com/...` or `docs/...`).
7. **Using the wrong skill directory.** All UO skills belong under `~/AppData/Local/hermes/skills/software-development/uo-*` and use `category: software-development`. Putting them in `gaming/` is wrong; the category is metadata for the *skill*, not the *game*.
8. **Localizing the skill body.** All skill artifacts are in English by Hermes convention. German/Chinese/etc. content goes in conversation, not in the saved skill.
9. **Skipping `metadata.cromesdk.sync.*` in new skills.** Without the marker, the cromesdk-plugin sync tooling cannot identify the skill as user-owned. The minimum required tags are `cromesdk-personal-skill`, `cromesdk-sync-managed`, `plugin-allowed`.
10. **Forgetting the `category` field in `metadata.hermes`.** The category must match the folder group (e.g. `category: software-development` for `software-development/`). Mismatched category is a metadata lint failure.
11. **Doing 1 web call per item instead of finding the master list.** Many UO subsystems have a single canonical master-list page (e.g. `uo.com/wiki/ultima-online-wiki/items/weapons/` lists every standard weapon in one table). Always check for the master list first; bulk-extracting it once with `curl` + regex beats N parallel `web_extract` calls. See `references/uo-master-list-extraction.md` for the parse recipe and URL generators.
12. **Using `web_search` per item to discover URLs.** UOGuide and Stratics Wiki URLs follow deterministic patterns: UOGuide is `https://www.uoguide.com/{Name_With_Underscores}` (apostrophes → `%27`); Stratics Wiki is `https://wiki.stratics.com/index.php?title=UO:{Name}`. Generate the URL from the code class name, only fall back to a `web_search` if the generated URL 404s.
13. **Treating code-vs-canonical diffs as bugs by default.** When the repo diverges from the canonical UO source, the cause is often an *intentional era gate* (the repo keeps the pre-2016 Revamp stats for a pre-Revamp shard) or a *deliberate parity choice* (the ModernUO project has not yet back-ported Publish 96 special-move changes). Verify with the era enum (`Core.AOS`, `Core.SE`, `Core.ML`, `Core.SA`) and the in-repo `docs/mondains-legacy-content-matrix.md` before flagging the diff as a bug.
14. **Leaving a long UO analysis only in chat.** When the answer becomes a reusable design analysis or content-policy argument, write a standalone Markdown under `docs/` and summarize the path in the final response. This is especially important for German player-/shard-design explanations where the user needs to read and revise the argument outside chat. Keep the chat concise; put the full structured analysis, decision tables, player-facing wording, developer-facing wording, and open questions in the Markdown.
15. **Re-parsing the same source file 168 times in 168 separate `read_file` calls.** When the task is "extract a stat from every class in a folder", one `execute_code` script that does `rglob("*.cs")` + regex per file is dramatically faster and gives you structured JSON you can sort/filter/diff. Only fall back to per-file reads when the regex misses something you need to inspect manually.

## Verification Checklist

- [ ] Web sources are cited with the exact page URL and (when present) the "last modified" date.
- [ ] Repo anchors are cited with the file path and line range, not the file name alone.
- [ ] Era-gate is named for every era-specific behavior.
- [ ] SKILL.md size is 8-25 KB; per-skill detail that would push it past 25 KB lives in `references/`.
- [ ] Frontmatter passes validation: `name` ≤ 64 chars, `description` ≤ 1024 chars and starts with "Use when...", `version` is present, `metadata.hermes.tags` includes the three CromeSDK tags, `metadata.cromesdk.sync.*` is present with the right `marker`/`owner`/`plugin-allowed`.
- [ ] `related_skills` lists the UO siblings and the non-UO dependencies.
- [ ] Any web citations are noted in the SKILL.md's "Related Skills" footer for offline reference, and any longer primary research is parked in `references/<topic>.md` linked from SKILL.md.
- [ ] For parity audits over many items: the bulk-extraction recipe in Phase 6 was used, and the resulting diff table is parked in the repo (e.g. `Projects/UOContent/<Category>/<topic>-parity.md`) for the next session.

## Related Skills

### Sibling UO skills (build these from the same research pattern)

- `uo-items-foundation` - Item entity, Constructible, GetProperties, LootType, Decay.
- `uo-aos-item-properties` - the AoS property containers, the 5 attributes, the property roll.
- `uo-crafting-recipes-resources` - CraftSystem, Def*, subresources, recipes, BODs.
- `uo-magic-spells` - Spell base class, the 6 schools, CastTimer, reagents.
- `uo-combat-pipeline` - BaseWeapon swing, AOS.Damage, resists, slayer, special moves.
- `uo-skills-stats-races` - the 58 skills, the 3 stats, the 3 races, gain mechanics.
- `uo-world-facets-regions` - the 7 facets, Map/Sector, Region hooks, travel, Champion Spawns.

### Companion skills

- `hermes-skill-creator` - strict SKILL.md schema (frontmatter, headings, ordering, validation). Use this for the "is the skill valid?" check; use this umbrella for the "what should the skill contain?" workflow.
- `references/uo-source-tiers.md` (this skill's support file) - a curated index of the canonical UO sources by trust tier and topic, used as the default starting point for any new UO research.
- `references/uo-master-list-extraction.md` (this skill's support file) - the recipe for parity audits over many similar items: master-list URL pattern, `curl` + regex parse, bulk code extraction, name normalization, UOGuide/Stratics URL generators, and the four common code-vs-canonical divergence modes. Use when the task is "audit every X in the repo against canonical UO".
- `references/endless-journey-ml-no-housing.md` (this skill's support file) - condensed notes for Endless Journey / no-housing Mondain's Legacy analysis: content still reachable, housing/storage losses, 20-item bank limit, Arcane Circle group mechanics, and fair custom-solution patterns such as Public Arcane Circle Assist, Peerless Key Binder, whitelisted EJ Quest Vault, and Completion Satchel.
