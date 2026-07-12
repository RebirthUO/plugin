# ModernUO Skill Coverage Audit

Read this reference for a full skill-library inventory or gap report. Use `rg` and
runtime-provided discovery tools; skip paths/resources that do not exist.

## Inventory fields

For every discovered skill record:

- name and source location;
- source type: `installed`, `attached`, `repository`, `referenced`, or `unknown`;
- description/triggers and near neighbors;
- covered systems, rules, failure modes, output contract, and verification;
- references/scripts/assets actually used;
- overlap, stale content, tool/vendor coupling, and proposed action.

Inspect runtime-exposed skills, project plugin folders, repository instruction
files, and conventional `skills/`, `.skills/`, `.claude/skills/`, `agent/skills/`,
or `agents/skills/` locations only when present.

## Mechanical scan

Useful repository-root searches:

```text
rg --files -g 'SKILL.md'
rg -n '^(name:|description:|version:|author:|metadata:|# |## )' --glob 'SKILL.md'
rg -n 'must|never|always|warning|critical|anti-pattern|migration|serialization|hot path' dev-docs docs
rg -n 'OnDelete|OnAfterDelete|Serialize\(|Deserialize\(|Configure\(|Initialize\(' Projects
rg -n 'Task\.Run|new Thread|World\.Mobiles|World\.Items|ArrayPool|StringBuilder' Projects
```

Use a YAML parser and an actual Markdown-link resolver for validation; regex alone
cannot prove frontmatter or relative-link correctness.

## Coverage labels

- `covered`: accurate trigger, rules, workflow, output, and verification exist.
- `partial`: an existing skill owns the domain but misses material behavior.
- `missing`: no existing skill owns the recurring job.
- `duplicate`: a proposed skill substantially overlaps an existing owner.
- `vendor-specific but usable`: guidance is useful but tool-branded.
- `needs generalization`: project guidance should become runtime-neutral.
- `research needed`: evidence is insufficient for durable rules.

## Priority labels

- `P0`: save corruption, data loss, exploit, crash, severe performance, or client
  protocol risk.
- `P1`: frequent complex domain with likely implementation mistakes.
- `P2`: useful maintenance/onboarding coverage with lower risk.
- `P3`: niche, rare, speculative, or better folded into an existing owner.

## New-skill gate

Recommend a new skill only when evidence demonstrates:

1. a recurring job;
2. a reusable output contract;
3. distinct activation and near-neighbor exclusions;
4. domain-specific lifecycle/API/failure rules;
5. enough source evidence to verify guidance.

Otherwise patch the existing owner, record `research needed`, or place the idea
under not recommended.

## Report shape

Return:

1. summary counts and highest-risk gap;
2. skill inventory;
3. existing coverage matrix with evidence paths;
4. recommended updates;
5. new candidates with priority/confidence/overlap check;
6. not-recommended duplicates;
7. validation results and remaining research searches.

For implementation, add a changed-file list, trigger/boundary before/after,
context-size results, broken-link/YAML status, and explicit non-scoped issues.
