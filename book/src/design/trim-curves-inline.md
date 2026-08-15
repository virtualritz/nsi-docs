# Option 1 — Inline Attributes

This is the current draft, specified in full on the [`nurbs`](../nodes/nurbs.md) page: the complete trim description lives on the surface node as the `trim-curves.*` attribute group — loop and curve counts, orders, knots, ranges, control points, `hole` flags — plus integer edge identities (`trim-curves.edge-id`, `trim-curves.edge-orientation`) and the per-side `stitch.*` attributes for welds along natural boundaries.

```
Create "face_12" "nurbs"
SetAttribute "face_12"
    ...surface attributes...
    "trim-curves.loop-count" "int" 1 [2]
    "trim-curves.curve-count" "int" 2 [4 1]
    ...
```

## Rationale

A trim curve is data in one surface's parameter domain — it is meaningless anywhere else, so it has exactly one possible consumer. The classic reason ɴꜱɪ makes something a node (one definition, many consumers: `transform`, `shader`, `attributes`) is structurally absent, and the things stitching needs to share are *edge identities*, which travel fine as integers. Keeping the data on the node makes the trimmed surface one atomic, self-contained thing.

## Pros

- Simplest possible exporter: one `Create`, one attribute block, no handles to invent or track.
- Ordering is trivially explicit — array order *is* loop and curve order.
- Atomic updates: the all-or-nothing rule means a face's trim state is always consistent; no window where half the loops are connected.
- No cross-node lifetime questions (what happens to a trim node whose surface is deleted, and vice versa).
- Matches the one existing implementation precedent for ɴꜱɪ (3Delight's `trimcurves.*`).

## Cons

- Monolithic: editing one hole in a live session resends every loop on the face.
- No reuse: a hole pattern repeated on a hundred identical faces is transmitted a hundred times (though instancing at the object level covers the fully identical case).
- Welds are out-of-band integers — the scene graph does not show that two faces are connected, and nothing prevents id collisions between unrelated exporters feeding one scene.
- The `nurbs` attribute namespace absorbs everything (fourteen `trim-curves.*` names and counting).
