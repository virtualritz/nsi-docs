# NURBS Curves and Point Welds

Why separate renderable curve geometry from the points where curves join?

The retired `edge` proposal combined a shared boundary identity with a 3D curve. The [boundary-weld design](shared-boundaries.md) now supplies that identity without geometry. A [`nurbs-curves`](../nodes/nurbs-curves.md) node supplies renderable curves, including exact source curves for wireframe display. Neither feature requires one node per model edge.

## Precedent: `RiNuCurves`

The [AIR manual](https://www.sitexgraphics.com/air.pdf) documents `NuCurves` with per-curve counts, orders, knots, and active ranges. It accepts `P` or `Pw`, width, and user attributes. The [3Delight manual](https://documentation.3delightcloud.com/download/attachments/1376257/3Delight-UserManual.pdf?api=v2) also names `RiNuCurves`.

This proposal uses that geometry model with the existing ɴsɪ curve-attribute model. It does not claim exact compatibility with either renderer's interface. RenderDotC's historical support has not been verified from its documentation.

## Recommendation: Reuse the Namespace, Separate the Selectors

A boundary weld identifies a shared path. A point weld identifies one shared position. Both need scoped IDs, but they need different selectors.

The recommendation reuses the `weld` node and adds a separate point-use table on `nurbs-curves`:

| Attribute | Type | Meaning |
| --------- | ---- | ------- |
| `weld.point.id` | _`int`_ | One non-negative weld ID per point use |
| `weld.point.curve-index` | _`int`_ | One zero-based curve index per point use |
| `weld.point.parameter` | _`float`_ | One normalized active-range parameter per point use |

All three arrays have the same length. They use the geometry node's single `weld` connection. Each row selects one evaluated curve point, not a control point or tessellation vertex.

Parameter `s` lies in `[0, 1]`. For the selected curve, it evaluates at `min + s * (max - min)`. Thus, `0` selects the active start and `1` selects the active end. An interior value selects a meeting point without splitting the curve. The same parameter value on another curve need not select the same position.

All point uses with the same ID and namespace must identify the same position before displacement, within the source tolerance. The declared curve network must remain joined at these points during renderer evaluation and displacement. The renderer chooses how to enforce that condition. Exporters declare known relationships; the renderer does not discover them by proximity.

A namespace can contain both point-weld IDs and boundary-weld IDs. Each ID has exactly one role. Reusing one ID for both a point and a path is invalid. Point uses need no direction, perimeter index, segment count, or range.

The table initially applies to `nurbs-curves`. Extending it to `curves` requires a defined parameter domain for each supported basis and endpoint rule. Surface attachment selectors are a separate extension.

## End-to-End and End-to-Interior Joins

The exporter can join the two curves from the node reference with one namespace and two rows. It chooses the arbitrary ID `20` for the shared endpoint:

```text
Create "wire_joins" "weld"
Connect "wire_joins" "" "wires" "weld"
SetAttribute "wires"
    "weld.point.id" "int" 2 [20 20]
    "weld.point.curve-index" "int" 2 [0 1]
    "weld.point.parameter" "float" 2 [1 0]
```

The first row selects curve 0's end. The second selects curve 1's start. Both belong to the same join. Several joins fit in these arrays without additional nodes.

For an end-to-interior join, the second parameter could instead be `0.4`. That declaration is valid only if the actual geometry meets there. More than two rows can share an ID to declare a branch. Rows can also belong to different geometry nodes connected to the same namespace.

A renderer must evaluate and retain an interior join point even when its normal sampling would skip that parameter. This states the required result, not a tessellation method.

## What Stays Joined

A point weld declares a join in the curve network. The renderer must preserve that join during evaluation and displacement, so the curves do not tear apart there.

The declaration does not require equal tangents, widths, normals, materials, or parameter speeds. The source points must agree throughout the rendered time interval, in a common coordinate system.

The renderer chooses how to construct the junction for its curve representation. Junction shape and appearance are implementation details, including the treatment of tubes, ribbons, and caps. This proposal specifies the join, not its construction or appearance. No separate junction specification is required.

The same instance-scope question as for boundary welds remains open.

## Why Not a `spot-weld` Node?

| Design | Benefit | Cost |
| ------ | ------- | ---- |
| Shared `weld` namespace with a point table | Reuses connections and ID allocation; no unused selector fields | A namespace must reject IDs used for both points and paths |
| Separate `spot-weld` namespace | Node type separates point and path identities | Exporters manage another node type and connection |
| Point selectors in the boundary-use table | One table name | Segment counts, ranges, and direction have no point meaning |

A separate `spot-weld` node remains possible if point joins later need different node-level settings. The current distinction fits in separate tables without another node type. The shared ID always identifies one declared join; its meaning does not depend on unused tuple components.
