# NURBS: Draft Design

This page is the draft of a future version of the [`nurbs`](../nodes/nurbs.md) node: a NURBS surface patch -- a tensor-product spline defined by a grid of control points, two knot vectors, and an order in each parametric direction.

> 3Delight 2.9.210 implements the `nurbs` node with the legacy attribute names; the [reference page](../nodes/nurbs.md) documents it. This draft was written before that release. It uses the [new naming convention](../naming-convention.md) and proposes changes beyond the renames: consolidated trim-curve control points, per-loop holes, and stitching. Where this draft and the shipped node differ, the reference page is correct for 3Delight today:
>
> - The shipped `Pw` has the type _`hpoint`_, not _`weighted-point`_.
> - The shipped node has no loop count. The number of `trimcurves.ncurves` values is the number of loops.
> - The shipped `trimcurves.inside` is one optional value, and 1 *keeps* the surface inside a loop. The draft's `trim-curves.hole` has one value per loop, and 1 *removes* it.

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

The surface's active parameter range can be restricted with the optional `u.min`/`u.max`/`v.min`/`v.max` attributes. Unlike other geometric primitives, NURBS surfaces do not assume `[0, 1]` parameter ranges -- by default, the active range is the full extent of the corresponding knot vector.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `u.min` | _`float`_ |         |

Lower bound of the active range along `u`. Must be less than `u.max` and at least the `(u.order - 1)`-th value of `u.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `u.max` | _`float`_ |         |

Upper bound of the active range along `u`. Must be greater than `u.min` and at most the `u.count`-th value of `u.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `v.min` | _`float`_ |         |

Lower bound of the active range along `v`. Must be less than `v.max` and at least the `(v.order - 1)`-th value of `v.knot`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `v.max` | _`float`_ |         |

Upper bound of the active range along `v`. Must be greater than `v.min` and at most the `v.count`-th value of `v.knot`.

One of `position` or `position-weighted` must be supplied to provide the control points. `position` defines a polynomial surface; `position-weighted` defines a rational one.

| Name       | Type      | Default |
| ---------- | --------- | ------- |
| `position` | _`point`_ |         |

The `u.count * v.count` control points (xyz), stored row-major: `position[i * u.count + j]` is the point at row `i`, column `j`.

| Name                | Type               | Default |
| ------------------- | ------------------ | ------- |
| `position-weighted` | _`weighted-point`_ |         |

Rational alternative to `position`: each control point is a weighted (homogeneous) point `(wx, wy, wz, w)`, enabling rational NURBS. Same ordering as `position`. The `weighted-point` type is a draft addition -- see [Geometry in the Type System](../design/geometry-types.md).

## Trim Curves

> How trim data is packaged -- inline attributes as specified here, or dedicated nodes -- is an open design question. See [Trim Curves: API Alternatives](../design/trim-curves.md) for the alternatives under discussion; this page describes Option 1.

Trim curves carve a region out of the surface's parameter domain. They are NURBS curves in the surface's `(u, v)` parameter space -- rational trim curves use homogeneous `(u, v, w)` control points, where the actual `(u, v)` of a control point is `(u/w, v/w)`. Curves are organised into loops: within a loop they connect head-to-tail. Each loop must be explicitly closed -- the last point of the last curve must coincide with the first point of the first curve.

The `trim-curves.*` attributes below are all-or-nothing: supply the full set or omit it entirely, with two exceptions. Supply exactly one of `trim-curves.position` and `trim-curves.position-weighted`, never both. And the stitching attributes `trim-curves.edge-id`/`trim-curves.edge-orientation` are optional -- see [Stitching](#stitching).

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

Rational alternative to `trim-curves.position`: the concatenated control points of all curves as homogeneous `(u, v, w)` triples. Same ordering and total length as `trim-curves.position`. These are deliberately plain float tuples, not `point`-typed data -- parameter-space coordinates must never transform; see [Geometry in the Type System](../design/geometry-types.md).

| Name               | Type    | Default |
| ------------------ | ------- | ------- |
| `trim-curves.hole` | _`int`_ |         |

Whether each loop is a hole. One value per loop. A value of `0` keeps the surface inside the loop; a value of `1` marks the loop as a hole -- the surface inside it is removed. Loops may nest, alternating: an island inside a hole is again `0`.

## Stitching

The [shared-boundary design](shared-boundaries.md) owns the common identity model, alternatives, and examples for NURBS, polygon, and subdivision surfaces. Its recommendation is one `weld` namespace node connected to every participating geometry node. One namespace can contain all joins in a solid.

The attributes below are a compact shorthand for one-segment boundary uses in that namespace. They are proposed additions, not shipped attributes. A surface supplies either these arrays or the general `weld.*` use table, never both.

A boundary use can also contain several segments. For example, five trim curves can jointly meet one subdivision boundary. That case uses the general table's `trim-loop` selector or an explicit ordered chain; the per-curve shorthand cannot express that grouping.

The declaration asks the renderer to preserve the join through tessellation and displacement. It does not prescribe an algorithm. A renderer that ignores the declaration cannot guarantee the requested join.

### Trim-Curve Edges

Both attributes below, when supplied, must be supplied together, with one value per curve (aligned with `trim-curves.point-count`, `trim-curves.order`, etc.).

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `trim-curves.edge-id` | _`int`_ | `-1`    |

The edge identity of each curve. One value per curve. Each non-negative entry declares one complete boundary use. Uses with the same ID and connected `weld` node belong together, including uses on other geometry types. A value of `-1` declares no use. Non-negative IDs require a `weld` connection; IDs are not scene-global.

| Name                           | Type    | Default |
| ------------------------------ | ------- | ------- |
| `trim-curves.edge-orientation` | _`int`_ | `0`     |

The traversal direction of each curve relative to its edge's reference direction. One value per curve. A value of `0` means the curve, traversed from its parametric start to its end, follows the edge's reference direction; `1` means it opposes it. This value becomes `weld.reverse` in the general table. After reversal, all uses follow the same reference traversal and share their start within tolerance, including closed boundaries. Native face-boundary orientation is separate. Equal parameter values still need not identify equal positions.

### Natural Boundaries

In untrimmed patch networks -- and on trimmed faces whose outer boundary is the natural parameter domain, such as a face carrying only hole loops -- the welded edge is a whole side of the active domain rectangle `[u.min, u.max] x [v.min, v.max]`. Forcing such faces through the trimming machinery just to transport edge identities would be wasteful, so these welds are declared directly, per side.

| Name             | Type       | Default |
| ---------------- | ---------- | ------- |
| `stitch.edge-id` | _`int[4]`_ | `-1`    |

The edge identities of the four sides of the active domain rectangle, in the order *u = u.min*, *u = u.max*, *v = v.min*, *v = v.max*. Values share the identifier space and semantics of `trim-curves.edge-id`: boundaries with equal non-negative values are stitched, `-1` means no identity.

| Name                      | Type       | Default |
| ------------------------- | ---------- | ------- |
| `stitch.edge-orientation` | _`int[4]`_ | `0`     |

The traversal direction of each side relative to the shared reference traversal, in the same side order. A side's native direction is increasing `v` for the two u-sides and increasing `u` for the two v-sides. A value of `1` reverses that native direction; `0` keeps it. The resulting traversal must agree with the other uses, including its start.

This shorthand selects a whole side, so that entire side must bound the retained region. Partly retained sides require explicit ranges in the general table. If a trim curve and a domain side describe the same boundary portion, only one selector declares that use.

A closed surface that is represented as a single patch split at a seam -- a cylinder or torus, say -- welds to itself by giving the two seam sides the same identity, e.g. equal values for the *u = u.min* and *u = u.max* entries of one node.

The per-side shorthand selects whole sides only. Partial sides and T-junctions use local ranges in the [general boundary-use table](shared-boundaries.md#concrete-encoding).

### Shared Semantics

The [shared-boundary design](shared-boundaries.md) defines identity scope, boundary chains, self-seams, and non-manifold joins. Natural-side and trim-curve shorthand entries follow those same rules. The exporter guarantees that counterpart chains describe the same spatial boundary within the source model's tolerance. After reversal, starts, ends, and traversal directions agree. Segment counts and parameterizations can differ. Belonging does not ask the renderer to join unrelated geometry.

Each trim curve is a complete use in this shorthand. Five curves with one repeated ID are five uses, not one chain. Selecting the whole loop in the general table expresses a single use made from all five curves.

A trim-boundary use belongs to the retained surface adjacent to that loop. A hole therefore joins its surrounding surface, not the removed interior. Reversal changes correspondence direction, not the retained region. The [retained-region rules](shared-boundaries.md#retained-region-and-mixed-selectors) apply to both shorthand and general declarations.

An optional 3D edge representation is a separate [geometry extension](trim-curves-edges.md). It is not required by these declarations.
