#!/usr/bin/env python3
"""Validate deterministic UO official-evidence fixtures."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).parent
    trigger = json.loads((root / "trigger_cases.json").read_text(encoding="utf-8"))
    behavior = json.loads((root / "behavior_cases.json").read_text(encoding="utf-8"))["cases"]

    assert len(trigger["should_trigger"]) >= 6
    positive_text = " ".join(case["text"] for case in trigger["should_trigger"])
    assert "offiziellen" in positive_text
    assert "servidores oficiales" in positive_text
    assert any(case["family"] == "publish_mapping" for case in trigger["should_not_trigger"])

    names = {case["name"] for case in behavior}
    assert len(names) == len(behavior)
    assert {case["expected_conclusion"] for case in behavior} >= {
        "official-controls",
        "newer-official-controls-current",
        "UNRESOLVED",
    }
    assert all(case.get("required_labels") for case in behavior)
    print(json.dumps({"cases": len(behavior), "passing": len(behavior), "failing": 0}))


if __name__ == "__main__":
    main()
