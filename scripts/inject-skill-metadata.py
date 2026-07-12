#!/usr/bin/env python3
"""Inject skill_group metadata into all plugin SKILL.md files (text-safe)."""

import re
from pathlib import Path

PLUGIN_SKILLS = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\plugins\modernuo\skills")

GROUP_OVERRIDES = {
    "uo-game-docs-canonical-authoring": "rebirthuo",
    "uo-item-property-review": "rebirthuo",
}

REBIRTHUO_AGENTIC = {
    "rebirthuo-issue-create": ("create", "primary"),
    "rebirthuo-issue-review": ("review", "primary"),
    "rebirthuo-implement": ("implement", "primary"),
    "rebirthuo-implementation-checkpoints": ("implement", "support"),
    "rebirthuo-review-patterns": ("review", "reference"),
    "rebirthuo-modernuo-codebase": ("none", "support"),
}

MODERNUO_AGENTIC = {
    "modernuo-issue-create": ("create", "direct-modernuo"),
    "modernuo-issue-review": ("review", "direct-modernuo"),
    "modernuo-issue-implement": ("implement", "direct-modernuo"),
    "modernuo-issue-template-gate": ("create", "direct-modernuo"),
}

META_SKILLS = {"uo-modernuo-workflow", "modernuo-skill-discovery"}
GATE_SKILLS = {
    "modernuo-era-change-gate",
    "modernuo-verification-guard",
    "uo-era-publish-source-gate",
    "uo-living-world-review",
}

GHOST_REPLACEMENTS = [
    (r"\bmodernuo-ticket-triage\b", "rebirthuo-issue-review"),
    (r"\buo-domain-research\b", "uo-era-publish-source-gate"),
    (r"\bmodernuo-era-parity-check\b", "modernuo-content-taxonomy"),
    (r"\buo-modernuo-era-parity-check\b", "modernuo-content-taxonomy"),
    (r"\bultima-online-product-model\b", "uo-product-model"),
]


def infer_group(name: str) -> str:
    if name in GROUP_OVERRIDES:
        return GROUP_OVERRIDES[name]
    if name.startswith("rebirthuo-"):
        return "rebirthuo"
    if name.startswith("modernuo-") or name.startswith("migrate-"):
        return "modernuo"
    if name.startswith("uo-"):
        return "uo"
    return "modernuo"


def infer_subgroup(name: str) -> str:
    if name.startswith("migrate-"):
        return "migration"
    if name in META_SKILLS:
        return "meta"
    if name in GATE_SKILLS:
        return "gate"
    if name in REBIRTHUO_AGENTIC or name in MODERNUO_AGENTIC:
        return "agentic"
    return "domain"


def infer_workflow(name: str) -> tuple[str, str]:
    if name in REBIRTHUO_AGENTIC:
        return REBIRTHUO_AGENTIC[name]
    if name in MODERNUO_AGENTIC:
        return MODERNUO_AGENTIC[name]
    if name in {"modernuo-test-workflow", "modernuo-verification-guard", "modernuo-regression-testing"}:
        return ("implement", "support")
    return ("none", "support")


def skill_name(text: str, fallback: str) -> str:
    m = re.search(r"(?m)^name:\s*(.+)$", text)
    return m.group(1).strip().strip('"').strip("'") if m else fallback


def inject_metadata(text: str, name: str) -> str:
    group = infer_group(name)
    subgroup = infer_subgroup(name)
    phase, tier = infer_workflow(name)
    block = (
        f"    skill_group: {group}\n"
        f"    skill_subgroup: {subgroup}\n"
        f"    workflow_phase: {phase}\n"
        f"    workflow_tier: {tier}\n"
    )
    if "skill_group:" in text:
        text = re.sub(r"^\s*skill_group:\s*.+$", f"    skill_group: {group}", text, flags=re.M)
        text = re.sub(r"^\s*skill_subgroup:\s*.+$", f"    skill_subgroup: {subgroup}", text, flags=re.M)
        text = re.sub(r"^\s*workflow_phase:\s*.+$", f"    workflow_phase: {phase}", text, flags=re.M)
        text = re.sub(r"^\s*workflow_tier:\s*.+$", f"    workflow_tier: {tier}", text, flags=re.M)
        return text
    if "hermes:" not in text:
        return text
    return re.sub(r"(?m)^(\s*hermes:\s*\n)", r"\1" + block, text, count=1)


def fix_ghost_refs(text: str) -> str:
    for pattern, repl in GHOST_REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text


def main() -> None:
    missing = []
    for skill_md in sorted(PLUGIN_SKILLS.rglob("SKILL.md")):
        if skill_md.parent.name != skill_md.parent.parent.name.split("\\")[-1]:
            # skip nested duplicate paths
            rel = skill_md.relative_to(PLUGIN_SKILLS)
            if len(rel.parts) > 2:
                continue
        text = skill_md.read_text(encoding="utf-8")
        text = fix_ghost_refs(text)
        name = skill_name(text, skill_md.parent.name)
        text = inject_metadata(text, name)
        skill_md.write_text(text, encoding="utf-8", newline="\n")
        if "skill_group:" not in text:
            missing.append(str(skill_md))
    if missing:
        raise SystemExit(f"Missing skill_group: {missing}")
    print(f"Updated {len(list(PLUGIN_SKILLS.glob('*/SKILL.md')))} skills")


if __name__ == "__main__":
    main()
