# Shared Boundaries: Weld Declarations

> Proposal, revised after feedback from an experimental implementation. Names follow the [naming convention](../naming-convention.md).

The [implementation findings](#implementation-feedback-and-coverage) explain why the rules changed. They also show which cases still need tests. The implementation may not yet support the revised rules.

How can an exporter describe a join when the two surfaces represent their boundaries differently?

The declaration means: *these selected boundaries belong together and must stay joined when rendered*. Two boundaries at the same position do not necessarily belong together. The renderer decides how to preserve the join through tessellation and displacement. This proposal specifies no welding algorithm or displacement policy.

## Recommendation: One Scope, Many Welds

A `weld` node defines a set of local IDs, called a *namespace*. The exporter chooses an integer ID for each join. One node can provide the IDs for all joins in a solid. The connected geometry carries the boundary data. The `weld` node carries no curves and needs no attributes of its own.

```text
solid_welds --> face_a.weld
            --> face_b.weld
            --> subdivision_mesh.weld
```

Each geometry node accepts one `weld` connection. Its local attributes select boundaries and assign integer IDs. Two selected boundary chains belong together when they share an ID and connect to the same `weld` node. The same integer ID in a different `weld` node identifies an unrelated boundary.

The pair `(weld node, ID)` identifies a join. A connection to the node alone does not join every boundary. A solid with 10,000 shared boundaries can use one extra node, not 10,000 nodes. The exporter assigns IDs from source topology and writes arrays on the geometry it already exports.

An alternative uses one `weld` node per shared boundary and one `weld-use` node per use. The [comparison below](#alternatives-and-trade-offs) describes its costs. The recommended design stores the uses in arrays and needs only one namespace node.

## A Boundary Use Can Contain Several Segments

A *boundary use* is one connected, ordered chain on one surface. It can be open or closed. The two uses of a weld need not contain the same number or type of segments.

For example, one use can contain five NURBS trim curves. The other can select one subdivision edge whose limit boundary follows the same path. Together, these chains form two uses of one weld.

The exporter preserves the relationship from the source application. It selects each segment and sets its order and direction. It does not need to resample curves or change the geometry. Different knot vectors, segment counts, or parameter speeds do not change the identity.

The rules below require a common start and direction after selection and reversal. The earlier draft left those choices to the renderer.

### What the Exporter Guarantees

The exporter guarantees that matching uses follow the same path before displacement, within the source model's geometric tolerance. Their lengths must also agree within the applicable tolerance. Equal length alone is not enough: unrelated curves can have equal lengths.

This agreement applies to the complete boundaries, not just their endpoints or control vertices. The comparison uses evaluated surface boundaries in a common coordinate system. For subdivision, the comparison uses the limit boundary, not the control-cage edges. For animation, the declaration must remain valid throughout the rendered time interval.

Matching uses can have different vertex counts, segment counts, knot vectors, and parameter values. Five trim curves can meet seventeen mesh edges, or one boundary curve, under the same declaration. The exporter preserves known source topology. It does not need to supply a table that pairs samples across the join.

The tolerance limits the permitted difference between declared boundaries. It does not tell the renderer to find other nearby boundaries. Boundaries with different IDs remain unrelated, even when they coincide. How to supply the source tolerance remains an open design question. This draft sets no fixed tolerance and does not require the renderer to repair mismatched boundaries.

### Start, Direction, and Correspondence

For each weld ID, the exporter chooses a start point and direction along the boundary before displacement. Together, these define the *reference traversal*. Each use must follow that traversal after the renderer applies its ranges, segment order, and `weld.reverse` values. This rule needs no reference-use handle or additional direction attribute.

For an open boundary, all uses start at the same endpoint and finish at the same endpoint, within tolerance. For a closed boundary, all uses start at the same anchor and travel in the same direction, exactly once around. A use must not backtrack or traverse the boundary multiple times. These rules do not cover degenerate boundaries with no defined traversal.

If the source chain runs in the opposite direction, the exporter reverses each selected segment and the segment order. For a single segment, only `weld.reverse = 1` is needed. For a closed `trim-loop`, reversal changes both curve order and curve direction. The loop keeps its original start point.

Closed loops with different start points need different selections. If the common start is a segment endpoint, the exporter can rotate the segment order. If the common start lies inside a curve, the exporter can select two ranges: the tail, then the head. This selection does not split the source geometry. A whole `trim-loop` selector works when its stored start already matches the common start.

For example, suppose a periodic curve needs to start at local parameter `0.25`. The use selects ranges `[0.25, 1]` and `[0, 0.25]`. Both segments select the same curve index, in that order. Together, the two ranges start and end at the required point.

In an oriented manifold shell, the two face boundaries can run in opposite directions. The weld traversal provides a separate direction for matching their positions. Reversal does not change face orientation or which surface region is retained. A weld with more than two uses cannot make every pair run in opposite directions.

A renderer must not infer a closed use's direction from its coincident endpoints. A circle's midpoint also cannot distinguish the two directions. The exporter supplies the direction through the reference traversal.

Common starts and directions do not imply common parameter speeds. For example, consider these two curves over `0 <= t <= 1`:

```text
A(t) = (t, 0, 0)
B(t) = ((t + t*t)/2, 0, 0)
```

Both curves follow the same unit segment. At `t = 0.5`, their positions are `0.5` and `0.375`. Both uses can be valid. A renderer cannot assume that equal parameters or array indices identify matching positions.

The renderer can pair sample runs directly only when their sample locations match. It must handle differences in segment counts and parameter speeds. Equal fractions of the total boundary length can provide one way to match positions on a simple boundary. This draft does not require that algorithm.

### A Five-Curve Hole

The existing [NURBS trim model](nurbs-draft.md#trim-curves) already supports multiple curves in one loop:

```text
trim-curves.loop-count = 1
trim-curves.curve-count = [5]
trim-curves.hole = [1]
```

The five curves connect head-to-tail. The last curve ends at the start of the first curve. Their individual orders, knots, ranges, and control points remain separate. The hole flag applies to the whole loop.

An exporter might need either of these declarations:

- Each curve meets a different neighboring face: assign five different weld IDs, one to each boundary use.
- The entire loop meets one boundary on another surface: select the loop as one use and assign one weld ID.

The number of trim curves does not determine the number of welds.

## Concrete Encoding

The following is a proposed data layout, not a shipped API. It uses ordinary attributes and connections. No new C API function or connection parameter is needed.

Each geometry node carries a local boundary-use table:

- `weld.id`: one non-negative integer per use.
- `weld.segment-count`: segment count per use; omitted means one segment per use.
- `weld.kind`: one string per segment.
- `weld.index`: one _`int[3]`_ tuple per segment.
- `weld.reverse`: one integer per segment; omitted means all zero. `1` reverses the selected segment. The resulting chain must follow the shared reference traversal.
- `weld.range`: one _`float[2]`_ tuple per segment; omitted means the full selected segment.

The segment arrays list each use's segments in order. The counts mark where each use ends. Their sum equals the number of entries in each segment array. Each segment belongs to exactly one use. IDs belong to uses, not to segments.

Each `weld.index` entry contains three integers. For `mesh-edge`, they mean `[face, perimeter, edge]`. The first two locate a vertex list; the third selects one edge in that list. All indices start at zero.

The other selector types need only the first integer. Their remaining two integers are unused and must be zero. This proposed fixed-width layout lets every selector use the same array format. It is not a requirement of the ɴsɪ API.

| `weld.kind` | `weld.index` | Selected boundary |
| ----------- | ------------ | ----------------- |
| `trim-loop` | `[loop, 0, 0]` | Complete loop, in its stored curve order |
| `trim-curve` | `[curve, 0, 0]` | One curve in the flattened trim-curve arrays |
| `nurbs-side` | `[side, 0, 0]` | Active-domain side: 0 = u-min, 1 = u-max, 2 = v-min, 3 = v-max |
| `mesh-edge` | `[face, perimeter, edge]` | One directed edge within a face perimeter |

### Mesh Edges and Perimeters

A [polygon face can contain holes](../nodes/mesh.md). The mesh's `nholes` and `nvertices` arrays describe its outer perimeter and each hole perimeter. These perimeters are vertex lists, not NURBS trim curves.

For a `mesh-edge` selector, the three indices mean:

- `face`: the face within the mesh node.
- `perimeter`: `0` for the outer perimeter, `1` for the first hole, and so on.
- `edge`: the edge within the selected perimeter's vertex list.

An edge runs from a vertex to the next vertex in the list. The last edge returns to the first vertex. Thus, a perimeter with vertices `[a, b, c, d]` has these edges:

| Edge index | Start vertex | End vertex |
| ---------- | ------------ | ---------- |
| `0` | `a` | `b` |
| `1` | `b` | `c` |
| `2` | `c` | `d` |
| `3` | `d` | `a` |

Suppose face 7 is a square with one triangular hole. It has four outer edges and three hole edges:

- `[7, 0, 2]` selects the third edge of the square's outer perimeter.
- `[7, 1, 2]` selects the third edge of the triangular hole's perimeter.

Both selectors select one edge. Neither selects a whole perimeter. For a face without holes, the perimeter index is always `0`. The `trim-loop` selector, by contrast, selects a complete NURBS trim loop.

For subdivision, the selected control-cage edge identifies a limit-surface boundary. It does not select the straight control-cage segment. Each supported subdivision scheme must define this relationship. The same declaration applies to the draft `t-nurcc` control topology.

### Directions and Partial Ranges

A natural side follows increasing `v` for a u-side and increasing `u` for a v-side. A trim curve follows its stored parameter range. Reversal applies after selection.

A range selects a subinterval before reversal. Its endpoints satisfy `0 <= start < end <= 1`. These values are fractions of the curve's active parameter range or the edge's local parameter domain. A `trim-loop` selector accepts only its full range. Partial loops use ordered `trim-curve` selectors instead.

Matching uses must have the same start and end positions, within tolerance, after reversal. Where neighboring welds meet, their declarations must select the same geometric junction, within tolerance. A segment break inside one use needs no matching break in another use.

Local range numbers need not match across surfaces. For example, `[0, 0.5]` on `A(t)` above corresponds geometrically to `[0, (sqrt(5)-1)/2]` on `B(t)`. Both finish at position `0.5`. The exporter guarantees this geometric agreement. The renderer cannot assume equal range numbers or equal parameter increments.

The selected segments must form one connected chain on one boundary of the surface that remains after trimming. A closed-loop selector is a complete use and cannot be mixed with additional segments in that use. Empty uses, invalid indices, and disconnected chains are invalid declarations.

### Retained Region and Mixed Selectors

A weld belongs to the retained surface beside the selected boundary. Trimming determines that region before the weld is considered. The declaration does not restore removed surface. Traversal direction does not determine which region remains.

With the draft's `trim-curves.hole = 1`, the use belongs to the surface outside that hole. With `hole = 0`, the use belongs to the retained region inside the outer or island loop. Nested loops and domain clipping still determine the final retained region.

The legacy attribute `trimcurves.inside = 0` keeps the region outside the loops. A value of `1` keeps the region inside. In either case, the weld belongs to the surface that remains beside the loop. These trim settings do not require opposite weld directions. The `inside` and `hole` values have opposite meanings and are not interchangeable.

A selected portion must separate retained surface from removed surface or from the area outside the active domain. A curve that does not bound the final retained region cannot declare a boundary use there. If only part survives trimming, the declaration selects only that part.

A `nurbs-side` selector is valid wherever that domain side bounds retained surface. For example, a patch with one interior hole still has four outer boundary sides. A trim curve need not duplicate those sides.

A use can mix `nurbs-side` and `trim-curve` segments only when they follow consecutive portions of one boundary after trimming. The surface topology must connect their endpoints. The chain must follow the boundary without a jump or repeated portion. An open use need not close. A closed use must return to its start on the same boundary. Separate inner and outer loops cannot form one use merely because their 3D positions touch.

For example, a trim region can extend beyond the active domain. After clipping, its boundary can contain both trim arcs and domain-side portions. Consecutive portions can form one use. If a trim curve coincides with a domain side, either selector can describe that portion. The use must not include both copies.

A renderer that does not support mixed uses must report that limitation. It must not silently interpret them as separate complete uses or claim that the requested join was preserved.

### The Five-to-One Join

Suppose `patch` has the five-curve hole above. Suppose `subdiv` has one boundary edge whose limit boundary follows the same closed path. The exporter chooses ID `12` for this join. The number is arbitrary; it is not a curve or vertex index.

The exporter selects trim loop 0 on `patch` and edge 2 of the outer perimeter on subdivision face 7. Those indices identify existing geometry in this example. This stream fragment adds the weld declaration:

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

Both uses have ID `12` and connect to `solid_welds`, so they declare one join. The example assumes that both selections follow the same closed path, start, and direction. If one selector runs oppositely, its declaration also supplies `weld.reverse = 1`. An ordinary open edge cannot join an entire closed hole. If several subdivision edges form the matching ring, they form one use instead.

The exporter can also list the five trim curves separately. This alternative selects the same chain and keeps ID `12`:

```text
SetAttribute "patch"
    "weld.id" "int" 1 [12]
    "weld.segment-count" "int" 1 [5]
    "weld.kind" "string" 5 ["trim-curve" "trim-curve" "trim-curve" "trim-curve" "trim-curve"]
    "weld.index" "int[3]" 5 [0 0 0  1 0 0  2 0 0  3 0 0  4 0 0]
```

A chain of mesh edges uses the same counts and array order. Mixed selectors follow the retained-region rules above. Each side declares one use, regardless of its segment count.

### Several Independent Joins

The exporter now chooses ID `13` for a second join on the patch's u-max side. It keeps ID `12` for the hole. Both joins use the existing `solid_welds` node:

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

These arrays follow the same matching rules. A renderer can express them as entries in the general use table above. A surface supplies either these shorthand arrays or the general table, never both. An exporter can use the general table everywhere to avoid maintaining two encodings.

Assigning one shorthand ID to five consecutive curves would declare five complete uses of the same boundary. It would not make one five-segment use. A `trim-loop` selector or explicit segment count expresses that grouping.

With [separate trim nodes](trim-curves-nodes.md), a general table can reside on each trim node. Its trim indices refer to that node's arrays. The table uses the weld namespace of the surface connected to that trim node. Natural-side declarations stay on the surface. A trim node with weld declarations connects to exactly one surface. The choice of trim storage does not otherwise change weld identity.

## Alternatives and Trade-offs

For `E` shared boundaries and `U` uses, these counts exclude existing geometry and trim nodes:

| Encoding | Extra nodes | Benefit | Cost |
| -------- | ----------- | ------- | ---- |
| Original scene-global IDs | 0 | Small arrays; direct mapping from source IDs | Exporters must coordinate global IDs; no explicit scope connection |
| One `weld` namespace plus local use tables | 1 per namespace | Batches all joins; supports chains; IDs stay local; recommended | Exporter maintains arrays; one namespace per geometry node |
| One `weld` per boundary plus explicit `weld-use` nodes | `E + U` | Independent graph edits; each use has an explicit handle | More nodes, handles, connections, and lifetime bookkeeping |
| One `weld` per boundary with direct geometry connections | `E` | Fewer nodes than explicit uses | Still needs selectors and grouping on connections or attribute slots |

For 10,000 boundaries with two uses each, the explicit-use approach adds 30,000 nodes. The recommended encoding adds one namespace node for that solid. Both encodings still describe 20,000 uses. Arrays reduce the node count but still carry the topology data. These counts do not establish a rendering performance difference.

A [shared 3D edge curve](trim-curves-edges.md) is an independent extension. It could accompany either identity encoding. It does not identify the local boundary uses by itself.

## Scope, Edits, and Remaining Decisions

One geometry node participates in one weld namespace in this recommendation. A mesh containing several solids can use one namespace with distinct IDs. The exporter does not need to split that mesh into separate nodes. To combine namespaces from different sources, the exporter must change IDs that conflict. Combining indexed geometry similarly requires changes to conflicting indices.

Node handles identify definitions. Instances of those definitions need an additional scope rule. Repeating an assembly must repeat its internal joins without welding separate instances together. How to attach that scope to an assembly remains an open design question. If the instance scope is ambiguous, the renderer must not join every instance of the connected geometry.

Topology edits that change indices must update the use tables. At each render synchronization point, the table's arrays must describe one consistent set of uses. Removing the `weld` connection removes the geometry from that namespace. Its remaining IDs do not become scene-global. A renderer that ignores these declarations cannot claim to preserve the requested joins.

## Implementation Feedback and Coverage

The first implementer reported results from `nsi-intermediate` and `nsi-tessellate` in the [ɴsɪ repository](https://github.com/virtualritz/nsi). `nsi-intermediate` resolves declarations. `nsi-tessellate` welds NURBS nodes. The reported fixtures include io1-ec-214, with 17 faces and 35 edges, and boxy, with 80 faces and 124 edges. We did not independently reproduce these measurements during this documentation change.

| Reported finding | Consequence for this revision |
| ---------------- | ----------------------------- |
| Endpoint-only direction matching folded closed cylinder bands, producing areas 3.2 and 7.8 times the expected values. Quarter-point comparisons distinguished direction in the measured cases. | All uses must share a start and traversal direction after reversal. This removes the need to infer direction from endpoints. |
| Measured manifold uses had opposite source traversals and coincident starts. | Exporters align these traversals with `weld.reverse`. The shared traversal also supports more than two uses; it does not imply equal parameter speeds. |
| The implementation rejected outside-loop trims because the draft did not specify which surface region the weld joined. | A weld belongs to the retained region beside its selected boundary. Hole and outside-loop settings are valid and do not change weld traversal. |
| Mixed side/trim uses were unsupported and did not occur in the measured exports. | Mixed selections must follow consecutive portions of one boundary of the retained surface. Separate loops and duplicate portions remain invalid. |
| Of io1-ec-214's 70 segments, 48 were natural sides, including partial sides. Ranges worked where split points agreed. | Corresponding use endpoints and adjoining weld junctions must agree geometrically. Local range numbers need not match. |
| All uses across five STEP fixtures had one segment. Circular edges were single rational curves with doubled knots. | The default segment count stays one. Ordered chains remain available for differently segmented exports. |
| Twelve of io1-ec-214's 17 faces were cylinder bands with self-seams. Open declarations also served as useful diagnostics. | Two uses on the same geometry remain distinct uses of one weld. A lone use joins nothing and can help diagnose incomplete export. |

The report does not test mesh-edge selectors, chains with several segments, or different parameter speeds. The proposal supports those cases, but implementation tests are still needed. An open declaration alone cannot distinguish an intentional open boundary from missing export data.

The remaining decisions concern instance scope, how to supply tolerances, and the exact attribute encoding. One namespace contains many identities, and one use can contain many ordered segments. Displacement, tessellation, and geometric correspondence remain renderer decisions.
