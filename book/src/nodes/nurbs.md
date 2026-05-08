# `nurbs`

This node represents a NURBS surface patch. It has the following required attributes:

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nu` | _`int`_ |         |

Control-point count along `u`.

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nv` | _`int`_ |         |

Control-point count along `v`.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `uorder` | _`int`_ |         |

Order along `u` (degree + 1). Must be at least 2.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `vorder` | _`int`_ |         |

Order along `v` (degree + 1). Must be at least 2.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `uknot` | _`float`_ |         |

Knot vector along `u`. Its length must equal `nu + uorder`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `vknot` | _`float`_ |         |

Knot vector along `v`. Its length must equal `nv + vorder`.

One of `P` or `Pw` must be supplied to provide the control points:

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

The `nu * nv` control points (xyz), stored row-major such that `P[i*nu + j]` addresses the control point at row `i`, column `j`.

| Name | Type         | Default |
| ---- | ------------ | ------- |
| `Pw` | _`float[4]`_ |         |

A rational alternative to `P`. Each control point is four floats (xyzw); supplying `Pw` instead of `P` enables rational NURBS.

The node also accepts an optional set of trim curves. Trim curves are NURBS curves in the surface's homogeneous parameter space (`u`, `v`, `w`); the actual `(u, v)` position of a control point is `(u/w, v/w)`. They are organised into loops: within a loop, curves connect head-to-tail, and the loop must be explicitly closed — the last point of the last curve in a loop must coincide with the first point of the first curve. The `trimcurves.*` attributes are all-or-nothing: if any one of them is present, the full set must be supplied.

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
