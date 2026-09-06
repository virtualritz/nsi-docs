# `t-nurcc`

This node represents a T-NURCC, a Non-Uniform Rational Catmull-Clark surface with T-junctions, after Sederberg et al., [*T-splines and T-NURCCs*](https://doi.org/10.1145/1201775.882295) (SIGGRAPH 2003). It generalizes both smooth-surface primitives of this API. With a regular grid cage it reduces to a bicubic NURBS surface. With uniform knot intervals and no T-junctions it reduces to the Catmull-Clark limit surface of the [`mesh`](mesh.md) node. Three features distinguish it:

- arbitrary-topology control cages
- local refinement through T-junctions
- per-edge knot intervals

Together these features express a network of trimmed, stitched patches as a *single watertight surface*.

> This node is a draft: no renderer implements it yet. Like [`nurbs`](nurbs.md), its attributes follow the [new naming convention](../naming-convention.md).

## Control Cage

The control cage is a polygon mesh. It is described exactly like the topology of the [`mesh`](mesh.md) node. It has the following required attributes:

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `vertex-count` | _`int`_ |         |

The number of vertices for each face of the cage. The number of values for this attribute specifies the total face count. Four-sided faces are the norm. Faces of other valences are allowed and behave as in Catmull-Clark subdivision.

Supply one of `position` or `position-weighted` to provide the control points. `position` defines a polynomial surface. `position-weighted` defines a rational one.

| Name       | Type      | Default |
| ---------- | --------- | ------- |
| `position` | _`point`_ |         |

The positions of the cage's control points. Address them indirectly through a `position.indices` attribute, which holds the concatenated per-face vertex indices, as on the `mesh` node.

| Name                | Type               | Default |
| ------------------- | ------------------ | ------- |
| `position-weighted` | _`weighted-point`_ |         |

Rational alternative to `position`. Each control point is a weighted (homogeneous) point `(wx, wy, wz, w)`. Address the points indirectly through `position-weighted.indices`.

### T-Junctions

T-junctions need no dedicated attribute. They are a property of the connectivity. A T-junction is a vertex that lies on the interior of a neighbouring face's edge. Face *A* lists the edge `(a, b)`, while the faces on the other side list `(a, t)` and `(t, b)`. The vertex `t` is a T-junction of face *A*.

A T-junction must not lie on a face incident to an extraordinary vertex, which is an interior cage vertex of valence other than 4. At least one face must separate a T-junction from an extraordinary vertex.

## Knot Intervals

Each edge of the cage carries a non-negative knot interval. The interval is the parametric width the edge spans on the limit surface. Intervals default to `1` everywhere, which is the uniform (Catmull-Clark) case. List only the edges with non-unit intervals. Supply the two attributes below together.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `knot-interval.index` | _`int`_ |         |

A list of edges. Specify each edge as a pair of indices into the `position` attribute, like `position.indices`. Pair order is irrelevant here. List an edge at most once.

| Name                  | Type      | Default |
| --------------------- | --------- | ------- |
| `knot-interval.value` | _`float`_ |         |

The knot interval of each listed edge. Supply one value per pair in `knot-interval.index`. Values must be non-negative. A value of `0` is legal and produces a sharp feature. T-NURCCs express creases and corners this way, so this node has no separate sharpness attributes.

Knot intervals are subject to two consistency constraints:

- Opposing sides of a face must span equal parametric widths. For a plain four-sided face, opposite edges carry equal intervals. Where T-junctions subdivide a side, the *sum* of its sub-edge intervals must equal the interval of the opposing side.
- Across a T-junction, the two sub-edges must sum to the undivided edge they subdivide: `interval(a, t) + interval(t, b) = interval(a, b)`.

## Stitching

A T-NURCC is watertight by construction, so the interior of the surface needs no stitching. That is the point of the node. Stitching applies only to the *open borders* of a T-NURCC sheet. Weld those borders to the boundaries of other nodes, either `nurbs` patches or other `t-nurcc` sheets. The weld uses the same scene-global edge-identifier space that the [Stitching](nurbs.md#stitching) section of the `nurbs` node defines. Supply the two attributes below together.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `stitch.index` | _`int`_ |         |

A list of boundary cage edges. Specify each edge as a pair of indices into the `position` attribute. Unlike `knot-interval.index`, pair order is significant. The pair `(a, b)` states that a walk along the boundary from `a` to `b` follows the reference direction of the shared edge. Reverse the pair to oppose that direction. No separate orientation attribute is needed.

| Name             | Type    | Default |
| ---------------- | ------- | ------- |
| `stitch.edge-id` | _`int`_ |         |

The edge identity of each listed boundary edge. Supply one value per pair in `stitch.index`. The semantics are those of the `trim-curves.edge-id`/`stitch.edge-id` attributes of the `nurbs` node. Boundaries anywhere in the scene that carry the same non-negative value trace the same model edge in 3D, and the renderer welds them. The welded counterpart is the arc of the limit-surface boundary that the listed cage edge maps to.

## Semantics

The NURCC subdivision rules of the paper cited above define the limit surface. The surface is bicubic. It is C² in regular regions with non-zero knot intervals, and G¹ at extraordinary vertices. Local knot insertion resolves the T-junctions. Two reductions anchor the definition:

- A cage can have no T-junctions, equal knot intervals throughout, and equal weights. Such a cage renders identically to the same cage as a `mesh` node with `subdivision.scheme` `"catmull-clark"`.
- A cage can be a regular grid: every interior vertex has valence 4, and no T-junctions exist. Such a cage renders identically to the equivalent bicubic [`nurbs`](nurbs.md) node.

## Design Notes

This node is the complement of the `nurbs` stitching design. That design *conserves* the weld topology of a CAD shell across a network of trimmed patches. This node lets a pipeline *eliminate* that topology instead. The pipeline merges the network into one surface, whose continuity is structural rather than declared. T-splines were conceived for exactly this merge. The T-junctions make it lossless, because local refinement absorbs patch boundaries that do not run through the whole network. The pipeline chooses which representation to export. The shared edge-identifier space lets the two representations coexist in one scene, welded to each other at their open borders.

This node is a separate node type rather than an extension of `mesh`. Its data model diverges in every direction that matters:

- rational control points
- per-edge knot intervals
- T-junction validity rules
- an evaluation scheme that is neither pure subdivision nor tensor-product NURBS

Open questions for this draft:

- Boundary rules for open sheets: interpolating boundaries versus free boundaries.
- Semi-sharp creases. Zero knot intervals give infinitely sharp features only. A `crease.sharpness` mechanism like the one of the `mesh` node may still be wanted.
- Whether to restrict cages to the analysis-suitable ("standard") T-spline subset, or to flag that subset.
- Trim curves on a T-NURCC are deliberately omitted. Local refinement and open borders cover the use cases that trimming covers on `nurbs`.
