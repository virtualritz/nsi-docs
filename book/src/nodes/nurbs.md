# `nurbs`

This node represents a NURBS surface patch — a tensor-product spline defined by a grid of control points, two knot vectors, and an order in each parametric direction.

> This node is a draft: no renderer implements it yet. Unlike the rest of this reference, its attributes already follow the [new naming convention](../naming-convention.md).

It has the following required attributes:

| Name      | Type    | Default |
| --------- | ------- | ------- |
| `u.count` | _`int`_ |         |

Control-point count along `u`. Total control-point count is `u.count * v.count`. Should be at least `u.order`; if smaller, the surface is rendered with order equal to `u.count`.

| Name      | Type    | Default |
| --------- | ------- | ------- |
| `v.count` | _`int`_ |         |

Control-point count along `v`. Same constraint as `u.count` relative to `v.order`.

| Name      | Type    | Default |
| --------- | ------- | ------- |
| `u.order` | _`int`_ |         |

Order along `u`: degree + 1, so `2` is linear, `3` quadratic, `4` cubic. Must be at least 2. May differ from `v.order`.

| Name      | Type    | Default |
| --------- | ------- | ------- |
| `v.order` | _`int`_ |         |

Order along `v`. See `u.order`.

| Name     | Type      | Default |
| -------- | --------- | ------- |
| `u.knot` | _`float`_ |         |

Knot vector along `u`. Length must equal `u.count + u.order`. Values must be non-decreasing.

| Name     | Type      | Default |
| -------- | --------- | ------- |
| `v.knot` | _`float`_ |         |

Knot vector along `v`. Length must equal `v.count + v.order`. Values must be non-decreasing.

The surface's active parameter range can be restricted with the optional `u.min`/`u.max`/`v.min`/`v.max` attributes. Unlike other geometric primitives, NURBS surfaces do not assume `[0, 1]` parameter ranges — by default, the active range is the full extent of the corresponding knot vector.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `u.min` | _`float`_ |         |

Lower bound of the active range along `u`. Must be less than `u.max` and at least the `(u.order − 1)`-th value of `u.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `u.max` | _`float`_ |         |

Upper bound of the active range along `u`. Must be greater than `u.min` and at most the `u.count`-th value of `u.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `v.min` | _`float`_ |         |

Lower bound of the active range along `v`. Must be less than `v.max` and at least the `(v.order − 1)`-th value of `v.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `v.max` | _`float`_ |         |

Upper bound of the active range along `v`. Must be greater than `v.min` and at most the `v.count`-th value of `v.knot`.

One of `position` or `position-weighted` must be supplied to provide the control points. `position` defines a polynomial surface; `position-weighted` defines a rational one.

| Name       | Type      | Default |
| ---------- | --------- | ------- |
| `position` | _`point`_ |         |

The `u.count * v.count` control points (xyz), stored row-major: `position[i * u.count + j]` is the point at row `i`, column `j`.

| Name                | Type         | Default |
| ------------------- | ------------ | ------- |
| `position-weighted` | _`float[4]`_ |         |

Rational alternative to `position`: each control point is four floats `(x, y, z, w)`, enabling rational NURBS. Same ordering as `position`.

## Trim Curves

Trim curves carve a region out of the surface's parameter domain. They are NURBS curves in the surface's `(u, v)` parameter space — rational trim curves use homogeneous `(u, v, w)` control points, where the actual `(u, v)` of a control point is `(u/w, v/w)`. Curves are organised into loops: within a loop they connect head-to-tail. Each loop must be explicitly closed — the last point of the last curve must coincide with the first point of the first curve.

The `trim-curves.*` attributes below are all-or-nothing: supply the full set or omit it entirely, with two exceptions. Supply exactly one of `trim-curves.position` and `trim-curves.position-weighted`, never both. And the stitching attributes `trim-curves.edge-id` / `trim-curves.edge-orientation` are optional — see [Stitching](#stitching).

| Name                     | Type    | Default |
| ------------------------ | ------- | ------- |
| `trim-curves.loop-count` | _`int`_ |         |

The number of trim loops.

| Name                      | Type    | Default |
| ------------------------- | ------- | ------- |
| `trim-curves.curve-count` | _`int`_ |         |

The number of curves in each loop. One value per loop.

| Name                      | Type    | Default |
| ------------------------- | ------- | ------- |
| `trim-curves.point-count` | _`int`_ |         |

The control-point count of each curve. One value per curve.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `trim-curves.order` | _`int`_ |         |

The order of each curve. One value per curve.

| Name               | Type      | Default |
| ------------------ | --------- | ------- |
| `trim-curves.knot` | _`float`_ |         |

The concatenated knot vectors for all curves. The total length is the sum over curves of `point-count[i] + order[i]`.

| Name              | Type      | Default |
| ----------------- | --------- | ------- |
| `trim-curves.min` | _`float`_ |         |

The parametric start of each curve. One value per curve.

| Name              | Type      | Default |
| ----------------- | --------- | ------- |
| `trim-curves.max` | _`float`_ |         |

The parametric end of each curve. One value per curve.

| Name                   | Type         | Default |
| ---------------------- | ------------ | ------- |
| `trim-curves.position` | _`float[2]`_ |         |

The concatenated control points of all curves as non-rational `(u, v)` pairs. The total length is the sum over curves of `point-count[i]`.

| Name                            | Type         | Default |
| ------------------------------- | ------------ | ------- |
| `trim-curves.position-weighted` | _`float[3]`_ |         |

Rational alternative to `trim-curves.position`: the concatenated control points of all curves as homogeneous `(u, v, w)` triples. Same ordering and total length as `trim-curves.position`.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `trim-curves.sense` | _`int`_ |         |

The sense of each loop. One value per loop. A value of `0` keeps the surface inside the loop; a value of `1` keeps the surface outside the loop (i.e. the loop describes a hole).

## Stitching

CAD solid formats (STEP, IGES, Parasolid) represent a solid as a shell of faces sewn together along shared edges: each edge of the model is stored once and referenced by the faces it bounds — typically two — each of which carries its own parameter-space curve for that edge. When such a model is exported as one `nurbs` node per face, the boundaries of adjacent nodes are two views of the same model edge.

The attributes below conserve that shared-edge topology. They declare which boundaries — on the same or on different `nurbs` nodes — trace the same edge and were welded in the source model, so the renderer can keep the geometry watertight across the edge. This matters wherever the renderer perturbs or evaluates geometry independently per surface: displacement mapping in particular will tear adjacent faces apart along an edge whose normals are discontinuous unless the renderer knows the faces belong together and makes their displaced boundaries agree.

A welded boundary is either a trim curve or a natural side of the patch's parameter domain; there is one mechanism for each, sharing a single identifier space. All stitching attributes are optional and add no geometry of their own, so a renderer that does not implement stitching can ignore them safely.

### Trim-Curve Edges

Both attributes below, when supplied, must be supplied together, with one value per curve (aligned with `trim-curves.point-count`, `trim-curves.order`, etc.).

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `trim-curves.edge-id` | _`int`_ | `-1`    |

The edge identity of each curve. One value per curve. A non-negative value identifies the model edge this curve is a use of: all boundaries carrying the same non-negative value — in this node or any other `nurbs` node in the scene — trace the same edge in 3D and are stitched. A value of `-1` means the curve carries no edge identity. Identifiers are scene-global; the exporter is responsible for their uniqueness (a serial number per edge of the source model suffices).

| Name                           | Type    | Default |
| ------------------------------ | ------- | ------- |
| `trim-curves.edge-orientation` | _`int`_ | `0`     |

The traversal direction of each curve relative to its edge's reference direction. One value per curve. A value of `0` means the curve, traversed from its parametric start to its end, follows the edge's reference direction; `1` means it opposes it. On a consistently oriented manifold shell the two uses of an edge traverse it in opposite directions, so their values differ. This puts the two parameterizations into correspondence without requiring the renderer to match them geometrically.

### Natural Boundaries

In untrimmed patch networks — and on trimmed faces whose outer boundary is the natural parameter domain, such as a face carrying only hole loops — the welded edge is a whole side of the active domain rectangle `[u.min, u.max] × [v.min, v.max]`. Forcing such faces through the trimming machinery just to transport edge identities would be wasteful, so these welds are declared directly, per side.

| Name             | Type       | Default |
| ---------------- | ---------- | ------- |
| `stitch.edge-id` | _`int[4]`_ | `-1`    |

The edge identities of the four sides of the active domain rectangle, in the order *u = u.min*, *u = u.max*, *v = v.min*, *v = v.max*. Values share the identifier space and semantics of `trim-curves.edge-id`: boundaries with equal non-negative values are stitched, `-1` means no identity.

| Name                      | Type       | Default |
| ------------------------- | ---------- | ------- |
| `stitch.edge-orientation` | _`int[4]`_ | `0`     |

The traversal direction of each side relative to its edge's reference direction, in the same side order. The reference direction of a side is increasing `v` for the two u-sides and increasing `u` for the two v-sides; `0` follows the edge's reference direction, `1` opposes it.

A side's entry applies only where that side actually bounds the rendered region. Where the outer boundary is expressed as trim curves instead, the identities belong on the curves via `trim-curves.edge-id`.

A closed surface that is represented as a single patch split at a seam — a cylinder or torus, say — welds to itself by giving the two seam sides the same identity, e.g. equal values for the *u = u.min* and *u = u.max* entries of one node.

Welds covering only part of a side, or a side stitched to several neighbours (T-junctions), cannot be expressed per side; use trim curves for those.

### Semantics

Boundaries that share an edge identity must describe the same locus in 3D — each mapped through its own surface — within the source model's tolerance. The renderer is not required to repair uses that disagree beyond that.

The two mechanisms interoperate through the common identifier space: a trim curve on one face may be welded to a natural side of another, as happens where a trimmed face meets an untrimmed patch.

An edge normally has exactly two uses. If more than two boundaries share an identity (a non-manifold edge), all of them are stitched together.

Stitching a renderer supports means: along a shared edge, evaluate displacement and shading such that all welded uses produce coincident positions — for example by deriving a single displacement along the edge and applying it to every use — so that no cracks open where the surfaces meet, even where their geometric normals are discontinuous.

### Design Notes

A renderer can attempt to reconstruct adjacency without these attributes by detecting boundary proximity, and may still do so as a fallback when they are absent. But proximity detection depends on guessed tolerances and cannot distinguish faces that were welded in the source model from faces of separate solids that merely touch — a distinction CAD formats make topologically. Exporters should therefore conserve the topology whenever the source data has it; it maps one-to-one onto these attributes (e.g. STEP's `edge_curve` entities and their oriented uses).

The edge identifier deliberately leaves room for a future `edge` node type carrying the authoritative shared 3D curve of an edge — useful for exact reprojection or wireframe rendering — referenced by the same identifier. Such a node is not part of this specification.
