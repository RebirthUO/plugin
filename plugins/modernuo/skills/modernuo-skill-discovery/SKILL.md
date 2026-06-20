---
name: modernuo-skill-discovery
description: Trigger when asked to analyze the ModernUO codebase, inspect installed or attached skills, compare repository patterns against existing skill coverage, and discover missing or under-covered skills that would improve development, review, migration, onboarding, or automation quality.
---

# ModernUO Skill Discovery

Use this skill to audit ModernUO repository patterns against every discoverable skill source and identify evidence-backed gaps in the skill library. Be conservative: inventory existing skills first, read current repository evidence, compare coverage semantically, and recommend updates before proposing new skills.

Do not edit files unless explicitly asked. Do not delete, rename, merge, collapse, or rewrite existing skills unless explicitly asked. Do not run destructive commands.

## Workflow

1. Inventory skills before scanning for new candidates.
2. Inspect repository guidance, developer docs, conventional skill folders, and ModernUO source domains.
3. Extract each discovered skill's name, source location, source type, description, covered systems, key rules, anti-patterns, examples, related documentation, overlap, gaps, and whether it is generic or tool-specific.
4. Compare repository patterns against skill coverage by meaning, not only by filename or heading.
5. Propose new skills only when repository evidence shows a distinct domain with lifecycle rules, APIs, anti-patterns, or recurring code patterns.
6. Prefer updating an existing skill when the gap is small.
7. Mark uncertain recommendations as `research needed`.

## Skill Sources To Inspect

Inspect all available skill sources. Do not assume only one skill directory exists.

- Skills installed in the current assistant or AI agent environment, if discoverable.
- Skills attached to the current task or session.
- Skills bundled with the project repository.
- Skill files referenced by project documentation.
- Conventional repository directories: `skills/`, `.skills/`, `dev-docs/skills/`, `dev-docs/claude-skills/`, `.claude/skills/`, `docs/skills/`, `tooling/skills/`, `agent/skills/`, `agents/skills/`.

Inspect these ModernUO locations when available:

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `.cursorrules`
- `dev-docs/`
- `docs/`
- `skills/`
- `.skills/`
- `dev-docs/skills/`
- `dev-docs/claude-skills/`
- `.claude/skills/`
- `Projects/Server/`
- `Projects/UOContent/`
- `Projects/Tests/`
- `Projects/BuildTool/`

## Inventory Commands

Use the commands below from the repository root when the paths exist. Prefer `rg` for speed. Use platform equivalents only when the shell does not support these commands.

```bash
find . -type f \( -iname '*skill*.md' -o -path '*/skills/*' -o -path '*/.skills/*' \) | sort
find . -type d \( -iname 'skills' -o -iname '.skills' -o -iname '*skills*' \) | sort
rg -n "^(name:|description:|# |## |---)" . --glob '*.md'
rg -n "skill|skills|agent|assistant|instructions|onboarding|workflow" README.md CLAUDE.md AGENTS.md GEMINI.md .cursorrules dev-docs docs 2>/dev/null
```

For each discovered skill, record:

- Skill name.
- Source location.
- Source type: `installed`, `attached`, `repository`, `referenced`, or `unknown`.
- Description and trigger conditions.
- Covered systems.
- Key rules.
- Anti-patterns.
- Real examples.
- Related documentation.
- Overlap with other skills.
- Missing examples or trigger conditions.
- Whether the skill is generic or tool-specific.
- Whether the skill should be updated, replaced, generalized, or left unchanged.

## Developer Docs Scan

Scan developer docs for:

- Rules.
- Anti-patterns.
- `must`, `never`, `always`, `critical`, or `warning` statements.
- Code examples.
- Migration notes.
- Performance-sensitive patterns.
- Serialization or save-compatibility guidance.
- Agent-specific instructions.
- Project-specific terminology.
- Repeated developer workflows.

```bash
find dev-docs docs -type f -name '*.md' 2>/dev/null | sort
rg -n "MUST|Must|must|Never|never|Always|always|WARNING|Warning|CRITICAL|Critical|Anti-Pattern|Pattern|Rule|rule|migration|serialization|performance|hot path|allocation" dev-docs docs 2>/dev/null
```

## Codebase Scan

Scan source code for domains that may deserve skill coverage:

- Server lifecycle and startup.
- Serialization and migrations.
- Items, mobiles, creatures.
- Skills and abilities.
- Spells and combat.
- AI and pathfinding.
- Gumps and UI.
- Commands and targeting.
- Regions and maps.
- Events and schedulers.
- Timers.
- Networking and packets.
- Accounts and persistence.
- Housing.
- Vendors.
- Guilds and factions.
- Crafting.
- Loot.
- Spawners.
- Quests.
- Localization and cliloc handling.
- Logging and diagnostics.
- Memory, pooling, and string handling.
- Tests, benchmarks, build tooling, and release tooling.

Use representative searches:

```bash
find Projects -maxdepth 3 -type d | sort
rg --files Projects | sed 's#^Projects/##' | cut -d/ -f1-3 | sort | uniq -c | sort -nr | head -100
rg -n "class .*: .*" Projects/Server Projects/UOContent
rg -n "class .*: (Item|Mobile|BaseCreature|BaseWeapon|BaseArmor|Spell|Gump|StaticGump|DynamicGump|Region|Packet|GenericPersistence)" Projects
rg -n "\[(SerializationGenerator|SerializableField|SerializableProperty|Constructible|AfterDeserialization|CommandProperty|SerializedCommandProperty|Usage|ConfigProperty|TypeAlias)\]" Projects
rg -n "(OnThink|OnMovement|OnDoubleClick|OnDragDrop|OnDelete|OnAfterDelete|Serialize\(|Deserialize\(|Configure\(|Initialize\(|BuildLayout|OnResponse)" Projects
rg -n "(Console\.WriteLine|Console\.Write|Task\.Run|new Thread|ThreadPool\.QueueUserWorkItem|lock\s*\(|volatile |ConcurrentDictionary|World\.Mobiles|World\.Items|ArrayPool\.Shared|new List<|StringBuilder)" Projects
rg -n "(BaseAI|Pathfind|AStar|Combatant|Damage|SpellHelper|SkillCheck|BaseVendor|BaseHouse|Quest|Spawner|Loot|Localization|cliloc|BuffInfo|ContextMenu|Notoriety|Faction|Guild|Account|CraftSystem|HarvestSystem)" Projects
```

## Coverage Classification

Use these exact labels:

- `covered`: An existing skill clearly covers the domain with accurate triggers, rules, and examples.
- `partial`: An existing skill mentions the domain but lacks important rules, examples, or activation conditions.
- `missing`: No existing skill covers the domain well.
- `duplicate`: A proposed skill would overlap too much with an existing skill.
- `vendor-specific but usable`: A skill is tied to a specific tool or agent name, but its guidance is still relevant.
- `needs generalization`: A skill contains useful project guidance but should be rewritten in neutral language.
- `research needed`: There is evidence, but not enough to safely draft rules.

If an existing skill is tool-specific but its content is generally useful, classify the content neutrally and avoid recommending a duplicate generic replacement unless there is a clear maintenance reason.

## Priority Labels

Use these exact priorities for proposed skills:

- `P0`: Critical. High risk, frequent edits, possible save corruption, crash, exploit, data loss, severe performance regression, or client-breaking behavior.
- `P1`: High value. Common development area with complex conventions and likely AI agent mistakes.
- `P2`: Medium value. Useful for onboarding or maintenance but lower risk.
- `P3`: Low value. Niche, rare, speculative, or better handled inside another skill.

## Recommendation Rules

- Do not invent missing skills from intuition.
- Ground every proposed skill in repository evidence.
- Use exact file paths and line numbers where possible.
- Include `rg` counts or representative matches when useful.
- Compare against all discoverable installed, attached, bundled, referenced, and repository-provided skills.
- Recommend a new skill only when the domain has distinct lifecycle rules, APIs, anti-patterns, or recurring code patterns.
- Prefer updating an existing skill when the gap is small.
- Put uncertain candidates under `research needed`.
- Put overlapping candidates under `Not Recommended`.

## Final Report

Use this structure for the final report:

```markdown
# ModernUO Skill Discovery Report

## Summary

- Installed skills reviewed:
- Attached skills reviewed:
- Repository skills reviewed:
- Referenced skills reviewed:
- Developer docs reviewed:
- Code domains scanned:
- Candidate new skills:
- Existing skills needing updates:
- Existing skills needing neutralization/generalization:
- Highest-value gap:

## Skill Inventory

| Skill | Source | Type | Description | Covered Domain | Notes |
|---|---|---|---|---|---|

Source type must be one of:
- installed
- attached
- repository
- referenced
- unknown

## Existing Skill Coverage

| Skill | Covered Domain | Evidence | Coverage Quality | Notes |
|---|---|---|---|---|

Coverage quality must be one of:
- covered
- partial
- duplicate
- vendor-specific but usable
- needs generalization
- research needed

## Domain Coverage Matrix

| Domain | Evidence | Existing Skill Coverage | Gap | Recommendation |
|---|---|---|---|---|

## Recommended New Skills

For each candidate:

### Priority: skill-name

**Why this matters:**

**Evidence:**
- path/file.cs:line - observed pattern
- path/doc.md:line - related rule or documentation
- rg count or representative matches

**Overlap check:**

**Existing skills compared:**

**Suggested activation triggers:**

**Suggested skill outline:**
- Purpose
- When this activates
- Key rules
- Patterns
- Anti-patterns
- Real examples
- See also

**Confidence:** high / medium / low

## Existing Skills to Update

| Skill | Missing Content | Evidence | Suggested Change |
|---|---|---|---|

## Existing Skills to Generalize or Neutralize

| Skill | Current Issue | Evidence | Suggested Neutral Version |
|---|---|---|---|

## Not Recommended

| Candidate | Reason |
|---|---|

## Follow-Up Searches

List commands that should be run next to confirm uncertain candidates.
```

## Drafting New Skills

Draft a new skill only when explicitly requested. A drafted new skill must include:

- YAML front matter with `name` and `description`.
- Purpose.
- When This Activates.
- Key Rules.
- Patterns.
- Anti-Patterns.
- Real Examples.
- How to Report Issues.
- See Also.

Keep drafted skills neutral. Refer to `AI agent`, `assistant`, `skill`, `repository`, `project`, and `development workflow` instead of vendor-specific terms unless an existing repository path or document name must be cited as evidence.

## How to Report Issues

When this skill finds a problem or leaves an uncertainty, report the smallest reproducible evidence:

- Task or trigger that activated the skill.
- Relevant repository path and line, or external source URL/date when parity research is involved.
- Risk category: save compatibility, client behavior, performance, economy, security, era parity, or operator workflow.
- Validation performed, including commands run or why a runtime/manual check is still needed.
- Open questions or source conflicts that need user judgment.
