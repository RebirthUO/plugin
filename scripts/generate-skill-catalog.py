#!/usr/bin/env python3
"""Generate the ModernUO skill catalog from portable, repository-relative data."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def frontmatter(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("SKILL.md must start with closed YAML frontmatter")
    return parts[1]


def scalar(block: str, key: str, default: str = "") -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)$", block)
    if not match:
        return default
    value = match.group(1).strip().strip("\"'")
    if value not in {">", "|", ">-", "|-"}:
        return value
    lines: list[str] = []
    for line in block[match.end() :].splitlines():
        if line and not line[0].isspace():
            break
        if line.strip():
            lines.append(line.strip())
    return " ".join(lines)


def nested_scalar(block: str, key: str, default: str) -> str:
    match = re.search(rf"(?m)^\s+{re.escape(key)}:\s*([^#\r\n]+)", block)
    return match.group(1).strip().strip("\"'") if match else default


def catalog_rows(skills_root: Path) -> dict[str, list[tuple[str, str, str, str]]]:
    rows: dict[str, list[tuple[str, str, str, str]]] = {
        "uo": [],
        "modernuo": [],
    }
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        fm = frontmatter(skill_md.read_text(encoding="utf-8"))
        name = scalar(fm, "name", skill_md.parent.name)
        description = re.sub(r"\s+", " ", scalar(fm, "description"))[:180]
        group = nested_scalar(fm, "skill_group", "modernuo")
        subgroup = nested_scalar(fm, "skill_subgroup", "domain")
        phase = nested_scalar(fm, "workflow_phase", "none")
        rows.setdefault(group, []).append((name, subgroup, phase, description))
    return rows


def render(skills_root: Path) -> str:
    rows = catalog_rows(skills_root)
    count = sum(len(group) for group in rows.values())
    lines = [
        "# Skill Catalog",
        "",
        f"Curated index for the ModernUO plugin skill payload ({count} skills). Skills stay in a flat `skills/<name>/` layout; grouping is via frontmatter (`skill_group`, `skill_subgroup`, `workflow_phase`, `workflow_tier`).",
        "",
        "See [README.md](../../../README.md) for repository resolution, evidence policy, and workflow routing.",
        "",
        "## Agentic Workflow (Primary)",
        "",
        "| Phase | Skill | Repository | Stop condition |",
        "|---|---|---|---|",
        "| Create | `modernuo-issue-create` | Exact repository from project `AGENTS.md` | Stop after `IntakePacket` |",
        "| Research | `modernuo-issue-research` | Same verified repository | Ask and stop on unresolved behavior |",
        "| Implement | `modernuo-issue-implement` | Same verified repository and push remote | Require current `READY` research |",
        "",
        "**Companion skills:** `uo-official-evidence`, `uo-living-world-review`, `modernuo-codebase`, `modernuo-test-workflow`, `modernuo-code-audit`, and `modernuo-verification-guard`.",
        "",
        "## Removed / Deprecated",
        "",
        "| Skill | Action | Redirect |",
        "|---|---|---|",
        "| `rebirthuo-issue-create` | absorbed | `modernuo-issue-create` |",
        "| `rebirthuo-issue-review` | absorbed | `modernuo-issue-research` |",
        "| `rebirthuo-review-patterns` | absorbed | `modernuo-issue-research` |",
        "| `modernuo-issue-review` | absorbed | `modernuo-issue-research` |",
        "| `modernuo-issue-template-gate` | absorbed | `modernuo-issue-create` |",
        "| `rebirthuo-implementation-checkpoints` | absorbed | `modernuo-issue-research` / `modernuo-issue-implement` |",
        "| `rebirthuo-implement` | absorbed | `modernuo-issue-implement` |",
        "| `rebirthuo-modernuo-codebase` | absorbed | `modernuo-codebase` |",
        "| `uo-era-publish-source-gate` | absorbed | `uo-official-evidence` |",
        "| `uo-era-product-timeline` | absorbed | `uo-official-evidence` / `uo-living-world-review` |",
        "| `uo-product-model` | absorbed | `uo-living-world-review` |",
        "| `uo-modernuo-workflow` | absorbed | README and this catalog |",
        "| `ultima-online-product-model` | removed | `uo-living-world-review` |",
        "| `rebirthuo-implementation` | removed | `modernuo-issue-implement` |",
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
    for title, key in [
        ("UO (Game Mechanics)", "uo"),
        ("ModernUO (Engine & Dev)", "modernuo"),
    ]:
        lines.extend(
            [
                f"## {title}",
                "",
                f"**Count:** {len(rows.get(key, []))}",
                "",
                "| Skill | Subgroup | Workflow phase | Description |",
                "|---|---|---|---|",
            ]
        )
        for name, subgroup, phase, description in rows.get(key, []):
            safe_description = description.replace("|", "\\|")
            lines.append(f"| `{name}` | {subgroup} | {phase} | {safe_description} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=repo_root / "plugins" / "modernuo" / "skills",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="Fail if the catalog is stale")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skills_root = args.skills_root.resolve()
    output = (args.output or skills_root / "SKILL-CATALOG.md").resolve()
    rendered = render(skills_root) + "\n"
    if args.check:
        current = output.read_text(encoding="utf-8") if output.exists() else ""
        if current != rendered:
            raise SystemExit(f"Catalog is stale: run {Path(__file__).name}")
        print(f"Catalog is current: {output}")
        return
    output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
