---
name: uoguide-item-properties
description: Use when extracting UOGuide Item Properties table rows for AoS-and-later item property parity checks before mapping property ranges, found-on data, and source uncertainty to ModernUO/RebirthUO code.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    - UltimaOnline
    - ItemProperties
    - Parity
    - AOS
    related_skills:
    - uo-aos-item-properties
    - modernuo-item-property-parity-check
    - uo-domain-research
license: MIT
---
# UOGuide Item Properties Reference

## Overview

This skill uses UOGuide's Item Properties page as a compact source for UO item property parity checks, especially AoS-and-later property ranges, activation types, and allowed item classes. It does not treat UOGuide as live code truth or override official/source evidence; always define the era/ruleset and verify repository behavior. It needs only Hermes tools and Python standard library when fetching raw wikitext through `terminal`.

## When to Use

- The user says "item properties", "UOGuide Item Properties", or "AoS item property range".
- You need to answer which item classes can roll a named property.
- You are auditing properties such as Hit Curse, Hit Fatigue, Hit Mana Drain, Splintering Weapon, Damage Eater, Resonance, or Soul Charge.
- You need to separate main AoS properties from Stygian Abyss, special, negative, or pre-AoS property behavior.
- You are preparing a ModernUO/RebirthUO item-property parity note and need a source-backed row before touching code.

## Prerequisites

- Web access to `https://www.uoguide.com/Item_Properties`.
- No credentials, environment variables, or package installs are required.
- Before applying the data to a shard, define publish base, emulator, client, era gates, and custom deviations.
- For ModernUO/RebirthUO implementation work, load `skill_view` for `uo-aos-item-properties`, `modernuo-item-property-parity-check`, and `modernuo-era-expansion` after extracting the source fact.

## How to Run

Invoke the source fetch through the `terminal` tool and use the raw MediaWiki endpoint so table rows are visible without browser markup:

```bash
python - <<'PY'
import urllib.request
url = "https://www.uoguide.com/index.php?title=Item_Properties&action=raw"
text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "replace")
print(text)
PY
```

Use `read_file` and `search_files` for repository anchors, `execute_code` for small table parsing, and `patch` only after the source row, era gate, and test target are clear.

## Quick Reference

- Source page: `https://www.uoguide.com/Item_Properties`
- Raw wikitext: `https://www.uoguide.com/index.php?title=Item_Properties&action=raw`
- Main columns: `Property Name`, `Intensity Range`, `Type`, `Found On`
- Found-on order: `Armor`, `Jewelry`, `Shield`, `Spellbook`, `Weapon`
- Type values: `Hit`, `Permanent`, `Persistent`
- Main section: `==Properties==`
- SA section: `===Stygian Abyss Item Properties===`
- Special section: `===Special Item Properties===`
- Negative section marker: `===Negitive Item Properties===`
- Pre-AoS section: `==Item Properties Pre-AoS==`

## Procedure

1. **Establish the era scope first.** If the target is pre-AoS, use the pre-AoS section instead of the main AoS table. If the target is AoS or later, record whether SA, later publish, event, or custom rules are in scope.

2. **Fetch the raw source.** Use the `terminal` command above or `browser_navigate` on the source page if raw fetch is unavailable. Completion means the text contains the expected section markers from Quick Reference.

3. **Apply the table key literally.** `Intensity Range` is the common-item allowable range; artifacts and other special items may break it. `Hit` activates when an animal, monster, or player is hit; `Permanent` affects the item whether equipped or not; `Persistent` activates while equipped.

4. **Extract one property row at a time.** Preserve the source property name, range, type, and found-on columns in the order Armor/Jewelry/Shield/Spellbook/Weapon. Do not silently normalize duplicates or spelling oddities; compare the page row with the named property's own page when a row looks suspicious.

5. **Bucket the row by system.** Main `Properties` rows describe normal loot, runic-tool, and imbuing candidates. `Stygian Abyss Item Properties` contains Blood Drinker, Battle Lust, Casting Focus, Damage Eater, Reactive Paralyze, Resonance, Soul Charge, and Splintering Weapon. Special and negative rows describe item-state or event-specific properties, not default magical loot rolls.

6. **Use property-family checks before coding.** Weapon hit effects are normally weapon-only and often 2-50%, while Life/Mana leech can reach 100% and Stamina leech is 2-50%. Casting properties split across Faster Cast Recovery, Faster Casting, Spell Damage Increase, Lower Mana Cost, and Lower Reagent Cost with different item classes. Resist rows are all 1-15% but their shield availability differs by element, so verify the exact row.

7. **Handle pre-AoS as a different product model.** The page describes the original system as a small set of durability, damage, newbified, battle tactics, armor resistance, and hit-spell style properties. Armor had up to three property categories; weapons had five, and weapon hit spells were counted as one category even when several spell names existed.

8. **Cross-check before implementation.** For live parity or RebirthUO code changes, compare UOGuide with UO.com, Stratics when needed, and the repository source. Report the era assumption, source URL, property row, code anchor, expected player-visible behavior, and test coverage.

## Pitfalls

- Artifacts and special items may break both intensity ranges and found-on restrictions; do not use the common-item table to reject an artifact property by itself.
- The UOGuide source spells the negative section as `Negitive`; use the exact marker when verifying the raw page.
- `Brittle` appears in both special and negative contexts; decide whether you are auditing a displayed property, an item-state rule, or a generation rule before deduping.
- Publish/event-specific rows such as Bane, Shard Bound, Rage Focus, and Treasures items are not normal AoS loot-generation evidence.
- Pre-AoS and AoS labels can share words while using very different formulas; the page notes old Vanquishing damage was far below modern 100% damage increase expectations.
- For ModernUO/RebirthUO, a source row is not enough: check era gates, OPL tooltip output, item generation, combat formulas, serialization safety, and regression tests.

## Verification

Invoke this through the `terminal` tool; it proves the source still resolves and all expected sections are present:

```bash
python - <<'PY'
import urllib.request
url = "https://www.uoguide.com/index.php?title=Item_Properties&action=raw"
text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "replace")
for marker in [
    "==Properties==",
    "===Stygian Abyss Item Properties===",
    "===Special Item Properties===",
    "===Negitive Item Properties===",
    "==Item Properties Pre-AoS==",
]:
    assert marker in text, marker
print("UOGuide Item Properties raw page contains all expected sections.")
PY
```
