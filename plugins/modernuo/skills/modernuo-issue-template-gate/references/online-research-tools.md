# Online research for issue drafts (Hermes tools)

Use when `web_extract` is unavailable or UO.com tables are hard to scrape as plain text.

## UO.com Magic Item Properties table

1. `browser_navigate` to `https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/`
2. `browser_console` with an expression that filters `table` rows, e.g. search for property name:

```javascript
(() => {
  const t = document.querySelector('table');
  const rows = [...t.querySelectorAll('tr')].map(r =>
    [...r.querySelectorAll('td,th')].map(c => c.innerText.trim()).join(' | ')
  );
  return rows.filter(r => /Massive/i.test(r)).join('\n');
})()
```

3. If the browser console rejects a multiline expression, retry as a single-line IIFE:

```javascript
(()=>{const rows=[...document.querySelectorAll('table tr')].map(r=>[...r.querySelectorAll('td,th')].map(c=>c.innerText.trim()).join(' | ')); return rows.filter(r=>/Soul Charge/i.test(r)).join('\n');})()
```

4. For Publish 86 negative-property bullet list, navigate to UO.com or UOGuide Publish 86 page and `browser_console` `document.body.innerText` slice around the property name.

## UO.com publish/page discovery

When the exact UO.com URL is unknown or the visible publish index omits older publishes, use the WordPress REST search endpoint before falling back to general web search:

```bash
python - <<'PY'
import json, urllib.parse, urllib.request
QUERY = "Soul Charge Publish 60"
url = "https://uo.com/wp-json/wp/v2/search?" + urllib.parse.urlencode({"search": QUERY, "per_page": 10})
req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
for item in json.load(urllib.request.urlopen(req, timeout=30)):
    print(item.get("title"), item.get("url"))
PY
```

This is especially useful for old paths under `/technical/previous-publishes/<year>/...`.

## UOGuide API fallbacks

If `browser_navigate` to UOGuide times out, try the MediaWiki API. Some pages return empty `extracts`; in that case fetch raw wikitext through `prop=revisions&rvprop=content` and search within it.

```bash
python - <<'PY'
import json, urllib.parse, urllib.request
TITLE = "Publish 60"
params = urllib.parse.urlencode({
    "action": "query",
    "prop": "revisions",
    "rvprop": "content",
    "titles": TITLE,
    "format": "json",
    "redirects": 1,
})
req = urllib.request.Request("https://www.uoguide.com/api.php?" + params, headers={"User-Agent": "Hermes/1.0"})
data = json.load(urllib.request.urlopen(req, timeout=45))
page = next(iter(data["query"]["pages"].values()))
text = page.get("revisions", [{}])[0].get("*") or page.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("*", "")
for term in ["Soul Charge", "Stygian Abyss", "Imbuing"]:
    i = text.lower().find(term.lower())
    if i >= 0:
        print(f"--- {term} ---")
        print(text[max(0, i - 400):i + 900])
PY
```

## ServUO / RunUO snippets (no GitHub code search auth)

```bash
curl -sL --max-time 20 "https://raw.githubusercontent.com/ServUO/ServUO/master/Scripts/Items/Equipment/Weapons/BaseWeapon.cs" | grep -n "Massive\|NegativeAttr"
```

For spell issues, raw-path guessing can fail because upstream filenames or directories may differ from ModernUO conventions (for example a file may be under `Scripts/Spells/Mysticism/SpellDefinitions/` or include an unexpected space in the name). Use the GitHub contents API to list the directory first, then fetch the returned `download_url`:

```bash
python - <<'PY'
import json, urllib.parse, urllib.request
repo = "ServUO/ServUO"
path = "Scripts/Spells/Mysticism/SpellDefinitions"
url = f"https://api.github.com/repos/{repo}/contents/" + urllib.parse.quote(path) + "?ref=master"
req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0", "Accept": "application/vnd.github+json"})
for item in json.load(urllib.request.urlopen(req, timeout=30)):
    print(item["name"], item.get("download_url"))
PY
```

When a matching spell exists upstream, capture only behaviorally useful precedent in the issue: spell ID/slot, gump or target flow, conflict checks, temporary-state cleanup hooks, buff icons/messages, and how temporary properties are made visible to the combat pipeline.

## Item property issues

When template is `item_property.yml`, also `skill_view('uo-item-property-review')` and any `references/*-item-property-review.md` for that property before `gh issue create`. Capture UO.com vs ServUO conflicts under `## Research Notes`.

## Windows `gh issue create`

`--body-file` via `gh.exe` may reject MSYS paths; use `cygpath -w` for the body file path.