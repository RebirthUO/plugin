"""Assert intake cases against the executable skill contract text."""
import json
from pathlib import Path

root = Path(__file__).parents[1]
cases = json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
contract = "\n".join(path.read_text(encoding="utf-8") for path in [root / "SKILL.md", root / "references/authoring-contract.md"]).casefold()
assertions = {
 "standalone-continuation":["ask exactly once", "ask_research"], "workflow-continuation":["asking again", "continuation: ask_research | research"],
 "owned-placeholder":["research owner", "claim-specific"], "repository-failure":["never infer it from cwd", "intake_blocked"],
 "template-drift":["template digest immediately before creation", "re-read and compare"], "duplicate":["duplicate blocks creation", "code: repository | template | duplicate"],
 "missing-label":["separate label-maintenance", "never creates or edits labels"], "unauthorized":["drafting is read-only", "explicit request"],
 "readback-mismatch":["intake_provider_blocked", "no blind retry"], "ambiguous-create":["search for the exact title/body before retrying", "mutation_performed: false | unknown"]}
ids={case["id"] for case in cases}; assert ids==set(assertions), f"case/assertion mismatch: {ids ^ set(assertions)}"
for case_id,tokens in assertions.items(): assert all(token.casefold() in contract for token in tokens), f"{case_id}: missing contract token"
print(json.dumps({"contract_cases":len(cases),"passing":len(cases),"failing":0}))
