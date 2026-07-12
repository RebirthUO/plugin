# Client Cliloc and schema verification for item-property implementations

Use this when an issue requires a concrete client label / cliloc assertion, generated persistence schema, or both.

## Client-label verification

1. Do **not** parse `Cliloc.enu` with a simple record reader first. Classic client files may be BWT-compressed.
2. Verify through ModernUO's production path: `Server.Localization.LoadClilocs` / `Localization.GetText`. `Localization.cs` detects the header and calls `BwtDecompress` when needed.
3. Configure `MODERNUO_TEST_DATA_DIR` to the installed UO client directory before starting the test host.
4. Keep this probe local and temporary when CI does not carry copyrighted client data:
   - create a uniquely named `hermes-verify-*` temporary test/script using an OS-safe tempfile API;
   - assert the exact expected text returned by `Localization.GetText(cliloc)`;
   - run it, report its result as **ad-hoc client verification**, then remove it;
   - do not commit a test that makes CI depend on proprietary client files.
5. If the first expected text fails, treat the returned actual text as evidence and rerun with the exact label; do not claim client verification from a raw parser or an upstream comment.

## Generated migration discipline

1. Run `ModernUOSchemaGenerator` after adding a `[SerializationGenerator]` content type.
2. Stage only the schema belonging to the new/changed type.
3. The generator can discover unrelated missing schemas. Inspect status and remove unrelated generator output rather than broadening the issue/PR scope.
4. Re-run `git diff --check`, build, and focused tests after cleanup.

## PR reporting

Separate evidence classes:
- UO.com / official publish notes: canonical gameplay and era claims.
- Engine precedent: implementation details such as a cooldown, unless official evidence independently establishes it.
- Installed client: exact localized text only.

State temporary client probing as ad-hoc validation; do not call it broad suite coverage.
