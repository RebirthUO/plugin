# Changelog

## 3.4.0 - 2026-07-22

- Add `ultima-mcp` for bounded, read-only local Ultima Online Classic client
  data lookup through a configured active UltimaMCP server.
- Route ModernUO Gump client-data lookups through `ultima-mcp` while retaining
  Gump layout, response-safety, and visual-composition ownership.
- Keep UltimaMCP evidence explicitly separate from official UO gameplay
  evidence and preserve transparent unresolved-data fallback.
- Make live Issue Template selection conditional: new RebirthUO intake uses
  the governed fallback format when neither the request nor project
  instructions require a template.
- Permit only documented, existing, issue-relevant labels to be applied
  add-only during intake and research; preserve `blocked` as the sole
  readiness-state label.
- Add repository- and plugin-level README guides for host discovery, skill
  selection, governed delivery, UltimaMCP boundaries, and validation.

## 3.3.2 - 2026-07-22

- Allow RebirthUO issue intake and research to apply existing, live-verified,
  issue-relevant labels add-only with recorded rationale and read-back.
- Preserve template labels and repository label inventory through the issue
  workflow; retain `blocked` as the sole readiness-state label.
- Add focused behavior contracts for label selection, missing/ambiguous labels,
  add-only publication, and workflow handoff.
