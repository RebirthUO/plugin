# Swarm Publish 96 weapon-property implementation notes

Use this reference when implementing or reviewing UO.com `Swarm` magic-item-property tickets in RebirthUO/ModernUO.

## Source and era stance

- UO.com Magic Item Properties lists `Swarm` as `Weapons (L)`, no imbue weight, chance to activate an insect swarm that causes physical damage over time until the target takes fire damage or equips a torch, and does not activate from special moves.
- UO.com Publish 96 / Doom Update places Swarm with other new Doom weapon properties such as Sparks and Bone Breaker.
- RebirthUO has expansion gates but no fine-grained Publish-96 gate; use `Core.TOL` as the practical post-ToL/Publish-96 gate unless maintainers add a dedicated publish/custom-policy flag.
- Do not put Swarm in `SaWeaponAttributes`: it is post-ToL Doom content, not SA launch content.

## Recommended implementation shape

- Store Swarm in the existing post-ToL `ExtendedWeaponAttribute` / `ExtendedWeaponAttributes` weapon-only container.
- Tooltip: add cliloc `1157325` (`Swarm ~1_val~%`) only when `Core.TOL` and `HitSwarm > 0`.
- Trigger path: call from `BaseWeapon.OnHit` after successful normal damage, using the property value as a percentage chance.
- Exclusions: if `WeaponAbility` or `SpecialMove` is active, do not trigger Swarm.
- Runtime context: keep Swarm contexts transient/static; do not serialize timers or active DoT state.
- Damage: apply physical damage through `AOS.Damage(defender, attacker, damage, 100, 0, 0, 0, 0)` so physical resistance and combat pipeline behavior apply.
- Fire removal: remove active Swarm only when the post-resist fire component is positive; fully resisted fire should not clear it.
- Torch counterplay: a burning equipped `Torch` should remove/neutralize active Swarm and prevent tick damage. Hook both the tick path and torch equip/ignite path so player counterplay works immediately.
- Distribution remains a separate economy decision: do not add Swarm to loot, runic, reforging, imbuing, artifact drops, or Doom rewards unless a ticket explicitly scopes that rollout.

## Focused tests to add

- `GetValue` sums `HitSwarm` only in TOL/later.
- `GetProperties` adds cliloc `1157325` only in TOL/later.
- Normal TOL hit with `HitSwarm = 100` starts an active Swarm context.
- HS/pre-TOL does not start Swarm or show tooltip.
- Weapon Abilities and Special Moves do not start Swarm.
- `ApplySwarmTick` uses physical `AOS.Damage` and respects physical resistance.
- Positive post-resist fire damage removes Swarm; fully resisted fire does not.
- Burning equipped torch removes active Swarm and causes subsequent Swarm tick to return no damage.
- Distribution guard: `git grep -n 'HitSwarm' -- Projects/UOContent ':!Projects/UOContent/Misc/AOS.cs' ':!Projects/UOContent/Items/Weapons/BaseWeapon.cs'` should find no loot/runic/reforging/imbuing/artifact surfaces.

## Validation pattern

For PR readiness, run:

```bash
git diff --check HEAD~1..HEAD -- \
  Projects/UOContent.Tests/Tests/Items/Weapons/ExtendedWeaponAttributesTests.cs \
  Projects/UOContent/Items/Lights/Torch.cs \
  Projects/UOContent/Items/Weapons/BaseWeapon.cs \
  Projects/UOContent/Misc/AOS.cs

MSBUILDDISABLENODEREUSE=1 dotnet build ModernUO.slnx --nologo --verbosity quiet -m:1

MODERNUO_TEST_DATA_DIR='<client-data-folder>' dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --filter "FullyQualifiedName~ExtendedWeaponAttributesTests" \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"

MODERNUO_TEST_DATA_DIR='<client-data-folder>' dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj \
  --no-build --no-restore --nologo --verbosity quiet \
  --logger "console;verbosity=minimal"
```

If the Hermes post-edit guard asks for fresh evidence after commit/push, create a temporary `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*.sh` script that prints repo/branch/local head/remote head/status, runs the committed changed-path `git diff --check`, the distribution guard, build, focused tests, and the broad relevant UOContent test project, then removes the script. Report it as ad-hoc/focused guard verification, not as CI green.
