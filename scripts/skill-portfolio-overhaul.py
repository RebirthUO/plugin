#!/usr/bin/env python3
"""Skill portfolio overhaul v2: text-safe metadata injection and Hermes->plugin sync."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

HERMES_ROOT = Path(r"C:\Users\Jsiem\AppData\Local\hermes\profiles\ultima-online\skills")
PLUGIN_SKILLS = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\plugins\modernuo\skills")
PLUGIN_ROOT = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin")

GHOST_REPLACEMENTS = [
    (r"\bmodernuo-ticket-triage\b", "rebirthuo-issue-review"),
    (r"\buo-domain-research\b", "uo-era-publish-source-gate"),
    (r"\bmodernuo-era-parity-check\b", "modernuo-content-taxonomy"),
    (r"\buo-modernuo-era-parity-check\b", "modernuo-content-taxonomy"),
    (r"\bultima-online-product-model\b", "uo-product-model"),
]

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

SYNC_PREFIX = re.compile(r"^(uo-|modernuo-|rebirthuo-|migrate-)")
REMOVE_FROM_PLUGIN = {
    "ultima-online-product-model",
    "polymarket",
    "rebirthuo-implementation",
}


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


def find_hermes_skill_dirs() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for skill_md in HERMES_ROOT.rglob("SKILL.md"):
        content = skill_md.read_text(encoding="utf-8")
        m = re.search(r"(?m)^name:\s*(.+)$", content)
        if not m:
            continue
        name = m.group(1).strip().strip('"').strip("'")
        mapping[name] = skill_md.parent
    return mapping


def skill_name_from_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"(?m)^name:\s*(.+)$", text)
    return m.group(1).strip().strip('"').strip("'") if m else path.parent.name


def fix_ghost_refs(text: str) -> str:
    for pattern, repl in GHOST_REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text


def inject_metadata(text: str, name: str) -> str:
    if "skill_group:" in text:
        # update existing values
        group = infer_group(name)
        subgroup = infer_subgroup(name)
        phase, tier = infer_workflow(name)
        text = re.sub(r"^\s*skill_group:\s*.+$", f"    skill_group: {group}", text, flags=re.M)
        text = re.sub(r"^\s*skill_subgroup:\s*.+$", f"    skill_subgroup: {subgroup}", text, flags=re.M)
        text = re.sub(r"^\s*workflow_phase:\s*.+$", f"    workflow_phase: {phase}", text, flags=re.M)
        text = re.sub(r"^\s*workflow_tier:\s*.+$", f"    workflow_tier: {tier}", text, flags=re.M)
        return text

    if "metadata:" not in text or "hermes:" not in text:
        return text

    group = infer_group(name)
    subgroup = infer_subgroup(name)
    phase, tier = infer_workflow(name)
    injection = (
        f"    skill_group: {group}\n"
        f"    skill_subgroup: {subgroup}\n"
        f"    workflow_phase: {phase}\n"
        f"    workflow_tier: {tier}\n"
    )
    return re.sub(r"(?m)^(\s*hermes:\s*\n)", r"\1" + injection, text, count=1)


def clean_related_skills(text: str, valid_names: set[str]) -> str:
    def repl_block(match: re.Match[str]) -> str:
        block = match.group(0)
        items = re.findall(r"-\s+(\S+)", block)
        if not items:
            inline = re.search(r"related_skills:\s*\[(.*?)\]", block, re.S)
            if inline:
                items = [x.strip().strip("'\"") for x in inline.group(1).split(",") if x.strip()]
        cleaned = []
        for item in items:
            item = item.strip().strip("'\"[]")
            if item in valid_names or item.startswith("github-"):
                if item not in cleaned:
                    cleaned.append(item)
        if not cleaned:
            return ""
        lines = ["    related_skills:"] + [f"    - {x}" for x in cleaned]
        return "\n".join(lines) + "\n"

    # multiline related_skills under hermes
    text = re.sub(
        r"(?ms)^    related_skills:\n(?:    - .+\n)+",
        repl_block,
        text,
    )
    return text


def process_skill_md(path: Path, valid_names: set[str]) -> None:
    name = skill_name_from_md(path)
    text = path.read_text(encoding="utf-8")
    text = fix_ghost_refs(text)
    text = inject_metadata(text, name)
    text = clean_related_skills(text, valid_names)
    path.write_text(text, encoding="utf-8", newline="\n")


def sync_skill(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def restore_hermes_from_plugin(hermes_dirs: dict[str, Path]) -> None:
    """Restore Hermes SKILL.md from plugin when plugin copy is authoritative."""
    for skill_dir in PLUGIN_SKILLS.iterdir():
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        plugin_md = skill_dir / "SKILL.md"
        if not plugin_md.exists() or name not in hermes_dirs:
            continue
        hermes_md = hermes_dirs[name] / "SKILL.md"
        plugin_text = plugin_md.read_text(encoding="utf-8")
        hermes_text = hermes_md.read_text(encoding="utf-8")
        # restore if hermes lost inline tags block
        if "tags:\n    related_skills:" in hermes_text and "tags: [" in plugin_text:
            hermes_md.write_text(plugin_text, encoding="utf-8", newline="\n")


def main() -> None:
    hermes_dirs = find_hermes_skill_dirs()

    # Ensure uo-game-docs exists in Hermes
    plugin_game_docs = PLUGIN_SKILLS / "uo-game-docs-canonical-authoring"
    hermes_game_docs = HERMES_ROOT / "software-development" / "uo-game-docs-canonical-authoring"
    if plugin_game_docs.exists() and not hermes_game_docs.exists():
        shutil.copytree(plugin_game_docs, hermes_game_docs)
        hermes_dirs = find_hermes_skill_dirs()

    restore_hermes_from_plugin(hermes_dirs)
    hermes_dirs = find_hermes_skill_dirs()

    # Merge ad-hoc verification ref into rebirthuo-implement before deleting rebirthuo-implementation
    impl_src = hermes_dirs.get("rebirthuo-implementation")
    implement_dir = hermes_dirs.get("rebirthuo-implement")
    if impl_src and implement_dir:
        ref_src = impl_src / "references" / "ad-hoc-focused-verification.md"
        ref_dst_dir = implement_dir / "references"
        ref_dst_dir.mkdir(parents=True, exist_ok=True)
        if ref_src.exists():
            shutil.copy2(ref_src, ref_dst_dir / "ad-hoc-focused-verification.md")

    for deprecated in ["rebirthuo-implementation"]:
        dep_dir = hermes_dirs.get(deprecated)
        if dep_dir and dep_dir.exists():
            shutil.rmtree(dep_dir)
    hermes_dirs = find_hermes_skill_dirs()

    valid_names = {n for n in hermes_dirs if n not in REMOVE_FROM_PLUGIN}
    valid_names.update(GROUP_OVERRIDES.keys())

    for name, skill_dir in sorted(hermes_dirs.items()):
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists() and name not in REMOVE_FROM_PLUGIN:
            process_skill_md(skill_md, valid_names)

    sync_names = sorted(
        n for n in hermes_dirs if SYNC_PREFIX.match(n) and n not in REMOVE_FROM_PLUGIN
    )

    for remove in REMOVE_FROM_PLUGIN:
        target = PLUGIN_SKILLS / remove
        if target.exists():
            shutil.rmtree(target)

    for child in PLUGIN_SKILLS.iterdir():
        if child.is_dir() and child.name not in sync_names:
            shutil.rmtree(child)

    for name in sync_names:
        sync_skill(hermes_dirs[name], PLUGIN_SKILLS / name)
        nested = PLUGIN_SKILLS / name / name
        if nested.is_dir():
            shutil.rmtree(nested)

    # Post-sync content patches on plugin (manual improvements)
    apply_manual_patches()

    # Re-process plugin metadata after manual patches
    plugin_names = {p.name for p in PLUGIN_SKILLS.iterdir() if p.is_dir()}
    for skill_dir in PLUGIN_SKILLS.iterdir():
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            process_skill_md(skill_md, plugin_names)

    ghost_hits = []
    for skill_md in PLUGIN_SKILLS.rglob("SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        for ghost in [
            "modernuo-ticket-triage",
            "uo-domain-research",
            "modernuo-era-parity-check",
            "ultima-online-product-model",
        ]:
            if ghost in text:
                ghost_hits.append(f"{skill_md}:{ghost}")

    inventory = {
        "skill_count": len(plugin_names),
        "sync_names": sync_names,
        "ghost_hits": ghost_hits,
    }
    out = PLUGIN_ROOT / "scripts" / "skill-inventory.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(json.dumps(inventory, indent=2))
    if ghost_hits:
        raise SystemExit(f"Ghost references remain: {ghost_hits}")


def apply_manual_patches() -> None:
    """Apply hand-authored workflow improvements to plugin skills."""
    patches: list[tuple[str, str, str]] = [
        (
            "uo-modernuo-workflow/SKILL.md",
            "Do not use this as a replacement for a domain skill. Once the owning domain is clear, load the child skill and work from that narrower checklist.\n\n## Skill Routing",
            """Do not use this as a replacement for a domain skill. Once the owning domain is clear, load the child skill and work from that narrower checklist.

## Agentic Issue Workflow (Primary)

Use this three-step path for RebirthUO feature work unless the user explicitly targets a ModernUO-only issue:

| Phase | User intent | Load first | Then |
|---|---|---|---|
| Create | Idea → review-ready ticket | `rebirthuo-issue-create` | `uo-living-world-review`, `uo-era-publish-source-gate`, domain UO skills |
| Review | `needs-review` fachlich prüfen | `rebirthuo-issue-review` | `rebirthuo-review-patterns`, domain UO skills, `rebirthuo-modernuo-codebase` |
| Implement | Ticket → Branch/Tests/PR in ModernUO | `rebirthuo-implement` | `rebirthuo-implementation-checkpoints`, `modernuo-test-workflow`, `modernuo-code-audit`, `modernuo-verification-guard` |

**Escape hatch — direct ModernUO issues:** When the ticket already lives in `RebirthUO/ModernUO` without rebirthuo intake, use `modernuo-issue-create`, `modernuo-issue-review`, or `modernuo-issue-implement` instead. Prefer `rebirthuo-implement` for implementation unless the user explicitly names the direct-modernuo skill.

## Skill Routing""",
        ),
        (
            "uo-modernuo-workflow/SKILL.md",
            "- For **expansion parity epics** (feature inventory + GitHub Epic + `dev-docs/eras/*.md`), use `modernuo-era-parity-check` and its `references/ml-expansion-epic-workflow.md`",
            "- For **expansion parity epics** (feature inventory + GitHub Epic + `dev-docs/eras/*.md`), use `modernuo-content-taxonomy`, `uo-living-world-review`, and `uo-era-product-timeline`",
        ),
        (
            "rebirthuo-implement/SKILL.md",
            "# RebirthUO Issue to Tested Pull Request\n\n## Mandatory Repository Gate",
            """# RebirthUO Issue to Tested Pull Request

## Canonical Implementation Skill

This is the **canonical** RebirthUO implementation skill for `RebirthUO/ModernUO`. Prefer this over `modernuo-issue-implement` unless the user explicitly names the direct-modernuo skill. The deprecated `rebirthuo-implementation` skill (wrong repo gate) was merged into this skill.

## Mandatory Repository Gate""",
        ),
        (
            "rebirthuo-implement/SKILL.md",
            "`.html_url == \"https://github.com/RebirthUO/ModernUO\"`, and `.fork == false`.",
            "`.html_url == \"https://github.com/RebirthUO/ModernUO\"`. The canonical repository may report `fork: true`; exact canonical identity is allowed, but every other fork or lookalike is rejected.",
        ),
        (
            "rebirthuo-implement/SKILL.md",
            "- Pure triage-only planning with no implementation request; use `modernuo-ticket-triage`.",
            "- Pure triage-only planning with no implementation request; use `rebirthuo-issue-review` or `modernuo-issue-review`.",
        ),
        (
            "rebirthuo-implement/SKILL.md",
            "- RebirthUO/ModernUO issue planning: `modernuo-ticket-triage` and `uo-modernuo-workflow`.",
            "- RebirthUO issue planning/review: `rebirthuo-issue-review`, `rebirthuo-review-patterns`, and `uo-modernuo-workflow`.\n- Decision gaps during implementation: `rebirthuo-implementation-checkpoints`.\n- Stale verification evidence: `modernuo-verification-guard` and `references/ad-hoc-focused-verification.md`.",
        ),
        (
            "modernuo-issue-implement/SKILL.md",
            "# ModernUO Implement Issue\n\n## Mandatory Repository Gate",
            """# ModernUO Implement Issue

## Redirect to Canonical Skill

Unless the user explicitly names this skill, load **`rebirthuo-implement`** first. Use this skill only when the issue lives directly in `RebirthUO/ModernUO` without a linked rebirthuo intake ticket and the user explicitly requests the direct-modernuo implementation path.

## Mandatory Repository Gate""",
        ),
    ]

    for rel, old, new in patches:
        path = PLUGIN_SKILLS / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if old in text:
            path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

    # Add references section to rebirthuo-implement if missing
    impl = PLUGIN_SKILLS / "rebirthuo-implement" / "SKILL.md"
    if impl.exists():
        text = impl.read_text(encoding="utf-8")
        if "## References" not in text and "## Verification Checklist" in text:
            text = text.replace(
                "## Verification Checklist",
                """## References

- `references/ad-hoc-focused-verification.md` — Disposable focused build/test harness when verification evidence is stale.
- `references/test-gap-and-noop-issue-waves.md` — Test-only and no-op issue waves.
- `references/item-property-review-ticket-analysis.md` — Item-property ticket patterns from review work.

## Verification Checklist""",
            )
            extra_pitfalls = """14. **Stopping at a local branch.** Completion requires commit, push, PR, and remote verification.
15. **Implementing gameplay from memory.** When the issue cites an authoritative source, fetch or inspect the source and use it to correct formulas before commit.
16. **Post-damage multipliers outside cap paths.** Put bonuses in the same formula/cap path as the existing mechanic.
17. **Persistent stat mutation for temporary effects.** Use runtime state and cleanup/clamping unless the issue explicitly requires save-visible mutation.

"""
            if "14. **Stopping at a local branch.**" not in text:
                text = text.replace("## Verification Checklist", extra_pitfalls + "## Verification Checklist")
            impl.write_text(text, encoding="utf-8", newline="\n")

    # Copy manual patches back to Hermes for key skills
    for name in [
        "uo-modernuo-workflow",
        "rebirthuo-implement",
        "modernuo-issue-implement",
        "uo-game-docs-canonical-authoring",
    ]:
        plugin_dir = PLUGIN_SKILLS / name
        hermes_dirs = find_hermes_skill_dirs()
        if plugin_dir.exists() and name in hermes_dirs:
            sync_skill(plugin_dir, hermes_dirs[name])


if __name__ == "__main__":
    main()
