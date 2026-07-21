"""Assert workflow cases, state unions, and child dependencies."""
import json
from pathlib import Path

root=Path(__file__).parents[1]; skills_root=root.parent; cases=json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
contract="\n".join(path.read_text(encoding="utf-8") for path in [root/"SKILL.md",root/"references/workflow-state-machine.md"]).casefold()
assertions={
 "existing-route":["existing_issue","do not call issue creation"], "new-route":["new_request","without another confirmation"],
 "stale-template":["template","repeat template selection"], "stale-issue":["stale issue revision","transitions to"],
 "blocked-label":["`blocked`-label","implementation_blocked"], "access-failure":["external access","blocked"],
 "concurrent-state":["unsafe concurrent state","delivery_blocked"], "research-loop":["return to autonomous research","resume implementation"],
 "push-without-pr":["last_proven_step","retry only the unproven step"], "pr-readback-fails":["ambiguous read-back","remains blocked"],
 "delivered":["verified pr url","high confidence"]}
ids={case["id"] for case in cases}; assert ids==set(assertions), f"case/assertion mismatch: {ids ^ set(assertions)}"
for child in ["rebirthuo-issue-template-gate","rebirthuo-issue-create","rebirthuo-issue-research","rebirthuo-issue-implement"]: assert (skills_root/child/"SKILL.md").is_file(), f"missing child: {child}"
for case_id,tokens in assertions.items(): assert all(token.casefold() in contract for token in tokens), f"{case_id}: missing contract token"
print(json.dumps({"contract_cases":len(cases),"passing":len(cases),"failing":0}))
