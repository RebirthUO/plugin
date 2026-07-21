# Scanner Evidence and Triage Contract

## Evidence classes

The scanner emits only the following classifications:

| Classification | Meaning | Required follow-up |
|---|---|---|
| `exact_path` | A changed repository path is quoted verbatim by a skill artifact. | Inspect whether the quoted claim or command is stale. |
| `keyword_overlap` | At least two normalized changed-path terms overlap a skill's activation boundary. | Treat as a lead only; verify current local anchors. |
| `declared_relation` | One skill explicitly names another installed sibling. | Check that routing and boundary wording still agree. |
| `scope_overlap` | Two descriptions share unusually specific vocabulary without a declared route. | Review the boundary; do not merge by default. |
| `uncovered_change_area` | Changed-path vocabulary has no meaningful portfolio match. | Offer a capability candidate for user decision. |

## Candidate rules

- `needs_review` is a triage status, never proof that a skill must change.
- A capability candidate remains `USER_DECISION_REQUIRED`, even when multiple
  uncovered paths share the same area.
- Ignore generic path words such as `src`, `test`, `tests`, `data`, `project`,
  and extensions. The report records its normalized tokens so results are
  reproducible.
- Scan only committed changes from the explicit base by default. The optional
  working-tree comparison is reported separately because it has no immutable
  revision identity.

## Interpretation order

1. Prefer exact path evidence over keyword overlap.
2. Prefer an explicit sibling route over description similarity.
3. Treat source changes as repository evidence; do not derive official gameplay
   behavior from them.
4. Ask the user to approve or reject every `uncovered_change_area` candidate
   before any new-skill work begins.
