# Living-World Impact Map

Use this reference after `uo-official-evidence` establishes expected behavior.
It is a consequence checklist, not a source hierarchy or mechanics reference.

## Assumption frame

Record the exact official era/ruleset, facet/map, configured project profile,
and whether the requested result is parity or an explicit custom deviation.

## Player loops

Name affected and intentionally unaffected loops:

- progression, skills, stats, races, and new-player onboarding;
- PvM encounters, risk, rewards, and group roles;
- PvP risk, counterplay, escape, criminality, and consent boundaries;
- economy, crafting, vendors, faucets, sinks, trade, insurance, and storage;
- housing, lockdowns, vendors, decay/IDOC, ownership, and player trust;
- travel, maps, regions, ships, access, and spawn reachability;
- quests, events, guild/social systems, and recurring schedules;
- client presentation, localization, gumps, tooltips, art, and compatibility.

## Side-effect row

```yaml
change:
  era_or_ruleset:
  facet_or_map:
  parity_or_custom:
  affected_loops: []
  unaffected_loops: []
  beneficiaries: []
  stressed_or_losing_playstyles: []
  economy:
    faucets: []
    sinks: []
    trade_or_storage: []
    farming_or_bot_risk: []
  pvp:
    power_or_risk:
    counterplay:
  pvm:
    risk_or_reward:
    group_or_solo_effect:
  housing_and_trust:
  client_and_save_compatibility:
  exploit_or_security:
  rollback:
  validation:
```

## Guardrails

- A class, enum, or property is not live behavior; verify registration,
  configuration, data, map/spawn access, and consumers.
- Do not reduce Felucca/Trammel, housing, insurance, loot, or account rules to a
  single combat or safety dimension.
- Do not balance from anecdotes. Separate official behavior, reproducible local
  behavior, telemetry when available, and explicit policy.
- Prefer the smallest reversible action and state monitoring/rollback for
  live-impacting changes.
