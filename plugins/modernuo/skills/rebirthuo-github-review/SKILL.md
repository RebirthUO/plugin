---
name: rebirthuo-github-review
description: Review RebirthUO needs-review issues fachlich.
version: 0.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [GitHub, RebirthUO, Review, Triage, ModernUO]
    related_skills: [github-issues, rebirthuo-implement, uo-modernuo-workflow, uo-living-world-review, rebirthuo-modernuo-codebase]
---
# RebirthUO GitHub Review

Dieser Skill erstellt ein fachliches, implementierungsnahes Review für RebirthUO-GitHub-Issues mit dem Label `needs-review`. Er implementiert keinen Code und öffnet keine PRs; er entscheidet, ob alle Voraussetzungen für eine sichere Code-Implementierung erfüllt sind. Er nutzt `gh` über das `terminal`-Tool sowie `read_file`, `search_files`, `browser_navigate`/`browser_snapshot` (oder `web_extract`, falls in der aktuellen Tool-Oberfläche verfügbar) und `skill_view`; zusätzliche Pakete sind nicht erforderlich.

## When to Use

- "rebirthuo-github-review" oder "fachliches Review für RebirthUO #123".
- "prüfe das nächste needs-review Ticket".
- "review das nächste Issue mit needs-review".
- Wenn ein RebirthUO-Ticket vor der Implementierung auf Quellen, Repo-Anker, Akzeptanzkriterien und Testbarkeit geprüft werden soll.
- Nicht verwenden, wenn der User direkt Code-Implementierung/PRs verlangt; dann `rebirthuo-implement` laden.

## Prerequisites

- Lokales Repo: `C:\Users\Jsiem\Documents\GitHub\RebirthUO\service` oder ein anderes Checkout von `RebirthUO/service`.
- GitHub CLI `gh` ist authentifiziert und darf Issues lesen, kommentieren und Labels bearbeiten.
- Standard-Repo, falls nicht explizit gesetzt: das GitHub-Repo des aktuellen `origin`.
- Companion-Skills vor der Arbeit laden: `github-issues`, `uo-modernuo-workflow`, `uo-living-world-review`, `rebirthuo-modernuo-codebase`; bei code-nahen Risiken zusätzlich die passende ModernUO/UO-Domain-Skill.
- Bei fehlendem GitHub-Zugriff keine Ticketinhalte erfinden; User um Issue-Body/Kommentare bitten oder Zugriff wiederherstellen.

## How to Run

Ohne explizites Ticket wähle über das `terminal`-Tool das offene Issue mit `needs-review` und der kleinsten Issue-Nummer:

```bash
OWNER_REPO=${OWNER_REPO:-$(git remote get-url origin | sed -E 's|.*github\.com[:/]||; s|\.git$||')}
ISSUE=$(gh issue list --repo "$OWNER_REPO" --state open --label "needs-review" --limit 1000 --json number --jq 'sort_by(.number)[0].number')
printf '%s\n' "$ISSUE"
```

Mit explizitem Ticket setze `ISSUE=<number>` oder nutze die Nummer aus der Issue-URL. Erstelle den Reviewtext mit `write_file`, poste ihn mit `terminal`, und entferne `needs-review` nur bei Entscheidung `Implementierungsreif`.

## Quick Reference

- `OWNER_REPO=${OWNER_REPO:-$(git remote get-url origin | sed -E 's|.*github\.com[:/]||; s|\.git$||')}`
- `gh repo view "$OWNER_REPO" --json nameWithOwner,defaultBranchRef --jq '.nameWithOwner + " " + .defaultBranchRef.name'` (positional repo form; some installed `gh` versions do not support `gh repo view --repo`)
- `gh issue list --repo OWNER/REPO --state open --label "needs-review" --limit 1000 --json number,title,url --jq 'sort_by(.number)'`
- `gh issue view ISSUE --repo OWNER/REPO --json number,title,body,state,labels,comments,assignees,author,url,closedByPullRequestsReferences`
- `gh issue comment ISSUE --repo OWNER/REPO --body-file REVIEW.md`
- `gh issue edit ISSUE --repo OWNER/REPO --remove-label "needs-review"`
- `git status --short --branch`

## Procedure

1. **Kontext laden.** Nutze `skill_view` für `github-issues`, `uo-modernuo-workflow`, `uo-living-world-review` und `rebirthuo-modernuo-codebase`; lade weitere Domain-Skills, sobald das Ticket Systeme wie Housing, Loot, Combat, Crafting, Serialization, Timers, Gumps oder Tests berührt. Fertig, wenn alle risikobehafteten UO/ModernUO-Domains einen geladenen Skill oder eine begründete Ausnahme haben.

2. **Ticket bestimmen.** Wenn der User ein Issue oder eine URL nennt, verwende genau dieses Ticket. Wenn kein Ticket genannt ist, führe über `terminal` die Auswahl aus `How to Run` aus und nimm die niedrigste offene Issue-Nummer mit Label `needs-review`. Fertig, wenn `OWNER_REPO`, `ISSUE` und die Issue-URL eindeutig sind; bei leerem Ergebnis gibt es kein Review-Ticket.

3. **Ticket vollständig lesen.** Hole Titel, Body, Labels, State, Kommentare, Autor, URL, Assignees und verlinkte/closing PRs:

```bash
gh issue view "$ISSUE" --repo "$OWNER_REPO" --json number,title,body,state,labels,comments,assignees,author,url,closedByPullRequestsReferences
```

Fertig, wenn die Review-Notizen nicht nur auf dem Titel beruhen, sondern Body und Kommentare abdecken.

3a. **Doppelkommentar vermeiden.** Wenn bereits ein vollständiger `## Fachliches Review — #ISSUE`-Kommentar vorhanden ist und `updatedAt` nicht nach diesem Kommentar liegt, poste keinen zweiten identischen Review. Verifiziere stattdessen Label-Status, Kommentar-URL und stichprobenartig die wichtigsten Quellen/Repo-Anker; melde dem User `Kommentar-Status: bereits vorhanden` und lasse `needs-review` bei `Nicht implementierungsreif` unverändert. Wenn das Issue seit dem Review geändert wurde oder neue Kommentare danach stehen, erstelle einen aktualisierten Review-Kommentar.

4. **Quellen und Repo-Anker sammeln.** Nutze `browser_navigate`/`browser_snapshot` oder, falls verfügbar, `web_extract` für im Ticket genannte UO.com-, UOGuide-, Stratics- oder GitHub-Quellen. Nutze `search_files` und `read_file` im RebirthUO-Repo, um betroffene Klassen, Daten, Tests, Era-Gates und vorhandene Muster zu belegen. Bei Item-Property-Tickets prüfe zusätzlich lokale Client-Clilocs, wenn Tooltip-/Buff-/Property-Zeilen relevant sind; siehe `references/item-property-review-cliloc-and-battle-lust.md` für Cliloc-, Battle-Lust-, Bane- und Bestial/Berserk-Review-Muster sowie `references/casting-focus-item-property-review.md` für Casting-Focus-Unterbrechungsschutz, Inscription-Bonus und SA-Absorption-Container-Anker. Für gezielte lokale Cliloc-IDs nutze `scripts/extract-cliloc-ids.py` gegen den Client-`Cliloc.enu`/`Cliloc.deu`, statt Strings aus Erinnerung zu rekonstruieren. Wenn das Ticket ausdrücklich ein Custom-/Staff-/Testwerkzeug und kein OSI-Parity-Feature beschreibt, ist eine externe UO-Paritätsquelle nicht zwingend; markiere es dann als `Custom policy` und stütze Mechanik- und Risikoaussagen auf Issue-Text, geladene Domain-Skill-Referenzen und konkrete Repo-Anker. Prüfe bei wiederkehrenden Mechanikklassen zuerst die Support-Dateien der geladenen Domain-Skills (z. B. `uo-aos-item-properties/references/mechanics-test-dummy-mobile.md`), damit bekannte Review-Fallen nicht neu erarbeitet werden. Fertig, wenn jede fachliche Behauptung entweder eine Quelle, einen Repo-Anker, `Custom policy` oder den Marker `Quelle fehlt` hat.

5. **Implementierungsreife prüfen.** Entscheide `Implementierungsreif` nur, wenn alle Punkte erfüllt sind:
   - Problem und erwartetes Verhalten sind klar.
   - Era/Ruleset oder Custom-Policy ist geklärt.
   - Scope und Non-Goals sind erkennbar.
   - Quellen oder Issue-Belege tragen die Mechanik.
   - Repo-Anker zeigen, wo die Änderung sicher hingehört.
   - Ein minimaler Code-Änderungsplan ist möglich.
   - Akzeptanzkriterien sind beobachtbar.
   - Konkrete Test-/QA-Werte oder Szenarien sind ableitbar.
   - Risiken für PvP, PvM, Wirtschaft, Housing, Saves, Client, Performance und Exploits sind benannt oder plausibel `nicht betroffen`.

   Wenn ein Punkt fehlt, lautet die Entscheidung `Nicht implementierungsreif` und `needs-review` bleibt gesetzt.

6. **Deutschen Review-Kommentar schreiben.** Erstelle den Kommentar mit `write_file` als Markdown-Datei. Nutze diese Struktur:

```markdown
## Fachliches Review — #ISSUE

### Kurzfassung
- Entscheidung: Implementierungsreif / Nicht implementierungsreif
- Nächster Schritt: <Implementieren mit ... / fehlende Daten ergänzen>

### Ziel
- <Spieler-/Staff-/Operator-sichtbares Ziel>

### Quellen & Repo-Anker
- Issue: <URL>
- Quellen: <URLs oder Quelle fehlt>
- Repo: `<path:line-range>`

### Code-Änderungsplan
- <minimale Änderungspunkte oder warum kein sicherer Plan möglich ist>

### Erwartete Formel-/Testwerte
- <konkrete Werte, Tabellen, Szenarien oder fehlt>

### Akzeptanzkriterien
- [ ] <beobachtbares Kriterium>

### Testplan
- Fokus: `<command/filter oder Testidee>`
- Broad/Baseline: `<command oder Blocker>`
- Manuelle QA: <falls nötig>

### Risiken & Nebenwirkungen
- Era/Ruleset: <...>
- PvP/PvM: <...>
- Wirtschaft/Housing: <...>
- Saves/Client/Performance/Security: <...>

### Fehlende Voraussetzungen
- <nur ausfüllen, wenn nicht implementierungsreif>
```

Fertig, wenn der Kommentar fachlich nachvollziehbar ist und keine unbelegte UO-Mechanik als Fakt darstellt.

7. **Erkenntnisse zurückschreiben.** Poste den Kommentar über das `terminal`-Tool:

```bash
gh issue comment "$ISSUE" --repo "$OWNER_REPO" --body-file "$REVIEW_FILE"
```

Fertig, wenn GitHub die Kommentar-URL oder erfolgreiche Ausgabe zurückgibt. Falls das Posten fehlschlägt, Label nicht verändern.

8. **Label nur bei Implementierungsreife entfernen.** Wenn und nur wenn die Entscheidung `Implementierungsreif` lautet und der Kommentar erfolgreich gepostet wurde, entferne `needs-review`:

```bash
gh issue edit "$ISSUE" --repo "$OWNER_REPO" --remove-label "needs-review"
```

Bei `Nicht implementierungsreif` bleibt `needs-review` erhalten, damit das Ticket weiter sichtbar bleibt. Keine anderen Labels erfinden oder setzen, außer der User fordert es.

9. **Abschluss melden.** Teile dem User Issue-Nummer, URL, Entscheidung, Kommentar-Status und Label-Status mit. Wenn `needs-review` entfernt wurde, nenne den nächsten sinnvollen Skill für die Implementierung, meist `rebirthuo-implement`.

## Pitfalls

- `gh issue list` ohne explizites Sortieren ist nicht der gewünschte Modus; für "aufsteigend" immer nach `.number` sortieren.
- In Repos mit `upstream` kann `gh repo view` ohne `--repo` auf das falsche Repository zeigen. Für RebirthUO-Reviews `OWNER_REPO` aus `git remote get-url origin` ableiten oder das Issue-URL-Repo explizit setzen, und danach jedes `gh issue ...` mit `--repo "$OWNER_REPO"` ausführen.
- Wenn der User eine vollständige Issue-URL nennt, parse `OWNER_REPO` aus der URL und verwende genau dieses Repo. Verlasse dich dann nicht auf `gh repo view` im lokalen Checkout: RebirthUO-Worktrees können `origin`/Default-Repo auf `modernuo/ModernUO` zeigen, obwohl das Ticket in `RebirthUO/service` liegt.
- Bei kombinierten Bash+Python-Helfern auf Windows/MSYS keine `/tmp/...`-Dateien zwischen Shell und Python voraussetzen. Nutze besser ein natives `C:/Users/Jsiem/AppData/Local/Temp/...` oder gib JSON direkt an Python/stdout weiter, damit Review-Notizen nicht durch MSYS/Python-Pfadmapping verloren gehen.
- Beim Posten mit `gh issue comment --body-file` auf Windows/MSYS eine native Windows-Pfadform übergeben, weil `gh.exe` den Pfad außerhalb der MSYS-Pfadübersetzung auswerten kann. Sichere Form: `REVIEW_FILE_UNIX=$(cygpath -u 'C:\\Users\\Jsiem\\AppData\\Local\\Temp\\review.md')`, `REVIEW_FILE_WIN=$(cygpath -w "$REVIEW_FILE_UNIX")`, `gh issue comment "$ISSUE" --repo "$OWNER_REPO" --body-file "$REVIEW_FILE_WIN"`.
- `needs-review` ist ein Arbeitsqueue-Label. Entferne es nie bei fehlender Era/Ruleset-Entscheidung, fehlenden Quellen, unklarem Scope, fehlenden Testwerten oder ungelösten Sicherheits-/Exploit-Fragen.
- Dieses Review ist kein Code-Review eines PRs und keine Implementierung. Keine Branches, Commits oder PRs erzeugen.
- Ticket-Titel reichen nicht. Kommentare können die eigentliche Spezifikation, Korrekturen oder Blocker enthalten.
- Lokaler Code beweist nur RebirthUO-Ist-Zustand, nicht offizielle UO-Parität. Offizielle/Community-Mechanik separat belegen.
- Keine Exploitdetails öffentlich ausformulieren; bei Sicherheitsrisiko minimal kommentieren und interne Klärung verlangen.
- Focused Tests oder Testideen sind keine Broad-Suite-Freigabe. Im Review klar unterscheiden.
- Das Entfernen des Labels ist eine externe Nebenwirkung; erst nach erfolgreichem Kommentar und verifizierter Implementierungsreife ausführen.

## Verification

Nach Kommentar und optionaler Label-Änderung über das `terminal`-Tool prüfen:

```bash
gh issue view "$ISSUE" --repo "$OWNER_REPO" --json number,url,labels,comments --jq '{number,url,labels:[.labels[].name],lastComment:(.comments[-1].body // "")}'
```
