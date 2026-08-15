# `nurbs`

This node represents a NURBS surface patch — a tensor-product spline defined by a grid of control points, two knot vectors, and an order in each parametric direction. It has the following required attributes:

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nu` | _`int`_ |         |

Control-point count along `u`. Total control-point count is `nu * nv`. Should be at least `uorder`; if smaller, the surface is rendered with order equal to `nu`.

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nv` | _`int`_ |         |

Control-point count along `v`. Same constraint as `nu` relative to `vorder`.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `uorder` | _`int`_ |         |

Order along `u`: degree + 1, so `2` is linear, `3` quadratic, `4` cubic. Must be at least 2. May differ from `vorder`.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `vorder` | _`int`_ |         |

Order along `v`. See `uorder`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `uknot` | _`float`_ |         |

Knot vector along `u`. Length must equal `nu + uorder`. Values must be non-decreasing.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `vknot` | _`float`_ |         |

Knot vector along `v`. Length must equal `nv + vorder`. Values must be non-decreasing.

The surface's active parameter range can be restricted with the optional `umin`/`umax`/`vmin`/`vmax` attributes. Unlike other geometric primitives, NURBS surfaces do not assume `[0, 1]` parameter ranges — by default, the active range is the full extent of the corresponding knot vector.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `umin` | _`float`_ |         |

Lower bound of the active range along `u`. Must be less than `umax` and at least the `(uorder − 1)`-th value of `uknot`.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `umax` | _`float`_ |         |

Upper bound of the active range along `u`. Must be greater than `umin` and at most the `nu`-th value of `uknot`.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `vmin` | _`float`_ |         |

Lower bound of the active range along `v`. Must be less than `vmax` and at least the `(vorder − 1)`-th value of `vknot`.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `vmax` | _`float`_ |         |

Upper bound of the active range along `v`. Must be greater than `vmin` and at most the `nv`-th value of `vknot`.

One of `P` or `Pw` must be supplied to provide the control points. `P` defines a polynomial surface; `Pw` defines a rational one.

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

The `nu * nv` control points (xyz), stored row-major: `P[i*nu + j]` is the point at row `i`, column `j`.

| Name | Type         | Default |
| ---- | ------------ | ------- |
| `Pw` | _`float[4]`_ |         |

Rational alternative to `P`: each control point is four floats `(x, y, z, w)`, enabling rational NURBS. Pass as a single flat array of `4 * nu * nv` floats — do **not** declare it with `array_len(4)`.

## Trim Curves

Trim curves carve a region out of the surface's parameter domain. They are NURBS curves in homogeneous `(u, v, w)` parameter space — the actual `(u, v)` of a control point is `(u/w, v/w)`. Curves are organised into loops: within a loop they connect head-to-tail. Each loop must be explicitly closed — the last point of the last curve must coincide with the first point of the first curve.

The `trimcurves.*` attributes are all-or-nothing: supply the full set or omit it entirely.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `trimcurves.nloops` | _`int`_ |         |

The number of trim loops.

| Name                 | Type    | Default |
| -------------------- | ------- | ------- |
| `trimcurves.ncurves` | _`int`_ |         |

The number of curves in each loop. One value per loop.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `trimcurves.n` | _`int`_ |         |

The control-point count of each curve. One value per curve.

| Name               | Type    | Default |
| ------------------ | ------- | ------- |
| `trimcurves.order` | _`int`_ |         |

The order of each curve. One value per curve.

| Name              | Type      | Default |
| ----------------- | --------- | ------- |
| `trimcurves.knot` | _`float`_ |         |

The concatenated knot vectors for all curves. The total length is the sum over curves of `n[i] + order[i]`.

| Name             | Type      | Default |
| ---------------- | --------- | ------- |
| `trimcurves.min` | _`float`_ |         |

The parametric start of each curve. One value per curve.

| Name             | Type      | Default |
| ---------------- | --------- | ------- |
| `trimcurves.max` | _`float`_ |         |

The parametric end of each curve. One value per curve.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.u` | _`float`_ |         |

Concatenated `u` coordinates of all trim-curve control points. The total length is the sum over curves of `n[i]`.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.v` | _`float`_ |         |

Concatenated `v` coordinates of all trim-curve control points. The total length is the sum over curves of `n[i]`.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.w` | _`float`_ |         |

Concatenated weights of all trim-curve control points. The total length is the sum over curves of `n[i]`. Use `1.0` for non-rational curves.

| Name               | Type    | Default |
| ------------------ | ------- | ------- |
| `trimcurves.sense` | _`int`_ |         |

The sense of each loop. One value per loop. A value of `0` keeps the surface inside the loop; a value of `1` keeps the surface outside the loop (i.e. the loop describes a hole).

## Stitching

CAD solid formats (STEP, IGES, Parasolid) represent a solid as a shell of faces sewn together along shared edges: each edge of the model is stored once and referenced by the faces it bounds — typically two — each of which carries its own parameter-space curve for that edge. When such a model is exported as one `nurbs` node per face, the trim curves of adjacent nodes are two views of the same model edge.

The two attributes below conserve that shared-edge topology. They declare which trim curves — on the same or on different `nurbs` nodes — trace the same edge and were welded in the source model, so the renderer can keep the geometry watertight across the edge. This matters wherever the renderer perturbs or evaluates geometry independently per surface: displacement mapping in particular will tear adjacent faces apart along an edge whose normals are discontinuous unless the renderer knows the faces belong together and makes their displaced boundaries agree.

Both attributes are optional. When supplied, both must be supplied, with one value per curve (aligned with `trimcurves.n`, `trimcurves.order`, etc.). They add no geometry of their own, so a renderer that does not implement stitching can ignore them safely.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `trimcurves.edgeid` | _`int`_ | `-1`    |

The edge identity of each curve. One value per curve. A non-negative value identifies the model edge this curve is a use of: all trim curves carrying the same non-negative value — in this node or any other `nurbs` node in the scene — trace the same edge in 3D and are stitched. A value of `-1` means the curve carries no edge identity. Identifiers are scene-global; the exporter is responsible for their uniqueness (a serial number per edge of the source model suffices).

| Name                         | Type    | Default |
| ---------------------------- | ------- | ------- |
| `trimcurves.edgeorientation` | _`int`_ | `0`     |

The traversal direction of each curve relative to its edge's reference direction. One value per curve. A value of `0` means the curve, traversed from its parametric start to its end, follows the edge's reference direction; `1` means it opposes it. On a consistently oriented manifold shell the two uses of an edge traverse it in opposite directions, so their values differ. This puts the two parameterizations into correspondence without requiring the renderer to match them geometrically.

### Semantics

Curves that share an edge identity must describe the same locus in 3D — each mapped through its own surface — within the source model's tolerance. The renderer is not required to repair uses that disagree beyond that.

An edge normally has exactly two uses. If more than two curves share an identity (a non-manifold edge), all of them are stitched together.

Stitching a renderer supports means: along a shared edge, evaluate displacement and shading such that all welded uses produce coincident positions — for example by deriving a single displacement along the edge and applying it to every use — so that no cracks open where the surfaces meet, even where their geometric normals are discontinuous.

Because stitching information rides on trim curves, a face that is welded along its natural, untrimmed boundary must express that boundary as an explicit outer trim loop (with sense `0`) whose curves carry the edge identities. The loop may simply coincide with the surface's parametric domain.

### Design Notes

A renderer can attempt to reconstruct adjacency without these attributes by detecting boundary proximity, and may still do so as a fallback when they are absent. But proximity detection depends on guessed tolerances and cannot distinguish faces that were welded in the source model from faces of separate solids that merely touch — a distinction CAD formats make topologically. Exporters should therefore conserve the topology whenever the source data has it; it maps one-to-one onto these attributes (e.g. STEP's `edge_curve` entities and their oriented uses).

The edge identifier deliberately leaves room for a future `edge` node type carrying the authoritative shared 3D curve of an edge — useful for exact reprojection or wireframe rendering — referenced by the same identifier. Such a node is not part of this specification.
