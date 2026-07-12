# SA Item-Property Implementation Map

Use this reference only after `modernuo-issue-research` returns a current
`READY` contract for the named property. It contains implementation checks, not
property formulas or cached official facts.

## Procedure

1. Confirm official era/ruleset, host items, tooltip, formula/order, caps,
   timing, PvP/PvM, lifecycle, acceptance criteria, and non-goals.
2. Inspect current property containers, free values, staff wrappers,
   serialization, item families, consumers, client-data access, and tests.
3. Keep storage, tooltip, aggregation, gameplay, and distribution as separate
   approved surfaces.
4. Select an existing container only when family semantics and persistence
   match. Prefer mechanic/family ownership over an expansion-named overflow
   container and never copy historical enum values.
5. Gate tooltip and gameplay at the exact approved era/profile. Add a pre-era
   control proving stored state is inert and invisible.
6. Hook the live owning pipeline at the approved ordering point. For
   incoming-damage mechanics, trace normal, ignore-armor, typed, direct, PvP cap,
   barding/bonus, and keep-alive branches as applicable.
7. Keep points, targets, cooldowns, decay, immunity, and active effects
   transient unless the ready contract explicitly requires save persistence.
8. Test behavior through real owning seams, not static registration alone.

## Verification matrix

- safe current container value/key and staff API;
- default, duplicate, serialization/migration, and rollback;
- verified client tooltip ID/arguments/order and era suppression;
- supported and unsupported item hosts;
- trigger/order, raw versus applied values, caps, rounding, PvP/PvM;
- cooldown/stacking/decay and every cleanup boundary;
- applicable normal, typed, ignore-armor, direct, and mixed branches;
- distribution unchanged unless explicitly approved;
- owning build, final focused tests, and proportional adjacent/broad tests.

If a value or branch behavior is missing from the research contract, stop and
return it to `modernuo-issue-research`; do not import a default from a prior
ticket or emulator.
