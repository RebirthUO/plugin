# Item Properties Internet Extraction Notes

Use when the user asks for a source-backed list of Ultima Online item properties to be written as documentation files.

## Durable Sources

- UO.com official page: `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
- UOGuide API wikitext endpoint: `https://www.uoguide.com/api.php?action=query&prop=revisions&rvprop=content&titles=Item%20Properties&format=json&formatversion=2`
- UOGuide readable page form: `https://www.uoguide.com/Item_Properties`

## Extraction Pattern

1. Fetch UO.com HTML and parse the main `Magic Item Properties` table.
   - It is useful for modern properties and includes columns like `Property`, `Intensity Range`, `Imbue Weight`, `Found on`, `Capped`, `Description`.
   - Preserve repeated rows for the same property when UO.com has separate item-class rows.
2. Fetch UOGuide wikitext through the API instead of scraping the rendered page when possible.
   - Parse tables under headings: `Properties`, `Stygian Abyss Item Properties`, `Special Item Properties`, and the misspelled `Negitive Item Properties`.
   - UOGuide breaks out concrete tooltip variants such as `Cold Resist`, `Hit Fire Area`, `No-Drop`, `No-Trade` that UO.com may group under broader rows like `Resist` or `Hit Area Damage`.
3. Merge by normalized property name.
   - Keep UO.com as the official source row where present.
   - Add UOGuide rows for variants or special-state properties.
   - For UOGuide-only concrete variants, optionally attach the related UO.com umbrella row, e.g. resist variants -> `Resist`, hit area variants -> `Hit Area Damage`, `Unlucky` -> `Luck`.
4. Generate one Markdown file per property plus a README index.
   - Include a clear warning: these are internet-source docs, not proof of local RebirthUO implementation.
   - Include repo anchors for local AoS containers: `Projects/UOContent/Misc/AOS.cs` (`AosAttribute`, `AosWeaponAttribute`, `AosArmorAttribute`, `AosSkillBonuses`).
5. Verify counts and links.
   - Count Markdown files, property files, README rows, missing local links, and required sections.
   - Verify primary source endpoints returned HTTP 200 during generation.

## Pitfalls

- UO.com groups some variants; do not omit concrete UOGuide variants just because the official page uses an umbrella row.
- UOGuide rendered pages may be slow or time out intermittently; the API endpoint is often more reliable for extraction.
- `index.php?title=` links can be flaky; prefer direct `/Page_Title` links for normal pages, and anchor back to `/Item_Properties#Special_Item_Properties` for composite targets like `No-Drop/No-Trade`.
- Do not present the generated list as implementation parity. Follow-up parity requires repository/code inspection and era gates (`Core.AOS`, `Core.SE`, `Core.ML`, `Core.SA`).
