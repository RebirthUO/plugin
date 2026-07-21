#!/usr/bin/env python3
"""Execute captured-response contract checks for this migration skill."""

import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
skill = (root / "SKILL.md").read_text(encoding="utf-8")
data = json.loads((root / "evals" / "behavior_cases.json").read_text(encoding="utf-8"))
triggers = json.loads((root / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
semantic = json.loads((root / "evals" / "semantic_config.json").read_text(encoding="utf-8"))
allowed = set(data["global_assertions"]["status_values"])
headings = ["Outcome", "Scope", "Migration Inventory", "Evidence", "Checklist", "Compatibility Decisions", "Files", "Validation", "Residual Risk"]
errors = []

for case in data["cases"]:
    response = case.get("response_fixture", "")
    state = case.get("expected_status")
    if state not in allowed:
        errors.append(f"{case['name']}: invalid or missing expected_status")
    found = re.findall(r"^# (.+)$", response, re.MULTILINE)
    if found != headings:
        errors.append(f"{case['name']}: response headings differ: {found}")
    if f"| {state} |" not in response:
        errors.append(f"{case['name']}: response does not emit {state}")
    for key in ("must_reject", "must_require"):
        if case.get(key) and case[key].lower() not in response.lower():
            errors.append(f"{case['name']}: response omits {key} assertion")
    if case.get("must_preserve_mode") and f"| {case['must_preserve_mode'].upper()} |" not in response:
        errors.append(f"{case['name']}: response changes requested mode")

positive = [x["text"] for x in triggers["should_trigger"]]
if not any(re.search(r"\b(diese|dieser|dieses|nach|mit|samt)\b|[äöüß]", text.lower()) for text in positive):
    errors.append("missing representative German positive trigger")
semantic_actions = set(semantic["optimizer_hints"]["trigger_actions"])
if not semantic_actions.issubset(set(positive)):
    errors.append("semantic trigger actions are not synchronized with trigger fixtures")
for heading in headings:
    if f"`# {heading}`" not in skill:
        errors.append(f"SKILL.md omits contract heading {heading}")
for state in allowed:
    if f"`{state}`" not in skill:
        errors.append(f"SKILL.md omits status {state}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"captured behavior responses: passed ({len(data['cases'])} cases); multilingual triggers: passed")
