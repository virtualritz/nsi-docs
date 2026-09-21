# Retired: `edge` Nodes

The proposal for one geometry-bearing `edge` node per shared boundary is retired.

- [Shared-boundary declarations](shared-boundaries.md) preserve which surface boundaries belong together.
- [`nurbs-curves`](../nodes/nurbs-curves.md) defines renderable 3D curve collections, including wireframe geometry.
- [Curve point welds](curve-point-welds.md) propose joins at curve endpoints and interior parameter values.

A renderable curve does not become the authoritative shape of a surface boundary. Curve geometry and weld identity remain separate.
