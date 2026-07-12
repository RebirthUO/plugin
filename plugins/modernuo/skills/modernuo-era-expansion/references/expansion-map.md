# Expansion Map

Verify this map against the repository's current `Expansion` enum and configuration before editing; custom branches may extend it.

| Order | Expansion | Convenience gate | Common aliases / major surface |
|---:|---|---|---|
| 0 | `None` | pre-`Core.T2A` | Original, pre-T2A |
| 1 | `T2A` | `Core.T2A` | The Second Age |
| 2 | `UOR` | `Core.UOR` | Renaissance |
| 3 | `UOTD` | `Core.UOTD` | Third Dawn |
| 4 | `LBR` | `Core.LBR` | Lord Blackthorn's Revenge |
| 5 | `AOS` | `Core.AOS` | Age of Shadows; combat/item-property overhaul |
| 6 | `SE` | `Core.SE` | Samurai Empire; Tokuno, Bushido, Ninjitsu |
| 7 | `ML` | `Core.ML` | Mondain's Legacy; Spellweaving, peerless |
| 8 | `SA` | `Core.SA` | Stygian Abyss; gargoyles, Mysticism, Imbuing, Throwing |
| 9 | `HS` | `Core.HS` | High Seas |
| 10 | `TOL` | `Core.TOL` | Time of Legends; skill masteries |
| 11 | `EJ` | `Core.EJ` | Endless Journey |

Convenience gates are normally ordinal/cumulative. Use exact equality only when
later eras must not inherit the behavior. Configured-project profiles may
enable, block, or tune content independently of the enum, so inspect the actual
active expansion and profile configuration.

Minimum test matrix for a cumulative target `X`:

- immediately before `X`: behavior absent/legacy;
- `X`: behavior active with target values;
- a later era: deliberate inheritance or explicit override;
- each named custom profile: activation and overrides.
