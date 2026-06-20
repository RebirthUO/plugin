# Endless Journey / No-Housing ML Analysis Notes

Use when analyzing whether Ultima Online Mondain's Legacy content remains playable under Endless Journey or no-housing account rules, and when proposing shard-specific custom mitigations.

## Core conclusion

Endless Journey / no-housing can cover nearly all player-facing Mondain's Legacy gameplay content because ML progression is mostly quest-, dungeon-, skill-, boss-, loot-, recipe-, and resource-based rather than house-based. The major losses are infrastructure and persistence convenience, not ML story or boss access.

Clean summary wording:

> EJ can play nearly all of ML. EJ cannot hoard ML like a Veteran / Housing account.

## Content generally still reachable

- ML quest chains: Heartwood, Sanctuary, Bedlam, Blighted Grove, Citadel, New Haven, Heritage, courier chains.
- Spellweaving unlock and Spellweaving Book acquisition.
- Spellweaving scroll farming / purchasing.
- ML dungeon routes and points of interest.
- Peerless key loops and Peerless bosses.
- ML Peerless artifacts and minor artifacts.
- ML crafting, recipes, resources, runic tools, and BOD-adjacent goals.
- Normal character power progression when the account model keeps the standard skill cap.

## Infrastructure that falls away

- Own housing.
- Locked-down house storage.
- Secure-container house storage.
- Mailbox-based asynchronous transfer.
- Own Auction Safe placement / operation.
- Broad bank storage.

Important nuance: Auction Safes may still be interactable as a buyer/bidder depending on shard policy, but EJ/no-housing should not be described as having its own auction-safe sales/storage channel.

## Bank limit implication

Official UO Endless Journey bank storage is a small fixed item cap: 20 items by default, up to 28 with storage expansions. This turns inventory discipline into the main practical constraint.

Recommended player rule: only store long-term items that are active progression, rare/unlearned, high-value, or one-time. Everything else should be consumed, sold, traded, transferred to an allowed mule, or discarded.

Likely long-term keepers:

- Active Peerless keys.
- Active quest items.
- Rare unlearned recipe scrolls.
- Runic tools / high-value crafting tools.
- ML Peerless artifacts.
- ML set pieces still needed for a target set.
- High-value PowerScrolls / StatScrolls.
- Irreplaceable event or one-time rewards.

## Mule-management framing

If shard rules allow mules, describe mule management as disciplined logistics, not as a loophole. Suggested roles:

- Main: current combat gear, active quest items, current keys.
- Crafter mule: recipe learning, runic tools, crafting identity.
- Resource mule: only rare ML resources, not bulk common hoards.
- Scroll / recipe mule: Spellweaving scrolls, recipes, power/stat scrolls.
- Gear mule: replacement sets, resist sets, slayer/luck/utility gear.
- Sell mule: near-term trade/sale inventory.

Do not recommend IP/VPN workarounds for account restrictions. If multiaccounting is allowed, say so openly; if not, solve the design problem mechanically.

## Arcane Circle special case

Spellweaving itself is solo-reachable, but Arcane Circle / Arcane Focus is the one ML mechanic that can break a pure solo interpretation.

Source-backed claims to cite inline when writing docs:

- UO.com Spellweaving: Arcane Circle creates an Arcane Focus for caster and participating arcanists; focus improves duration, damage, healing effectiveness, and area of effect; West Britain Bank / Prism of Light can add +1 focus; participants must be within 20 Spellweaving skill points.
- UOGuide Arcane Circle: caster and up to four other arcanists; Prism of Light bonus; max focus 6.
- Stratics Arcane Circle: a lone spellweaver cannot create a focus; focus is calculated from spellweavers in the circle with special-circle modifiers.

Recommended wording:

> Spellweaving can be unlocked and used solo, but full Arcane Focus is group-shaped. Mark Arcane Circle as available but group-required unless the shard intentionally adds a custom assist mechanic.

## Custom-solution menu

Good custom solutions should reduce ML-completion friction without turning EJ/no-housing into free Veteran storage.

Preferred options:

1. Public Arcane Circles in Heartwood, Sanctuary, and optionally WBB/Luna/Prism.
2. Lesser Arcane Focus, capped at Focus 1 or 2, unlocked by quest or public assist.
3. Arcanist NPC assist with cost/cooldown and low cap; real players remain required for Focus 5/6.
4. Peerless Key Binder: one item per Peerless loop that absorbs only matching keys and becomes altar-usable when complete.
5. Whitelisted EJ Quest Vault: stores only ML progression items, not gear, artifacts, gold, resources, or generic loot.
6. Completion Satchel: stores flags/statistics, not items, for completion proof without storage bypass.
7. Public trade board with text listings only, no escrow, to replace mailbox/auction-safe convenience without creating storage.

Avoid:

- Generic extra storage.
- Removing Arcane Circle group value entirely.
- IP/VPN/multibox workarounds as the recommended path.
- Letting custom helpers hold wealth, gearsets, resources, or artifacts.

## Markdown deliverable pattern

When the analysis grows beyond a short answer, write a standalone Markdown document under `docs/` and cite it in the final response. This user specifically found the full analysis easier to read in Markdown than in chat. Prefer a reader-friendly document with sections, decision tables, player-facing wording, developer-facing wording, and open design questions.

For player-facing German completion guides, do not leave the full guide only in chat. Create the Markdown artifact, then verify it with real file/source coverage checks before finalizing. A good pattern is:

1. Read the era profile, content matrix, crafting matrix, quest config, Peerless artifact mapping, and ML monster/item source folders.
2. Generate checklist sections from authoritative repo data rather than hand-copying long lists:
   - parse `Distribution/Data/MLQuests.cfg` by `#` headers for all quest groups;
   - parse `Projects/UOContent/Misc/MLPeerlessArtifacts.cs` for source-to-artifact mappings;
   - walk `Projects/UOContent/Mobiles/Monsters/ML/**/*.cs` for all ML creature classes;
   - walk ML weapon/minor-artifact folders for item checklists.
3. Preserve player-readable wording in German while keeping technical IDs in backticks so the entries remain searchable in source/tests.
4. Include a Pre-ML baseline section for inherited weapon/armor families when the user asks for “ML + Pre-ML” or “100% completion”; explain that EJ completion should track families/sources, not physical hoarding of every generated item.
5. Add an explicit EJ restriction section with `verfügbar` / `eingeschränkt` / `nicht möglich` labels for housing, locked-down/secures, mailbox, auction safes, bank limit, mule discipline, and Arcane Circle.
6. Add a custom-solution section that separates fair ML-completion helpers from free Veteran storage: Peerless Key Binder, whitelisted EJ Quest Vault, low-cap Public Arcane Circle Assist, Completion Ledger, and non-escrow Trade Board.
7. Verify coverage with a script: every non-comment quest row in `MLQuests.cfg`, every ML monster file stem (trim accidental filename whitespace), and every `MLPeerlessArtifacts.Entry(...)` artifact type should appear in the Markdown.
8. In the final response, give only the path, verification counts, and git status; do not paste the whole guide back into chat.

Suggested headings:

1. Kurzfazit / Executive summary.
2. Scope and assumptions.
3. Why near-100% ML content remains realistic.
4. What falls away.
5. Bank-limit / mule-management implications.
6. Arcane Circle special case.
7. Custom-solution menu.
8. Recommended combined solution.
9. Decision matrix.
10. Player communication.
11. Developer communication.
12. Open design questions.
13. Final position.
