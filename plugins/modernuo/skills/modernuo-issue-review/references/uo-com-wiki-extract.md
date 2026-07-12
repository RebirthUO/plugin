# UO.com wiki text extraction (issue review)

Use when `browser_snapshot` truncates long wiki tables or when you need an exact quote for `## Research Notes` / `## References`.

## Steps

1. `browser_navigate` to the canonical URL (Magic Item Properties, Publish notes, etc.).
2. `browser_console` with `expression` set to one of the snippets below.
3. Classify the result as **Canonical** in the issue body; paraphrase only when the full sentence is too long for a bullet.

## Expressions

**Magic Item Properties — row around a property name** (replace `Massive`):

```javascript
(() => {
  const t = document.body.innerText;
  const m = t.match(/Massive[\s\S]{0,800}/);
  return m ? m[0] : 'not found';
})()
```

**Publish notes — negative property bullets** (page must be Publish 86 or similar):

```javascript
(() => {
  const t = document.body.innerText;
  const i = t.indexOf('Massive');
  return i >= 0 ? t.substring(i - 100, i + 400) : 'not found';
})()
```

General property lookup: change the regex/window to the property under review (`Prized`, `Brittle`, `Sparks`, `Unwieldy`, etc.).

**Publish 96 — Sparks / Swarm / Bone Breaker block** (`publish-notes/publish-96/`):

```javascript
(() => {
  const t = document.body.innerText;
  const i = t.indexOf('Sparks');
  return i >= 0 ? t.substring(i - 200, i + 800) : 'not found';
})()
```

## Pitfalls

- Snapshot ref IDs are for clicking, not for copying table text; prefer `innerText` extraction.
- UOGuide pages are shorter; `browser_snapshot` is usually enough for cross-check, not primary canonical proof.