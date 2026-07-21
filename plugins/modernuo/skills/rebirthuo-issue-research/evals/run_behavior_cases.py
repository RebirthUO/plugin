"""Assert research cases against the executable skill contract text."""
import json
from pathlib import Path

root=Path(__file__).parents[1]; cases=json.loads(Path(__file__).with_name("behavior_cases.json").read_text(encoding="utf-8"))["cases"]
contract="\n".join(path.read_text(encoding="utf-8") for path in [root/"SKILL.md",root/"references/research-contract.md",root/"references/issue-publication.md"]).casefold()
assertions={
 "retry-success":["materially different pass","does not count"], "era-inference":["infer likely era","record eliminated candidates"],
 "era-policy":["ambiguity_is_product_intent","supported choices"], "official-gap":["narrow scope","visibly labeled custom policy"],
 "repository-missing":["research_repository_blocked","never infer from cwd"], "issue-input":["issue_input_blocked","cross-repository locators"],
 "domain-skill-missing":["domain_skill: unavailable","repository directly"], "concurrent-overlap":["overlapping or ambiguous change","renewed authorization"],
 "advice-only":["advice_complete","leave action arrays empty"], "authorization":["authorization_required","proposed body"], "body-ok-label-fails":["state `partial`","record only proven actions"],
 "readback-mismatch":["read-back mismatch","never claim `ready`"]}
ids={case["id"] for case in cases}; assert ids==set(assertions), f"case/assertion mismatch: {ids ^ set(assertions)}"
for case_id,tokens in assertions.items(): assert all(token.casefold() in contract for token in tokens), f"{case_id}: missing contract token"
print(json.dumps({"contract_cases":len(cases),"passing":len(cases),"failing":0}))
