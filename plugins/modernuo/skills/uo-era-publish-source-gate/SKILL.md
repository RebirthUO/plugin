---
name: uo-era-publish-source-gate
description: Require official sources for UO eras and publishes.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
    skill_group: uo
    skill_subgroup: gate
    workflow_phase: none
    workflow_tier: support
---
# UO Era and Publish Source Gate

This skill enforces a mandatory source gate for Ultima Online era, expansion, and publish claims. It does not replace mechanics-specific UO skills or repo inspection; it prevents unsourced timeline assertions from becoming implementation decisions. It uses Hermes tools and live source pages only; no extra packages or scripts are required.

## When to Use

- "Which era or publish introduced this?"
- "Is this publish/era accurate?"
- "Map this feature to an expansion, era, or publish."
- "Create/update a RebirthUO issue involving eras or publishes."
- Any answer, plan, PR review, or issue body that names T2A, UOR, AoS, SE, ML, SA, HS, ToL, EJ, or a publish number.

## Prerequisites

- Internet access for Broadsword/UO.com and UOGuide pages.
- No credentials or environment variables are required.
- Use Broadsword/UO.com as the official current source.
- Use UOGuide as the mandatory historical cross-check named by the user.
- If code behavior matters, also inspect local repo anchors with `read_file` and `search_files`.

## How to Run

Use `browser_navigate` and `browser_snapshot` to open the Broadsword/UO.com and UOGuide pages before making an era or publish claim. If UOGuide is slow in the browser, invoke a small stdlib Python lookup through the `terminal` tool against its MediaWiki API. Use `read_file` and `search_files` for local RebirthUO/ModernUO era gates, but never treat repo code as the source of official era history.

## Quick Reference

- Broadsword publish index: `https://uo.com/wiki/ultima-online-wiki/publish-notes/`
- Broadsword wiki root: `https://uo.com/wiki/ultima-online-wiki/`
- Broadsword publish pattern: `https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-<number>/`
- UOGuide expansion index: `https://www.uoguide.com/Expansion`
- UOGuide publish pattern: `https://www.uoguide.com/Publish_<number>`
- UOGuide API search: `https://www.uoguide.com/api.php?action=query&list=search&srsearch=Publish&format=json`
- Local expansion data: `Distribution/Data/expansions.json`
- Local expansion gates: `Projects/Server/ExpansionInfo.cs`
- Local era gate search: `Core\.(T2A|UOR|UOTD|LBR|AOS|SE|ML|SA|HS|TOL|EJ)`

## Procedure

1. **Scope the claim.** Identify the exact era, expansion, publish number, or timeline assertion in the user's request. You are done when every timeline claim is listed as a check item, not implied in prose.

2. **Open the Broadsword source first.** Use `browser_navigate` on `https://uo.com/wiki/ultima-online-wiki/publish-notes/` for publish work or `https://uo.com/wiki/ultima-online-wiki/` for current wiki work. For a numbered publish, click the index entry when present instead of guessing a named slug. You are done when the Broadsword/UO.com URL and page title are captured.

3. **Open the UOGuide source second.** Use `browser_navigate` on `https://www.uoguide.com/Expansion` for expansion history or `https://www.uoguide.com/Publish_<number>` for a numbered publish. You are done when the UOGuide URL and page title are captured.

4. **Use the UOGuide API fallback when pages hang.** Invoke this through the `terminal` tool and change only `QUERY`:

   ```bash
   python - <<'PY'
   import json, urllib.parse, urllib.request
   QUERY = "Publish 43"
   params = urllib.parse.urlencode({
       "action": "query",
       "list": "search",
       "srsearch": QUERY,
       "format": "json",
       "srlimit": 5,
   })
   url = "https://www.uoguide.com/api.php?" + params
   req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
   with urllib.request.urlopen(req, timeout=30) as response:
       data = json.load(response)
   for item in data["query"]["search"]:
       print(item["title"], "-", item["snippet"])
   PY
   ```

   You are done when the API returns a matching UOGuide title or you mark the UOGuide source unavailable.

5. **Cross-check, do not average.** If Broadsword and UOGuide disagree, prefer Broadsword for current official behavior and record the UOGuide difference as historical context. Do not silently merge dates, names, or mechanics.

6. **Inspect repo anchors only after source capture.** Use `read_file` on `Distribution/Data/expansions.json` and `Projects/Server/ExpansionInfo.cs`, then `search_files` for the feature gate. You are done when local behavior is labeled as `matches source`, `custom deviation`, `partial implementation`, or `not implemented`.

7. **Write the answer with source labels.** For each era or publish claim, include both `Broadsword/UO.com:` and `UOGuide:` URLs, or explicitly state which mandatory source could not be reached. Unsupported claims must be phrased as `Needs source confirmation`, not fact.

## Pitfalls

- Do not answer era or publish questions from memory, even when the claim sounds obvious.
- Do not use repo enum names as proof of official chronology.
- Do not treat private shard wikis, forum posts, or old notes as substitutes for Broadsword/UO.com plus UOGuide.
- Broadsword publish slugs for named publishes can differ from `publish-<number>`; use the publish index link when available.
- UOGuide may time out in browser navigation; the MediaWiki API usually still works.
- Older UOGuide publish pages may cite archived `update.uo.com` design documents; preserve those links as breadcrumbs, but still label the current source set.

## Verification

Before finalizing, every era/publish claim has a Broadsword/UO.com URL and a UOGuide URL, or is marked `Needs source confirmation` with the missing source named.
