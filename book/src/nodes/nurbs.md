# `nurbs`

This node represents a non-uniform rational B-spline surface: a grid of control points, a knot vector and an order in each parametric direction.

The draft of a future version of this node, with renamed attributes and proposed extensions such as stitching, is in [NURBS: Draft Design](../design/nurbs-draft.md).

It has the following required attributes:

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

The control points of the surface. The number of values must be `nu` × `nv`. Either this or `Pw` is required.

| Name | Type       | Default |
| ---- | ---------- | ------- |
| `Pw` | _`hpoint`_ |         |

The control points of the surface, as homogeneous coordinates. The number of values must be `nu` × `nv`. Either this or `P` is required.

Each value is `(w·x, w·y, w·z, w)`: the coordinates are premultiplied by the weight. In 3Delight 2.9.210, a patch whose four control points span ±1 with `w` = 2 renders at half the size of the same patch given as `P`.

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nu` | _`int`_ |         |

The number of control points in the u parametric direction.

| Name | Type    | Default |
| ---- | ------- | ------- |
| `nv` | _`int`_ |         |

The number of control points in the v parametric direction.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `uorder` | _`int`_ |         |

The order of the surface in the u parametric direction: the degree plus one, so 2 is linear and 4 is cubic.

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `vorder` | _`int`_ |         |

The order of the surface in the v parametric direction.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `uknot` | _`float`_ |         |

The knot vector in the u parametric direction. The number of values must be `nu` + `uorder`.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `vknot` | _`float`_ |         |

The knot vector in the v parametric direction. The number of values must be `nv` + `vorder`.

It also has optional attributes:

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `umin` | _`float`_ |         |

The lower bound of the u parametric range where the surface is defined. If not specified, the `uknot` value at index `uorder` − 1 is used.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `umax` | _`float`_ |         |

The upper bound of the u parametric range where the surface is defined. If not specified, the `uknot` value at index `nu` is used.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `vmin` | _`float`_ |         |

The lower bound of the v parametric range where the surface is defined. If not specified, the `vknot` value at index `vorder` − 1 is used.

| Name   | Type      | Default |
| ------ | --------- | ------- |
| `vmax` | _`float`_ |         |

The upper bound of the v parametric range where the surface is defined. If not specified, the `vknot` value at index `nv` is used.

## Trim Curves

Trim curves remove part of the surface. The trimming is done by closed trim loops. Each loop is made of NURBS curves in the parametric space of the surface. The attributes below concatenate the values of all curves of all loops.

| Name                 | Type    | Default |
| -------------------- | ------- | ------- |
| `trimcurves.ncurves` | _`int`_ |         |

One value per trim loop: the number of curves in that loop. The number of values is the number of loops.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `trimcurves.n` | _`int`_ |         |

One value per curve: the number of control points of that curve.

> **Note:** The specification prints this attribute as `n`. The name that 3Delight reads is `trimcurves.n`.

| Name               | Type    | Default |
| ------------------ | ------- | ------- |
| `trimcurves.order` | _`int`_ |         |

One value per curve: the order of that curve.

| Name              | Type      | Default |
| ----------------- | --------- | ------- |
| `trimcurves.knot` | _`float`_ |         |

The knot vectors of all curves, with `n` + `order` values for each curve.

| Name             | Type      | Default |
| ---------------- | --------- | ------- |
| `trimcurves.min` | _`float`_ |         |

One value per curve: the lower bound of the valid parametric range of the curve.

| Name             | Type      | Default |
| ---------------- | --------- | ------- |
| `trimcurves.max` | _`float`_ |         |

One value per curve: the upper bound of the valid parametric range of the curve.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.u` | _`float`_ |         |

The u component of the control points of all curves.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.v` | _`float`_ |         |

The v component of the control points of all curves.

| Name           | Type      | Default |
| -------------- | --------- | ------- |
| `trimcurves.w` | _`float`_ |         |

The w component of the control points of all curves.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `trimcurves.inside` | _`int`_ | `1`     |

Optional. When 1, the part of the surface inside a trim loop is rendered. When 0, the part outside a trim loop is rendered.
