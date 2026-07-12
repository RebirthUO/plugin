# Symbol Decision Examples

Read this reference after consumer/contract search when the correct symbol level
is still ambiguous.

Inline a local that only relabels a one-use literal:

```csharp
// Avoid
var bodyId = 0x1234;
Body = bodyId;

// Prefer
Body = 0x1234;
```

Keep locals that snapshot mutable state, avoid repeated/side-effectful calls, or
name a meaningful formula term:

```csharp
var ninjitsu = attacker.Skills.Ninjitsu.Value;
var movedEnough = steps >= 5;
var divisor = movedEnough ? MovingDamageDivisor : StandingDamageDivisor;
```

Fields hold real state such as dictionaries, ownership, timers, or persistence:

```csharp
private static readonly Dictionary<Mobile, DeathStrikeTimer> _table = new();
private TimerExecutionToken _timerToken;
private readonly Mobile _target;
```

Avoid a field/property pair that only hides a literal:

```csharp
// Avoid
private readonly int _baseMana = 30;
public override int BaseMana => _baseMana;

// Prefer
public override int BaseMana => 30;
```

A `Policy*` constant is earned only when it represents a deliberate configured
project decision under incomplete/conflicting evidence and is reused, tested, documented,
or intentionally exposed for parity review. An era branch alone does not make a
value policy. Prefer a mechanic name and narrow visibility.
