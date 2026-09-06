# Geometry in the Type System

The [`nurbs`](../nodes/nurbs.md) and [`t-nurcc`](../nodes/t-nurcc.md) drafts raise a type-system question. Rational control points are homogeneous `(wx, wy, wz, w)` tuples. The legacy API passed them as `float` arrays of length 4, together with a spec warning about how *not* to declare them. Trim curves add a second case. Their control points are `(u, v)` or homogeneous `(u, v, w)` tuples in the surface's parameter domain. What type should these tuples have?

## What ɴsɪ's types actually encode

`point`, `vector`, and `normal` occupy identical storage -- three floats. The type distinguishes *behavior*: how the value responds to a transform. Points translate, vectors do not, and normals transform by the inverse transpose. Size was never the distinguishing axis, because `float` plus an array length already expresses any size. This observation decides both questions.

**A rational control point is transformable geometry with its own rule.** The four components transform as one unit under a 4x4 matrix, which is exactly why rational NURBS survive projective transforms. A `float[4]` hides that rule from every generic consumer. The legacy warning ("do **not** declare with `array_len(4)`") is a design smell: it admits that the type is missing. Hence the draft type:

| Constant               | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| `NSITypeWeightedPoint` | Weighted (homogeneous) point `(wx, wy, wz, w)`, four 32-bit floats. |

Under the [naming convention](../naming-convention.md) it reads as _`weighted-point`_. The [Type Names](type-names.md) draft asks whether that name should also carry a storage width. That name uses the vocabulary the attributes already use, as in `position-weighted`. RenderMan's type system grew `hpoint` for exactly this attribute.

**Trim-curve control points are the opposite case.** `(u, v, w)` is a *projective 2D* point in the surface's parameter domain. It is not `point`-typed data that happens to be small. A `point` type would be wrong twice. First, it misstates the geometry: the point is projective 2D, not Euclidean 3D. Second, it invites type-correct corruption. A transform-baking tool, an instancing optimizer, or a space-converting importer would do the right thing for `point` data. It would then destroy every trim curve, because parameter-space data must never transform.

## The principle

> **Semantic types are for geometry that transforms; `float[N]` is the honest type for inert tuples.**
>
> `point`, `vector`, `normal`, `weighted-point` each name a transform rule. Data that no transform ever applies to -- parameter-space coordinates, knots, weights on their own -- is typed `float` with an array length, deliberately.

This principle is why `trim-curves.position` is _`float[2]`_ and `trim-curves.position-weighted` is _`float[3]`_, while the surface's `position-weighted` is _`weighted-point`_. The first two live in the parameter domain; the third lives in object space. The `float[4]` smell was never the tuple. It was the inert typing of *transformable* geometry.

## The alternative considered: a dimensional family

A symmetric family was considered and rejected: `point-2d`, `point`, and `point-4d`, with bare `point` keeping parity with `vector` and `normal`.

**For it:** the family is discoverable and uniform, it gives every tuple in the API a typed home, and one rule covers future needs.

**Against it, decisively:** the family encodes the wrong axis. Size is already expressible. Behavior is what the type system uniquely encodes, and the dimensional names leave that behavior as fine print. `point-4d` does not say *homogeneous*; it could mean a 4D position, or four channels. `point-2d` does not say *parametric, never transforms*. Each member would need exactly the per-type behavioral documentation whose absence the family was meant to cure. The family also invites a combinatorial zoo: `vector-2d`, `normal-4d`, and more. The projective-2D trim point still fits nowhere in it, as three floats that would masquerade as a 3D point.

Industry precedent supports the semantic choice on both sides. RenderMan named its four-float type `hpoint`, which is a behavior, not a size. USD faced the 2D question directly and typed texture coordinates as the semantic role `texCoord2f`, not as the dimensional `float2`. It did so precisely so that tools know the data is parametric rather than spatial.

## Door left open

Generic tooling may one day need parameter-space data to be self-describing, for inspectors that plot trim curves without node-specific knowledge. The consistent move is then a semantic role, a `parametric-point` in the spirit of USD's `texCoord2f`, not a dimensional `point-2d`. This page reserves the name. It is deliberately not part of the current draft.
