#!/usr/bin/env python3
"""Verify plugin skill portfolio invariants."""

import hashlib
import json
import re
from pathlib import Path

PLUGIN_SKILLS = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\plugins\modernuo\skills")
GHOST = [
    "modernuo-ticket-triage",
    "uo-domain-research",
    "modernuo-era-parity-check",
    "ultima-online-product-model",
]
REMOVED = {"ultima-online-product-model", "rebirthuo-implementation", "polymarket"}


def main() -> None:
    names = sorted(p.name for p in PLUGIN_SKILLS.iterdir() if p.is_dir())
    errors = []
    for bad in REMOVED:
        if bad in names:
            errors.append(f"removed skill still present: {bad}")
    for name in names:
        md = PLUGIN_SKILLS / name / "SKILL.md"
        if not md.exists():
            errors.append(f"missing SKILL.md: {name}")
            continue
        text = md.read_text(encoding="utf-8")
        if "skill_group:" not in text:
            errors.append(f"missing skill_group: {name}")
        for ghost in GHOST:
            if ghost in text:
                errors.append(f"ghost ref {ghost} in {name}")
        if not text.startswith("---"):
            errors.append(f"no frontmatter: {name}")
        if text.count("---") < 2:
            errors.append(f"unclosed frontmatter: {name}")
    catalog = PLUGIN_SKILLS / "SKILL-CATALOG.md"
    if not catalog.exists():
        errors.append("missing SKILL-CATALOG.md")
    report = {"skill_count": len(names), "errors": errors, "ok": not errors}
    out = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\scripts\skill-verify-report.json")
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
