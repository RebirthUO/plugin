# Item-Property Review Checklist

Research each named property from current official evidence and the configured
repository. Do not reuse ticket snapshots, remembered constants, issue-specific
defaults, or another engine's bit/container layout.

## Review record

```yaml
identity:
  property:
  official_era_or_publish:
  configured_repository:
  repository_revision:
official_contract:
  sources: []
  hosts: []
  formula_and_order:
  pvp_pvm:
  duration_cooldown_stacking:
  distribution:
implementation:
  storage:
  staff_api:
  serialization:
  tooltip_cliloc:
  aggregation:
  gameplay_consumer:
  cleanup:
  distribution:
tests:
  - default_and_dupe
  - round_trip_and_migration
  - era_suppression
  - tooltip
  - trigger_and_boundaries
  - cleanup
  - supported_and_unsupported_hosts
  - non_distribution
unresolved_questions: []
```

## Guardrails

- Re-locate current free bits, containers, and consumers; never copy a cached
  enum layout.
- Verify client strings separately from server mechanics.
- Keep rollability/acquisition separate from storage, display, and gameplay.
- A missing official formula, restriction, or lifecycle rule remains a research
  blocker and requires a focused user decision for custom policy.
