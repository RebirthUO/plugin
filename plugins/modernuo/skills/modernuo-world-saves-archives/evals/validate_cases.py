#!/usr/bin/env python3
"""Validate behavior fixtures, capture provenance, and captured responses."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTCOMES = {
    "ADVICE_ONLY", "REVIEW_ONLY", "PLAN_ONLY", "IMPLEMENTED",
    "CLARIFICATION_REQUIRED", "BLOCKED", "INCONCLUSIVE",
}
LOCATOR = re.compile(r"\b[0-9a-f]{40}:[^#\r\n]+#(?:L\d+|symbol:[^\r\n]+)", re.I)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_schema(data):
    names = set()
    for case in data["cases"]:
        name = case["name"]
        if name in names:
            raise ValueError(f"duplicate case: {name}")
        names.add(name)
        if case["expected_outcome"] not in OUTCOMES:
            raise ValueError(f"invalid outcome for {name}")
        for field in ("input", "expected_mode", "must_include", "must_not_claim"):
            if field not in case:
                raise ValueError(f"missing {field} for {name}")
    headings = data["global_assertions"]["required_headings_in_order"]
    if headings[0] != "Status" or len(headings) != len(set(headings)):
        raise ValueError("headings must be unique and start with Status")


def validate_activation_alignment():
    skill = (ROOT.parent / "SKILL.md").read_text(encoding="utf-8").lower()
    baseline = (ROOT / "baseline_description.txt").read_text(encoding="utf-8").lower()
    semantic = load(ROOT / "semantic_config.json")
    triggers = load(ROOT / "trigger_cases.json")
    for phrase in ("entity field serialization", "arbitrary archive"):
        if phrase not in skill:
            raise ValueError(f"SKILL.md exclusion missing: {phrase}")
    for phrase in ("entity field serialization", "archive utilities"):
        if phrase not in baseline:
            raise ValueError(f"baseline exclusion missing: {phrase}")
    if not semantic["optimizer_hints"]["exclusions"]:
        raise ValueError("semantic exclusions are empty")
    for group in ("should_trigger", "should_not_trigger", "near_neighbor"):
        if not triggers[group]:
            raise ValueError(f"empty trigger group: {group}")


def validate_provenance(responses_path):
    meta = load(ROOT / "captured_responses.meta.json")
    required = {
        "schema", "captured_at", "generator_runtime", "generator_model",
        "source_agent", "generator_prompt", "repository_revision",
        "skill_sha256", "behavior_cases_sha256", "captured_responses_sha256",
    }
    if not required.issubset(meta) or meta["schema"] != "skill-behavior-capture/v1":
        raise ValueError("captured-response provenance is incomplete")
    checks = {
        "skill_sha256": sha256(ROOT.parent / "SKILL.md"),
        "behavior_cases_sha256": sha256(ROOT / "behavior_cases.json"),
        "captured_responses_sha256": sha256(responses_path),
    }
    for field, actual in checks.items():
        if meta[field] != actual:
            raise ValueError(f"stale captured-response provenance: {field}")


def validate_responses(data, responses):
    headings = data["global_assertions"]["required_headings_in_order"]
    failures = []
    for case in data["cases"]:
        name = case["name"]
        response = responses.get(name)
        if not isinstance(response, str):
            failures.append(f"{name}: missing response")
            continue
        actual_headings = re.findall(r"(?m)^# ([^\r\n]+)\r?$", response)
        if actual_headings != headings:
            failures.append(f"{name}: exact H1 headings missing, duplicated, or out of order")
        status_match = re.search(r"(?ms)^# Status\s*\n+([^\r\n]+)", response)
        status = status_match.group(1).strip() if status_match else ""
        if status != case["expected_outcome"]:
            failures.append(f"{name}: status must equal expected outcome")
        confidence = re.findall(r"(?i)\bconfidence:\s*(high|medium|low)\b", response)
        if not confidence:
            failures.append(f"{name}: calibrated confidence is missing")
        lowered = response.lower()
        missing_revision = any(
            phrase in lowered
            for phrase in ("revision: missing", "revision: not supplied", "revision was not identified", "revision: not provided", "none was supplied")
        )
        if missing_revision and confidence and confidence[0].lower() != "low":
            failures.append(f"{name}: missing revision requires overall low confidence")
        for phrase in case["must_include"]:
            if phrase.lower() not in lowered:
                failures.append(f"{name}: missing phrase {phrase}")
        for phrase in case["must_not_claim"]:
            if phrase.lower() in lowered:
                failures.append(f"{name}: forbidden claim {phrase}")
        if status == "IMPLEMENTED":
            if "unresolved" in lowered or "tests pass" not in lowered:
                failures.append(f"{name}: implementation lacks resolved decisions or passed tests")
            if not LOCATOR.search(response):
                failures.append(f"{name}: implementation claim lacks revision-bound locator")
        safety_claim = re.search(r"(?i)\b(?:restore|data)[ -]?safe\b|\bsafety guarantee(?:d|s)?\b", response)
        if safety_claim and (status != "IMPLEMENTED" or "isolated restore" not in lowered or "not run" in lowered):
            failures.append(f"{name}: unsupported safety claim")
        if status in {"BLOCKED", "INCONCLUSIVE", "CLARIFICATION_REQUIRED"} and "# Recovery and Risk" not in response:
            failures.append(f"{name}: degraded outcome lacks recovery and risk")
    extra = set(responses) - {case["name"] for case in data["cases"]}
    if extra:
        failures.append(f"unexpected captured cases: {sorted(extra)}")
    if failures:
        raise ValueError("\n".join(failures))


def self_test(data):
    headings = data["global_assertions"]["required_headings_in_order"]
    responses = {}
    for case in data["cases"]:
        required = " ".join(case["must_include"])
        responses[case["name"]] = "\n\n".join(
            f"# {heading}\n{case['expected_outcome'] if heading == 'Status' else required or 'Confidence: low.'}"
            for heading in headings
        ).replace("# Repository Evidence\n", "# Repository Evidence\nConfidence: low. ")
    validate_responses(data, responses)
    first = data["cases"][0]["name"]
    bypass = dict(responses)
    bypass[first] += "\n\n# Status\nBLOCKED"
    try:
        validate_responses(data, bypass)
    except ValueError:
        pass
    else:
        raise ValueError("negative self-test accepted a duplicate status heading")
    implemented_case = dict(data["cases"][0])
    implemented_case["expected_outcome"] = "IMPLEMENTED"
    implemented_case["must_include"] = []
    implemented_case["must_not_claim"] = []
    implemented_data = {"cases": [implemented_case], "global_assertions": data["global_assertions"]}
    implemented_response = "\n\n".join(
        f"# {heading}\n{'IMPLEMENTED' if heading == 'Status' else 'Confidence: high. Tests passed.'}"
        for heading in headings
    )
    for invalid in (
        implemented_response,
        implemented_response + " Unresolved decision.",
        implemented_response.replace("Confidence: high", "Confidence: unknown"),
        implemented_response.replace("Tests passed.", "Tests passed. Restore-safe.")
    ):
        try:
            validate_responses(implemented_data, {implemented_case["name"]: invalid})
        except ValueError:
            continue
        raise ValueError("negative self-test accepted an implementation safety violation")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", type=Path, help="JSON mapping case names to captured responses")
    parser.add_argument("--self-test", action="store_true", help="unit-test the validator with synthetic responses")
    args = parser.parse_args()
    data = load(ROOT / "behavior_cases.json")
    validate_schema(data)
    validate_activation_alignment()
    responses_path = args.responses or ROOT / "captured_responses.json"
    if responses_path.exists():
        if responses_path.resolve() == (ROOT / "captured_responses.json").resolve():
            validate_provenance(responses_path)
        validate_responses(data, load(responses_path))
    elif not args.self_test:
        raise ValueError("captured responses are missing")
    if args.self_test:
        self_test(data)
    print("World-save behavior fixtures are valid.")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
