"""Assert template-gate cases against the executable skill contract text."""
import json
from pathlib import Path

root = Path(__file__).parents[1]
cases = json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
contract = "\n".join(path.read_text(encoding="utf-8") for path in [root / "SKILL.md", root / "references/template-selection-contract.md"]).casefold()
assertions = {
    "researchable-field": ["research placeholder", "do not block on a mechanics field"],
    "ambiguous-template": ["template_blocked", "stable ids"],
    "repository-missing": ["applicable `agents.md`", "never infer identity"],
    "no-template": ["no live template exists", "template_blocked"],
    "no-fit": ["no candidate fits", "do not fall back to a free-form issue"],
    "drift": ["digest changed", "repeat selection"],
    "provider-failure": ["template_provider_blocked", "mutation_performed: false"],
}
ids = {case["id"] for case in cases}
assert ids == set(assertions), f"case/assertion mismatch: {ids ^ set(assertions)}"
for case_id, tokens in assertions.items():
    assert all(token.casefold() in contract for token in tokens), f"{case_id}: missing contract token"
print(json.dumps({"contract_cases": len(cases), "passing": len(cases), "failing": 0}))
