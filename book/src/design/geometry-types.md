# Geometry in the Type System

The [`nurbs`](../nodes/nurbs.md) and [`t-nurcc`](../nodes/t-nurcc.md) drafts raise a type-system question: rational control points are homogeneous `(wx, wy, wz, w)` tuples, and the legacy API passed them as `float` arrays of length 4 — complete with a spec warning about how *not* to declare them. Trim curves add a second case: their control points are `(u, v)` or homogeneous `(u, v, w)` tuples in the surface's parameter domain. What should these be typed as?

## What ɴꜱɪ's types actually encode

`point`, `vector`, and `normal` occupy identical storage — three floats. The type distinguishes *behavior*: how the value responds to a transform (points translate, vectors don't, normals transform by the inverse transpose). Size was never the distinguishing axis; `float` plus an array length already expresses any size. This observation decides both questions.

**A rational control point is transformable geometry with its own rule** — the four components transform as one unit under a 4×4 matrix, which is exactly why rational NURBS survive projective transforms. Passing it as `float[4]` hides that from every generic consumer, and the legacy warning ("do **not** declare with `array_len(4)`") is a design smell admitting the type is missing. Hence the draft type:

| Constant               | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| `NSITypeWeightedPoint` | Weighted (homogeneous) point `(wx, wy, wz, w)`, four 32-bit floats. |

Under the [naming convention](../naming-convention.md) it reads as _`weighted-point`_ — the vocabulary the attributes already use (`position-weighted`). RenderMan's type system grew `hpoint` for exactly this attribute.

**Trim-curve control points are the opposite case.** `(u, v, w)` is a *projective 2D* point in the surface's parameter domain. It is not `point`-typed data that happens to be small — typing it `point` would be wrong twice: it misstates the geometry (projective 2D, not Euclidean 3D), and it invites type-correct corruption — a transform-baking tool, instancing optimizer, or space-converting importer doing the right thing for `point` data would destroy every trim curve, because parameter-space data must never transform.

## The principle

> **Semantic types are for geometry that transforms; `float[N]` is the honest type for inert tuples.**
>
> `point`, `vector`, `normal`, `weighted-point` each name a transform rule. Data that no transform ever applies to — parameter-space coordinates, knots, weights on their own — is typed `float` with an array length, deliberately.

This is why `trim-curves.position` is _`float[2]`_ and `trim-curves.position-weighted` is _`float[3]`_, while the surface's `position-weighted` is _`weighted-point`_: the former live in the parameter domain, the latter in object space. The `float[4]` smell was never the tuple — it was inert-typing *transformable* geometry.

## The alternative considered: a dimensional family

A symmetric family — `point-2d`, `point`, `point-4d`, with bare `point` keeping parity with `vector` and `normal` — was considered and rejected.

**For it:** discoverable, uniform, gives every tuple in the API a typed home, and one rule covers future needs.

**Against it, decisively:** it encodes the wrong axis. Size is already expressible; behavior is what the type system uniquely encodes, and the dimensional names leave it as fine print — `point-4d` does not say *homogeneous* (a 4D position? four channels?), `point-2d` does not say *parametric, never transforms*. Each member would need exactly the per-type behavioral documentation whose absence the family was meant to cure, while inviting a combinatorial zoo (`vector-2d`? `normal-4d`?). And the projective-2D trim point still fits nowhere: three floats that would masquerade as a 3D point.

Industry precedent supports the semantic choice on both sides: RenderMan named its four-float type `hpoint` (a behavior, not a size), and USD — facing the 2D question directly — typed texture coordinates as the semantic role `texCoord2f` rather than the dimensional `float2`, precisely so tools know the data is parametric rather than spatial.

## Door left open

If generic tooling ever needs parameter-space data to be self-describing (inspectors plotting trim curves without node-specific knowledge), the consistent move is a semantic role — a `parametric-point`, in the spirit of USD's `texCoord2f` — not a dimensional `point-2d`. The name is reserved here; it is deliberately not part of the current draft.
