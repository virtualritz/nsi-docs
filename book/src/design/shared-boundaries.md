# Shared Boundaries: Weld Declarations

> Proposal, not implemented. This page unifies the NURBS stitching and weld-node alternatives. Names follow the [naming convention](../naming-convention.md).

How can an exporter preserve joined boundaries with little bookkeeping, even when the two sides have different representations?

The declaration means: *these selected boundaries belong together and must stay joined when rendered*. Spatial coincidence alone does not declare a join. The renderer decides how to preserve the join through tessellation and displacement. This proposal specifies no welding algorithm or displacement policy.

## Recommendation: One Scope, Many Welds

A `weld` node supplies an identity namespace. It can describe all joins in a solid through the boundary declarations on its connected geometry. It carries no curves and needs no attributes of its own.

```text
solid_welds --> face_a.weld
            --> face_b.weld
            --> subdivision_mesh.weld
```

Each geometry node accepts one `weld` connection. Its local attributes select boundaries and assign integer IDs. Two boundary uses with the same ID and the same connected `weld` node belong together. ID `12` in another weld node is unrelated.

The effective identity is `(weld node, ID)`. Membership in the node alone does not weld every boundary together. A solid with 10,000 shared boundaries can use one extra node, not 10,000 nodes. The exporter assigns IDs from source topology and writes arrays on the geometry it already exports.

The earlier proposal used one `weld` per shared edge and one `weld-use` per occurrence. That remains an alternative below. The recommendation here changes the granularity: one namespace node, with boundary uses stored as data.

## A Boundary Use Can Contain Several Segments

A *boundary use* is one connected, ordered chain on one surface. It can be open or closed. The two uses of a weld need not contain the same number or type of segments.

For example, one use can contain five NURBS trim curves. The other can select one subdivision boundary edge whose limit boundary follows the same locus. These are two uses of one weld, not six competing definitions of an edge.

The exporter declares the relationship already known by the source application. It does not resample curves, split matching geometry, or construct parameter maps for the renderer. Direction describes traversal only. Different knot vectors, segment counts, or parameter speeds do not change the identity.

For a closed chain, a different starting point does not create a different boundary. The renderer resolves geometric correspondence. A declaration does not require matching loop seams.

### What the Exporter Guarantees

The exporter guarantees that counterpart uses trace the same undisplaced spatial path within the source model's geometric tolerance. Their lengths must also agree within the applicable tolerance. Equal length alone is insufficient: two unrelated curves can have equal lengths.

This agreement applies to the complete boundaries, not just their endpoints or control vertices. Comparisons concern the evaluated surface boundaries in a common coordinate system. For subdivision, this means the limit boundary, not the cage polyline. Animated declarations must remain valid over the rendered time interval.

No equality of vertex counts, segment counts, knot vectors, or parameter values is required. Five trim curves can meet seventeen mesh edges, or one boundary curve, under the same declaration. The exporter preserves known source topology; it need not generate a sample-to-sample correspondence table.

A numerical tolerance is a validity condition, not a search radius for discovering joins. Coincident boundaries with different IDs remain unrelated. The exact way to convey the source tolerance, if needed by a renderer, remains an open attribute-design decision. This draft does not invent a fixed epsilon or require a renderer to repair mismatched boundaries.

### A Five-Curve Hole

The existing [NURBS trim model](nurbs-draft.md#trim-curves) already supports multiple curves in one loop:

```text
trim-curves.loop-count = 1
trim-curves.curve-count = [5]
trim-curves.hole = [1]
```

The five curves connect head-to-tail. The last curve ends at the start of the first curve. Their individual orders, knots, ranges, and control points remain separate. The hole flag applies to the whole loop.

There are two different topological declarations an exporter might need:

- Each curve meets a different neighboring face: assign five different weld IDs, one to each boundary use.
- The entire loop meets one boundary on another surface: select the loop as one use and assign one weld ID.

Trim segmentation therefore does not determine weld granularity.

## Concrete Encoding

The following is a proposed data layout, not a shipped API. It uses ordinary attributes and connections. No new C API function or connection parameter is needed.

Each geometry node carries a local boundary-use table:

- `weld.id`: one non-negative integer per use.
- `weld.segment-count`: segment count per use; omitted means one segment per use.
- `weld.kind`: one string per segment.
- `weld.index`: one _`int[3]`_ tuple per segment.
- `weld.reverse`: one integer per segment; omitted means all zero. `1` reverses the selected segment.
- `weld.range`: one _`float[2]`_ tuple per segment; omitted means the full selected segment.

Segments are concatenated in use order. Counts partition those arrays; their sum equals the segment-array length. Each segment belongs to exactly one use. IDs belong to uses, not to segments.

The index tuple has a fixed width so exporters can build one table without node handles for every segment. Unused components are zero. All indices are zero-based.

| `weld.kind` | `weld.index` | Selected boundary |
| ----------- | ------------ | ----------------- |
| `trim-loop` | `[loop, 0, 0]` | Complete loop, in its stored curve order |
| `trim-curve` | `[curve, 0, 0]` | One curve in the flattened trim-curve arrays |
| `nurbs-side` | `[side, 0, 0]` | Active-domain side: 0 = u-min, 1 = u-max, 2 = v-min, 3 = v-max |
| `mesh-edge` | `[face, loop, edge]` | Directed local edge occurrence in a polygon or subdivision control mesh |

For meshes, loop 0 is the outer perimeter; later loops are polygon holes. The edge runs from a local vertex to the next vertex in that loop, with wraparound. For subdivision, the selection denotes the associated limit-surface boundary, not the straight control-cage segment. Each supported subdivision scheme must define that association. The same declaration applies to the draft `t-nurcc` control topology.

A natural side follows increasing `v` for a u-side and increasing `u` for a v-side. A trim curve follows its stored parameter range. Reversal applies after selection.

A range selects a subinterval before reversal. Its endpoints lie in `[0, 1]`, normalized over the selected curve's active range or the selected edge's local domain. This normalization selects a local portion; it does not assert equal parameter values across surfaces. A `trim-loop` selector accepts only its full range. Partial loops use ordered `trim-curve` selectors instead.

The selected segments must form one connected chain. A closed-loop selector is a complete use and cannot be mixed with additional segments in that use. Empty uses, invalid indices, and disconnected chains are invalid declarations.

### The Five-to-One Join

Suppose `patch` already has the five-curve hole above. Suppose `subdiv` has a boundary edge that describes the same closed locus. This illustrative stream fragment contains the entire additional declaration:

```text
Create "solid_welds" "weld"
Connect "solid_welds" "" "patch" "weld"
Connect "solid_welds" "" "subdiv" "weld"

SetAttribute "patch"
    "weld.id" "int" 1 [12]
    "weld.kind" "string" 1 ["trim-loop"]
    "weld.index" "int[3]" 1 [0 0 0]

SetAttribute "subdiv"
    "weld.id" "int" 1 [12]
    "weld.kind" "string" 1 ["mesh-edge"]
    "weld.index" "int[3]" 1 [7 0 2]
```

This declares that trim loop 0 joins edge 2 of loop 0 on subdivision face 7. The example assumes that the selected subdivision boundary really is the same closed locus. An ordinary open edge cannot join an entire closed hole. If several subdivision edges form the matching ring, they form one use instead.

The five trim curves could also be listed explicitly. The following replaces the patch's three attributes above and selects the same chain:

```text
SetAttribute "patch"
    "weld.id" "int" 1 [12]
    "weld.segment-count" "int" 1 [5]
    "weld.kind" "string" 5 ["trim-curve" "trim-curve" "trim-curve" "trim-curve" "trim-curve"]
    "weld.index" "int[3]" 5 [0 0 0  1 0 0  2 0 0  3 0 0  4 0 0]
```

A chain of mesh edges uses the same count and concatenation mechanism. Mixed segment kinds can describe a boundary that follows both a natural patch side and trim curves. The renderer sees one use on each side regardless of segmentation.

### Several Independent Joins

The same patch can declare another boundary without another node:

```text
SetAttribute "patch"
    "weld.id" "int" 2 [12 13]
    "weld.kind" "string" 2 ["trim-loop" "nurbs-side"]
    "weld.index" "int[3]" 2 [0 0 0  1 0 0]
```

Loop 0 belongs to weld 12. The u-max side belongs to weld 13. Another surface declares ID 13 in the same namespace to complete that join. These two IDs remain independent.

Two uses on the same geometry can have the same ID, which expresses a self-seam. More than two uses can share an ID, which expresses a non-manifold join. A use without a counterpart is an open declaration; it joins nothing by itself.

## Relation to the Original Stitching Arrays

The [NURBS stitching attributes](nurbs-draft.md#stitching) remain a compact shorthand for one-segment uses. They use the same `weld` connection and ID namespace:

- Each non-negative `trim-curves.edge-id` entry selects its corresponding trim curve as one complete use.
- Each non-negative `stitch.edge-id` entry selects its corresponding natural side as one complete use.
- The paired orientation value supplies that use's direction.
- `-1` means no use is declared for that entry.

These arrays need no separate matching rules. They lower to the boundary-use table described above. A surface supplies either these shorthand arrays or the general table, never both. An exporter can use the general table everywhere to avoid maintaining two encodings.

Assigning one shorthand ID to five consecutive curves would declare five complete uses of the same boundary. It would not make one five-segment use. A `trim-loop` selector or explicit segment count expresses that grouping.

With [separate trim nodes](trim-curves-nodes.md), a general table can reside on each trim node. Its trim indices refer to that node's arrays. It obtains the weld namespace through its single consuming surface; natural sides stay on the surface. A trim node carrying weld declarations has one consuming surface, to keep its use unambiguous. Trim packaging does not otherwise change the identity model.

## Alternatives and Trade-offs

For `E` shared boundaries and `U` uses, these counts exclude existing geometry and trim nodes:

| Encoding | Extra nodes | Benefit | Cost |
| -------- | ----------- | ------- | ---- |
| Original scene-global IDs | 0 | Small arrays; direct mapping from source IDs | Exporters must coordinate global IDs; no explicit scope connection |
| One `weld` namespace plus local use tables | 1 per namespace | Batches all joins; supports chains; IDs stay local; recommended | Exporter maintains arrays; one namespace per geometry node |
| One `weld` per boundary plus explicit `weld-use` nodes | `E + U` | Independent graph edits; each use has an explicit handle | More nodes, handles, connections, and lifetime bookkeeping |
| One `weld` per boundary with direct geometry connections | `E` | Fewer nodes than explicit uses | Still needs selectors and grouping on connections or attribute slots |

For 10,000 boundaries with two uses each, the explicit-use approach adds 30,000 nodes. The recommended encoding adds one namespace node for that solid. Both still describe 20,000 uses; batching removes node overhead, not the topology data. No render-time performance claim follows from these counts.

A [shared 3D edge curve](trim-curves-edges.md) is an independent extension. It could accompany either identity encoding. It is not required to preserve belonging, and it does not select the local boundaries by itself.

## Scope, Edits, and Remaining Decisions

One geometry node participates in one weld namespace in this recommendation. A mesh containing several solids can use one namespace with distinct IDs. This avoids splitting geometry solely to allocate scopes. Combining independently authored namespaces needs ID remapping, just as combining indexed geometry needs index remapping.

Node handles identify definitions; rendered occurrences need an additional scope rule. Repeating an assembly must repeat its internal joins without welding separate instances together. The exact attachment of that assembly scope remains an implementation discussion. Ambiguous instances must not silently weld to every occurrence of a connected geometry node.

Topology edits that change indices must update the use tables. A table's arrays form one coherent declaration at a render synchronization point. Removing the `weld` connection removes its membership; the remaining IDs do not become scene-global. A renderer that ignores these declarations cannot claim to preserve the requested joins.

The main remaining decisions are occurrence scope and the exact attribute encoding. The structural requirement illustrated by the examples is: one namespace contains many identities, and one use can contain many ordered segments. Displacement, tessellation, and geometric correspondence remain renderer decisions.
