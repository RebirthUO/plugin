#!/usr/bin/env python3
"""Forward-test ModernUO skill behavior fixtures in a read-only Codex runtime."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml


FIELDS = [
    "Outcome",
    "Repository revision",
    "Decision",
    "Evidence",
    "Verification",
    "Confidence",
    "Limitations",
]

PROMPT_VARIANTS = (
    ("direct", "Treat this as a direct, well-scoped request."),
    ("paraphrase", "Treat this as an informal paraphrase of the same request; preserve the skill boundary."),
    ("competing-scope", "A neighboring concern is mentioned, but do not take ownership of it unless this skill explicitly owns it."),
    ("incomplete-context", "The request may omit incidental context; apply the skill's own required-context gate instead of inventing facts."),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_inventory(package: Path) -> dict[str, str]:
    return {
        path.relative_to(package).as_posix(): sha256(path)
        for path in sorted(package.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def response_has_field(text: str, field: str) -> bool:
    return bool(
        re.search(
            rf"(?im)^\s*(?:[-*]\s+)?{re.escape(field)}:",
            text.replace("**", ""),
        )
    )


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def fenced_blocks(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"(?ms)^```(?P<language>[^\n]*)\n(?P<body>.*?)^```\s*$", text))


def validate_runtime_contract(section: str, case: dict[str, object], contract: dict[str, object]) -> dict[str, bool]:
    """Validate an opt-in package-specific response contract without constraining other skills."""
    blocks = fenced_blocks(section)
    yaml_blocks = [block for block in blocks if block.group("language").strip() == "yaml"]
    text_language = str(contract["visual_fence_language"])
    text_blocks = [block for block in blocks if block.group("language").strip() == text_language]
    parsed: object = None
    if len(yaml_blocks) == 1:
        try:
            parsed = yaml.safe_load(yaml_blocks[0].group("body"))
        except yaml.YAMLError:
            parsed = None
    yaml_mapping = isinstance(parsed, dict)
    required_fields = contract.get("required_yaml_fields", FIELDS)
    yaml_fields = yaml_mapping and all(field in parsed for field in required_fields)

    heading = str(contract["visual_heading"])
    headings = list(re.finditer(rf"(?m)^{re.escape(heading)}\s*$", section))
    visual_order = False
    if len(yaml_blocks) == 1 and len(text_blocks) == 1 and len(headings) == 1 and len(blocks) == 2:
        between = section[yaml_blocks[0].end() : headings[0].start()]
        after_heading = section[headings[0].end() : text_blocks[0].start()]
        trailing = section[text_blocks[0].end() :]
        visual_order = not between.strip() and not after_heading.strip() and not trailing.strip()

    details_ok = False
    if yaml_mapping:
        decision = parsed.get("Decision")
        records = decision.get("records") if isinstance(decision, dict) else None
        details_contract = contract.get("decision_details", {})
        required_detail_keys = details_contract.get("required_keys", []) if isinstance(details_contract, dict) else []
        allowed_types = details_contract.get("types", {}) if isinstance(details_contract, dict) else {}
        details_ok = isinstance(records, list) and bool(records)
        for record in records if isinstance(records, list) else []:
            details = record.get("details") if isinstance(record, dict) else None
            if not isinstance(details, dict) or not all(key in details for key in required_detail_keys):
                details_ok = False
                break
            detail_type = details.get("type")
            fields = details.get("fields")
            if not isinstance(detail_type, str) or detail_type not in allowed_types or not isinstance(details.get("summary"), str) or not isinstance(fields, dict):
                details_ok = False
                break
            if not all(key in fields for key in allowed_types[detail_type]):
                details_ok = False
                break

    required_assertions = [
        value
        for key, value in case.items()
        if key in {"must_require", "must_preserve", "must_verify"} and isinstance(value, str)
    ]
    assertions_ok = (
        not contract.get("require_exact_case_assertions")
        or all(normalize_whitespace(value) in normalize_whitespace(section) for value in required_assertions)
    )
    return {
        "yaml_mapping": yaml_mapping,
        "yaml_fields": bool(yaml_fields),
        "visual_contract": visual_order,
        "decision_details": details_ok,
        "case_assertions": assertions_ok,
    }


def run_case(repo: Path, package: Path, output_dir: Path, codex: str) -> dict[str, object]:
    skill_path = package / "SKILL.md"
    cases_path = package / "evals" / "behavior_cases.json"
    skill = skill_path.read_text(encoding="utf-8")
    behavior = json.loads(cases_path.read_text(encoding="utf-8"))
    base_cases = behavior["cases"]
    runtime_contract = behavior.get("runtime_contract")
    cases = [
        {
            **case,
            "variant": variant_name,
            "scenario": f"{variant_instruction} {case['scenario']}",
        }
        for variant_name, variant_instruction in PROMPT_VARIANTS
        for case in base_cases
    ]
    response_path = output_dir / f"{package.name}.md"
    prompt = (
        "Apply the following Agent Skill exactly. Do not use tools or commands and do not modify files. "
        "Evaluate every supplied behavior case and respond in Markdown with one labeled response per case. "
        "Each response must contain every required output field and must honor the expected outcome. "
        "When a case has must_require, must_preserve, or must_verify, include its value verbatim in a Decision record so the behavior assertion is auditable. "
        "When the behavior cases declare runtime_contract, satisfy it exactly.\n\n"
        f"# Agent Skill\n{skill}\n# Behavior Cases\n{json.dumps({'cases': cases}, ensure_ascii=False, indent=2)}"
    )
    result = subprocess.run(
        [
            codex,
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "-C",
            str(repo),
            "--output-last-message",
            str(response_path),
            "-",
        ],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    text = response_path.read_text(encoding="utf-8") if response_path.exists() else ""
    normalized = text.replace("**", "")
    sections = re.split(
        r"(?im)^(?:#{1,4}\s*Case\s+\d+[^\n]*|\s*-\s+Label:\s*[\"']?Case\s+\d+[^\n]*)\n",
        normalized,
    )[1:]
    outcomes = re.findall(r"(?im)^\s*(?:[-*]\s+)?Outcome:\s*`?([A-Z]+)`?", normalized)
    expected = [case["expected_outcome"] for case in cases]
    fields_ok = len(sections) == len(cases) and all(
        all(response_has_field(section, field) for field in FIELDS) for section in sections
    )
    contract_results = [
        validate_runtime_contract(section, case, runtime_contract)
        for section, case in zip(sections, cases)
    ] if isinstance(runtime_contract, dict) and len(sections) == len(cases) else []
    runtime_contract_passed = not isinstance(runtime_contract, dict) or (
        len(contract_results) == len(cases) and all(all(result.values()) for result in contract_results)
    )
    return {
        "package": package.name,
        "package_files": package_inventory(package),
        "skill_sha256": sha256(skill_path),
        "behavior_cases_sha256": sha256(cases_path),
        "prompt_variants": [variant_name for variant_name, _ in PROMPT_VARIANTS],
        "response_file": response_path.name if response_path.exists() else None,
        "response_sha256": sha256(response_path) if response_path.exists() else None,
        "returncode": result.returncode,
        "expected_outcomes": expected,
        "observed_outcomes": outcomes,
        "required_fields": FIELDS,
        "field_contract_passed": fields_ok,
        "runtime_contract": runtime_contract,
        "runtime_contract_results": contract_results,
        "runtime_contract_passed": runtime_contract_passed,
        "passed": result.returncode == 0 and fields_ok and runtime_contract_passed and outcomes == expected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--codex", default=shutil.which("codex") or shutil.which("codex.cmd"))
    args = parser.parse_args()
    if not args.codex:
        raise SystemExit("Codex CLI is unavailable; runtime smoke cannot run.")

    repo = Path.cwd().resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    packages = [package.resolve() for package in args.packages]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda package: run_case(repo, package, output_dir, args.codex), packages))

    summary = {
        "schema": "modernuo-runtime-smoke/v1",
        "execution": {
            "runner": "codex exec --ignore-user-config --ephemeral --sandbox read-only",
            "codex_path": args.codex,
            "working_directory": str(repo),
        "mode": "skill and behavior cases injected into a read-only runtime prompt; no tool use",
            "runner_sha256": sha256(Path(__file__).resolve()),
        },
        "results": results,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    failures = [result["package"] for result in results if not result["passed"]]
    print(f"runtime smoke: {len(results) - len(failures)}/{len(results)} passed")
    if failures:
        raise SystemExit("failed: " + ", ".join(failures))


if __name__ == "__main__":
    main()
