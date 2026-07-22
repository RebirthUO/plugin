"""Validate the portable runtime behavior contract."""
import json
from pathlib import Path

cases=json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
assert [case["kind"] for case in cases] == ["missing_context","safety_branch","label_handoff","verification_branch","output_contract"]
assert [case["expected_outcome"] for case in cases] == ["BLOCKED","REVIEWED","REVIEWED","REVIEWED","REVIEWED"]
assert all(case["scenario"] for case in cases)
assert cases[-1]["required_fields"] == ["Outcome","Repository revision","Decision","Evidence","Verification","Confidence","Limitations"]
contract="\n".join(path.read_text(encoding="utf-8") for path in [Path(__file__).parents[1]/"SKILL.md",Path(__file__).parents[1]/"references/workflow-state-machine.md"]).casefold()
for token in ["format: fallback", "template_provider_blocked", "verified pr url", "label_selection", "does not decide whether a label is relevant"]: assert token in contract
print(json.dumps({"contract_cases":len(cases),"passing":len(cases),"failing":0}))
