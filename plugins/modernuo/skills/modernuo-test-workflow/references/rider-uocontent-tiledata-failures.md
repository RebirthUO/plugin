# Rider / UOContent.Tests: bulk failures from missing client tiledata

## Symptom

Rider (or CLI) runs `Projects/UOContent.Tests/UOContent.Tests.csproj` and reports a large cluster of failures, e.g. `328 failed, 164 passed, 492 total`.

The failures share the same root message:

```text
System.IO.FileNotFoundException : Data: tiledata.mul was not found
at Server.Core.FindDataFile(String path, Boolean throwNotFound) in Projects/Server/Main.cs
at Server.TileData.Load() in Projects/Server/TileData.cs
```

## Root cause

This is usually a test-host bootstrap/data-path problem, not hundreds of unrelated gameplay regressions.

`Projects/UOContent.Tests/Fixtures/TestServerInitializer.cs` force-loads `TileData` because pathfinding and movement tests need real UO client tile/map data. It gets the client path from:

1. `MODERNUO_TEST_DATA_DIR`, or
2. fallback `C:\Ultima Online Classic`.

If neither contains `tiledata.mul`, `Core.FindDataFile("tiledata.mul")` throws during fixture initialization. Any test in `Sequential UOContent Tests` / `Sequential Pathfinding Tests` that touches the shared fixture can then fail before its own assertions.

`Projects/UOContent.Tests/UOContent.Tests.csproj` also has a `ProjectReference` to `Projects/Server.Tests/Server.Tests.csproj`, so a UOContent test run may discover `Server.Tests.*` cases too. Do not interpret that as Rider randomly mixing suites until you have confirmed discovery with `dotnet test ... --list-tests`.

## Triage commands

```bash
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --list-tests --nologo --verbosity quiet

rm -rf TestResults/hermes-rider-triage && mkdir -p TestResults/hermes-rider-triage
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity minimal \
  --logger "trx;LogFileName=uocontent.trx" \
  --results-directory TestResults/hermes-rider-triage
```

Parse the TRX and cluster by message before debugging individual tests. If every failure says `Data: tiledata.mul was not found`, fix the client data path first.

## Fix / Rider setup

Set environment variables in the Rider run configuration to a real UO/ClassicUO client data directory:

```text
MODERNUO_TEST_DATA_DIR=C:\Path\To\Ultima Online Classic
MODERNUO_CLIENT_PATH=C:\Path\To\Ultima Online Classic
```

`MODERNUO_TEST_DATA_DIR` is used by `UOContent.Tests`; `MODERNUO_CLIENT_PATH` is used by `Server.Tests` tile-data fixture paths. The directory must contain `tiledata.mul`; pathfinding coverage also needs the relevant map/statics/multi client files.

## Reporting guidance

When this cluster appears, report it as a shared fixture/data-path blocker. Keep it separate from independent failures, such as culture-sensitive `ValueStringBuilder` expectations (`3.14` vs `3,14`) in `Server.Tests` on comma-decimal locales.
