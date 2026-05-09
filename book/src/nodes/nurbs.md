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

Trim curves carve a region out of the surface's parameter domain. They are NURBS curves in homogeneous `(u, v, w)` parameter space — the actual `(u, v)` of a control point is `(u/w, v/w)`. Curves are organised into loops: within a loop they connect head-to-tail, and the loop must be explicitly closed (the last point of the last curve coincides with the first point of the first curve).

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
