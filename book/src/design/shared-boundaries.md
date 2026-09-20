# Shared Boundaries: Weld Declarations

> Proposal, revised after feedback from an experimental implementation. Names follow the [naming convention](../naming-convention.md).

The [implementation findings](#implementation-feedback-and-coverage) below explain the revised rules and their evidence limits. They do not establish that the implementation already supports this revision.

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

The exporter declares the relationship already known by the source application. It orders and directs the selected segments without resampling curves or changing the underlying geometry. Different knot vectors, segment counts, or parameter speeds do not change the identity.

The proposed correspondence contract below requires a common start and direction after selection and reversal. This strengthens the earlier draft, which allowed unrelated loop seams and left direction matching to the renderer.

### What the Exporter Guarantees

The exporter guarantees that counterpart uses trace the same undisplaced spatial path within the source model's geometric tolerance. Their lengths must also agree within the applicable tolerance. Equal length alone is insufficient: two unrelated curves can have equal lengths.

This agreement applies to the complete boundaries, not just their endpoints or control vertices. Comparisons concern the evaluated surface boundaries in a common coordinate system. For subdivision, this means the limit boundary, not the cage polyline. Animated declarations must remain valid over the rendered time interval.

No equality of vertex counts, segment counts, knot vectors, or parameter values is required. Five trim curves can meet seventeen mesh edges, or one boundary curve, under the same declaration. The exporter preserves known source topology; it need not generate a sample-to-sample correspondence table.

A numerical tolerance is a validity condition, not a search radius for discovering joins. Coincident boundaries with different IDs remain unrelated. The exact way to convey the source tolerance, if needed by a renderer, remains an open attribute-design decision. This draft does not invent a fixed epsilon or require a renderer to repair mismatched boundaries.

### Start, Direction, and Correspondence

For each weld ID, the exporter chooses one reference traversal of the undisplaced boundary. Every use follows that same traversal after its ranges, segment order, and `weld.reverse` values are applied. No reference-use handle or additional direction attribute is needed: agreement between the resulting traversals is the contract.

For an open boundary, all uses start at the same endpoint and finish at the same endpoint, within tolerance. For a closed boundary, all uses start at the same anchor and travel in the same direction, exactly once around. A use must not backtrack or traverse the boundary multiple times. Degenerate boundaries without a defined traversal are outside this contract.

The exporter expresses an opposite source traversal by reversing its selected segments and their order. For a single segment, only `weld.reverse = 1` is needed. Reversing a closed `trim-loop` reverses both curve order and curve traversal while retaining the loop's original start as the anchor.

Different closed-loop seams need an explicit selection adjustment. Segment order can rotate when the common anchor is already a segment endpoint. An anchor inside a curve can be expressed by two ranges of that curve: the tail first, then the head. This changes only the selection; it does not split the source geometry. A whole `trim-loop` selector is suitable when its stored start already matches the anchor.

For example, a periodic curve with the desired anchor at local parameter `0.25` can use ranges `[0.25, 1]` and `[0, 0.25]`. Both segments select the same curve index, in that order. Their joint traversal starts and ends at the desired anchor.

Opposite *face-boundary* traversals in an oriented manifold shell remain valid source topology. The weld traversal is a separate convention used for correspondence. Reversal does not change face orientation or which surface region is retained. Requiring every pair of uses to be anti-parallel would also fail for a weld with more than two uses.

A renderer must not infer a closed use's direction from its coincident endpoints. A circle's midpoint also cannot distinguish the two senses. The exporter supplies direction through the reference-traversal contract, rather than through a geometric direction test.

Common starts and directions do not imply common parameter speeds. For example, `A(t) = (t, 0, 0)` and `B(t) = ((t + t*t)/2, 0, 0)` traverse the same unit segment. At `t = 0.5`, their positions are `0.5` and `0.375`. Both declarations can be valid, but pairing samples by parameter or array index is invalid.

Consequently, a consumer can pair sample runs directly only after establishing corresponding sample locations. It still resolves correspondence and refinement when segmentation or parameterization differs. Equal normalized distance along a simple boundary is one possible correspondence convention; this draft does not require that algorithm.

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
- `weld.reverse`: one integer per segment; omitted means all zero. `1` reverses the selected segment. The resulting chain must follow the shared reference traversal.
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

A range selects a subinterval before reversal. Its endpoints satisfy `0 <= start < end <= 1`, normalized over the curve's active range or the edge's local domain. A `trim-loop` selector accepts only its full range. Partial loops use ordered `trim-curve` selectors instead.

The resulting *use* endpoints must coincide with the counterpart's endpoints in reference-traversal order. At a split between neighboring welds, the adjoining declarations must also select the same geometric junction. Internal segment breaks need no counterpart break when the other use has different granularity.

Local range numbers need not match across surfaces. For example, `[0, 0.5]` on `A(t)` above corresponds geometrically to `[0, (sqrt(5)-1)/2]` on `B(t)`. Both finish at position `0.5`. The exporter guarantees that geometric agreement; the renderer cannot assume equal range numbers or equal parameter increments.

The selected segments must form one connected chain on one effective boundary component of the retained surface. A closed-loop selector is a complete use and cannot be mixed with additional segments in that use. Empty uses, invalid indices, and disconnected chains are invalid declarations.

### Retained Region and Mixed Selectors

A weld belongs to the retained surface adjacent to the selected boundary. Trimming determines that region before the weld is considered. The declaration does not restore removed surface or infer which material exists from traversal direction.

With the draft's `trim-curves.hole = 1`, the use belongs to the surface outside that hole. With `hole = 0`, it belongs to the retained region inside the outer or island loop. Nested loops and domain clipping still determine the final retained region.

The documented legacy `trimcurves.inside = 0` similarly selects the retained region outside the loops; `inside = 1` selects the inside. A weld on such a loop therefore has a defined incident surface in either case. These opposite trim settings do not require opposite weld-reference directions. The `inside` and `hole` values have opposite meanings and are not interchangeable.

A selected portion must actually separate retained surface from removed surface or from the exterior of the active domain. A curve that does not bound the final retained region cannot declare a boundary use there. If only part survives trimming, the declaration selects only that part.

A `nurbs-side` selector is valid wherever that domain side bounds retained surface. This includes a patch whose only trim loop is an interior hole: its four outer sides remain boundaries. A trim curve need not duplicate those sides.

Mixed `nurbs-side` and `trim-curve` segments are permitted only when they are consecutive portions of one effective boundary component. Their endpoints must be adjacent in surface boundary topology, and the chain must follow that component without a jump or repeated portion. An open use need not close; a closed use must return to its start on the same component. Separate inner and outer loops cannot be concatenated merely because their 3D positions touch.

For example, clipping a trim region against the active domain can produce a boundary composed of trim arcs and domain-side portions. Such consecutive portions may form one use. If a trim curve coincides with a domain side, either selector may describe that portion, but the use must not include both copies.

A renderer that does not support mixed uses must report that limitation. It must not silently interpret them as separate complete uses or claim that the requested join was preserved.

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

This declares that trim loop 0 joins edge 2 of loop 0 on subdivision face 7. The example assumes the same closed locus, start, and traversal direction on both selectors. If one selector runs oppositely, its declaration also supplies `weld.reverse = 1`. An ordinary open edge cannot join an entire closed hole. If several subdivision edges form the matching ring, they form one use instead.

The five trim curves could also be listed explicitly. The following replaces the patch's three attributes above and selects the same chain:

```text
SetAttribute "patch"
    "weld.id" "int" 1 [12]
    "weld.segment-count" "int" 1 [5]
    "weld.kind" "string" 5 ["trim-curve" "trim-curve" "trim-curve" "trim-curve" "trim-curve"]
    "weld.index" "int[3]" 5 [0 0 0  1 0 0  2 0 0  3 0 0  4 0 0]
```

A chain of mesh edges uses the same count and concatenation mechanism. Mixed selectors follow the retained-boundary rules above. The renderer sees one use on each side regardless of segmentation.

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
- The paired orientation value becomes `weld.reverse`, aligning that selector with the shared reference traversal.
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

## Implementation Feedback and Coverage

The first implementer reported results from `nsi-intermediate` and `nsi-tessellate` in the [ɴsɪ repository](https://github.com/virtualritz/nsi). The former resolves declarations; the latter welds NURBS nodes. Reported fixtures include io1-ec-214 with 17 faces and 35 edges, and boxy with 80 faces and 124 edges. These measurements have not been independently reproduced for this documentation change.

| Reported finding | Consequence for this revision |
| ---------------- | ----------------------------- |
| Endpoint-only direction matching folded closed cylinder bands, producing areas 3.2 and 7.8 times the expected values. Quarter-point comparisons distinguished direction in the measured cases. | All uses must share a start and traversal direction after reversal. This removes the need to infer direction from endpoints. |
| Measured manifold uses had opposite source traversals and coincident starts. | Exporters align these traversals with `weld.reverse`. The shared traversal also supports more than two uses; it does not imply equal parameter speeds. |
| The implementation rejected outside-loop trims because the incident surface was unspecified. | A weld belongs to the retained region adjacent to its selected boundary. Hole and outside-loop settings are valid and do not change weld traversal. |
| Mixed side/trim uses were unsupported and did not occur in the measured exports. | Mixed selections must follow consecutive portions of one effective retained boundary component. Separate loops and duplicate portions remain invalid. |
| Of io1-ec-214's 70 segments, 48 were natural sides, including partial sides. Ranges worked where split points agreed. | Corresponding use endpoints and adjoining weld junctions must agree geometrically. Local range numbers need not match. |
| All uses across five STEP fixtures had one segment. Circular edges were single rational curves with doubled knots. | The default segment count stays one. Ordered chains remain available for differently segmented exports. |
| Twelve of io1-ec-214's 17 faces were cylinder bands with self-seams. Open declarations also served as useful diagnostics. | Two uses on the same geometry remain distinct uses of one weld. A lone use joins nothing and can help diagnose incomplete export. |

The report supplies no validation of mesh-edge selectors, multi-segment correspondence, or differing parameter speeds. Those capabilities remain part of the proposal, with implementation validation outstanding. Open declarations alone do not distinguish an intentional open boundary from missing export data.

The main remaining decisions are occurrence scope, tolerance transport, and the exact attribute encoding. One namespace contains many identities, and one use can contain many ordered segments. Displacement, tessellation, and geometric correspondence remain renderer decisions.
