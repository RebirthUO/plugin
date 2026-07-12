#!/usr/bin/env python3
"""Run Yao production gates across every ModernUO plugin skill."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(command: list[str], cwd: Path) -> dict:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip()[-12000:],
        "stderr": result.stderr.strip()[-12000:],
    }


def gate_commands(skill: Path, yao_root: Path, extended: bool) -> list[tuple[str, list[str]]]:
    scripts = yao_root / "scripts"
    python = sys.executable
    evals = skill / "evals"
    reports = skill / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    commands: list[tuple[str, list[str]]] = [
        (
            "validate",
            [python, str(scripts / "yao.py"), "validate", str(skill), "--require-manifest"],
        ),
        (
            "context",
            [python, str(scripts / "context_sizer.py"), "--json", str(skill)],
        ),
        (
            "resource-boundary",
            [python, str(scripts / "resource_boundary_check.py"), str(skill)],
        ),
        (
            "trigger",
            [
                python,
                str(scripts / "trigger_eval.py"),
                "--description-file",
                str(skill / "SKILL.md"),
                "--baseline-description-file",
                str(evals / "baseline_description.txt"),
                "--cases",
                str(evals / "trigger_cases.json"),
                "--semantic-config",
                str(evals / "semantic_config.json"),
            ],
        ),
        (
            "skill-ir",
            [
                python,
                str(scripts / "yao.py"),
                "skill-ir",
                str(skill),
                "--output-json",
                str(reports / "skill-ir.json"),
            ],
        ),
    ]
    if extended:
        commands.extend(
            [
                (
                    "conformance",
                    [
                        python,
                        str(scripts / "run_conformance_suite.py"),
                        str(skill),
                        "--output-json",
                        str(reports / "conformance-matrix.json"),
                        "--output-md",
                        str(reports / "conformance-matrix.md"),
                    ],
                ),
                (
                    "trust",
                    [
                        python,
                        str(scripts / "trust_check.py"),
                        str(skill),
                        "--output-json",
                        str(reports / "security_trust_report.json"),
                        "--output-md",
                        str(reports / "security_trust_report.md"),
                    ],
                ),
            ]
        )
    return commands


def validate_one(skill: Path, yao_root: Path, extended: bool) -> dict:
    gates: dict[str, dict] = {}
    for name, command in gate_commands(skill, yao_root, extended):
        gates[name] = run(command, yao_root)
        if gates[name]["returncode"] != 0 and name == "skill-ir":
            break
    return {
        "name": skill.name,
        "ok": all(gate["returncode"] == 0 for gate in gates.values()),
        "gates": gates,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Yao Portfolio Validation",
        "",
        f"Generated: {report['generated_at']}",
        f"Skills: {report['skill_count']}",
        f"Passing: {report['passing']}",
        f"Failing: {report['failing']}",
        "",
        "| Skill | Status | Failed gates |",
        "|---|---|---|",
    ]
    for skill in report["skills"]:
        failed = [
            name for name, gate in skill["gates"].items() if gate["returncode"] != 0
        ]
        lines.append(
            f"| `{skill['name']}` | {'pass' if skill['ok'] else 'fail'} | {', '.join(failed) or '—'} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            "These gates cover local package structure, context/resource boundaries, semantic trigger fixtures, Skill IR, and—when requested—static conformance and trust checks. They do not prove provider-backed model execution, human blind-review agreement, native client permission enforcement, or live adoption telemetry; those remain `missing evidence`.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=repo_root / "plugins" / "modernuo" / "skills",
    )
    parser.add_argument(
        "--yao-root",
        type=Path,
        default=Path(os.environ["YAO_META_SKILL_ROOT"])
        if os.environ.get("YAO_META_SKILL_ROOT")
        else None,
        help="Path containing the selected yao-meta-skill SKILL.md and scripts/",
    )
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument(
        "--report-json",
        type=Path,
        default=repo_root / "reports" / "yao-portfolio-validation.json",
    )
    parser.add_argument(
        "--report-md",
        type=Path,
        default=repo_root / "reports" / "yao-portfolio-validation.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.yao_root is None:
        raise SystemExit("Pass --yao-root or set YAO_META_SKILL_ROOT")
    yao_root = args.yao_root.resolve()
    if not (yao_root / "SKILL.md").exists() or not (yao_root / "scripts" / "yao.py").exists():
        raise SystemExit(f"Invalid Yao root: {yao_root}")
    all_skills = {
        path.parent.name: path.parent
        for path in args.skills_root.resolve().glob("*/SKILL.md")
    }
    requested = set(args.skills or all_skills.keys())
    missing = sorted(requested - all_skills.keys())
    if missing:
        raise SystemExit(f"Unknown skills: {', '.join(missing)}")

    selected = [all_skills[name] for name in sorted(requested)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(
            pool.map(
                lambda path: validate_one(path, yao_root, args.extended),
                selected,
            )
        )
    results.sort(key=lambda item: item["name"])
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "yao_root": str(yao_root),
        "extended": args.extended,
        "skill_count": len(results),
        "passing": sum(item["ok"] for item in results),
        "failing": sum(not item["ok"] for item in results),
        "skills": results,
    }
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    args.report_md.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    print(json.dumps({key: report[key] for key in ("skill_count", "passing", "failing")}, indent=2))
    if report["failing"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
