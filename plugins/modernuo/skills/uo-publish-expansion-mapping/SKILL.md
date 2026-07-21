---
name: uo-publish-expansion-mapping
description: >
  Map Ultima Online Publish numbers, release dates, and expansion-era questions
  to the next applicable true expansion and cumulative ModernUO Core gate. Use
  when research, documentation, issue intake, implementation, or review asks
  which expansion should own a Publish-era change, including post-TOL Publishes
  and Endless Journey restrictions.
---

# UO Publish-to-Expansion Mapping

## Workflow

1. Identify the exact Publish number, worldwide release date, and claimed
   expansion relationship. Prefer the current official UO.com Publish page and
   official archive; do not infer chronology from an issue, emulator, or memory.
2. Read [the era matrix](references/era-matrix.md). Refresh any boundary whose
   official source changed or whose evidence is incomplete before relying on it.
3. Use an explicit official expansion association when one exists. Otherwise,
   map a Publish between true expansion boundaries forward to the next named
   expansion. Treat the result as project activation policy, not a claim that
   the expansion was already live on the Publish date.
4. Recommend the consuming repository's cumulative guard only after inspecting
   its pinned expansion enum and `Core` flags. In current ModernUO, use the
   matching `Core.<ERA>` flag rather than a raw enum comparison when available.
5. Separate expansion era from account entitlement. Treat Endless Journey as a
   restricted account mode introduced with Publish 99, never as an expansion
   boundary. Map its underlying era to TOL and describe EJ checks separately.
6. Stop with `UNRESOLVED` when official sources conflict, the Publish cannot be
   identified, a future true expansion lacks a repository gate, or the consuming
   repository differs from the inspected ModernUO evidence.

## Authority and Guardrails

- Treat official OSI/EA/Broadsword material as the only gameplay and chronology
  authority. Use repository code only to prove the available implementation gate.
- Distinguish an official fact from the forward-mapping custom project policy.
- Apply expansion gates cumulatively: the selected era and later true eras own
  the behavior unless official evidence defines an entitlement-only exception.
- Map Publish 81 to TOL and later (`Core.TOL`) under the forward policy.
- Keep Publish 90 at TOL because it is directly tied to Time of Legends.
- Keep Publish 99 and all later Publishes at TOL until a future true expansion is
  officially released and represented by a verified repository gate.
- Never recommend `Core.EJ` as an era gate. Do not replace a required per-account
  EJ entitlement check with the shard-wide expansion setting.
- Do not invent a Publish number for expansions that predate numbered cycles or
  whose official launch falls between archived Publish releases.

## Output Contract

Return:

- `Publish`: normalized number and worldwide release date, or `UNRESOLVED`;
- `Official evidence`: direct UO.com URLs and what each proves;
- `Mapped expansion`: named true expansion and whether the mapping is direct or
  forward-policy-derived;
- `Implementation gate`: inspected repository revision, enum/flag, and cumulative
  behavior, or `UNVERIFIED`;
- `Endless Journey`: `not applicable`, or the distinct account restriction and
  required entitlement seam;
- `Confidence`: percentage plus any evidence gap that could change the result.

For implementation requests, also name the affected files, add boundary tests
for the previous and selected eras, and keep entitlement tests separate. For
advice-only requests, make no edits.

## Verification

- Publish 81 resolves to TOL and `Core.TOL` by forward project policy.
- Publish 90 resolves directly to TOL and `Core.TOL`.
- Publish 99 resolves to TOL; EJ appears only as an account restriction.
- Post-TOL Publishes remain TOL until a verified true expansion boundary exists.
- Unknown or conflicting official evidence returns `UNRESOLVED`.
- Repository gates are never presented as official gameplay evidence.
