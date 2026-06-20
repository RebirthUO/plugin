# UO Master-List Extraction Recipe

A reference for parity audits over many similar items in the UO repo. The shape is:

1. Find the canonical master list (one page, one table, all items).
2. `curl` it locally, regex-parse the HTML table.
3. Bulk-extract code stats from every `*.cs` file in one `execute_code` script.
4. Match code-to-canonical by normalized name (with ItemID as secondary key).
5. Generate per-item URLs from the class name (no `web_search` per item).
6. Emit a sorted markdown report grouped by source folder.

This pattern was used to produce `Projects/UOContent/Items/Weapons/weapons.md` in June 2026 (168 weapons, 85 matched to UO.com, 66 with measurable diffs, one session).

## 1. Master-list URL pattern

| Topic | URL | Master table shape |
|---|---|---|
| **Standard weapons** | `https://uo.com/wiki/ultima-online-wiki/items/weapons/` | 1 `<table>`, 144 `<tr>` rows. Skill sections are `<th colspan="6">` cells containing the skill name. Data rows are 6 cells: Weapon Name, Crafted By, Strength, Base Damage, Speed, Special Moves. |
| Spells (per-school) | `https://uo.com/wiki/ultima-online-wiki/skills/<school>/<school>/` | Per-school page; one table per circle. |
| Skills (per-skill) | `https://uo.com/wiki/ultima-online-wiki/skills/<skill>/` | Per-skill page with stat gains and training tips. |
| Item properties | `https://uoguide.com/Item_Properties` | Tier 1 source; per-property intensity table. |
| Special moves | `https://uoguide.com/Special_move` | Tier 1 source; per-move threshold table. |

Always do a quick `web_search` (`site:uo.com wiki items` or similar) before assuming no master list exists. UO.com tends to publish one master page per category; UOGuide tends toward per-item pages.

## 2. `curl` + parse recipe for uo.com master tables

```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://uo.com/wiki/ultima-online-wiki/items/weapons/" \
  -o /tmp/uo_weapons.html
```

The page returns one big `<table>`. Section headers are `<tr><th colspan="N">Skill Name</th></tr>`; data rows have uniform cell counts. Parse with regex, not a DOM library:

```python
import re
from pathlib import Path

html = Path("/tmp/uo_weapons.html").read_text(encoding="utf-8")
m = re.search(r'<table[^>]*>(.*?)</table>', html, flags=re.IGNORECASE | re.DOTALL)
table = m.group(1)
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, flags=re.IGNORECASE | re.DOTALL)

current_section = None
items = []
for r in rows:
    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, flags=re.IGNORECASE | re.DOTALL)
    clean = [re.sub(r'<[^>]+>', ' ', c).strip() for c in cells]
    clean = [re.sub(r'\s+', ' ', c).strip() for c in clean]
    if len(cells) == 1:
        # Section header (e.g. "Swordsmanship", "Axes (Swordsmanship)")
        current_section = clean[0]
        continue
    if len(cells) == 6 and clean[0] == "Weapon Name":
        continue  # column-header row
    if len(cells) == 6 and current_section:
        # Decode HTML entities BEFORE storing
        name = clean[0].replace('&#8211;', '-').replace('&amp;', '&')
        items.append({"name": name, "skill": current_section, **{k: v for k, v in zip(
            ["crafter", "strength", "damage", "speed", "moves"], clean[1:]
        )}})
```

Two things that bite if you skip them:
- **HTML entities** in cell text: `&#8211;` (en-dash), `&#8217;` (curly apostrophe), `&amp;`. Decode before storing or your name-matching will silently fail.
- **`<img>`-only cells** in some UO.com tables (the weapon name column has a small icon `<img>` and the text in a separate cell). Clean with `re.sub(r'<[^>]+>', ' ', c).strip()` then collapse whitespace.

## 3. Bulk code extraction

```python
import re, json
from pathlib import Path

root = Path(r"C:\Users\Jsiem\...\Projects\UOContent\Items\Weapons")
weapons = []

for cs in sorted(root.rglob("*.cs")):
    rel = cs.relative_to(root)
    if len(rel.parts) == 1: continue          # skip top-level files
    if "Abilities" in rel.parts: continue     # skip ability subfolder
    if rel.stem.startswith("Base"): continue  # skip abstract base classes
    
    text = cs.read_text(encoding="utf-8", errors="replace")
    
    # Class declaration
    m = re.search(r'public\s+(?:partial\s+)?class\s+(\w+)\s*:\s*(\w+)', text)
    if not m: continue
    
    # Stat extractors
    def get_int(prop):
        m = re.search(rf'public\s+override\s+int\s+{prop}\s*=>\s*(\d+)\s*;', text)
        return int(m.group(1)) if m else None
    def get_float(prop):
        m = re.search(rf'public\s+override\s+float\s+{prop}\s*=>\s*([\d.]+)f?\s*;', text)
        return float(m.group(1)) if m else None
    
    weapons.append({
        "category": rel.parts[0],
        "class": m.group(1),
        "base": m.group(2),
        "aos_min_dmg": get_int("AosMinDamage"),
        "aos_max_dmg": get_int("AosMaxDamage"),
        "ml_speed": get_float("MlSpeed"),
        "aos_str_req": get_int("AosStrengthReq"),
        # ... etc
    })
```

For 100-200 files this is sub-second. The regex per stat is `r'public\s+override\s+int\s+{prop}\s*=>\s*(\d+)\s*;'` — no escape needed for prop names like `AosMinDamage`. Match the actual override shape you see in one example file before generalizing.

## 4. Name normalization for matching

```python
def normalize(s):
    s = s.lower()
    s = s.replace("&#8217;", "'").replace("&#8211;", "-").replace("–", "-")
    s = re.sub(r"'", "", s)                  # drop apostrophes
    s = s.replace(" ", "").replace("-", "")  # drop spaces and hyphens
    s = re.sub(r'[^a-z0-9]', '', s)         # drop everything else
    return s
```

Build the canonical index with multiple forms per source name:
- Full name: `"Executioner's Axe"`
- Stripped of parenthetical suffixes: `"Executioner's Axe"` (already done)
- Stripped of trailing `*` and `(2 hands)`: `"Executioner's Axe"`
- First word only: `"Executioner's"`

For ambiguous matches, **the ItemID is the tiebreaker.** In the C# code: `[Flippable(0xF49, 0xF4a)]` and `: base(0xF49)`. UOGuide and Stratics always carry the art ID on the item page. Build a `(class, item_id) → uo_url` map and use it when name normalization fails.

## 5. URL pattern generators (no per-item `web_search`)

| Source | Pattern | Notes |
|---|---|---|
| **UOGuide** | `https://www.uoguide.com/{Name_With_Underscores}` | Apostrophes → `%27`. Examples: `Axe_of_the_Heavens`, `Executioner%27s_Axe`. For artifacts, the name is the *artifact* name (e.g. `Frostbringer`), not the *base weapon* name. |
| **Stratics Wiki** | `https://wiki.stratics.com/index.php?title=UO:{Name_With_Underscores}` | Apostrophes → `%27`. Examples: `UO:Katana`, `UO:Axe_of_the_Heavens`. |
| **Stratics Catalog** (older) | `https://uo.stratics.com/database/view.php?db_content=gameitem&id={numeric_id}` | Requires the numeric database ID, not derivable from the class name. Use only when wiki format fails. |
| **uo.com** | `https://uo.com/wiki/ultima-online-wiki/items/weapons/#{skill_anchor}` | Master list page. Anchor format: lowercase, no spaces — e.g. `#swords`, `#mace`, `#fence`, `#bow`, `#throw`, `#fist`. No per-item page on uo.com. |

The CamelCase → UnderScore transform for class-name-based URLs:
```python
import re
def make_uoguide_url_class(cls):
    s = re.sub(r'([a-z])([A-Z])', r'\1_\2', cls)  # AxeOfTheHeavens -> Axe_Of_The_Heavens
    s = s.replace("'", "%27")
    return f"https://www.uoguide.com/{s}"
```

Verify the pattern with one `web_search` for each new content type (weapons, artifacts, ranged, etc.) before generating 100+ URLs blindly. UOGuide and Stratics both 404 silently on bad slugs.

## 6. Diff heuristics for the report

When the diff table shows the code diverging systematically from the canonical, the most common causes in this repo (June 2026) are:

- **Pre-2016 Weapon Revamp**: `Longsword` code says `MaxDamage=16`, UO.com says `18` (canonical post-revamp). Affects ~60 weapons; the code keeps the AoS pre-revamp values. Verify by checking the project era profile in `Core.AOS`/`Core.SE` and looking for a `Distribution/Data/Eras/*.json` post-2016 revamp profile.
- **ML introduction date**: weapons added in ML (Publish 36, Aug 2005) sometimes carry the ML stat instead of the AoS stat. E.g. `ElvenCompositeLongbow` code says `Dmg 12-16`, UO.com says `15-19` — code is the pre-ML stat.
- **Custom balancing outliers**: `Yumi` in the code has `Dmg 20, Speed 4.5s`, UO.com says `13-17, 3.25s`. The code is *stronger*, which is the opposite of the pre/revamp pattern. Flag for manual review — could be a bug, a deliberate PvM buff, or a copy-paste from the wrong weapon.
- **Inherent weapons**: `MagicWand`, `FireworksWand`, `ShepherdsCrook` often have different damage types or slot-only rules. UO.com has stats for them but the code may use utility hooks. Cross-check by reading the class for any `OverrideDamageType` or `GetDamageTypes` override.

Report each diff as a single line with the format `code=X uo.com=Y (+N)` or `(–N)`. The sign convention is **uo.com minus code**, so a positive diff means the canonical is higher than the code.

## 7. Output structure

A parity audit report should be a single `.md` file in the audited folder with these sections, in order:

1. **Header** + "Quellen" table (3 sources with URL + one-line description each).
2. **Methodology** (4-6 bullets: what was extracted, how, what was matched, what was not).
3. **Coverage summary** (total / matched / unmatched counts).
4. **Headline finding** (the one or two sentences that justify the audit — e.g. "Code is pre-2016 Revamp, UO.com is post-Revamp").
5. **Per-category tables** (one table per source folder, sorted by class name, columns: Class, File, UO.com Name, Skill, AOS Min, AOS Max, ML Speed, Str, Prim., Sek., UO.com link, UOGuide link, Stratics link).
6. **Master diff table** (only the rows with diffs, sorted by class).
7. **Unmatched list** (the items in code with no canonical entry, with artifact-flag column and the auto-generated UOGuide/Stratics URLs).
8. **Source-coverage note** ("UO.com does not cover Doom Artifacts; UOGuide is the primary source for those").

For the weapons audit specifically, the report is `Projects/UOContent/Items/Weapons/weapons.md` (~80 KB, ~490 lines for 168 weapons). It is the template for any future "audit N similar items" task in this repo.
