## Konkretisierter Implementierungsplan

### Kurzfassung
<Einordnung: Test-Gap, Quellen-Gap, Code-Gap, Runtime-Proof, Doc/Ledger-Gap, Not-Planned-Kandidat. Kurz sagen, ob bestehender Code wahrscheinlich reicht oder ob echte Implementierung noetig ist.>

### Ziel
<SE-/ML-/SA-/... Atom gilt als erledigt, wenn:>

- <konkretes Done-Kriterium 1>
- <konkretes Done-Kriterium 2>
- <konkretes Done-Kriterium 3>

### Quellen
- <official/canonical/issue-supplied source>: <exakte Aussage, die diese Quelle belegt>
- <official/canonical/issue-supplied source>: <exakte Aussage, die diese Quelle belegt>

### Relevante Repo-Anker
- `<path/to/file.cs>`
  - <Klasse/Methode/System und warum es die Implementierungsstelle ist.>
- `<path/to/test.cs>`
  - <Warum dies der richtige Test-Slice ist.>
- `<path/to/doc-or-data>`
  - <Nur wenn vorhanden; wenn im Zielbranch fehlend, explizit als conditional behandeln.>

### Code-Change-Plan
1. <Kleinster erster Schritt, z.B. deterministischen Helper extrahieren / Testdatenzeile anlegen / Source-Reference-Konstante ergaenzen.>
2. <Gezielte Tests mit exakten Testnamen oder Testklasse.>
3. <Falls Test rot wird: kleinste Abweichung in Datei/Methode X korrigieren.>
4. <Ledger/Doku nur aktualisieren, wenn Datei im Branch existiert; sonst PR/Issue-Body als Resolution Record nutzen.>

### Erwartete Testwerte / Formelhinweise
- <Formel/Konstante/Mapping 1, inklusive Prozent-vs-Bruchteil-Konvertierung falls relevant.>
- <Formel/Konstante/Mapping 2.>
- <Helper-/Testnamen-Vorschlag.>

### Akzeptanzkriterien
- <Quelle-backed observable condition.>
- <Repo/test condition.>
- <Keine unerwuenschte Nebenwirkung / Nicht-Ziel.>

### Testplan
```powershell
dotnet test Projects\\UOContent.Tests\\UOContent.Tests.csproj --filter "FullyQualifiedName~<FocusedTestClassOrNamespace>"
```

Optional breiter:

```powershell
dotnet build
dotnet test Projects\\UOContent.Tests\\UOContent.Tests.csproj --filter "FullyQualifiedName~<DomainOrEra>"
```

### Risiken / Hinweise fuer den Implementierer
- <Hot-path / Allocation / LINQ / ModernUO-Code-Audit Hinweis.>
- <Era/Profile/PvP/PvM/Economy/Save/Client Risiko.>
- <Dirty checkout / target branch / missing ledger caveat.>
- <Explizite Nicht-Ziele: kein breiter Refactor, keine Era-Policy-Aenderung ohne separates Ticket.>
