# Generated Serialization and Migration Patterns

Read this reference after classifying the change as new generated serialization,
generated-version migration, legacy/manual migration, or custom persistence.

## Core attributes

| Attribute | Purpose |
|---|---|
| `[SerializationGenerator(version)]` | Generate entity serialization for a `partial` class |
| `[SerializableField(index)]` | Persist a private field and generate its property |
| `[SerializableProperty(index)]` | Persist a property with custom logic |
| `[InvalidateProperties]` | Refresh tooltip from a generated setter |
| `[SerializedCommandProperty(level)]` | Expose generated property to staff props |
| `[EncodedInt]` | Variable-length integer encoding |
| `[DeltaDateTime]` | Store time relative to save/load time |
| `[InternString]` | Intern repeated strings where appropriate |
| `[Tidy]` | Remove invalid/deleted collection entries after load |
| `[AfterDeserialization(false)]` | Defer hook until the full world is loaded |
| `[DeserializeTimerField(index)]` | Rebuild a supported serialized `Timer` from remaining delay |
| `[TypeAlias(...)]` | Preserve old serialized type names |

Inspect the current annotation/generator source for exact parameters and supported
types before relying on this summary.

## New type

```csharp
using ModernUO.Serialization;

[SerializationGenerator(0)]
public partial class ChargedItem : Item
{
    [SerializableField(0)]
    [InvalidateProperties]
    [SerializedCommandProperty(AccessLevel.GameMaster)]
    private int _charges;

    private TimerExecutionToken _token; // runtime-only

    [Constructible]
    public ChargedItem() : base(0x1234)
    {
        _charges = 10;
    }
}
```

Omit the encoded parameter for new generated types. Add `[Constructible]` only
when the entity should be created through the in-game add command.

## Generated version bump

When adding/removing/reordering fields on an already generated type:

1. Preserve existing field indexes and assign a new index for new data.
2. Increment `[SerializationGenerator(N)]`.
3. Generate the schema/migration artifact with the repository's current migrate
   or publish command and commit it.
4. Add the expected `MigrateFrom(VNContent content)` transition for the previous
   version and copy every retained value explicitly.
5. Test an old-version fixture plus default/new round trip.

```csharp
private void MigrateFrom(V0Content content)
{
    _charges = content.Charges;
    _quality = GemQuality.Rough;
}
```

Do not edit the legacy `Deserialize(reader, version)` path for an ordinary
post-codegen version bump.

## Pre-codegen/manual migration

Preserve the original stream exactly:

- base call placement;
- version read type (`ReadInt` versus `ReadEncodedInt`);
- field read order and conditional branches;
- old type aliases and default values.

If the legacy stream used a plain integer version, use the generator's applicable
plain-version setting (historically the second parameter `false`). Confirm against
current generator docs and a real legacy implementation.

## Custom persistence purity

`GenericPersistence.Serialize()` and entity serialization can execute on
background world-save workers. Serialization is a read-only snapshot:

```csharp
public override void Serialize(IGenericWriter writer)
{
    writer.WriteEncodedInt(0);
    writer.WriteEncodedInt(_records.Count);

    foreach (var (key, value) in _records)
    {
        writer.Write(key);
        writer.Write(value);
    }
}
```

Never create/delete/move entities, start/stop timers, send packets, touch
`NetState`, or mutate shared collections there. Restore timers, registrations,
caches, and cross-entity links in an appropriate after-load hook.

## High-index save-flag trap

Before adding `[SerializableFieldSaveFlag(31)]` or another high index, inspect the
generated flag type and build immediately. Some generator versions can emit a
`uint` flag expression where `int` is expected. If the value can
default safely (for example a raw/defaultable attributes container), prefer no
save flag and make the migration schema's `usesSaveFlag` value match.

## Verification evidence

- Schema exists at the expected project migration path.
- Generator output compiles from a clean owning build.
- New instance defaults, current round trip, previous version, and legacy stream
  tests pass as applicable.
- Custom setters mark dirty and tooltip state invalidates where required.
- Runtime-only handles are absent from the persisted layout and restore once.
