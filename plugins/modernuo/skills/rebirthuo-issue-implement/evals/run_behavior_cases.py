"""Assert implementation cases against the executable skill contract text."""
import json
from pathlib import Path

root=Path(__file__).parents[1]; cases=json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
contract="\n".join(path.read_text(encoding="utf-8") for path in [root/"SKILL.md",root/"references/implementation-workflow.md",root/"references/temporary-weapon-effects.md"]).casefold()
assertions={
 "blocked-rejected":["`not_ready` before edits","no `blocked` label"], "stale-revision":["matching post-publication","stale"],
 "new-gap":["freeze and preserve the worktree","next_skill: rebirthuo-issue-research"], "missing-constant":["never invent a deterministic table","visibly labeled custom"],
 "partial-publication":["ambiguous result requires read-back","mutation: { authorized: [], performed: [], failed: [] }"], "rollback":["regressions","`not_ready`"],
 "test-freshness":["focused tests run again after the final","after_final_edit: true"], "ready-delivery":["read back remote sha","state: not_ready | research | implemented | delivered"]}
ids={case["id"] for case in cases}; assert ids==set(assertions), f"case/assertion mismatch: {ids ^ set(assertions)}"
for case_id,tokens in assertions.items(): assert all(token.casefold() in contract for token in tokens), f"{case_id}: missing contract token"
print(json.dumps({"contract_cases":len(cases),"passing":len(cases),"failing":0}))
