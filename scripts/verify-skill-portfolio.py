#!/usr/bin/env python3
"""Verify ModernUO portfolio structure, routing metadata, and Yao readiness."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - operator guidance
    raise SystemExit(
        "PyYAML is required for portfolio verification; install scripts/requirements.txt"
    ) from exc


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/]+Users[\\/]|/Users/)", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
MOJIBAKE = ("â†’", "â€”", "â€“", "â€", "Ã")
NON_ENGLISH_MARKERS = (
    "Bestandsaufnahme",
    "Fehlend",
    "Unvollständig",
    "Offene Punkte",
    "Kurzfassung",
    "Voraussetzungen",
    "Quellen",
    "fachlich",
    "implementierungsreif",
    "was fehlt",
)
HARD_CODED_REPOSITORIES = ("RebirthUO/ModernUO", "RebirthUO/rebirthuo")
REQUIRED_TARGETS = {"openai", "claude", "generic", "vscode"}
MANIFEST_FIELDS = {
    "name",
    "version",
    "owner",
    "updated_at",
    "review_cadence",
    "status",
    "maturity_tier",
    "lifecycle_stage",
    "target_platforms",
}
REMOVED = {
    "modernuo-issue-review",
    "modernuo-issue-template-gate",
    "rebirthuo-implement",
    "rebirthuo-implementation",
    "rebirthuo-implementation-checkpoints",
    "rebirthuo-issue-create",
    "rebirthuo-issue-review",
    "rebirthuo-modernuo-codebase",
    "rebirthuo-review-patterns",
    "ultima-online-product-model",
    "uo-era-product-timeline",
    "uo-era-publish-source-gate",
    "uo-modernuo-workflow",
    "uo-product-model",
}
GHOSTS = REMOVED | {
    "modernuo-ticket-triage",
    "uo-domain-research",
    "modernuo-era-parity-check",
}
REQUIRED_PHASES = {
    "modernuo-issue-create": "create",
    "modernuo-issue-research": "research",
    "modernuo-issue-implement": "implement",
}


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected a YAML mapping")
    return data


def load_skill(skill_md: Path) -> tuple[dict, str, str]:
    text = skill_md.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("missing or unclosed leading YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, parts[2].lstrip(), text


def check_interface(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append("missing agents/interface.yaml")
        return
    try:
        data = load_yaml(path)
    except Exception as exc:
        errors.append(f"invalid agents/interface.yaml: {exc}")
        return
    interface = data.get("interface", {})
    compatibility = data.get("compatibility", {})
    for field in ("display_name", "short_description", "default_prompt"):
        if not str(interface.get(field, "")).strip():
            errors.append(f"interface.{field} is required")
    targets = set(compatibility.get("adapter_targets", []))
    missing_targets = REQUIRED_TARGETS - targets
    if missing_targets:
        errors.append(f"interface missing targets: {sorted(missing_targets)}")
    degradation = compatibility.get("degradation", {})
    if not REQUIRED_TARGETS.issubset(degradation):
        errors.append("interface degradation must cover every required target")


def check_manifest(path: Path, name: str, errors: list[str]) -> None:
    if not path.exists():
        errors.append("missing manifest.json")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid manifest.json: {exc}")
        return
    missing = MANIFEST_FIELDS - data.keys()
    if missing:
        errors.append(f"manifest missing fields: {sorted(missing)}")
    if data.get("name") != name:
        errors.append("manifest name does not match directory")


def check_evals(path: Path, errors: list[str], warnings: list[str]) -> None:
    if not path.exists():
        errors.append("missing evals/trigger_cases.json")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid trigger eval JSON: {exc}")
        return
    minimums = {"should_trigger": 4, "should_not_trigger": 3, "near_neighbor": 2}
    for bucket, minimum in minimums.items():
        count = len(data.get(bucket, []))
        if count < minimum:
            errors.append(f"{bucket} has {count} cases; need at least {minimum}")
    if not (path.parent / "baseline_description.txt").exists():
        warnings.append("missing frozen baseline description")
    if not (path.parent / "semantic_config.json").exists():
        warnings.append("missing semantic trigger config")


def check_links(skill_md: Path, text: str, errors: list[str]) -> None:
    for target in LINK_RE.findall(text):
        clean = target.split("#", 1)[0].strip().strip("<>")
        if clean and not (skill_md.parent / clean).exists():
            errors.append(f"broken relative link: {clean}")


def verify_skill(skill_md: Path, max_chars: int) -> dict:
    name = skill_md.parent.name
    errors: list[str] = []
    warnings: list[str] = []
    try:
        frontmatter, body, text = load_skill(skill_md)
    except Exception as exc:
        return {"name": name, "errors": [f"invalid SKILL.md: {exc}"], "warnings": []}

    declared_name = str(frontmatter.get("name", ""))
    description = str(frontmatter.get("description", "")).strip()
    if declared_name != name:
        errors.append(f"frontmatter name {declared_name!r} does not match directory")
    if not NAME_RE.fullmatch(declared_name) or len(declared_name) > 64:
        errors.append("name violates Agent Skills naming rules")
    if not description or len(description) > 1024:
        errors.append(f"description length is {len(description)}; expected 1..1024")
    if not description.lower().startswith("use when"):
        warnings.append("description should start with 'Use when' for trigger clarity")
    if len(text) > max_chars:
        errors.append(f"SKILL.md has {len(text)} chars; budget is {max_chars}")
    if not re.search(r"(?im)^##\s+(scope|boundary|when to use|purpose)", body):
        warnings.append("no explicit scope/boundary section")
    if not re.search(r"(?im)^##\s+.*(workflow|process|procedure|core)", body):
        warnings.append("no explicit executable workflow section")
    if not re.search(r"(?im)^##\s+.*(output|deliverable|report)", body):
        warnings.append("no explicit output contract section")
    if not re.search(r"(?im)^##\s+.*(verify|verification|self-check|completion)", body):
        warnings.append("no explicit verification section")
    if LOCAL_PATH_RE.search(text):
        errors.append("contains an absolute user-local path")
    for marker in NON_ENGLISH_MARKERS:
        if re.search(rf"\b{re.escape(marker)}\b", text, re.IGNORECASE):
            errors.append(f"contains non-English contract marker: {marker}")
            break
    for repository in HARD_CODED_REPOSITORIES:
        if repository.lower() in text.lower():
            errors.append(f"contains hard-coded target repository: {repository}")
    for marker in MOJIBAKE:
        if marker in text:
            errors.append(f"contains mojibake marker {marker!r}")
            break
    for ghost in GHOSTS:
        if ghost in text:
            errors.append(f"contains stale skill reference: {ghost}")
    check_links(skill_md, text, errors)
    check_interface(skill_md.parent / "agents" / "interface.yaml", errors)
    check_manifest(skill_md.parent / "manifest.json", name, errors)
    check_evals(skill_md.parent / "evals" / "trigger_cases.json", errors, warnings)
    hermes = frontmatter.get("metadata", {}).get("hermes", {})
    related_skills = hermes.get("related_skills", [])
    if not isinstance(related_skills, list):
        errors.append("metadata.hermes.related_skills must be a list")
        related_skills = []
    return {
        "name": name,
        "skill_group": str(hermes.get("skill_group", "")),
        "workflow_phase": str(hermes.get("workflow_phase", "")),
        "related_skills": [str(value) for value in related_skills],
        "description_length": len(description),
        "skill_chars": len(text),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def check_payload_text(skills_root: Path) -> list[str]:
    errors: list[str] = []
    text_suffixes = {".md", ".yaml", ".yml", ".json", ".txt", ".py"}
    for path in sorted(skills_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in text_suffixes:
            continue
        relative = path.relative_to(skills_root)
        if "reports" in relative.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if LOCAL_PATH_RE.search(text):
            errors.append(f"{relative}: contains an absolute user-local path")
        for marker in NON_ENGLISH_MARKERS:
            if re.search(rf"\b{re.escape(marker)}\b", text, re.IGNORECASE):
                errors.append(f"{relative}: contains non-English contract marker: {marker}")
                break
        for repository in HARD_CODED_REPOSITORIES:
            if repository.lower() in text.lower():
                errors.append(f"{relative}: contains hard-coded target repository: {repository}")
        if path.name != "SKILL-CATALOG.md":
            for ghost in GHOSTS:
                if ghost in text:
                    errors.append(f"{relative}: contains stale skill reference: {ghost}")
    return sorted(set(errors))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=repo_root / "plugins" / "modernuo" / "skills",
    )
    parser.add_argument(
        "--expected-count",
        type=int,
        help="Optional explicit count; the inventory name set is authoritative by default",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=repo_root / "scripts" / "skill-inventory.json",
    )
    parser.add_argument("--max-skill-chars", type=int, default=7000)
    parser.add_argument(
        "--report",
        type=Path,
        default=repo_root / "scripts" / "skill-verify-report.json",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skills_root = args.skills_root.resolve()
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    results = [verify_skill(path, args.max_skill_chars) for path in skill_files]
    names = [result["name"] for result in results]
    name_set = set(names)
    portfolio_errors: list[str] = []
    if args.expected_count is not None and len(skill_files) != args.expected_count:
        portfolio_errors.append(
            f"expected {args.expected_count} skills, found {len(skill_files)}"
        )
    if not args.inventory.exists():
        portfolio_errors.append(f"missing skill inventory: {args.inventory}")
    else:
        try:
            inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
            expected_names = set(inventory.get("sync_names", []))
            expected_count = int(inventory.get("skill_count", len(expected_names)))
            if expected_count != len(expected_names):
                portfolio_errors.append(
                    "inventory skill_count does not match inventory sync_names"
                )
            missing = sorted(expected_names - name_set)
            extra = sorted(name_set - expected_names)
            if missing or extra:
                portfolio_errors.append(
                    f"inventory mismatch: missing={missing}, extra={extra}"
                )
        except Exception as exc:
            portfolio_errors.append(f"invalid skill inventory: {exc}")
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        portfolio_errors.append(f"duplicate skill names: {duplicates}")
    present_removed = sorted(REMOVED.intersection(names))
    if present_removed:
        portfolio_errors.append(f"removed skills still present: {present_removed}")
    for result in results:
        name = result["name"]
        if result.get("skill_group") == "rebirthuo":
            portfolio_errors.append(f"{name}: project-specific skill_group is not allowed")
        unknown_related = sorted(set(result.get("related_skills", [])) - name_set)
        if unknown_related:
            portfolio_errors.append(
                f"{name}: related_skills reference missing skills: {unknown_related}"
            )
    for name, phase in REQUIRED_PHASES.items():
        result = next((item for item in results if item["name"] == name), None)
        if result is None:
            portfolio_errors.append(f"missing required workflow skill: {name}")
        elif result.get("workflow_phase") != phase:
            portfolio_errors.append(
                f"{name}: expected workflow_phase {phase!r}, "
                f"found {result.get('workflow_phase')!r}"
            )
    if "uo-official-evidence" not in name_set:
        portfolio_errors.append("missing uo-official-evidence")
    portfolio_errors.extend(check_payload_text(skills_root))
    if not (skills_root / "SKILL-CATALOG.md").exists():
        portfolio_errors.append("missing SKILL-CATALOG.md")

    error_count = len(portfolio_errors) + sum(len(r["errors"]) for r in results)
    warning_count = sum(len(r["warnings"]) for r in results)
    report = {
        "skill_count": len(skill_files),
        "portfolio_errors": portfolio_errors,
        "error_count": error_count,
        "warning_count": warning_count,
        "ok": error_count == 0 and (not args.strict or warning_count == 0),
        "skills": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("skill_count", "error_count", "warning_count", "ok")}, indent=2))
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
