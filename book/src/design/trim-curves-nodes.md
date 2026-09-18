# Option 2: `trim` Nodes

Trim data moves to a dedicated `trim` node type, connected to the surface it trims. This node type is the graph-native descendant of RenderMan's `RiTrimCurve`. That entity was also separate from the patch: it set graphics state for the `RiNuPatch` calls that followed, and it was reusable across patches.

A `trim` node carries **one or more complete loops**. The payload is the same as in the inline design, but the `trim-curves.` prefix drops away, because the node type supplies the context. Rule R4 of the [naming convention](../naming-convention.md) requires this. The trim attributes are `loop-count`, `curve-count`, `point-count`, `order`, `knot`, `min`, `max`, `position`/`position-weighted`, and `hole`. Optional `edge-id` and `edge-orientation` arrays encode one-segment weld uses. A general `weld.*` table can instead select whole loops or segment chains, as described in the [shared-boundary design](shared-boundaries.md). The two weld encodings are alternatives.

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

`trim-curves` on the `nurbs` node becomes a multi-connection attribute, plural per rule R7. The surface's trim state is the union of the loops of all connected `trim` nodes.

## Ordering

A loop orders its curves head-to-tail, but ɴsɪ connections have no order. This mismatch is the usual objection to node-based trims. There are two answers:

- **Whole-loop granularity dissolves the problem.** One node describes a loop in full, and array order inside that node is explicit. *Between* loops no meaningful order exists: the geometry of the loops and the `hole` flags determine the trimmed region, not the sequence of the loops. The unordered connection set is therefore harmless. This rule is the recommended one: a loop must not span nodes.
- Sub-loop granularity, if anyone ever wants it, keeps the connection API stateless by supplying the order as data. An `index` attribute on each node ranks its fragments. This answer is listed for completeness. Whole-loop granularity makes it unnecessary.

## Reuse

One `trim` node may connect to any number of `nurbs` nodes whose parameter domains it fits. A bolt-hole pattern stamped across identical panel faces is then defined once. Two caveats bound this benefit:

- Reuse needs identically parameterized faces. CAD faces usually have per-face domains.
- **Weld declarations are local uses.** A trim node carrying a weld table or a non-negative `edge-id` has exactly one consuming surface in this proposal. Its IDs belong to that surface's connected weld namespace. Reusable trim nodes carry no weld declarations.

The natural-boundary `stitch.*` attributes stay on the `nurbs` node in any case.

## Pros

- Independent edits: a swap of one small node replaces or deletes one hole group. The face's other loops stay put. This granularity is the natural one for live sessions.
- Reuse of repeated trim patterns across compatible faces.
- It follows the established precedent, `RiTrimCurve`, and the general shape of ɴsɪ: shared, composable components are nodes.
- Attribute names get shorter (R4), and the `nurbs` namespace stays lean.
- A loop group can be updated without replacing unrelated trim data.

## Cons

- Exporters must invent and track a handle per trim group, and emit `Connect` calls. This bookkeeping is modest but real, next to Option 1.
- Several nodes assemble the face's trim state. Partially-connected intermediate states exist during editing, and a face is debugged by chasing its connections.
- Lifetime rules need a specification: recursive delete semantics, for when a surface or a shared trim node goes away.
- The stitching restriction above. Reuse and welds exclude each other per node, and users must learn that rule.
