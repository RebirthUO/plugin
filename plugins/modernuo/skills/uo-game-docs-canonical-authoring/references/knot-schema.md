# Canonical Game-Docs Tree and Knot Schema

Use this reference while creating or auditing `01_Broadsword` nodes.

## Tree Shape

```text
game-docs/GameDocs/01_Broadsword/<Domain>/<Era>/
├── README.md
├── <topic-a>/
│   ├── README.md
│   ├── <mechanic-a>.md
│   └── <mechanic-b>.md
└── <topic-b>/
    ├── README.md
    └── <mechanic-c>.md
```

The domain/era README indexes topic folders. Each topic README indexes its mechanic nodes with relative links and the most useful short comparison fields. Order mechanics by their natural progression, such as skill gate or feature flow.

Independent hooks get independent nodes even when they belong to a larger skill. Examples include item, pet, special-move, weapon-parry, equipment, or talisman hooks.

## Knot Schema

Every mechanic node contains:

1. **Kopfblock / identity** — topic/skill, mechanic type, era/publish, costs or gates, and canonical source URL.
2. **Summary** — one or two precise paraphrased sentences.
3. **Prerequisites** — skill gates, companion skills, trainer/acquisition anchors, books/items, and region/facet restrictions.
4. **Mechanik / behavior** — formulas, caps, duration, reset, PvP diminishing returns/caps, exceptions, and cross-skill hooks. Use `Needs source confirmation` for unresolved values.
5. **PvP / PvM / Economy** — player counterplay, sustain/burst/group effects, faucets/sinks/tradeability, and housing/new-player/veteran effects when material.
6. **Repo-Anker / repository anchors** — comparison paths and lines in current source. Explain whether the anchor matches, diverges, or only locates the surface.
7. **Sources** — official primary URLs first; discovery sources are separately labeled and never fill an official gameplay claim.

## Index Layers

- `00_Index/README.md` links every domain and era tree. Re-read immediately before editing.
- `01_Broadsword/<Domain>/<Era>/README.md` is the canonical domain/era entry point.
- `01_Broadsword/<Domain>/<Era>/<topic>/README.md` lists every mechanic node.
- `01_Broadsword/Systems/<Era>.md` is the era umbrella and should cross-link relevant domain trees.
- `02_Project_Parity/<Domain>/<Era>/<topic>.md` mirrors implementation status and links back to canonical nodes; it must not redefine canonical behavior.

## Audit Checklist

- Inventory count matches node count plus intentional exclusions.
- Every README link and node cross-link resolves.
- Every node has all seven sections.
- Claims are paraphrased and sourced; no unsupported exact value is presented as fact.
- Repository anchors use current paths and are explicitly comparison evidence.
- Canonical files contain no triage state such as `Triage required` or `Human Review`.
