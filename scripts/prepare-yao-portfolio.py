#!/usr/bin/env python3
"""Generate consistent Yao interfaces, lifecycle manifests, and trigger smoke evals."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - operator guidance
    raise SystemExit(
        "PyYAML is required; install scripts/requirements.txt before running this tool"
    ) from exc


TARGETS = ["openai", "claude", "generic", "vscode"]
TARGET_PLATFORMS = [*TARGETS[:3], "agent-skills-compatible", TARGETS[3]]


def split_skill(text: str) -> tuple[dict, str]:
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("SKILL.md must begin with closed YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, parts[2].lstrip()


def manual_description(text: str) -> str:
    parts = text.split("---", 2)
    block = parts[1] if len(parts) == 3 else text
    match = re.search(r"(?m)^description:\s*(.*)$", block)
    if not match:
        return ""
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


def heading(body: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", body)
    return match.group(1).strip() if match else fallback.replace("-", " ").title()


def hermes_metadata(frontmatter: dict) -> dict:
    metadata = frontmatter.get("metadata", {})
    if not isinstance(metadata, dict):
        return {}
    hermes = metadata.get("hermes", {})
    return hermes if isinstance(hermes, dict) else {}


def clean_markdown(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[*_]+", "", value)
    return re.sub(r"\s+", " ", value).strip().rstrip(".")


def section_bullets(body: str, names: tuple[str, ...]) -> list[str]:
    wanted = "|".join(re.escape(name) for name in names)
    match = re.search(
        rf"(?ims)^##\s+(?:{wanted})\s*$\n(.*?)(?=^##\s+|\Z)", body
    )
    if not match:
        return []
    bullets: list[str] = []
    for item in re.findall(r"(?m)^\s*[-*]\s+(.+)$", match.group(1)):
        item = clean_markdown(item)
        if item and len(item) <= 240:
            bullets.append(item)
    return bullets


def to_prompt(fragment: str) -> str:
    fragment = clean_markdown(fragment)
    if not fragment:
        return ""
    if fragment[-1:] in {"?", "!"}:
        return fragment
    lower = fragment[0].lower() + fragment[1:] if len(fragment) > 1 else fragment.lower()
    return f"Help me with {lower}."


def activation_mode(name: str, hermes: dict, description: str) -> str:
    subgroup = str(hermes.get("skill_subgroup", ""))
    phase = str(hermes.get("workflow_phase", "none"))
    if subgroup == "agentic" or phase != "none" or "explicitly" in description.lower():
        return "manual"
    return "implicit"


def interface_document(name: str, title: str, description: str, hermes: dict) -> dict:
    short = title[:72]
    default_prompt = (
        f"Use ${name} to apply {title} guidance to this Ultima Online, ModernUO, "
        "or RebirthUO task and verify the result."
    )
    mode = activation_mode(name, hermes, description)
    return {
        "interface": {
            "display_name": title,
            "short_description": short,
            "default_prompt": default_prompt,
        },
        "compatibility": {
            "canonical_format": "agent-skills",
            "adapter_targets": TARGETS,
            "activation": {"mode": mode, "paths": []},
            "execution": {"context": "inline", "shell": "powershell"},
            "trust": {
                "source_tier": "plugin",
                "remote_inline_execution": "forbid",
                "remote_metadata_policy": "allow-metadata-only",
            },
            "degradation": {
                "openai": "Use the canonical SKILL.md and load references on demand.",
                "claude": "Use the neutral Agent Skills source and preserve explicit safety gates.",
                "generic": "Use SKILL.md with relative references; no client-specific automation is assumed.",
                "vscode": "Use the Agent Skills source in workspace trust and confirm mutations explicitly.",
            },
        },
    }


def manifest_document(
    skill_dir: Path, name: str, frontmatter: dict, updated_at: str
) -> dict:
    components = [
        component
        for component in ("references", "scripts", "assets")
        if (skill_dir / component).exists()
    ]
    components.extend(["evals", "reports"])
    return {
        "name": name,
        "version": str(frontmatter.get("version", "1.0.0")),
        "owner": "RebirthUO",
        "updated_at": updated_at,
        "review_cadence": "quarterly",
        "status": "active",
        "maturity_tier": "production",
        "lifecycle_stage": "production",
        "context_budget_tier": "governed",
        "target_platforms": TARGET_PLATFORMS,
        "factory_components": components,
    }


def baseline_from_git(repo_root: Path, skill_md: Path, fallback: str) -> str:
    relative = skill_md.relative_to(repo_root).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return fallback
    try:
        data, _ = split_skill(result.stdout)
        return str(data.get("description", fallback)).strip()
    except Exception:
        return manual_description(result.stdout) or fallback


def fallback_prompts(name: str, title: str, group: str) -> list[str]:
    subject = title.lower()
    prompts = [
        f"Review this {subject} task and give me the repository-specific checks.",
        f"I need an evidence-backed plan for {subject} in the configured ModernUO-based repository.",
        f"Help me implement a {subject} change and identify the focused verification.",
        f"Audit this {subject} diff for era, persistence, lifecycle, and regression risks.",
    ]
    if name.startswith("migrate-"):
        prompts[0] = f"Migrate this RunUO {subject} code to current ModernUO conventions."
    if name == "modernuo-issue-create":
        prompts[0] = (
            "Create an intake issue from the live template after resolving the exact "
            "GitHub repository only from project AGENTS.md."
        )
    elif name == "modernuo-issue-research":
        prompts = [
            (
                "Research this issue against official OSI/EA sources and the configured "
                "repository, rewrite its existing fields without appending a report, "
                "remove resolved requirements and blockers, and stop on unresolved behavior."
            ),
            (
                "Review this ModernUO issue, preserve its current headings and field order, "
                "and replace obsolete information with verified findings."
            ),
            (
                "Clean this researched issue in place: remove resolved RESEARCH_REQUIRED "
                "markers and answered blockers but retain genuinely unresolved items."
            ),
            (
                "Make this existing UO issue implementation-ready without changing its "
                "title, adding headings, or appending a research contract."
            ),
        ]
    elif name == "modernuo-issue-implement":
        prompts[0] = (
            "Implement this issue only from a READY research handoff at the current "
            "revision, then run focused verification."
        )
    elif name == "modernuo-issue-template-gate":
        prompts[0] = (
            "Select the one live GitHub issue template for this ModernUO request, "
            "or ask me when no current template is an unambiguous fit."
        )
    elif name == "modernuo-issue-workflow":
        prompts[0] = (
            "Take this ModernUO issue from template-gated intake or an existing issue "
            "through a format-preserving research rewrite, blocker interviews, an "
            "isolated worktree, branch push, and PR."
        )
    elif name == "uo-official-evidence":
        prompts[0] = (
            "Establish the official OSI/EA behavior for this claim and keep community "
            "or emulator evidence separate."
        )
    elif group == "uo":
        prompts[1] = (
            f"Compare the requested {subject} behavior with official evidence for the "
            "named UO era and the configured repository."
        )
    return prompts


def negative_prompts(group: str, manual: bool) -> list[str]:
    negatives = {
        "uo": [
            "Refactor this unrelated ASP.NET service; no Ultima Online or ModernUO code is involved.",
            "Create a marketing image for our shard announcement.",
            "Manage a GitHub issue without researching any UO mechanic or repository source.",
        ],
        "modernuo": [
            "Explain this UO mechanic as player lore only; do not inspect a server codebase.",
            "Review generic C# in an unrelated application.",
            "Create an unrelated GitHub issue without a repository declared in project instructions.",
        ],
        "rebirthuo": [
            "Audit an unrelated upstream library with no RebirthUO task or repository context.",
            "Summarize UO lore without issue, code, or product-workflow implications.",
            "Create a generic GitHub issue in a repository the user has not identified.",
        ],
    }[group]
    if manual:
        negatives[-1] = "Give general advice only; do not create, edit, push, or update any GitHub artifact."
    return negatives


def unique_cases(values: list[str], family: str, minimum: int) -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    seen: set[str] = set()
    for value in values:
        value = re.sub(r"\s+", " ", value).strip()
        if not value or value.lower() in seen:
            continue
        seen.add(value.lower())
        cases.append({"text": value, "family": family})
    if len(cases) < minimum:
        raise ValueError(f"could not generate {minimum} distinct {family} cases")
    return cases


def first_prompt(skill: dict) -> str:
    return skill["positive_prompts"][0]


def build_skill_records(skills_root: Path) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        frontmatter, body = split_skill(skill_md.read_text(encoding="utf-8"))
        name = str(frontmatter.get("name", skill_md.parent.name))
        hermes = hermes_metadata(frontmatter)
        group = str(hermes.get("skill_group", "modernuo"))
        title = heading(body, name)
        bullets = section_bullets(body, ("When to Use", "Scope", "Triggers", "Use Cases"))
        prompts = fallback_prompts(name, title, group)
        prompts.extend(to_prompt(item) for item in bullets if to_prompt(item))
        records[name] = {
            "dir": skill_md.parent,
            "md": skill_md,
            "frontmatter": frontmatter,
            "body": body,
            "title": title,
            "description": str(frontmatter.get("description", "")).strip(),
            "hermes": hermes,
            "group": group,
            "related": [str(value) for value in hermes.get("related_skills", []) or []],
            "positive_prompts": [case["text"] for case in unique_cases(prompts, "positive", 4)],
        }
    return records


def eval_document(record: dict, records: dict[str, dict]) -> dict:
    positives = unique_cases(record["positive_prompts"], "owned_job", 4)[:8]
    related_prompts = [
        first_prompt(records[name])
        for name in record["related"]
        if name in records and name != record["frontmatter"].get("name")
    ]
    if len(related_prompts) < 2:
        for name, candidate in records.items():
            if (
                name != record["frontmatter"].get("name")
                and candidate["group"] == record["group"]
                and first_prompt(candidate) not in related_prompts
            ):
                related_prompts.append(first_prompt(candidate))
            if len(related_prompts) >= 2:
                break
    near = unique_cases(related_prompts, "near_neighbor", 2)[:4]
    manual = activation_mode(
        str(record["frontmatter"].get("name")), record["hermes"], record["description"]
    ) == "manual"
    negatives = unique_cases(
        negative_prompts(record["group"], manual), "out_of_scope", 3
    )
    return {
        "recommended_threshold": 0.33,
        "should_trigger": positives,
        "should_not_trigger": negatives,
        "near_neighbor": near,
    }


def semantic_document(record: dict) -> dict:
    name = str(record["frontmatter"].get("name"))
    phrases = [record["title"].lower(), name.replace("-", " ")]
    precise = {
        "modernuo-issue-create": ["create an intake issue", "live issue template", "intakepacket"],
        "modernuo-issue-research": [
            "research this issue",
            "review and rewrite this issue",
            "rewrite existing issue fields",
            "remove resolved requirements and blockers",
            "official osi ea sources",
            "researchpacket",
        ],
        "modernuo-issue-implement": [
            "implement this issue",
            "ready research handoff",
            "implementationresult",
        ],
        "modernuo-issue-template-gate": [
            "select the one live github issue template",
            "select the live issue template",
            "templatepacket",
            "no matching issue template",
        ],
        "modernuo-issue-workflow": [
            "take this modernuo issue from template-gated intake or an existing issue",
            "blocker interviews isolated worktree branch push and pr",
            "issue to pull request workflow",
            "existing issue skip creation",
            "interview until research is ready",
        ],
        "uo-official-evidence": [
            "official osi ea behavior",
            "official evidence",
            "unresolved official evidence",
        ],
    }
    phrases = list(dict.fromkeys([*phrases, *precise.get(name, [])]))
    exclusions = [related.replace("-", " ") for related in record["related"][:8]]
    return {
        "optimizer_hints": {
            "capability": record["title"],
            "inputs": phrases,
            "trigger_actions": record["positive_prompts"][:4],
            "exclusions": exclusions,
            "artifacts": ["source evidence", "implementation plan", "verification result"],
        },
        "fallback_positive_concepts": ["owned_job"],
        "positive_concepts": {
            "owned_job": {"weight": 1.0, "phrases": phrases},
        },
        "negative_concepts": {
            "near_neighbor": {
                "weight": 0.0,
                "exclusive": False,
                "phrases": [],
            },
            "explicit_no_action": {
                "weight": 0.5,
                "exclusive": True,
                "phrases": ["do not modify", "advice only", "unrelated repository"],
            },
        },
    }


def merge_cases(existing: dict | None, generated: dict) -> dict:
    return generated


def write_or_check(path: Path, content: str, check: bool, stale: list[str]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == content:
        return
    if check:
        stale.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=repo_root / "plugins" / "modernuo" / "skills",
    )
    parser.add_argument("--updated-at", default="2026-07-12")
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skills_root = args.skills_root.resolve()
    repo_root = Path(__file__).resolve().parents[1]
    records = build_skill_records(skills_root)
    requested = set(args.skills or records.keys())
    missing = sorted(requested - records.keys())
    if missing:
        raise SystemExit(f"Unknown skills: {', '.join(missing)}")
    stale: list[str] = []

    for name in sorted(requested):
        record = records[name]
        interface = yaml.safe_dump(
            interface_document(
                name,
                record["title"],
                record["description"],
                record["hermes"],
            ),
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )
        write_or_check(record["dir"] / "agents" / "interface.yaml", interface, args.check, stale)

        manifest = json.dumps(
            manifest_document(
                record["dir"], name, record["frontmatter"], args.updated_at
            ),
            indent=2,
            ensure_ascii=False,
        ) + "\n"
        write_or_check(record["dir"] / "manifest.json", manifest, args.check, stale)

        eval_path = record["dir"] / "evals" / "trigger_cases.json"
        existing = None
        if eval_path.exists():
            try:
                existing = json.loads(eval_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = None
        cases = json.dumps(
            merge_cases(existing, eval_document(record, records)),
            indent=2,
            ensure_ascii=False,
        ) + "\n"
        write_or_check(eval_path, cases, args.check, stale)

        baseline_path = record["dir"] / "evals" / "baseline_description.txt"
        baseline = baseline_from_git(
            repo_root, record["md"], record["description"]
        ).strip() + "\n"
        if baseline_path.exists() and baseline_path.read_text(encoding="utf-8").strip():
            baseline = baseline_path.read_text(encoding="utf-8").strip() + "\n"
        write_or_check(baseline_path, baseline, args.check, stale)

        semantic_path = record["dir"] / "evals" / "semantic_config.json"
        semantic = json.dumps(
            semantic_document(record), indent=2, ensure_ascii=False
        ) + "\n"
        write_or_check(semantic_path, semantic, args.check, stale)

    if stale:
        print("Stale generated files:")
        for path in stale:
            print(f"- {path}")
        raise SystemExit(1)
    action = "checked" if args.check else "prepared"
    print(f"{action} {len(requested)} skill packages")


if __name__ == "__main__":
    main()
