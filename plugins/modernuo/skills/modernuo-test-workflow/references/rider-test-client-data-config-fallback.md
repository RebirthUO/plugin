# Rider/xUnit UO client data config fallback

## Trigger

Use this when Rider or CLI `UOContent.Tests` shows a large burst of failures like:

```text
System.IO.FileNotFoundException : Data: tiledata.mul was not found
at Server.Core.FindDataFile(...)
at Server.TileData.Load()
```

This often appears after checking out a branch where the shared `UOContent.Tests` bootstrap force-loads `TileData` before most tests run.

## Root cause pattern

The app/server first-boot path stores the operator-selected UO client folder in:

```text
Distribution/Configuration/modernuo.json
```

But xUnit test hosts run with `Core.BaseDirectory` set to the test assembly output, for example:

```text
Projects/UOContent.Tests/bin/Debug/net10.0/win-x64/
Projects/Server.Tests/bin/Debug/net10.0/win-x64/
```

So the tests do not automatically read the app's `Distribution/Configuration/modernuo.json`. If the test fixture falls back only to `MODERNUO_TEST_DATA_DIR`, `MODERNUO_CLIENT_PATH`, or `C:\Ultima Online Classic`, Rider can fail even though the app itself starts correctly with a configured client path.

## Preferred repo fix

Add/reuse a test helper in `Projects/Server.Tests/Fixtures/` that resolves a client data directory in this order:

1. Environment variables (`MODERNUO_TEST_DATA_DIR` for `UOContent.Tests`, `MODERNUO_CLIENT_PATH` for `Server.Tests`; accept either for convenience).
2. Walk upward from `Core.BaseDirectory` and `Directory.GetCurrentDirectory()` looking for `Distribution/Configuration/modernuo.json`.
3. Deserialize `ServerSettings` with `JsonConfig.Deserialize<ServerSettings>()` and use the first configured `dataDirectories` entry containing `tiledata.mul`.
4. Fall back to `C:\Ultima Online Classic` only if it contains `tiledata.mul`.

Use the helper from both:

```text
Projects/UOContent.Tests/Fixtures/TestServerInitializer.cs
Projects/Server.Tests/Fixtures/TestServerInitializer.cs
```

For `UOContent.Tests`, fail fast with a clear `InvalidOperationException` if no path with `tiledata.mul` is found. For `Server.Tests`, keep tile-data-dependent tests skippable if the fixture intentionally supports partial operation without client data.

## Verification shape

After committing/pushing, if Hermes guard asks for fresh evidence, create a temporary script under `C:/Users/Jsiem/AppData/Local/Temp` with prefix `hermes-verify-`, unset both env vars, then run:

```bash
git diff --check HEAD~1..HEAD -- \
  Projects/Server.Tests/Fixtures/TestClientDataDirectory.cs \
  Projects/Server.Tests/Fixtures/TestServerInitializer.cs \
  Projects/UOContent.Tests/Fixtures/TestServerInitializer.cs
MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
dotnet test Projects/Server.Tests/Server.Tests.csproj --filter "FullyQualifiedName!~ValueStringBuilderTests" --no-build --no-restore --nologo --verbosity quiet --logger "console;verbosity=minimal"
```

Report this as **ad-hoc/focused verification** unless the full broad suite actually ran. If German/comma-decimal culture makes `ValueStringBuilderTests` fail, label that as a separate known culture-sensitive Server.Tests issue, not a client-data fallback failure.
