# `nurbs-curves`

> Draft node, not implemented. This proposal follows the [naming convention](../naming-convention.md), including its decision to retain `P` and `Pw`.

This node represents a collection of renderable NURBS curves. It supports wireframe rendering and other uses of curves with width. One node can contain many curves with different orders, knot vectors, and control-point counts.

The node uses the appearance and attribute-assignment model of [`curves`](curves.md). Explicit orders and knots replace `basis` and `extrapolate`. These two attributes do not apply to this node.

## Curve Geometry

| Name | Type | Required data |
| ---- | ---- | ------------- |
| `vertex-count` | _`int`_ | One control-point count per curve |
| `order` | _`int`_ | One order per curve |
| `knot` | _`float`_ | Concatenated knot vectors, in curve order |
| `min` | _`float`_ | One active-range start per curve |
| `max` | _`float`_ | One active-range end per curve |
| `P` | _`point`_ | Concatenated non-rational control points |
| `Pw` | _`hpoint`_ | Concatenated rational control points, as an alternative to `P` |
| `width` | _`float`_ | Curve width, with the assignment rules below |

The length of `vertex-count` gives the number of curves. The topology arrays contain one value per curve, even when several curves share an order or count. Supply exactly one of `P` and `Pw`.

For curve `i`, let `n = vertex-count[i]` and `k = order[i]`. The order is the degree plus one. Valid data satisfies `2 <= k <= n`. The curve has `n + k` knots in nondecreasing order.

Within the active range, an interior knot may occur at most `k - 1` times. This keeps each curve continuous. Disconnected pieces use separate curves.

With zero-based indices in that curve's knot vector, the active range satisfies `knot[k-1] <= min < max <= knot[n]`. The point-array length equals the sum of the control-point counts. The knot-array length equals the sum of `vertex-count[i] + order[i]`.

A `Pw` control point contains `(wx, wy, wz, w)`. Its type matches the existing [`nurbs`](nurbs.md) node. This proposal requires positive weights. The node does not approximate missing knots or change an invalid order.

The explicit knot vector and active range determine endpoint behavior. A closed curve includes its closure in its geometry and knots. No separate periodic flag or automatic endpoint extrapolation applies.

## Width and Other Attributes

As with `curves`, a single curve counts as one face for `NSIParamPerFace`. Attributes can contain one value for the whole node, one per curve, or one per control point. A control-point array can repeat across curves with equal counts when supplied with `NSIParamPerVertex`, as on `curves`.

A value assigned per curve is constant along that curve. A value assigned per control point follows the curve's spline basis. For rational curves, this proposal uses the normalized rational basis for these values, including width. This interpolation choice requires renderer review before adoption.

Shader and geometry attributes use the same connections and inheritance rules as `curves`. A renderer's curve-shape options also apply to this node. The NURBS representation alone does not select ribbons, tubes, caps, or a junction shape.

## Example

This example defines two linear NURBS curves. Curve 0 ends at `(1, 0, 0)`, where curve 1 starts. Geometry coincidence alone does not declare a weld.

```text
Create "wires" "nurbs-curves"
SetAttribute "wires"
    "vertex-count" "int" 2 [2 2]
    "order" "int" 2 [2 2]
    "knot" "float" 8 [0 0 1 1  0 0 1 1]
    "min" "float" 2 [0 0]
    "max" "float" 2 [1 1]
    "P" "point" 4 [0 0 0  1 0 0  1 0 0  1 1 0]
    "width" "float" 1 [0.01]
```

## Point Welds

The proposed [curve point-weld table](../design/curve-point-welds.md) selects endpoints or interior parameter values. It declares joins through the same `weld` namespace used for surface boundaries. The renderer must preserve these joins under displacement so the curve network does not tear apart. Junction construction and appearance are renderer implementation details. It does not make the curve authoritative over another surface's boundary.
