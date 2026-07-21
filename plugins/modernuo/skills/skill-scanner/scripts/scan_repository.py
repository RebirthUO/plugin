#!/usr/bin/env python3
"""Create a reproducible, read-only ModernUO skill-portfolio change report."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9]{2,}")
PATH_TOKEN = re.compile(r"(?<![A-Za-z0-9_.-])(?:[A-Za-z0-9_.-]+/){1,}[A-Za-z0-9_.-]+")
CODE_TOKEN = re.compile(r"`([^`]+)`")
SKILL_NAME = re.compile(r"\b(?:modernuo|rebirthuo|uo)-[a-z0-9-]+\b")
STOP = {
    "add", "and", "are", "based", "change", "changed", "code", "current", "data",
    "existing", "file", "files", "for", "from",
    "into", "modernuo", "plugin", "project", "repository", "skill", "source",
    "server", "src", "test", "tests", "the", "this", "use", "with", "your",
}
GENERIC_PATH = {
    "bin", "config", "data", "docs", "object", "project", "projects", "server",
    "src", "test", "tests",
}


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> set[str]:
    normalized = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return {
        token.lower()
        for token in TOKEN.findall(normalized.replace("-", " ").replace("_", " "))
        if token.lower() not in STOP and len(token) >= 3
    }


def changed_paths(repo: Path, base: str, working_tree: bool) -> tuple[list[dict[str, str]], str]:
    resolved = run_git(repo, "rev-parse", "--verify", f"{base}^{{commit}}").strip()
    lines = run_git(repo, "diff", "--name-status", "-M", f"{resolved}..HEAD").splitlines()
    changes: list[dict[str, str]] = []
    for line in lines:
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status = fields[0]
        path = fields[-1].replace("\\", "/")
        changes.append({"status": status, "path": path, "source": "committed"})
    if working_tree:
        for line in run_git(repo, "diff", "--name-status", "-M").splitlines():
            fields = line.split("\t")
            if len(fields) >= 2:
                changes.append({"status": fields[0], "path": fields[-1].replace("\\", "/"), "source": "working_tree"})
        for path in run_git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
            changes.append({"status": "A", "path": path.replace("\\", "/"), "source": "untracked"})
    return changes, resolved


def load_skill(skill_dir: Path) -> dict[str, Any]:
    files = sorted(path for path in skill_dir.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    text_by_path = {
        path.relative_to(skill_dir).as_posix(): path.read_text(encoding="utf-8", errors="replace")
        for path in files
    }
    skill_text = text_by_path["SKILL.md"]
    frontmatter = skill_text.split("---", 2)[1] if skill_text.startswith("---") else ""
    name_match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", frontmatter)
    desc_match = re.search(r"(?ms)^description:\s*(.+?)(?=^\w[\w_-]*:|\Z)", frontmatter)
    name = name_match.group(1).strip() if name_match else skill_dir.name
    description = " ".join(desc_match.group(1).split()) if desc_match else ""
    all_text = "\n".join(text_by_path.values())
    exact_paths = {
        candidate.replace("\\", "/")
        for candidate in [*PATH_TOKEN.findall(all_text), *CODE_TOKEN.findall(all_text)]
        if "/" in candidate and not candidate.startswith(("http://", "https://"))
    }
    return {
        "name": name,
        "directory": skill_dir.name,
        "description": description,
        "files": [{"path": path, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()} for path, text in text_by_path.items()],
        "text": all_text,
        "routing_tokens": words(f"{name} {description}"),
        "exact_paths": exact_paths,
        "declares": sorted({s for s in SKILL_NAME.findall(all_text) if s != name}),
    }


def skill_inventory(skills_root: Path) -> list[dict[str, Any]]:
    return [load_skill(path.parent) for path in sorted(skills_root.glob("*/SKILL.md"))]


def relation_edges(skills: list[dict[str, Any]]) -> list[dict[str, str]]:
    names = {skill["name"] for skill in skills}
    return [
        {"from": skill["name"], "to": sibling, "kind": "declared_relation"}
        for skill in skills
        for sibling in skill["declares"]
        if sibling in names
    ]


def report(repo: Path, skills_root: Path, base: str, working_tree: bool) -> dict[str, Any]:
    changes, resolved_base = changed_paths(repo, base, working_tree)
    skills = skill_inventory(skills_root)
    if not skills:
        raise ValueError(f"no skill packages found under {skills_root}")
    changed_tokens = {change["path"]: words(change["path"]) - GENERIC_PATH for change in changes}
    candidates: list[dict[str, Any]] = []
    covered: dict[str, int] = defaultdict(int)
    for skill in skills:
        signals: list[dict[str, Any]] = []
        for change in changes:
            path = change["path"]
            if path in skill["exact_paths"]:
                signals.append({"kind": "exact_path", "path": path, "source": change["source"]})
            overlap = sorted(changed_tokens[path] & skill["routing_tokens"])
            if len(overlap) >= 2:
                signals.append({"kind": "keyword_overlap", "path": path, "tokens": overlap[:8], "source": change["source"]})
        if signals:
            for signal in signals:
                covered[signal["path"]] += 1
            candidates.append({
                "skill": skill["name"],
                "status": "needs_review",
                "signals": signals,
                "reason": "Changed repository terminology or a quoted path overlaps this skill; verify current anchors before editing.",
            })
        else:
            candidates.append({"skill": skill["name"], "status": "verified_current", "signals": [], "reason": "No direct path or terminology overlap was found."})
    descriptions = {skill["name"]: words(skill["description"]) for skill in skills}
    declared = {(edge["from"], edge["to"]) for edge in relation_edges(skills)}
    scope_overlaps: list[dict[str, Any]] = []
    for index, left in enumerate(skills):
        for right in skills[index + 1:]:
            union = descriptions[left["name"]] | descriptions[right["name"]]
            common = descriptions[left["name"]] & descriptions[right["name"]]
            similarity = len(common) / len(union) if union else 0.0
            related = (left["name"], right["name"]) in declared or (right["name"], left["name"]) in declared
            if similarity >= 0.32 and len(common) >= 4 and not related:
                scope_overlaps.append({
                    "left": left["name"], "right": right["name"],
                    "shared_terms": sorted(common), "similarity": round(similarity, 3),
                    "status": "needs_review",
                })
    uncovered_by_area: dict[str, dict[str, Any]] = {}
    for change in changes:
        path = change["path"]
        if not covered[path] and changed_tokens[path]:
            area = "/".join(path.split("/")[:2])
            candidate = uncovered_by_area.setdefault(area, {
                "changed_area": area,
                "paths": [],
                "tokens": set(),
                "status": "user_decision_required",
                "reason": "No portfolio artifact contains an exact path or two-term routing overlap.",
            })
            candidate["paths"].append(path)
            candidate["tokens"].update(changed_tokens[path])
    uncovered = [
        {**candidate, "paths": sorted(candidate["paths"]), "tokens": sorted(candidate["tokens"])}
        for _, candidate in sorted(uncovered_by_area.items())
    ]
    return {
        "schema": "modernuo-repository-scan/v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repository": {
            "path": str(repo), "head": run_git(repo, "rev-parse", "HEAD").strip(),
            "base": resolved_base, "dirty": bool(run_git(repo, "status", "--porcelain")),
        },
        "comparison": {"base_input": base, "working_tree_included": working_tree, "changes": changes},
        "portfolio": {"path": str(skills_root), "skills": [{key: value for key, value in skill.items() if key not in {"text", "routing_tokens", "exact_paths", "declares"}} for skill in skills]},
        "maintenance_candidates": candidates,
        "relationships": {"declared": relation_edges(skills), "scope_overlap_warnings": scope_overlaps},
        "capability_candidates": uncovered,
        "limitations": [
            "Keyword overlap is a deterministic triage signal, not proof that a skill is stale.",
            "Descriptions are compared for routing ambiguity; runtime behavior and natural-language intent are not executed by this scanner.",
            "Capability candidates require explicit user approval before any new-skill work.",
        ],
    }


def markdown(data: dict[str, Any]) -> str:
    lines = ["# ModernUO Repository Scanner Report", "", f"- Head: `{data['repository']['head']}`", f"- Base: `{data['repository']['base']}`", f"- Changed paths: {len(data['comparison']['changes'])}", "", "## Skill Maintenance Candidates", "", "| Skill | Status | Signals |", "|---|---|---:|"]
    lines.extend(f"| `{item['skill']}` | `{item['status']}` | {len(item['signals'])} |" for item in data["maintenance_candidates"])
    lines.extend(["", "## Declared Relationships", ""])
    relations = data["relationships"]["declared"]
    if relations:
        lines.extend(f"- `{edge['from']}` -> `{edge['to']}`" for edge in relations)
    else:
        lines.append("- None")
    lines.extend(["", "## Scope-overlap Warnings", ""])
    overlaps = data["relationships"]["scope_overlap_warnings"]
    if overlaps:
        lines.extend(f"- `{item['left']}` / `{item['right']}` ({item['similarity']})" for item in overlaps)
    else:
        lines.append("- None")
    lines.extend(["", "## Capability Candidates", ""])
    capabilities = data["capability_candidates"]
    if capabilities:
        lines.extend(f"- `{item['changed_area']}` — `USER_DECISION_REQUIRED`" for item in capabilities)
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="confirmed repository root to compare")
    parser.add_argument("--base", required=True, help="Git revision or ref used as the comparison base")
    parser.add_argument("--skills-root", type=Path, required=True, help="portfolio root containing skill folders")
    parser.add_argument("--working-tree", action="store_true", help="include local modified and untracked paths")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path, help="write report to this path instead of stdout")
    args = parser.parse_args()
    repo = args.repo.resolve()
    skills_root = args.skills_root.resolve()
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        raise SystemExit(f"--repo is not a Git checkout: {repo}")
    if not skills_root.is_dir():
        raise SystemExit(f"--skills-root is not a directory: {skills_root}")
    try:
        data = report(repo, skills_root, args.base, args.working_tree)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else markdown(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"report: wrote {args.output}")
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
