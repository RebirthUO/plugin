# Publish Era Measurement

Use this reference when `modernuo-ticket-triage` sees a publish number, publish note, era name, expansion, or Endless Journey claim. The goal is to choose the correct measurement target before planning code.

## Rule

- Treat publish-derived information as a measurement target, not a generic current-live fact.
- If a publish introduced or changed behavior, compare the repo against the era/profile active for that publish.
- Do not assign a publish to an era without repo or internet evidence.
- If the mapping is disputed, use `source-conflict` and keep the issue blocked on a verified mapping decision.

## Verified Anchors

These are anchors, not a complete publish catalog.

| Publish / Source | Verified evidence | Measurement guidance |
|---|---|---|
| Publish 81 | UO.com lists World Wide Release as `04/16/2013`; UOGuide also has `Publish_81`. | Not Time of Legends. Treat as a post-High Seas, pre-Time of Legends publish-level measurement unless a repo era profile defines a finer gate. |
| Publish 90 | UO.com announcement says `Publish 90, The Time of Legends` was available after maintenance on October 8, 2015; UOGuide `Publishes` lists Publish 90 as the Time of Legends expansion. | Time of Legends measurement. Behavior introduced here normally needs a `Core.TOL`, `Expansion.TOL`, or ToL EraProfile decision. |
| Endless Journey | UOGuide expansion timeline lists EJ as March 2018; repo guidance has treated EJ as account/policy/profile-heavy rather than ordinary content parity. | Special case. Measure EJ as profile/account-policy restrictions unless evidence shows a normal expansion/content gate. Check account, bank/storage, housing, and active EraProfile evidence. |

## Working Method

1. Find the publish note or publish index entry in UO.com, UOGuide, repo docs, or another cited source.
2. Record publish number, release date, linked source, and changed behavior.
3. Map that evidence to one of:
   - named expansion era (`Core.TOL`, `Core.SA`, etc.);
   - publish-level measurement when between expansions;
   - EraProfile/profile measurement;
   - EJ policy/profile measurement;
   - `open-research` when not enough evidence exists.
4. Use that measurement in `Publish / Era Check`, `Acceptance Criteria`, and any recommended gate.

## Source Starting Points

- `https://uo.com/wiki/ultima-online-wiki/publish-notes/`
- `https://www.uoguide.com/Publishes`
- `https://uo.com/2015/10/07/time-of-legends-available-world-wide/`
- `https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2013-2/publish-81-16th-april/`
- `https://www.uoguide.com/Ultima_Online:_Time_of_Legends`
- `https://www.uoguide.com/Expansion`
