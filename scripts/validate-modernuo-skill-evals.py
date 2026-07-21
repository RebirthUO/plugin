#!/usr/bin/env python3
"""Validate portable trigger fixtures for one or more ModernUO skill packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate(package: Path) -> list[str]:
    errors: list[str] = []
    triggers = json.loads((package / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
    semantic = json.loads((package / "evals" / "semantic_config.json").read_text(encoding="utf-8"))
    behavior = json.loads((package / "evals" / "behavior_cases.json").read_text(encoding="utf-8"))
    positives = triggers.get("should_trigger", [])
    negatives = triggers.get("should_not_trigger", [])
    neighbors = triggers.get("near_neighbor", [])
    if not positives or not negatives or not neighbors:
        errors.append(f"{package.name}: each trigger family must be non-empty")
    if not any(case.get("family", "").endswith("_de") for case in positives):
        errors.append(f"{package.name}: missing representative German positive trigger")
    actions = semantic.get("optimizer_hints", {}).get("trigger_actions", [])
    positive_texts = {case.get("text") for case in positives}
    if not set(actions).issubset(positive_texts):
        errors.append(f"{package.name}: semantic trigger actions must be positive fixtures")
    concepts = semantic.get("positive_concepts", {}).values()
    phrases = {phrase for concept in concepts for phrase in concept.get("phrases", [])}
    for case in positives:
        if case.get("text") not in phrases:
            errors.append(f"{package.name}: positive fixture is not covered by a semantic phrase")
    for case in [*negatives, *neighbors]:
        if case.get("text") in phrases:
            errors.append(f"{package.name}: non-owned fixture is covered by a semantic phrase")
    cases = {case.get("kind"): case for case in behavior.get("cases", [])}
    required = {"missing_context", "safety_branch", "verification_branch", "output_contract"}
    if not required.issubset(cases):
        errors.append(f"{package.name}: missing required behavior-case kind")
    elif cases["missing_context"].get("expected_outcome") != "BLOCKED":
        errors.append(f"{package.name}: missing-context case must be BLOCKED")
    elif not cases["safety_branch"].get("must_preserve"):
        errors.append(f"{package.name}: safety case must preserve a named guard")
    elif not cases["verification_branch"].get("must_verify"):
        errors.append(f"{package.name}: verification case must name required evidence")
    elif set(cases["output_contract"].get("required_fields", [])) != {
        "Outcome",
        "Repository revision",
        "Decision",
        "Evidence",
        "Verification",
        "Confidence",
        "Limitations",
    }:
        errors.append(f"{package.name}: output case fields are incomplete")
    terminal_outcomes = behavior.get("terminal_outcomes")
    if terminal_outcomes is not None:
        if not isinstance(terminal_outcomes, dict) or not terminal_outcomes:
            errors.append(f"{package.name}: terminal_outcomes must be a non-empty object")
        else:
            for case in behavior.get("cases", []):
                kind = case.get("decision_kind")
                expected = case.get("expected_outcome")
                if kind not in terminal_outcomes:
                    errors.append(f"{package.name}: {case.get('kind')}: unknown decision_kind")
                elif expected not in terminal_outcomes[kind]:
                    errors.append(
                        f"{package.name}: {case.get('kind')}: expected_outcome is not permitted for {kind}"
                    )
    return errors


def main() -> None:
    packages = [Path(arg).resolve() for arg in sys.argv[1:]]
    if not packages:
        raise SystemExit("usage: validate-modernuo-skill-evals.py <skill-package> [...]")
    errors = [error for package in packages for error in validate(package)]
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"trigger fixtures: passed ({len(packages)} packages)")


if __name__ == "__main__":
    main()
