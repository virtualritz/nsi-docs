# Option 1: Inline Attributes

This option is the current draft, and the shape the shipped [`nurbs`](../nodes/nurbs.md) node already has under its legacy names. The [draft design](nurbs-draft.md) specifies it in full. The complete trim description lives on the surface node. The `trim-curves.*` attribute group holds the loop and curve counts, the orders, the knots, the ranges, the control points, and the `hole` flags. Optional stitching shorthand uses `trim-curves.edge-id` and `trim-curves.edge-orientation`. The per-side `stitch.*` attributes select natural boundaries. These IDs belong to the connected `weld` namespace. The [general use table](shared-boundaries.md#concrete-encoding) is an alternative when a use contains several segments.

```
Create "face_12" "nurbs"
SetAttribute "face_12"
    ...surface attributes...
    "trim-curves.loop-count" "int" 1 [2]
    "trim-curves.curve-count" "int" 2 [4 1]
    ...
```

## Rationale

A trim curve is data in a surface's parameter domain. Keeping that data on the surface minimizes exporter bookkeeping. Shared identity belongs to the connected weld namespace, while local arrays identify the participating boundaries. This separates trim packaging from the welding declaration.

## Pros

- Simplest possible exporter: one `Create`, one attribute block, no handles to invent or track.
- The order is explicit -- array order *is* loop and curve order.
- Atomic updates: the all-or-nothing rule keeps a face's trim state consistent. No window exists where half the loops are connected.
- No additional trim-node lifetime rules; the optional weld connection follows the shared-boundary design.
- It matches the one existing ɴsɪ implementation precedent, 3Delight's `trimcurves.*`.

## Cons

- Monolithic: an edit to one hole in a live session resends every loop on the face.
- No reuse: a hole pattern on a hundred identical faces travels a hundred times. Instancing at the object level covers the fully identical case.
- Individual weld identities live in arrays. The graph shows their shared namespace, but inspecting a specific join also requires reading the IDs.
- The `nurbs` attribute namespace absorbs everything: fourteen `trim-curves.*` names, and more to come.
