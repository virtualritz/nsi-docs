# Option 1: Inline Attributes

This option is the current draft. The [`nurbs`](../nodes/nurbs.md) page specifies it in full. The complete trim description lives on the surface node. The `trim-curves.*` attribute group holds the loop and curve counts, the orders, the knots, the ranges, the control points, and the `hole` flags. It also holds the integer edge identities `trim-curves.edge-id` and `trim-curves.edge-orientation`. The per-side `stitch.*` attributes hold the welds along natural boundaries.

```
Create "face_12" "nurbs"
SetAttribute "face_12"
    ...surface attributes...
    "trim-curves.loop-count" "int" 1 [2]
    "trim-curves.curve-count" "int" 2 [4 1]
    ...
```

## Rationale

A trim curve is data in one surface's parameter domain. It is meaningless anywhere else, so it has exactly one possible consumer. ɴsɪ makes something a node for one classic reason: one definition serves many consumers, as `transform`, `shader`, and `attributes` do. That reason is structurally absent here. Stitching must share only *edge identities*, and integers carry those well. Data on the node keeps the trimmed surface one atomic, self-contained object.

## Pros

- Simplest possible exporter: one `Create`, one attribute block, no handles to invent or track.
- The order is explicit -- array order *is* loop and curve order.
- Atomic updates: the all-or-nothing rule keeps a face's trim state consistent. No window exists where half the loops are connected.
- No cross-node lifetime questions. Nothing must define what happens to a trim node whose surface is deleted.
- It matches the one existing ɴsɪ implementation precedent, 3Delight's `trimcurves.*`.

## Cons

- Monolithic: an edit to one hole in a live session resends every loop on the face.
- No reuse: a hole pattern on a hundred identical faces travels a hundred times. Instancing at the object level covers the fully identical case.
- Welds are out-of-band integers. The scene graph does not show that two faces connect. Nothing prevents id collisions between unrelated exporters that feed one scene.
- The `nurbs` attribute namespace absorbs everything: fourteen `trim-curves.*` names, and more to come.
