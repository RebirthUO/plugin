# Local cliloc verification

Use the installed client data as the final check for item-property localization IDs; emulator precedent alone is not sufficient.

## ModernUO-based repository workflow

1. Confirm the client file exists, for example:
   ```bash
   test -f '<uo-client-dir>/cliloc.enu'
   ```
2. Modern client `cliloc.enu` files may be BWT-compressed. Do not parse the first bytes as an uncompressed cliloc header unless the file begins with the normal header. ModernUO already contains `Server.Client.BwtDecompress` in `Projects/Server/Client/BwtDecompress.cs`.
3. Build `Projects/Server/Server.csproj` or the solution, then use a temporary diagnostic program referencing the built `Server.dll` to set the stream position to 4 and call `BwtDecompress.Decompress(stream, (int)stream.Length - 4)`.
4. Parse the decompressed records as: `int number`, `byte flag`, `ushort UTF-8 byte length`, followed by the UTF-8 text. Confirm both the candidate ID and displayed text.

Record the resolved client-data path, file/version, cliloc ID, and exact text in
the research handoff. Still test the property-list ID, arguments, and era gate;
do not carry a cliloc value from an earlier ticket into a new implementation.

## Test bootstrap pitfall

When running UOContent tests with `--no-build`, build `ModernUO.slnx` first rather than only invoking the test project. A direct test-project build can omit copied `Distribution/Data` files because `SolutionDir` is not populated, causing fixture initialization failures such as a null `SkillInfo.Table`; this is a bootstrap/output issue, not an implementation failure.
