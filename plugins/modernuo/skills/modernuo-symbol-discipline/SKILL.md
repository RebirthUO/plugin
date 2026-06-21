---
name: modernuo-symbol-discipline
description: >
  Use when writing, reviewing, or refactoring ModernUO/RebirthUO C# code involving constants, local variables, fields, properties, public gameplay or parity surfaces, exposed in-game values, or Policy* names such as PolicySe*. Helps decide whether to inline a value, keep a local, create const or static readonly, add a field or property, or expose a RebirthUO policy symbol. Warn only and ask before changing code.
---

# ModernUO Symbol Discipline

Use this skill to keep generated code from inventing symbols that do not carry their own weight. The goal is not to ban constants, locals, fields, properties, or `Policy*` names; it is to make every introduced symbol justify its lifetime, scope, and visibility.

## Operating Rule

Report symbol-discipline issues as warnings. Do not silently rewrite code. Ask before changing existing code unless the user explicitly requested cleanup.

Use this report shape:

```text
[SYMBOL] WARNING: {why this symbol is unnecessary or overexposed}
  File: {path}:{line}
  Suggestion: {inline, reduce scope, rename, or keep with justification}
```

## Decision Ladder

1. **Inline one-off values** - Keep obvious literals or expressions inline when they are used once and do not name gameplay policy, client-visible behavior, or a non-obvious formula term.
2. **Use locals for real local work** - Keep a local when it is reused, snapshots mutable game state, avoids repeated expensive or side-effectful calls, clarifies a branch/formula, or gives a meaningful name to a non-obvious intermediate result.
3. **Use `const` for reusable compile-time values** - Add a `const` only when the value is reused, asserted by tests/docs, intentionally exposed as gameplay/parity surface, or names a non-obvious source-backed or policy-backed rule. Prefer the narrowest useful access level.
4. **Use `static readonly` for shared runtime objects** - Use it for `TimeSpan`, arrays, dictionaries, `SpellInfo`, `MonsterAbility[]`, cached `SearchValues`, loggers, or other shared values that cannot be `const` or must preserve identity.
5. **Use fields for state** - Add a field only for real object/system state: persistence, timers, lifecycle cleanup, cross-method state, caches, entity references, or data that changes over time.
6. **Use properties for public or engine surfaces** - Add or override properties for engine contracts, serialization/config/commands, gumps/tooltips, client-visible behavior, in-game exposed values, or stable external consumers. Do not add wrapper properties that only rename a one-off literal or forward to another symbol.
7. **Use `Policy*` only for explicit RebirthUO policy** - A `Policy*` symbol means "source-incomplete or intentionally chosen RebirthUO behavior." Require a clear reason: source pages lack exact values, the value is reused by helpers/tests/docs, the policy is important to parity review, or downstream code needs a stable name.

## Policy Name Checks

Flag a new `Policy*`, `PolicySe*`, `PolicyML*`, or similar symbol when it only exists because the code is in an era branch. Era gating alone is not policy.

Allow `Policy*` when all relevant checks hold:

- The value represents a deliberate RebirthUO decision, not just a convenience alias.
- The name describes the gameplay decision, not only the era.
- The value is reused, tested, documented, or intentionally exposed for parity review.
- A public `const` is actually needed; otherwise keep it private/internal or inline it.

Good policy surface:

```csharp
public const double PolicySeLowSkillHitChanceBase = 30.0;
public const double PolicySeLowSkillHitChancePerPoint = 2.2;

public static double GetSamuraiEmpireHitChance(double ninjitsu) =>
    PolicySeLowSkillHitChanceBase + (ninjitsu - 85.0) * PolicySeLowSkillHitChancePerPoint;
```

This is acceptable when the SE formula is source-incomplete, the values are part of a named helper, and tests or parity docs assert the behavior.

Bad policy surface:

```csharp
public const int PolicySeTreasureMapLevel = 5;
public override int TreasureMapLevel => PolicySeTreasureMapLevel;
```

If no source gap, reuse, test assertion, or review surface needs the symbol, prefer:

```csharp
public override int TreasureMapLevel => 5;
```

## Local And Field Examples

Inline a local that only re-labels a literal:

```csharp
var bodyId = 0x1234;
Body = bodyId;
```

Prefer:

```csharp
Body = 0x1234;
```

Keep locals that snapshot or clarify behavior:

```csharp
var ninjitsu = attacker.Skills.Ninjitsu.Value;
var movedEnough = steps >= 5;
var divisor = movedEnough ? PolicySeMovingDamageDivisor : PolicySeStandingDamageDivisor;
```

Keep fields that hold real state:

```csharp
private static readonly Dictionary<Mobile, DeathStrikeTimer> _table = new();
private TimerExecutionToken _timerToken;
private readonly Mobile _target;
```

Flag fields that only support unnecessary wrapper properties:

```csharp
private readonly int _baseMana = 30;
public override int BaseMana => _baseMana;
```

Prefer:

```csharp
public override int BaseMana => 30;
```

## Property Examples

Keep properties and overrides when they are the ModernUO contract or a client-visible surface:

```csharp
public override string DefaultName => "a yomotsu warrior";
public override int BaseMana => 30;
public override double RequiredSkill => 85.0;
public override MonsterAbility[] GetMonsterAbilities() => _abilities;
```

Flag properties that only duplicate another symbol or hide a one-off literal:

```csharp
public static int SeMovingDamageCap => PolicySeMovingDamageCap;
```

Prefer using the existing symbol directly, reducing its visibility, or inlining the value when no stable consumer exists.

## Final Check

Before accepting a new symbol, ask:

- Is it used more than once, exposed in-game, tested, documented, or required by an engine/API contract?
- Does the name make a non-obvious gameplay decision easier to audit?
- Is the access level no wider than the actual consumer set?
- Would inlining make the code simpler without losing parity, performance, or lifecycle clarity?
