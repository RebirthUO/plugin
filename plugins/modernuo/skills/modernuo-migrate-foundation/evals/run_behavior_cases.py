#!/usr/bin/env python3
"""Validate deterministic migration-foundation behavior fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ALLOWED_STATES = {
    "PLANNED",
    "IMPLEMENTED",
    "AUDITED",
    "OUT_OF_SCOPE",
    "BLOCKED_INPUT",
    "BLOCKED_COMPATIBILITY",
    "BLOCKED_EVIDENCE",
    "VALIDATION_FAILED",
}
REQUIRED_HEADINGS = {
    "Outcome",
    "Scope",
    "Migration Inventory",
    "Evidence",
    "Checklist",
    "Compatibility Decisions",
    "Files",
    "Validation",
    "Residual Risk",
}


def main() -> None:
    path = Path(__file__).with_name("behavior_cases.json")
    cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    names: set[str] = set()
    states: set[str] = set()
    for case in cases:
        assert case["name"] not in names, f"duplicate case: {case['name']}"
        assert case.get("prompt", "").strip(), f"missing prompt: {case['name']}"
        assert case["expected_state"] in ALLOWED_STATES, case
        names.add(case["name"])
        states.add(case["expected_state"])
        if "required_headings" in case:
            assert set(case["required_headings"]) == REQUIRED_HEADINGS, case["name"]
            assert case.get("required_outcome_columns") == ["State", "Mode", "Confidence"]
    required_states = {
        "PLANNED",
        "OUT_OF_SCOPE",
        "BLOCKED_INPUT",
        "BLOCKED_COMPATIBILITY",
        "BLOCKED_EVIDENCE",
        "VALIDATION_FAILED",
    }
    assert required_states <= states, f"missing states: {sorted(required_states - states)}"
    print(json.dumps({"cases": len(cases), "passing": len(cases), "failing": 0}))


if __name__ == "__main__":
    main()
