# Shared Boundaries: Topology Declarations

> Proposal, not implemented. This feature follows the [naming convention](../naming-convention.md). It adds shared topology across geometry types.

How can ɴsɪ preserve the fact that two surface boundaries belong to the same model edge?

A STEP solid supplies this information through its faces and shared edges. Exporting each face as a separate surface must preserve that relationship. The same declaration should connect polygon meshes, subdivision surfaces, and NURBS surfaces in any combination.

The declaration means: *these boundary uses represent the same edge and must stay joined when rendered*. Spatial coincidence alone does not declare a join. Two separate objects can touch without belonging together.

The renderer decides how to keep the declared join closed through tessellation and displacement. This proposal specifies topology, not displacement directions, parameter matching, or a welding algorithm. It does not require equal normals, materials, or texture coordinates across the join.

## Recommendation: Welds and Local Uses

`weld` names the relationship that the renderer must preserve. `weld-use` names one participating boundary occurrence. The name distinguishes this declaration from an edge geometry node.

Separate the shared identity from its occurrence on a surface:

- A `weld` node identifies one shared model edge. It needs no geometry attributes.
- A `weld-use` node selects one boundary occurrence on one surface.
- The use connects to both the weld and its surface.

This separation matters because a shared edge has different local descriptions on different surfaces. One side can be a NURBS trim curve; the other can be a subdivision boundary. A surface can also use the same edge twice, as at a periodic seam.

Proposed connection direction:

```text
                    +-> use_a.weld
shared_weld --------+
                    +-> use_b.weld

use_a ----------------> surface_a.weld-uses
use_b ----------------> surface_b.weld-uses
```

The `weld` input on each use accepts exactly one connection. The `weld-uses` input on geometry accepts multiple uses. Each use belongs to exactly one geometry node. Connections have no ordering requirement.

The graph attaches topology metadata to geometry through ordinary connections. Welds and uses do not render as separate objects. Their connections do not create additional geometry instances.

An illustrative C API fragment shows the structure. The node types and connection names are proposed; the API functions already exist:

```c
NSICreate(ctx, "weld_ab", "weld", 0, NULL);
NSICreate(ctx, "use_a", "weld-use", 0, NULL);
NSICreate(ctx, "use_b", "weld-use", 0, NULL);

/* Each use also carries its local boundary selector. */
NSIConnect(ctx, "weld_ab", "", "use_a", "weld", 0, NULL);
NSIConnect(ctx, "weld_ab", "", "use_b", "weld", 0, NULL);
NSIConnect(ctx, "use_a", "", "surface_a", "weld-uses", 0, NULL);
NSIConnect(ctx, "use_b", "", "surface_b", "weld-uses", 0, NULL);
```

The two surface nodes already exist in this example. No change to `NSIConnect` is needed. Renderer support for the new node types and connections is needed.

## What a Use Selects

A selector identifies existing surface topology. It does not duplicate the surface or add a 3D curve.

| Geometry | Local boundary selector |
| -------- | ----------------------- |
| NURBS natural boundary | One active-domain side: `u-min`, `u-max`, `v-min`, or `v-max` |
| NURBS trim | One trim-curve occurrence in the surface's trim data |
| Polygon mesh | One directed edge occurrence, identified by face, loop, and local edge index |
| Subdivision surface | One directed boundary edge occurrence in its control topology, denoting the corresponding limit-surface boundary |

A face-local mesh selector distinguishes occurrences that a pair of vertex indices can leave ambiguous. The loop identifies the outer perimeter or a polygon hole. The selector refers to authored topology, not a renderer's tessellation indices.

Subdivision schemes share the identity mechanism. Each scheme defines how its control topology identifies a surface boundary. This includes the draft [`t-nurcc`](../nodes/t-nurcc.md) representation. Joining two subdivision boundaries does not request a merge of their control cages.

Trim packaging stays independent. With inline trims, the selector identifies a curve in the surface's arrays. With [trim nodes](trim-curves-nodes.md), it identifies a connected trim node and a curve within it. A trim node reference would be a connection, not a handle stored in a string.

A use can retain the source model's orientation relative to the shared edge. Orientation expresses traversal direction only. It does not prescribe parameter correspondence or a renderer algorithm.

For a partial boundary, the selector also needs a local interval. At a T-junction, separate shared edges describe the spans on either side of the junction. Each span can select part of a longer patch side or mesh boundary. Exact selector attribute names and interval encoding remain a follow-up specification decision.

## Identity and Scene Structure

Two uses that connect to the same `weld` declare a join. Distinct weld nodes declare distinct identities, even when their boundaries coincide. More than two uses can share a weld, which expresses a non-manifold join. Two uses on the same surface can express a seam.

The weld node has no authoritative shape and no displacement settings. A STEP exporter can preserve shared-edge identity without exporting the model edge's separate 3D curve. Explicit endpoint nodes are not needed for this edge-belonging declaration.

Node handles identify definitions; rendered instances need a scope rule. Repeating a joined assembly should repeat its internal joins without joining separate copies. An initial specification can restrict joins to uniquely identified surface occurrences within one assembly occurrence. Joins across ambiguous instance paths need explicit occurrence addressing before they can be supported. This is a structural question for implementers, separate from welding algorithms.

Ordinary connections also make references visible to graph edits. Removing a use removes that boundary's membership. Missing required connections make a use incomplete; a missing weld node does not become an implicit identity token. Topology edits that change local indices must update the affected selectors.

## Alternatives and Trade-offs

| Representation | Benefit | Cost |
| -------------- | ------- | ---- |
| Inline edge IDs | Compact arrays; extends the existing stitching draft | Requires an identity namespace and per-geometry selector arrays; the relation is outside the connection graph |
| Shared `weld` with direct connections | One node per shared edge; fewer nodes than explicit uses | Local selectors need defined connection metadata or named attribute slots; repeated uses need distinct slots |
| Shared `weld` plus `weld-use` | Ordinary connections; each local occurrence has its own selector; supports mixed geometry and self-seams | One node per shared edge plus one node per use |
| Shared edge with a 3D curve | Also transports the model edge's geometry | Adds data that shared identity alone does not require |

Inline IDs are a reasonable compact alternative. Their identity should be scoped to an assembly or explicit topology namespace. Scene-global integers require coordination between exporters. The [existing NURBS stitching draft](nurbs-draft.md#stitching) already takes this approach; mesh selectors would extend it.

Direct connections are attractive if node count is the main concern. However, a connection between a weld and a surface does not identify which surface boundary participates. Encoding selectors in attribute names, or defining additional connection parameters, introduces another convention. Explicit use nodes keep those data in ordinary attributes and support independent edits.

The graph proposal therefore favors explicit uses for clarity. A later compact encoding could express the same relation if real scene sizes justify it. No performance advantage is assumed without measurement.

## Relation to the Existing Drafts

The [edge-node alternative for trim curves](trim-curves-edges.md) combines shared identity with an authoritative 3D curve. This proposal separates those decisions. A shared identity node is useful even when it carries no geometry.

The existing `trim-curves.edge-id` and `stitch.edge-id` proposals express the same basic belonging relation. They remain an alternative encoding, not attributes that this proposal requires alongside connections. A scene should not supply conflicting declarations through both forms.

This feature can use the proposed names without adopting the full node and attribute rename draft. It adds topology information that the current geometry definitions do not carry between nodes.

The remaining structural decisions are the use-node encoding, exact local selectors, and instance scope. Displacement and tessellation methods remain renderer decisions.
