# Option 3: `edge` Nodes

> Historical alternative, now separated into identity and optional geometry. The [shared-boundary design](shared-boundaries.md) owns the unified stitching proposal and its trade-offs.

The original option combined two roles in one `edge` node: shared identity and an authoritative 3D NURBS curve. Surfaces referred to that node through handle-valued attributes. This required roughly one node per model edge, in addition to the surface nodes.

The revised design separates those roles. A `weld` node can supply an identity namespace for all joins in a solid. Local use tables identify the participating boundaries, including chains of multiple trim curves or mesh edges. Those declarations do not require a shared 3D curve.

## What Additional Geometry Could Provide

An exporter might also preserve the source model's 3D edge curves for wireframe rendering or other geometry consumers. Such a curve would need an order, knots, a parameter range, and control points. Those are additional geometry, not required weld metadata.

A shared curve does not identify which trim loop, patch side, or mesh boundary uses it. Local selectors remain necessary. Nor does a shared curve by itself specify how a renderer reconciles displacement. That algorithm remains the renderer's responsibility.

## Trade-offs

The benefit is preservation of source geometry that a consumer might otherwise reconstruct. The cost is another curve representation and its relationship to the surface boundaries. An authoritative-curve extension would also need to state what happens when those representations disagree.

The original handle-valued attributes required custom lookup, dependency, and deletion semantics. Its missing-handle fallback treated unresolved references as identity tokens. The current recommendation uses ordinary connections to a real `weld` node instead. A disconnected declaration does not acquire a scene-global identity.

This extension remains optional and unspecified. It is not necessary to keep joined surfaces joined, and it makes no claim that an existing exporter produces cracks.
