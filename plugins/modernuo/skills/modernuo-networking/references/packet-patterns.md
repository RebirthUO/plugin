# Packet and Message Patterns

Read this reference after the packet contract is known. Match current neighboring
code over these illustrative shapes.

## Fixed outgoing packet

```csharp
public static class OutgoingMyPackets
{
    public const int PacketLength = 12;

    public static void SendMyPacket(this NetState ns, Serial target, int value)
    {
        if (ns.CannotSendPackets())
        {
            return;
        }

        var buffer = stackalloc byte[PacketLength].InitializePacket();
        CreateMyPacket(buffer, target, value);
        ns.Send(buffer);
    }

    public static void CreateMyPacket(Span<byte> buffer, Serial target, int value)
    {
        var writer = new SpanWriter(buffer);
        writer.Write((byte)0xBF);
        writer.Write((ushort)PacketLength);
        writer.Write((ushort)0x99);
        writer.Write(target);
        writer.Write((short)value);
    }
}
```

Use the current repository's initialized-buffer guard if the neighboring
`Create*` functions require one. Keep encoder functions deterministic so byte
layout can be tested without a live connection.

## Variable outgoing packet

```csharp
var writer = new SpanWriter(stackalloc byte[64]);
writer.Write((byte)0x99);
writer.Write((ushort)0); // length placeholder
writer.WriteBigUniNull(name);
writer.WritePacketLength();
ns.Send(writer.Span);
```

Use a resizable/pooled writer when the maximum cannot fit safely in bounded stack
storage. Dispose writers that rent buffers.

## Incoming handler

```csharp
public static unsafe void Configure()
{
    IncomingPackets.Register(0x99, 12, true, &HandleMyPacket);
}

public static void HandleMyPacket(NetState state, SpanReader reader)
{
    var from = state.Mobile;
    if (from == null || reader.Remaining < 6)
    {
        return;
    }

    var serial = (Serial)reader.ReadUInt32();
    var value = reader.ReadInt16();
    var target = World.FindMobile(serial);

    if (target?.Deleted != false || !CanUse(from, target, value))
    {
        return;
    }

    Apply(from, target, value);
}
```

Use length `0` only for protocol-defined variable packets. Encoded subpackets use
the existing `RegisterEncoded`/`EncodedReader` pattern. Validation must cover
authorization and game state, not just sufficient bytes.

## Writer/reader selection

- Numeric `Write`/`Read*` methods are big-endian by default.
- Use `WriteLE`/`Read*LE` only where the protocol specifies little-endian.
- Match ASCII, Latin-1, UTF-8, big-endian Unicode, little-endian Unicode, fixed
  length, and null termination exactly.
- Use safe string readers where control-character filtering is expected.
- Check `Remaining` before optional/variable fields and reject impossible counts
  before allocating or looping.

## Player-facing messages

Prefer existing `Mobile`/`Item` helpers for system text, speech, localized text,
and overhead messages. They already encode visibility/range rules and expose
handler-aware overloads:

```csharp
mobile.SendMessage($"You have {gold:N0} gold");
mobile.SendLocalizedMessage(cliloc, $"{current}\t{maximum}");
item.SendMessageTo(player, $"Hello, {player.Name}");
```

Keep the interpolation directly at the call site. Load
`modernuo-string-handling` for branches and allocation traps. For property lists,
load `modernuo-property-lists`; its literal/delimiter behavior is different.

## Current source anchors

- `Projects/Server/Network/Packets/OutgoingMobilePackets.cs`
- `Projects/Server/Network/Packets/OutgoingItemPackets.cs`
- `Projects/UOContent/Network/Packets/IncomingPlayerPackets.cs`
- `Projects/Server/Buffers/SpanWriter.cs`
- `Projects/Server/Buffers/SpanReader.cs`

Re-check names and signatures in the current branch before copying a pattern.
