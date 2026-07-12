# Bone Breaker ServUO Revision Drift

Use this note when drafting or reviewing Bone Breaker property issues.

## Evidence

- Canonical UO.com defines the public behavior: a 20% four-second stamina drain that blocks Refresh/Total Refresh potions, an independent mana-funded physical bonus at 30 or more current mana with 30 mana consumed after LMC scaling, no special-move activation, and a 60-second victim immunity.
- The pinned ServUO comparison commit `6fd01855840590e22cc73d94b5f7d9a97b1cf537` uses a +50 physical bonus, one-second ticks at roughly 10% of maximum stamina, and evaluates the mana-funded bonus before the immunity check. Therefore the independent mana bonus remains possible during the immunity window in that revision.
- Other/current ServUO revisions may reorder the immunity check or add a Tactics requirement. These are engine precedents, not canonical parity.

## Review rule

Always cite the exact comparison revision and inspect the relevant source lines. If revisions disagree, document the conflict as `Observed conflict`, `Likely interpretation`, and an explicit implementation policy; never write an unqualified “ServUO behavior” claim. UO.com is canonical for the player-facing rule, while ServUO revisions are lifecycle/constant precedent only.

For the Bone Breaker branch ambiguity, distinguish two independent questions: whether the mana branch can roll when the 20% drain roll fails, and whether a victim already inside the 60-second Bone Breaker immunity can receive that mana branch. The canonical “independent” wording resolves the first; it does not override the broad “immunity from Bone Breaker” wording. A conservative RebirthUO policy is therefore: independent branches on non-immune hits, broad immunity after the drain context ends, with no mana spent during immunity. Record this as shard policy because pinned ServUO revisions differ.

## RebirthUO anchors

- `Projects/UOContent/Misc/AOS.cs`: neutral `ExtendedWeaponAttributes` is the current weapon-property overflow container; verify the next free bit on the matching remote main rather than copying ServUO maps.
- `Projects/UOContent/Items/Weapons/BaseWeapon.cs`: normal-hit gating, additional physical `AOS.Damage`, and extended-property tooltip dispatch.
- `Projects/UOContent/Items/Skill Items/Magical/Potions/Refresh Potions/BaseRefreshPotion.cs`: narrow Refresh/Total Refresh `CanDrink` hook.
- `Projects/UOContent/Engines/BuffIcons/BuffIcon.cs`: Bone Breaker enum values may already exist without active presentation usage; treat that as repo evidence, not proof that buffs are required.

## Client cliloc verification

When a tooltip cliloc is only an engine candidate, verify it against the configured Classic client before making it an acceptance criterion. ModernUO's `Projects/Server/Localization/Localization.cs` first checks for the six-byte `(version=2, header=1)` format and otherwise BWT-decompresses the client file after its four-byte prefix using `Projects/Server/Client/BwtDecompress.cs`. Decode the local `Cliloc.enu` with that same format and report the exact strings for the OPL and any optional combat messages. A client-verified OPL does not automatically justify buff icons, overhead text, sounds, particles, or distribution changes.
