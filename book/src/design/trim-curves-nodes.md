# Option 2 — `trim` Nodes

Trim data moves to a dedicated `trim` node type, connected to the surface it trims. This is the graph-native descendant of RenderMan's `RiTrimCurve`, which was likewise separate from the patch — graphics state applied to subsequent `RiNuPatch` calls, reusable across patches.

A `trim` node carries **one or more complete loops** — the same payload as the inline design, with the `trim-curves.` prefix dropped since the node type provides the context (rule R4 of the [naming convention](../naming-convention.md)): `loop-count`, `curve-count`, `point-count`, `order`, `knot`, `min`, `max`, `position` / `position-weighted`, `hole`, `edge-id`, `edge-orientation`.

```
Create "face_12" "nurbs"
SetAttribute "face_12" ...surface attributes...

Create "face_12_outer" "trim"
SetAttribute "face_12_outer"
    "loop-count" "int" 1 [1]
    ...
Connect "face_12_outer" "" "face_12" "trim-curves"

Create "vent_hole_pattern" "trim"
SetAttribute "vent_hole_pattern"
    "loop-count" "int" 1 [64]
    "hole" "int" 64 [1 1 1 ...]
    ...
Connect "vent_hole_pattern" "" "face_12" "trim-curves"
```

`trim-curves` on the `nurbs` node becomes a multi-connection attribute (plural per rule R7). The surface's trim state is the union of the loops of all connected `trim` nodes.

## Ordering

Curves within a loop are ordered head-to-tail, and ɴꜱɪ connections are unordered — the usual objection to node-based trims. Two answers:

- **Whole-loop granularity dissolves the problem.** A loop is fully described inside one node, where array order is explicit. *Between* loops there is no meaningful order — the trimmed region is determined by the loops' geometry and `hole` flags, not by their sequence — so the unordered connection set is harmless. This is the recommended rule: a loop must not span nodes.
- If sub-loop granularity were ever wanted, the connection API stays stateless by supplying ordering as data: an `index` attribute on each node ranks its fragments. Listed for completeness; whole-loop granularity makes it unnecessary.

## Reuse

One `trim` node may be connected to any number of `nurbs` nodes whose parameter domains it fits — a bolt-hole pattern stamped across identical panel faces is defined once. Two caveats bound this benefit:

- Reuse requires identically parameterized faces; CAD faces usually have per-face domains.
- **Reuse conflicts with stitching.** `edge-id` names the edge of *one specific* face boundary; a node connected to two faces would claim the same edges on both, which is wrong. Rule: a `trim` node with any non-negative `edge-id` must have exactly one connection. Reusable trims are unstitched trims.

The natural-boundary `stitch.*` attributes remain on the `nurbs` node in any case.

## Pros

- Independent edits: replace or delete one hole group by swapping one small node — no resending the face's other loops. The natural granularity for live sessions.
- Reuse of repeated trim patterns across compatible faces.
- Follows the established precedent (`RiTrimCurve`) and ɴꜱɪ's general shape — shared, composable components as nodes.
- Attribute names get shorter (R4), and the `nurbs` namespace stays lean.
- Per implementer feedback, the extra API calls are noise next to render time, and memory cost is unchanged.

## Cons

- Exporters must invent and track a handle per trim group, and emit `Connect` calls — modest but real bookkeeping over Option 1.
- The face's trim state is assembled from several nodes: partially-connected intermediate states exist during editing, and debugging a face means chasing connections.
- Lifetime rules must be specified (recursive delete semantics when a surface or a shared trim node goes away).
- The stitching restriction above: the API's two features — reuse and welds — exclude each other per node, which is a rule users must learn.
