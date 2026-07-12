# Review-Derived Guards for Era-Gated Item Mechanics

Use this reference when an implementation adds a named artifact with transient combat state.

## Era-gated persistent stats

A post-expansion artifact can leak into an earlier ruleset even when its special mechanic and tooltip are gated. Check both surfaces:

1. Item property-list output.
2. Runtime aggregation (`AosAttributes.GetValue`, resist/stat helpers, or equivalent).

For an item whose fields remain serialized for compatibility, keep the stored values but gate both display and aggregation at the owning item/attribute boundary. Add a test that equips the item, asserts the values in the target era, switches to the earlier era, and asserts both property absence and runtime value `0`. Do not treat raw serialized fields as proof that the mechanic is active.

## Immediate target lifecycle cleanup

A transient item effect keyed only by its current target must reset when the target dies or is deleted, not only when the caster next reaches the damage hook. Avoid scanning `World.Mobiles`/`World.Items` from an event handler. Keep a small active-owner index (for example, a `HashSet` of active effect items or a target-to-owner map), add the item when a valid sequence starts, and remove it from the index in every reset path: target change, unequip, disable, owner death/delete/logout, item delete, invalid target, and sequence completion.

The target death/deletion event can then collect matching active items into `PooledRefList<T>` before resetting them, avoiding mutation during iteration and avoiding a full-world scan. Test the event-facing cleanup helper with an active sequence, invoke cleanup for the target, then verify the next same-target damage starts at the initial penalty. Also retain invalid-target coverage.

## Verification after a pushed follow-up

When the branch is already committed and pushed, run an ad-hoc script created with Python `tempfile.mkstemp(prefix="hermes-verify-", suffix=".sh", dir="C:/Users/<user>/AppData/Local/Temp")`. Convert the native path with `cygpath -u` before invoking Bash; on this Windows/MSYS host the Windows temp directory maps to `/tmp`, not necessarily `/c/...`. Use an exit-safe cleanup trap. Print local/remote heads and PR state, run committed diff checks and the distribution guard, then build, run the focused test, and run the broad owning project. Report this as ad-hoc verification, never CI or full-suite green.