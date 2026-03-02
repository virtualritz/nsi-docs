# `curves`

This node represents a group of curves. It has the following required attributes:

| Name        | Type    | Default |
| ----------- | ------- | ------- |
| `nvertices` | _`int`_ |         |

The number of vertices for each curve. This must be at least 4 for cubic curves and 2 for linear curves. There can be either a single value or one value per curve.

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

The positions of the curve vertices. The number of values provided, divided by `nvertices`, gives the number of curves which will be rendered.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `width` | _`float`_ |         |

The width of the curves.

| Name    | Type       | Default       |
| ------- | ---------- | ------------- |
| `basis` | _`string`_ | `catmull-rom` |

The basis functions used for curve interpolation. Possible choices are:

- `b-spline` — B-spline interpolation.
- `catmull-rom` — Catmull-Rom interpolation.
- `linear` — Linear interpolation.
- `hobby` — Hobby interpolation.

| Name          | Type    | Default |
| ------------- | ------- | ------- |
| `extrapolate` | _`int`_ | `0`     |

By default, cubic curves will not be drawn to their end vertices as the basis functions require an extra vertex to define the curve. If this attribute is set to 1, an extra vertex is automatically extrapolated so the curves reach their end vertices, as with linear interpolation.

Attributes may also have a single value, one value per curve, one value per vertex or one value per vertex of a single curve, reused for all curves. Attributes which fall in that last category must always specify `NSIParamPerVertex`. Note that a single curve is considered a face as far as use of `NSIParamPerFace` is concerned.
