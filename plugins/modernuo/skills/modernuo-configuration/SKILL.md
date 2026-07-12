---
name: modernuo-configuration
description: Use when adding or changing ModernUO server settings, modernuo.json keys, custom JsonConfig files, configuration defaults, or startup reads. Covers key ownership, persistence, validation, compatibility, and tests. Do not use for era behavior unless configuration is the actual control surface.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    skill_group: modernuo
    skill_subgroup: domain
    workflow_phase: none
    workflow_tier: support
    tags: [modernuo, configuration, json-config, settings, startup]
    related_skills:
      - modernuo-server-lifecycle
      - modernuo-events
      - modernuo-era-expansion
      - modernuo-code-audit
      - modernuo-test-workflow
---

# ModernUO Configuration

## Boundary

Own durable operator-facing settings and custom configuration files. Do not introduce a setting when a constant is genuinely invariant, and do not use a config key to hide an unresolved era-policy decision.

## Workflow

1. Define the owner, key, type, default, valid range, read phase, mutation behavior, compatibility, and operator-facing failure mode.
2. Inspect `ServerConfiguration`, `JsonConfig`, the active configuration files, and nearby keys before choosing an API or path.
3. Use `GetOrUpdateSetting` only when writing a missing default is intended; use `GetSetting` for non-mutating reads. Read startup settings in the locally appropriate `Configure` phase.
4. Use dot-separated stable keys. For structured collections/objects, use a dedicated `JsonConfig` file rather than stringifying data into `modernuo.json`.
5. Validate ranges and incompatible combinations before applying values. Log the actionable key/path without leaking secrets.
6. Preserve renamed/removed keys through a documented compatibility or migration decision; avoid silently resetting operator choices.
7. Test missing, valid, boundary, malformed, legacy, and read-only-file cases plus restart persistence where writes are supported.

## Safety gates

- Never store secrets or tokens in examples, logs, or committed defaults.
- Do not write configuration from arbitrary entity constructors or hot paths.
- Do not assume all values are native JSON types; inspect current serialization behavior.
- Keep generated/runtime output out of source control unless the repository intentionally tracks it.
- A bad optional setting should fail safely with a clear fallback or startup error, not partially initialize a system.

## Verification/self-check

Exercise missing/valid/boundary/malformed/legacy/read-only cases and restart behavior. Re-read keys, defaults, paths, logs, and migration notes for accidental writes or exposed secrets.

## Output contract

Return keys/files and defaults, read/write ownership, validation and compatibility policy, changed paths, verification results, and operator migration notes.

## Reference routing

- Read [configuration-patterns.md](references/configuration-patterns.md) for API selection and structured-config shape.
- Read [modernuo-server-lifecycle](../modernuo-server-lifecycle/SKILL.md) when the correct startup phase is unclear.
- Read [modernuo-era-expansion](../modernuo-era-expansion/SKILL.md) only when a setting interacts with expansion/profile behavior.
