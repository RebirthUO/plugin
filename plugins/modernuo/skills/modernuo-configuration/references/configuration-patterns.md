# Configuration Patterns

Use after deciding that a value belongs in operator configuration. Verify exact overloads and paths locally.

## API choice

- `ServerConfiguration.GetOrUpdateSetting(key, default)`: read and persist a missing default.
- `ServerConfiguration.GetSetting(key, default)`: read without adding the key.
- `ServerConfiguration.SetSetting(key, value)`: explicit runtime mutation when the workflow owns that write.
- `JsonConfig.Deserialize<T>` / `Serialize`: structured custom files.

Use a stable namespace such as `mySystem.enabled` or `mySystem.cooldown`. Prefer a rename migration over leaving two live keys indefinitely.

## Structured configuration shape

```csharp
public sealed class MyConfig
{
    public bool Enabled { get; set; } = true;
    public int MaxItems { get; set; } = 100;
}

public static void Configure()
{
    _config = JsonConfig.Deserialize<MyConfig>(ConfigPath) ?? new MyConfig();
    Validate(_config);
}
```

Build paths from the repository's configured base/data directories; do not embed a developer-machine absolute path. Inspect existing converters before adding custom serialization for types such as `Map`, `Point3D`, `TimeSpan`, or enums.

## Verification matrix

- missing key/file selects the documented default;
- valid custom value survives restart;
- minimum/maximum and invalid enum values;
- malformed JSON and unknown fields;
- legacy key migration or explicit deprecation;
- read-only/missing directory behavior;
- secrets never appear in log output.
