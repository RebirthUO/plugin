---
name: uo-official-evidence
description: >
  Establish current or historical official Ultima Online gameplay behavior from
  OSI, EA, and Broadsword production evidence. Use for UO facts, mechanics,
  formulas, items, systems, production parity, historically accurate behavior,
  or implementation questions in any user language, especially when the user
  says OSI, EA, Broadsword, official servers, production, or production-like.
  Do not use for purely creative UO writing or Publish-to-expansion mapping.
---

# UO Official Evidence

## Portfolio Coordination

For cross-cutting work, consult [the portfolio routing guide](../PORTFOLIO-ROUTING.md). Load only a named available neighbor, preserve this skill's boundary, and hand off a compact packet with scope, evidence, constraints, and next owner when the guide routes work elsewhere.

## Interpret the Target

- Treat `OSI`, `EA`, `Broadsword`, `official servers`, and `production` as the
  live official Ultima Online service unless the user names a historical date,
  Publish, expansion, or shard-specific exception.
- Define the mechanic, target era, production context, and requested artifact
  before comparing sources or code. Ask only when an ambiguity can change the
  conclusion.
- Research and respond in the user's language. Keep evidence labels and result
  states stable across languages.

## Research Workflow

1. Search the newest relevant UO.com wiki, Publish notes, archives, and other
   first-party OSI/EA/Broadsword material. Record each page's publication or
   update date when available and the date accessed.
2. Separate evidence into `current official`, `historical official`,
   `production third-party`, `freeshard`, `engine implementation`, and
   `repository implementation` classes. Never merge these classes.
3. Use third-party production sources to find leads, corroborate observations,
   and preserve history. Trace their claims back to first-party evidence when
   possible.
4. Use server engines to locate algorithms, lifecycle seams, tests, and possible
   implementation patterns. Bind every code claim to a repository and revision.
5. Resolve conflicts by scope and chronology. Newer applicable official evidence
   overrides older official behavior for a current-production question. Official
   evidence overrides third-party, freeshard, engine, client, and repository
   behavior for gameplay claims.
6. Return `UNRESOLVED` for every material formula, value, lifecycle rule, or
   historical claim that official evidence does not establish. Do not infer it
   from agreement among non-official sources.
7. For implementation work, use engines as a technical starting point while
   targeting production-near and historically correct behavior. Preserve every
   unresolved official gap as an explicit policy decision or blocker.

## Source Register

| Source | Evidence class | Permitted use |
| --- | --- | --- |
| [Ultima Online Wiki](https://uo.com/wiki/ultima-online-wiki/) | Official Broadsword/EA | Primary gameplay authority; also inspect linked official Publish notes and archives. |
| [UOGuide Directory](https://www.uoguide.com/UOGuide:Directory) | Production third-party wiki | Leads, historical context, and production observations; verify against official evidence. |
| [Ultima Forums Codex](https://ultimaforums.com/codex/Main_Page) | Production third-party wiki | Leads, historical context, and production observations. |
| [UO-CAH](https://www.uo-cah.com/) | Production third-party wiki | Production-oriented guides, measurements, and calculators; label methodology and date. |
| [Stratics Community](https://community.stratics.com/) | Production third-party forum | Dated player reports, developer-discussion leads, and historical observations. |
| [UO Tavern Wiki](https://www.uotavern.com/wiki/) | Production third-party wiki | Leads, historical context, and production observations. |
| [UOAlive Wiki](https://uoalive.com/wiki/UOA) | Freeshard wiki | Discovery only; it may reproduce UOGuide information, so trace provenance and do not count it as independent corroboration. |
| [ServUO](https://github.com/ServUO/ServUO) | Server engine | EA-parity implementation lead and technical comparison, never gameplay authority. |
| [TrueUO](https://github.com/TrueUO/TrueUO) | Server engine | EA-parity implementation lead and technical comparison, never gameplay authority. |
| [ModernUO-Edge](https://github.com/modernuo/ModernUO-Edge) | Server engine | ModernUO era-content implementation lead and technical comparison, never gameplay authority. |

The register permits these sources; it does not make every source mandatory.
Prefer the smallest set that establishes the claim and exposes meaningful
conflicts. Search additional first-party OSI/EA/Broadsword material whenever it
is more direct or current.

## Output Contract

Return:

- `Target`: mechanic, current or historical era, and production meaning;
- `Conclusion`: established behavior or `UNRESOLVED`;
- `Evidence`: source class, URL or repository revision, date, and the exact claim
  each source supports;
- `Reconciliation`: current versus historical behavior and every conflict;
- `Implementation guidance`: production target, usable engine patterns, and
  separately labeled custom policy, or `not requested`;
- `Confidence`: percentage justified by coverage, freshness, and directness;
- `Open questions`: only gaps that could change the conclusion or implementation.

Do not cite search-result pages, hide source-class transitions, present engine
behavior as OSI fact, or claim production parity while a material official rule
remains unresolved.

## Verification

- A current official source conflicting with a community page controls the
  current-production conclusion; record the community conflict.
- An engine-only numeric formula remains `UNRESOLVED` as official behavior.
- A historical official rule remains historical when newer official evidence
  establishes a changed current rule.
- Agreement among third-party sources without official evidence remains
  corroborated production reporting, not an official fact.
- Route Publish chronology or expansion-gate selection to
  `uo-publish-expansion-mapping`; retain this skill for the gameplay claim.
