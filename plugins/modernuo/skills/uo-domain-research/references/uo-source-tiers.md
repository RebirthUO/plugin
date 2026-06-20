# UO Source Tiers and Research Index

A curated, dated index of the canonical UO sources used to triangulate UO skills. When authoring a new UO skill or auditing an existing one, this file is the default starting point. Always cite the page URL and the "last modified" date when you reference a source in a skill.

## Tier 1 - UOGuide (uoguide.com)

The most reliable community source for game-mechanics tables. Pages are individually dated in the body. Use for:

- Per-spell mana / reagent / skill / delay tables.
- Per-skill taxonomies, categories, primary/secondary stat tables.
- Item property tables (intensity range, type, found-on).
- Race ability tables.
- Stat cap mechanics and stat gain rules.
- Faction tables (pre-Publish 86).
- Per-expansion feature list with release dates.
- Per-facet rule summary.
- Per-class special-move matrix.
- Champion Spawn level scaling, reward tables, dynamic event list.

Pages used in the UO skills (this library, June 2026):

| Page | Last seen modified | Notes |
|---|---|---|
| `uoguide.com/Main_Page` | 2025-02-06 | Index, latest Publish (123), Current Event (Moonveil). |
| `uoguide.com/Expansion` | 2026-02-13 | T2A → ToL timeline; KR is a client upgrade, not an expansion. |
| `uoguide.com/Facets` | 2016-01-13 | 7 facets, per-facet PvP/travel/duplication rules. |
| `uoguide.com/Skills` | 2016-01-10 | 58 skills in 6 categories, cap 720, 100 base, PowerScroll ext. |
| `uoguide.com/Item_Properties` | 2022-07-04 | Hit/Permanent/Persistent types, intensity, pre-AoS 5-property set, negative properties. |
| `uoguide.com/Stat` | 2016-09-12 | Str/Dex/Int, 125/150/225/260 caps, primary/secondary per skill, stat gain mechanics. |
| `uoguide.com/Special_move` | 2026-05-25 | Primary 30/70, Secondary 60/90 (Publish 96); ML/SE/SA moves; LMC rules. |
| `uoguide.com/Races` | 2014-05-29 | Human/Elf/Gargoyle racial abilities including SA Berserk math. |
| `uoguide.com/Resisting_Spells` | 2016-03-11 | Resist floor formula; per-spell resistable list. |
| `uoguide.com/Virtues` | 2017-07-28 | 8 Virtues, mantras, sins, town associations. |
| `uoguide.com/Factions` | 2014-09-28 | 4 factions, 8 cities, sigil rules, replaced by VvV in Publish 86. |
| `uoguide.com/Bulk_Order_Deed` | 2025-09-21 | SBOD/LBOD, bribery (Publish 74), point value (Publish 95). |
| `uoguide.com/Crafting` | 2025-12-13 | Crafting skills, primary/secondary resources, gathering. |
| `uoguide.com/Magery_Spells` | 2017-08-21 | 8 circles with mana costs 4/6/9/11/14/20/40/50. |
| `uoguide.com/Paralyze` | 2010-05-19 | Sample 5th-circle spell table: reagents, mana, delay, min skill. |
| `uoguide.com/Champion_spawn` | 2026-02-25 | 16-red-candle scaling, reward tiers, Star Room, dynamic events. |
| `uoguide.com/Animal_Lore` | (date varies) | Pet stat display, Veterinary link. |
| `uoguide.com/Pet_training` | (date varies) | Pet AI / training 1-6, derived from Publish 97 (out of ML scope). |

**Primary source for any artifact not in the uo.com master tables.** Per-weapon UOGuide pages carry the full per-artifact stat block (rarity, HitSpell, Damage, Elemental type, Ranged info, etc.) plus drop source. Use `https://www.uoguide.com/{Name_With_Underscores}` as the deterministic URL pattern (apostrophes → `%27`). See `references/uo-master-list-extraction.md` for URL generators and a parsing recipe.

## Tier 1 - UO Stratics (uo.stratics.com)

Original UO-era feature spotlights. Best for "how was this introduced and what changed in which publish" and for the AoS Combat Changes primary source. Stratics pages are older (most last edited pre-2010) but they are the contemporary developer-facing description of major systems, which is closer to the official intent than later retrospectives.

Pages used in the UO skills (this library, June 2026):

| Page | Era | Notes |
|---|---|---|
| `uo.stratics.com/content/aos/combatchanges.shtml` | AoS (Feb 2003) | Primary source for the AoS combat rework: 5 damage types, 4 new resistances, Reactive Armor, Magic Reflection, Archery, special moves, item insurance, stat-loss removal. |
| `uo.stratics.com/content/skills/` (per-skill pages) | various | Per-skill guides, in-game training notes. Useful for older skill pages not covered by UOGuide. |
| `uo.stratics.com/content/ml/crafting.shtml` | ML | ML recipes, rare resources, craftable items, craft quests. |
| `uo.stratics.com/content/basics/bod_smithing_calc.php` | various | Smith BOD calculator. |
| `uo.stratics.com/content/basics/bod_tailoring_calc.php` | various | Tailor BOD calculator. |

**Stratics Community Wiki** (`wiki.stratics.com`) is a separate site and the modern player-built wiki. URL pattern: `https://wiki.stratics.com/index.php?title=UO:{Name_With_Underscores}`. Use for player how-to content and old-school mechanics deep-dives when uoguide.com and uo.com are too thin.

Stratics is the right place when a UOGuide page is too thin or out of date for the AoS-era mechanics. Always cross-reference with a current UOGuide or uo.com page to catch post-2010 publishes (e.g. Publish 96 special-move threshold change).

## Tier 1 - uo.com Wiki (uo.com/wiki/ultima-online-wiki/...)

The official Broadsword wiki, currently active. Best for:

- The canonical per-spell page (reagents, mana, delay, min skill, formula, duration).
- The canonical per-skill page (primary/secondary stat, training locations, sample templates).
- The current Publish notes (the highest-numbered Publish is the live one, lower numbers are historical).
- **The canonical master-table pages for whole item categories** (e.g. `items/weapons/` lists every standard weapon in one table). This is the only source that has all standard weapons in one fetch — use it as primary source for any weapon parity audit, then use UOGuide per-item pages for crafting recipes and artifact-specific details.

Pages used in the UO skills (this library, June 2026):

| Page | Notes |
|---|---|
| `uo.com/wiki/ultima-online-wiki/skills/necromancy/necromancy/` | Full Necromancy spell list with reagents, mana, delay, min/max skill, descriptions. |
| `uo.com/wiki/ultima-online-wiki/skills/chivalry/chivalry/` | Chivalry spell list with Tithing/Mana/Skill/Description, tithing mechanic, Karma scaling. |
| `uo.com/wiki/ultima-online-wiki/skills/magery/magery-spells/` | Magery 1st-2nd circle full table. |
| `uo.com/wiki/ultima-online-wiki/skills/carpentry/` | Carpentry craft page with tools and resource list. |
| `uo.com/wiki/ultima-online-wiki/combat/champion-spawns/` | Champion Spawn escalation mechanic. |
| `uo.com/wiki/ultima-online-wiki/items/weapons/` | **Master weapons table** — 126 standard weapons in one `<table>`, grouped by skill (Swordsmanship / Axes / Mace Fighting / Fencing / Archery / Throwing / Unarmed), with damage, speed, strength, special moves. Use as primary source for any weapon parity audit. Does NOT cover artifacts — for those, UOGuide is primary. See `references/uo-master-list-extraction.md` for the parse recipe and URL generators. |

When the canonical answer disagrees with UOGuide (e.g. exact damage formula), the uo.com wiki is the tiebreaker for live client behavior; UOGuide is the tiebreaker for historical/publish-by-publish behavior.

## Tier 2 - Reputable secondary sources

Use these when the Tier 1 sources do not cover the topic, but verify against the repo before citing.

- `wiki.stratics.com` (Stratics Community Wiki) - the modern Stratics wiki, separate from `uo.stratics.com`. Best for player-built how-to content and mechanics deep-dives. Now Tier 1-equivalent for items; URL pattern `UO:{Name}`.
- `uoherald.com` - the historical UO Herald, archived. Good for early-era publish notes and dev interviews.
- `codex.ultimaaiera.com` - the Ultima Codex, lore-focused. Use for Virtue/lore explanations, not for game mechanics.
- `uodemod.com`, `runuo.com` - the RunUO/ServUO demods, useful as cross-references for "how a different open-source UO emulator did it". Do not cite as the canonical UO behavior.

## Tier 3 - Private shards and custom rulesets

- `uooutlands.com/wiki`, `uoevo.com/wiki`, `uoforum.com` - private shard wikis. Their content is shard-specific; only use for "how does Outlands / Evolution / UOF do X" comparative content. Never cite as canonical UO behavior.

## Citation Conventions

When citing a UO source in a UO skill's SKILL.md:

1. Place the citation in the "Related Skills" footer, prefixed with the source tier so the validation script can detect it (e.g. `www.uoguide.com/...`, `uo.stratics.com/...`, `uo.com/wiki/...`).
2. Mention the "last modified" date inline only if the mechanic is known to have changed (e.g. "Special Moves (Publish 96, 2017)"; "Resisting Spells (Publish 48, 2007) added Blood Oath reduction").
3. For per-spell or per-item tables, link the page and let the skill body summarize the relevant subset; do not paste the table.

## Era / Publish Timeline (from uoguide.com/Expansion)

| Era | Date | Headline mechanics |
|---|---|---|
| Original UO | 1997-09 | Pre-T2A, no item properties, simple damage. |
| T2A - The Second Age | 1998-10 | Lost Lands, first expansion. |
| UOR - Renaissance | 2000-05 | Trammel facet, Factions, special moves (3 of them), magic system changes. |
| UOTD - Third Dawn | 2001-03 | 3D client, Ilshenar, first Champion Spawns (titles only). |
| LBR - Blackthorn's Revenge | 2002-02 | No new land; Ilshenar open to 2D client; McFarlane creatures. |
| AOS - Age of Shadows | 2003-02 | **The Big Divide**: 5 damage types, 4 new resistances, item properties, item insurance, Necromancy, Chivalry, Malas, special moves reworked (13 total), Reactive Armor / Magic Reflection redesign, stat-loss removal in Felucca. |
| SE - Samurai Empire | 2004-11 | Tokuno, Bushido, Ninjitsu, reduced cast delay (250 ms). |
| ML - Mondain's Legacy | 2005-08 | Spellweaving, Heartwood, Elves, ML dungeons, ML recipes, ML Peerless bosses, ML scroll rates. |
| SA - Stygian Abyss | 2009-09 | Gargoyles, Ter Mur, Mysticism, Throwing, Imbuing, new Champion Spawns. |
| HS - High Seas | 2010-10 | First "booster"; ships, fishing expansion, floating village. |
| TOL - Time of Legends | 2015-10 | Shadowguard, Valley of Eodon, Dragon Turtle Champion, Skill Mastery, completed Virtues. |
| EJ - Endless Journey | 2018-03 | Free-to-play constraint layer; F2P account policy + content restrictions. |

Use this table when an era boundary in the codebase needs a date. The era enum in `Projects/Server/ExpansionInfo.cs` matches this order, so any era-gate in code maps 1:1 to a row above.

**Note on the 2016 Weapon Revamp:** not an expansion; a Publish-note-level rebalance that +1 to +3 buffed most weapons' MaxDamage and re-tuned speeds. The ModernUO repo's `AosMinDamage`/`AosMaxDamage` typically still reflect the pre-Revamp values — a parity audit will surface the diff as a systematic +N on MaxDamage for ~60 weapons. See `references/uo-master-list-extraction.md` § "Diff heuristics" for the four common divergence modes in this repo.

## Recurring Research Trap - Web Summarization

The `web_extract` tool returns summarized content for pages over a few thousand characters. Summarized content:

- Loses the per-spell mana cost in the 8-circle table (only the table headers survive).
- Loses the per-spell reagent list in the 4th-8th circles.
- Loses the per-race bonus magnitudes (only the bonus names survive).
- Loses the per-publish mechanical changes (only the headline survives).
- Loses the per-weapon row data in the master weapons table (only the skill-section headers and a few example rows survive).

**For master tables specifically, do not rely on `web_extract` — `curl` the page and parse locally.** The HTML table is small (one `<table>` with ~140 rows) and the per-row data fits in a single fetch. See `references/uo-master-list-extraction.md` for the recipe.

When a page is summarized, the per-row data must be re-extracted from a more granular source. The official `uo.com/wiki/...` per-spell pages and the Stratics AoS Combat Changes page are reliable for the granular data. When neither source yields the answer, the answer is "incomplete" - flag it in the skill and move on rather than invent the value.

## Cross-Reference With Repo Documents

The repo carries its own research bank. Use it as the "what we have actually implemented" side of the triangulation:

| Repo document | Coverage |
|---|---|
| `docs/server-engine-knowledge-base.md` | Engine architecture, atomic systems, the canonical layering model. |
| `docs/mondains-legacy-content-matrix.md` | ML parity status per area, per-area source evidence, implementation tickets. |
| `docs/mondains-legacy-crafting-matrix.md` | Crafting per-system recipe/resource matrix with parity gaps. |
| `docs/era-analysis-tickets.md` | Per-era analysis ticket template, applied to the 12 expansions. |
| `docs/manual-test-mondains-legacy.md` | Live QA checklist for ML. |
| `docs/superpowers/plans/2026-06-02-item-properties-completion.md` | The UOGuide item-property parity plan, open work items. |
| `dev-docs/era-expansion.md` | Per-era changes documented at the code level, with the pre-AoS/AoS/SE/ML/SA boundary. |
| `dev-docs/content-patterns.md` | Templates for new content (items, creatures, spells, gumps). |
| `Projects/UOContent/Items/Weapons/weapons.md` | The June 2026 weapon parity audit (168 weapons, 85 matched to UO.com, 66 with diffs) — the template for any future "audit N similar items" task. |

The repo documents are the tiebreaker for "what does the engine do today" and the canonical source for the per-area parity status. When the canonical UO source and the repo document disagree, the disagreement is a real bug or a deliberate parity choice; both must be acknowledged in the SKILL.md.
