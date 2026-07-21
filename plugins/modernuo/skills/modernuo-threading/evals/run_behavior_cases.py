"""Validate captured modernuo-threading outputs against behavior_cases.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def heading_positions(lines: list[str], heading: str) -> list[int]:
    pattern = re.compile(rf"^\s*{re.escape(heading)}\s*:\s*", re.IGNORECASE)
    return [index for index, line in enumerate(lines) if pattern.match(line)]


def validate(case: dict, output: str, assertions: dict) -> list[str]:
    errors: list[str] = []
    lines = output.splitlines()
    statuses = assertions["status_values"]
    status_lines = [lines[index] for index in heading_positions(lines, "Status")]
    status_match = (
        re.fullmatch(r"\s*Status\s*:\s*(SAFE|UNSAFE|INCONCLUSIVE|BLOCKED)\s*", status_lines[0])
        if len(status_lines) == 1 else None
    )
    if not status_match or status_match.group(1) != case["expected_status"]:
        errors.append("expected exactly one matching Status heading")

    positions = []
    for heading in case["required_headings_in_order"]:
        matches = heading_positions(lines, heading)
        if len(matches) != 1:
            errors.append(f"expected exactly one {heading} heading")
        else:
            positions.append(matches[0])
    if len(positions) == len(case["required_headings_in_order"]) and positions != sorted(positions):
        errors.append("headings are out of order")

    for token in case["must_include"]:
        if token.casefold() not in output.casefold():
            errors.append(f"missing required token: {token}")
    for claim in case["must_not_claim"]:
        if claim.casefold() in output.casefold():
            errors.append(f"forbidden claim: {claim}")
    sections = {}
    for index, heading in enumerate(case["required_headings_in_order"]):
        if index < len(positions):
            end = positions[index + 1] if index + 1 < len(positions) else len(lines)
            sections[heading] = "\n".join(lines[positions[index]:end])
    for heading, tokens in case.get("section_assertions", {}).items():
        section = sections.get(heading, "")
        for token in tokens:
            if token.casefold() not in section.casefold():
                errors.append(f"{heading} lacks semantic token: {token}")
    evidence = sections.get("Evidence", "")
    require_locator = assertions.get("require_source_locator_for_material_claims", False)
    if case["expected_status"] == "BLOCKED":
        if not re.search(r"\b(missing|unavailable|not provided)\b", evidence, re.IGNORECASE):
            errors.append("Blocked Evidence lacks the missing-input reason")
        if re.search(r"\b[0-9a-f]{40}\b", evidence, re.IGNORECASE) or re.search(r"\S+(?:#L\d+|:\d+)", evidence):
            errors.append("Blocked Evidence fabricates unavailable repository evidence")
    elif require_locator:
        context = case.get("repository_context") or {}
        repository_root = context.get("repository_root")
        if not repository_root or repository_root.casefold() not in evidence.casefold():
            errors.append("Evidence lacks the configured repository root")
        if not re.search(r"\b[0-9a-f]{40}\b", evidence, re.IGNORECASE):
            errors.append("Evidence lacks a resolved revision")
        if not re.search(r"\S+(?:#L\d+|:\d+)", evidence):
            errors.append("Evidence lacks a source locator")
    verification = sections.get("Verification", "")
    if not re.search(r"\b(passed|failed|not run)\b", verification, re.IGNORECASE):
        errors.append("Verification lacks a result token")
    unresolved = sections.get("Unresolved", "")
    if not re.search(r"\b(high|medium|low)\b", unresolved, re.IGNORECASE):
        errors.append("Unresolved lacks confidence")
    if assertions.get("forbid_measured_claims_without_measured_evidence", False):
        measured_claim = re.search(
            r"\b(runtime|stress|profile|trace)\b.{0,40}\b(passed|verified|safe)\b",
            output, re.IGNORECASE | re.DOTALL,
        )
        measured_evidence = re.search(
            r"\b(measured|runtime trace|stress result|profile result)\b", evidence, re.IGNORECASE
        )
        if measured_claim and not measured_evidence:
            errors.append("measured claim lacks measured Evidence")
    return errors


def valid_output(case: dict) -> str:
    tokens = " ".join(case["must_include"])
    evidence = (
        "missing repository; revision and source locator unavailable"
        if case["expected_status"] == "BLOCKED"
        else f"repository {case['repository_context']['repository_root']} revision aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa Server/Foo.cs#L10 static source locator"
    )
    values = {
        "Evidence": f"{evidence} {tokens}", "Context and Ownership": f"event loop {tokens}",
        "Crossings and Handoff": f"None {tokens}", "Lifecycle": f"bounded {tokens}",
        "Verification": f"focused check {'not run' if case['expected_status'] == 'BLOCKED' else 'passed'} {tokens}",
        "Unresolved": f"confidence {'low' if case['expected_status'] == 'BLOCKED' else 'high'} {tokens}",
    }
    for heading, expected in case.get("section_assertions", {}).items():
        values[heading] += " " + " ".join(expected)
    return "\n".join([f"Status: {case['expected_status']}"] + [
        f"{heading}: {values[heading]}" for heading in case["required_headings_in_order"][1:]
    ])


def self_test(fixture: dict) -> list[str]:
    assertions = fixture["global_assertions"]
    failures = []
    for case in fixture["cases"]:
        context = case.get("repository_context")
        if case["expected_status"] == "BLOCKED" and context is not None:
            failures.append(f"blocked {case['name']} fixture unexpectedly supplies repository context")
        if case["expected_status"] != "BLOCKED" and not isinstance(context, dict):
            failures.append(f"evidence-dependent {case['name']} fixture lacks repository context")
        errors = validate(case, valid_output(case), assertions)
        if errors:
            failures.append(f"valid {case['name']} fixture was rejected: {errors}")
    incidental = valid_output(fixture["cases"][-1]).replace(
        "Unresolved:", "Unresolved: would become BLOCKED if ownership evidence disappears;"
    )
    if validate(fixture["cases"][-1], incidental, assertions):
        failures.append("valid incidental status reference was rejected")
    case = next(case for case in fixture["cases"] if case["name"] == "safe event-loop continuation")
    valid = valid_output(case)
    corruptions = [
        valid.replace("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "unknown"),
        valid.replace("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "abcdef1"),
        valid.replace("Server/Foo.cs#L10", "no-locator"),
        valid.replace("C:/fixture/ModernUO", ""),
        re.sub(r"Verification:.*", "Verification: unknown", valid),
        re.sub(r"Unresolved:.*", "Unresolved: confidence unknown", valid),
        valid + "\nStatus: BLOCKED",
        valid.replace("Status: SAFE", "StatusDetail: SAFE"),
        valid.replace("Status: SAFE", "Status: SAFE-extra"),
        valid.replace("Lifecycle: bounded", "Lifecycle: runtime verified safe"),
        valid.replace("EventLoopContext", "unknown owner"),
    ]
    for index, output in enumerate(corruptions, 1):
        if not validate(case, output, assertions):
            failures.append(f"invalid fixture {index} was accepted")
    blocked = next(case for case in fixture["cases"] if case["expected_status"] == "BLOCKED")
    fabricated = valid_output(blocked).replace(
        "missing repository; revision and source locator unavailable",
        "missing repository aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa Fake.cs#L1",
    )
    if not validate(blocked, fabricated, assertions):
        failures.append("blocked fixture with fabricated repository evidence was accepted")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--outputs", type=Path)
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    fixture_path = Path(__file__).with_name("behavior_cases.json")
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    if args.self_test:
        failures = self_test(fixture)
        if failures:
            print("\n".join(failures))
            return 1
        print("Behavior validator self-test passed")
        return 0
    outputs = json.loads(args.outputs.read_text(encoding="utf-8"))
    failures = []
    for case in fixture["cases"]:
        output = outputs.get(case["name"])
        if not isinstance(output, str):
            failures.append(f"{case['name']}: missing string output")
            continue
        for error in validate(case, output, fixture["global_assertions"]):
            failures.append(f"{case['name']}: {error}")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"Validated {len(fixture['cases'])} behavior outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
