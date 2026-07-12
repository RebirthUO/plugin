# Spell issue research notes

Use this when drafting `spell.yml` issues for missing or partially implemented ModernUO/RebirthUO spells.

## Repo anchors to check

- `.github/ISSUE_TEMPLATE/spell.yml` for exact field labels and title/label contract.
- `Projects/UOContent/Spells/Initializer.cs` for registration IDs, era gates, and commented placeholders. A commented `Register(...)` line is strong repo evidence for intended spell ID and school slot, but not proof the spell is implemented.
- `Projects/UOContent/Spells/<School>/` for existing base classes and sibling spell patterns.
- `Projects/UOContent/Items/Skill Items/Magical/Scrolls/<School>/` for scroll classes that may already exist before the spell itself is implemented.
- `Projects/UOContent/Migrations/*.json` for existing serialized scroll/mobile metadata.
- Character creation / spellbook code before assuming player learning or starter-book support exists.

## Online source pattern

1. Prefer UO.com skill pages and publish notes as `Canonical` for era, publish, spell role, core costs, and reagent lists.
2. Use UOGuide/Stratics as `Community/reference` for tables, success chances, duration notes, and restrictions such as player-house casting. Do not silently override UO.com with community data when they disagree.
3. Use ServUO/RunUO as `Engine precedent` for class names, IDs, targeting shape, effects, control slots, scaling formulas, dispel values, and mobile stats.
4. If a direct raw ServUO path 404s, inspect the repository tree recursively. ServUO spell code may live under nested paths such as `Scripts/Spells/Mysticism/SpellDefinitions/<SpellName>Spell.cs`, while related scrolls/mobiles may live in separate `Items/Consumables/SpellScrolls/` or `Mobiles/Summons/` folders.

Example tree probe:

```bash
python - <<'PY'
import json, urllib.request
url='https://api.github.com/repos/ServUO/ServUO/git/trees/master?recursive=1'
req=urllib.request.Request(url, headers={'User-Agent':'Hermes/1.0'})
data=json.load(urllib.request.urlopen(req, timeout=60))
for item in data.get('tree', []):
    p=item['path']
    if 'Rising' in p or 'Colossus' in p or ('Mysticism' in p and p.endswith('.cs')):
        print(p)
PY
```

## Conflict handling

When UO.com, UOGuide, and engine precedent disagree, put the conflict in the issue body instead of picking silently:

- `Observed conflict`: name the sources and exact disagreement.
- `Likely interpretation`: prefer canonical UO.com when it matches engine precedent, unless repo behavior or shard policy says otherwise.
- `Decision needed`: only for the custom-policy choice evidence cannot decide.
- `Suggested default`: a conservative era-consistent recommendation, usually UO.com + tested engine precedent.

## Useful issue details for summon spells

- Follower/control slot cost and failure message.
- Target type: mobile vs ground/location; blocked-location and town/region checks.
- Duration formula and whether public sources provide exact values or only qualitative scaling.
- Power scaling source skills, especially schools where support skill changed by publish (for Mysticism, max(Focus, Imbuing), not Evaluating Intelligence).
- Dispel/Mass Dispel counterplay and dispel difficulty/focus.
- Housing/no-summon restrictions and PvP notoriety/aggression rules.
- Save compatibility for any new summon mobile: source-generated serialization and migration metadata.
