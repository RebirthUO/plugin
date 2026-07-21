# Screenshot Composition

## Inventory protocol

Treat the supplied image as one observation. Use its visible top-left corner as
`(0,0)` and record approximate integer bounds as `x,y,width,height`; use
`unknown` when cropping or scaling prevents a defensible estimate. Inventoried
components must use stable `C01`, `C02`, and so on identifiers.

| Field | Record |
|---|---|
| `role` | frame, decoration, text, data, image, input, control, navigation, or feedback |
| `bounds` | approximate screenshot-relative rectangle or `unknown` |
| `parent` / `z_order` | containment and visual layer |
| `state` | observed, proposed, or unresolved |
| `interaction` | none, close, submit, select, page, target, or verified local behavior |
| `asset_status` | observed-only, resolved, candidate, or unresolved |
| `source` | screenshot, user requirement, repository, client, ultima-mcp, official, or test |

Separate a repeated decorative tile from every independently actionable control.
When text is unreadable, record its role and bounds, not a guessed label. A
crop, scaling, translucency, or occlusion is a limitation, not permission to
invent a component.

## Ultima MCP lookup

Only query a tool that is both present in the active catalog and explicitly
described as providing Ultima Online data. Ask a narrow question tied to a
component role or visible candidate, such as a gump art, localized text, or
cliloc. Record the exact query, result locator, and whether the result is a
candidate or verified local use. No tool, access failure, no result, or
ambiguous result leaves `asset_status: unresolved`; continue with semantic
roles and a visual plan.

An MCP or client result is implementation/discovery evidence. It cannot prove
official gameplay behavior; keep such claims in their own official-evidence
record.

## Wireframe contract

Use a proportional `text` block with a clear viewport and component IDs. Draw
containment with borders, align columns/rows visibly, and use arrows for every
interactive component's response target. Put a short legend below the drawing:
`[O]` observed, `[P]` proposed, and `[U]` unresolved asset. Never draw a
button, input, or page control without a matching component record.

Example shape (labels and geometry must come from the task):

```text
Viewport 420x300
+--------------------------------------------------+  C01 [O] frame
| Title [C02 O]                                    |
| +---------------- list C03 [O] ----------------+ |
| | row C04 [O]       row C05 [P]                | |
| +------------------------------------------------+ |
| [C06 P: Cancel] -> close(0)  [C07 P: Apply] -> apply |
+--------------------------------------------------+
Legend: [O] observed; [P] proposed; [U] unresolved asset
```

The example is a reference template, not a source of dimensions, controls, or
asset IDs.
