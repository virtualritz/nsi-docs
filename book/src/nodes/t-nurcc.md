# `t-nurcc`

This node represents a T-NURCC — a Non-Uniform Rational Catmull-Clark surface with T-junctions, after Sederberg et al., [*T-splines and T-NURCCs*](https://doi.org/10.1145/1201775.882295) (SIGGRAPH 2003). It generalizes both of this API's smooth-surface primitives: with a regular grid cage it reduces to a bicubic NURBS surface, and with uniform knot intervals and no T-junctions it reduces to the Catmull-Clark limit surface of the [`mesh`](mesh.md) node. Its distinguishing features are arbitrary-topology control cages, local refinement through T-junctions, and per-edge knot intervals — together allowing a network of trimmed, stitched patches to be expressed as a *single watertight surface*.

> This node is a draft: no renderer implements it yet. Like [`nurbs`](nurbs.md), its attributes follow the [new naming convention](../naming-convention.md).

## Control Cage

The control cage is a polygon mesh, described exactly like the [`mesh`](mesh.md) node's topology. It has the following required attributes:

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `vertex-count` | _`int`_ |         |

The number of vertices for each face of the cage. The number of values for this attribute specifies the total face count. Four-sided faces are the norm; faces of other valences are allowed and behave as in Catmull-Clark subdivision.

One of `position` or `weighted-position` must be supplied to provide the control points. `position` defines a polynomial surface; `weighted-position` defines a rational one.

| Name       | Type      | Default |
| ---------- | --------- | ------- |
| `position` | _`point`_ |         |

The positions of the cage's control points. Addressed indirectly through a `position.indices` attribute holding the concatenated per-face vertex indices, as on the `mesh` node.

| Name                | Type         | Default |
| ------------------- | ------------ | ------- |
| `weighted-position` | _`float[4]`_ |         |

Rational alternative to `position`: each control point is four floats `(x, y, z, w)`. Addressed indirectly through `weighted-position.indices`.

### T-Junctions

T-junctions need no dedicated attribute — they are a property of the connectivity. A T-junction is a vertex that lies on the interior of a neighbouring face's edge: face *A* lists the edge `(a, b)` while the faces on the other side list `(a, t)` and `(t, b)`. The vertex `t` is a T-junction of face *A*.

A T-junction must not lie on a face incident to an extraordinary vertex (an interior cage vertex of valence other than 4); T-junctions and extraordinary vertices must be separated by at least one face.

## Knot Intervals

Each edge of the cage carries a non-negative knot interval — the parametric width the edge spans on the limit surface. Intervals default to `1` everywhere, which is the uniform (Catmull-Clark) case; only edges with non-unit intervals need to be listed. The two attributes below must be supplied together.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `knot-interval.index` | _`int`_ |         |

A list of edges, each specified as a pair of indices into the `position` attribute, like `position.indices`. Pair order is irrelevant here; an edge may be listed at most once.

| Name                  | Type      | Default |
| --------------------- | --------- | ------- |
| `knot-interval.value` | _`float`_ |         |

The knot interval of each listed edge. One value per pair in `knot-interval.index`. Values must be non-negative; a value of `0` is legal and produces a sharp feature, which is how T-NURCCs express creases and corners — no separate sharpness attributes exist on this node.

Knot intervals are subject to two consistency constraints:

- Opposing sides of a face must span equal parametric widths. For a plain four-sided face this means opposite edges carry equal intervals; where a side is subdivided by T-junctions, the *sum* of its sub-edge intervals must equal the opposing side's.
- Across a T-junction, the two sub-edges must sum to the undivided edge they subdivide: `interval(a, t) + interval(t, b) = interval(a, b)`.

## Stitching

A T-NURCC is watertight by construction, so the interior of the surface needs no stitching — that is its point. Stitching applies only to the *open borders* of a T-NURCC sheet, which can be welded to the boundaries of other nodes — `nurbs` patches or other `t-nurcc` sheets — using the same scene-global edge-identifier space defined in the `nurbs` node's [Stitching](nurbs.md#stitching) section. The two attributes below must be supplied together.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `stitch.index` | _`int`_ |         |

A list of boundary cage edges, each specified as a pair of indices into the `position` attribute. Unlike `knot-interval.index`, pair order is significant: listing `(a, b)` states that walking the boundary from `a` to `b` follows the shared edge's reference direction; reverse the pair to oppose it. No separate orientation attribute is needed.

| Name             | Type    | Default |
| ---------------- | ------- | ------- |
| `stitch.edge-id` | _`int`_ |         |

The edge identity of each listed boundary edge. One value per pair in `stitch.index`. Semantics are those of the `nurbs` node's `trim-curves.edge-id` / `stitch.edge-id`: boundaries anywhere in the scene carrying the same non-negative value trace the same model edge in 3D and are welded. The welded counterpart corresponds to the arc of the limit-surface boundary that the listed cage edge maps to.

## Semantics

The limit surface is defined by the NURCC subdivision rules of the paper cited above: bicubic, C² in regular regions with non-zero knot intervals, G¹ at extraordinary vertices, with T-junctions resolved by local knot insertion. Two reductions anchor the definition:

- A cage with no T-junctions, all knot intervals equal, and all weights equal renders identically to the same cage as a `mesh` node with `subdivision.scheme` `"catmull-clark"`.
- A cage that is a regular grid (every interior vertex of valence 4, no T-junctions) renders identically to the equivalent bicubic [`nurbs`](nurbs.md) node.

## Design Notes

This node is the complement of the `nurbs` stitching design. That design *conserves* the weld topology of a CAD shell across a network of trimmed patches; this node lets a pipeline *eliminate* it, by merging the network into one surface whose continuity is structural rather than declared. T-splines were conceived for exactly this merge, and the T-junctions are what make it lossless: local refinement absorbs patch boundaries that do not run through the whole network. Which representation to export is the pipeline's choice; the shared edge-identifier space lets the two coexist in one scene, welded to each other at their open borders.

It is a separate node type rather than an extension of `mesh` because its data model diverges in every direction that matters: rational control points, per-edge knot intervals, T-junction validity rules, and an evaluation scheme that is neither pure subdivision nor tensor-product NURBS.

Open questions for this draft:

- Boundary rules for open sheets (interpolating versus free boundaries).
- Semi-sharp creases. Zero knot intervals give infinitely sharp features only; a `crease.sharpness` mechanism like the `mesh` node's may still be wanted.
- Whether to restrict cages to the analysis-suitable ("standard") T-spline subset, or flag it.
- Trim curves on a T-NURCC are deliberately omitted: local refinement and open borders cover the use cases trimming covers on `nurbs`.
