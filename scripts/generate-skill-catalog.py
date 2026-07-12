#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\plugins\modernuo\skills")
out = root / "SKILL-CATALOG.md"

rows: dict[str, list[tuple[str, str, str, str]]] = {"uo": [], "modernuo": [], "rebirthuo": []}
for d in sorted(root.iterdir()):
    if not d.is_dir() or d.name.startswith("."):
        continue
    md = d / "SKILL.md"
    if not md.exists():
        continue
    t = md.read_text(encoding="utf-8")
    name = d.name
    desc_m = re.search(r"^description:\s*(.+)$", t, re.M)
    desc = (desc_m.group(1).strip().strip('"') if desc_m else "")[:100]
    group = re.search(r"skill_group:\s*(\w+)", t)
    subgroup = re.search(r"skill_subgroup:\s*(\w+)", t)
    phase = re.search(r"workflow_phase:\s*(\w+)", t)
    g = group.group(1) if group else "modernuo"
    sg = subgroup.group(1) if subgroup else "domain"
    ph = phase.group(1) if phase else "none"
    rows.setdefault(g, []).append((name, sg, ph, desc))

lines = [
    "# Skill Catalog",
    "",
    "Curated index for the ModernUO plugin skill payload (75 skills). Skills stay in a flat `skills/<name>/` layout; grouping is via frontmatter (`skill_group`, `skill_subgroup`, `workflow_phase`, `workflow_tier`).",
    "",
    "See [README.md](../../README.md) for sync contract and [uo-modernuo-workflow/SKILL.md](uo-modernuo-workflow/SKILL.md) for routing.",
    "",
    "## Agentic Workflow (Primary)",
    "",
    "| Phase | Skill | Repository | Notes |",
    "|---|---|---|---|",
    "| Create | `rebirthuo-issue-create` | `RebirthUO/rebirthuo` | Label `needs-review` |",
    "| Review | `rebirthuo-issue-review` | `RebirthUO/rebirthuo` | Use with `rebirthuo-review-patterns` |",
    "| Implement | `rebirthuo-implement` | `RebirthUO/ModernUO` | Canonical implementation skill |",
    "",
    "**Companion skills:** `rebirthuo-implementation-checkpoints`, `modernuo-test-workflow`, `modernuo-code-audit`, `modernuo-verification-guard`.",
    "",
    "**Escape hatch (direct ModernUO issues):** `modernuo-issue-create`, `modernuo-issue-review`, `modernuo-issue-implement`, `modernuo-issue-template-gate` (`workflow_tier: direct-modernuo`).",
    "",
    "## Removed / Deprecated",
    "",
    "| Skill | Action | Redirect |",
    "|---|---|---|",
    "| `ultima-online-product-model` | removed | `uo-product-model` |",
    "| `rebirthuo-implementation` | removed | `rebirthuo-implement` |",
    "",
    "## migrate-* → modernuo-* Pairs",
    "",
    "| migrate | modernuo counterpart |",
    "|---|---|",
    "| `migrate-serialization` | `modernuo-serialization` |",
    "| `migrate-timers` | `modernuo-timers` |",
    "| `migrate-gumps` | `modernuo-gump-system` |",
    "| `migrate-packets` | `modernuo-networking` |",
    "| `migrate-property-lists` | `modernuo-property-lists` |",
    "| `migrate-commands-events` | `modernuo-commands-targeting`, `modernuo-events` |",
    "| `migrate-persistence` | `modernuo-serialization`, `modernuo-events` |",
    "| `migrate-items-mobiles` | `modernuo-content-patterns`, `modernuo-serialization` |",
    "| `migrate-foundation` | hub for all `migrate-*` |",
    "| `migrate-systems` | multi-file orchestration |",
    "",
]

for title, key in [("UO (Game Mechanics)", "uo"), ("ModernUO (Engine & Dev)", "modernuo"), ("RebirthUO (Project-Specific)", "rebirthuo")]:
    lines += [f"## {title}", "", f"**Count:** {len(rows.get(key, []))}", "", "| Skill | Subgroup | Workflow phase | Description |", "|---|---|---|---|"]
    for name, sg, ph, desc in rows.get(key, []):
        lines.append(f"| `{name}` | {sg} | {ph} | {desc} |")
    lines.append("")

out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out}")
