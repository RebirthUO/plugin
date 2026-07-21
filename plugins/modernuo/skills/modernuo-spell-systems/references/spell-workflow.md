# Spell Workflow

Read this reference when a change crosses cast validation, target selection, or
effect lifetime. Confirm current APIs and ordering in the consuming checkout.

| Phase | Establish before editing |
|---|---|
| Start | Caster validity, registration, and activation gate |
| Commit | Cost timing and interruption semantics |
| Target | Selection validation and resolution-time revalidation |
| Resolve | Effects, immunity, range, and feedback ownership |
| End | Expiry, reversal, deletion, and durable restoration |

Keep a separate row for each retained effect or summoned entity. The row should
name its owner, cancellation path, teardown hook, and post-load behavior.
