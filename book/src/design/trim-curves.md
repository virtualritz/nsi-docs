# Trim Curves: API Alternatives

Where should a NURBS surface's trim data live? This packaging decision is separate from how surfaces declare shared boundaries.

The shipped [`nurbs`](../nodes/nurbs.md) node stores trim curves inline under the legacy names. The [NURBS draft](nurbs-draft.md#trim-curves) describes renamed attributes and proposed extensions. Both inline data and separate trim nodes can describe a hole made from several curves.

The [shared-boundary design](shared-boundaries.md) owns the stitching alternatives and their trade-offs. Its recommended `weld` node supplies one namespace for many joins. A local boundary use can select one curve, a whole loop, or an ordered chain. Trim packaging does not require one weld node per curve.

## Packaging Options

| Criterion | [Inline attributes](trim-curves-inline.md) | [Separate `trim` nodes](trim-curves-nodes.md) |
| --------- | ------------------------------------------ | ------------------------------------------ |
| Trim data lives | On the surface | On connected nodes |
| Extra trim nodes | None | One per loop group |
| Curve ordering | Arrays within each loop | Arrays within each loop; loops stay within one node |
| Independent loop edits | Replace the surface's trim data | Replace one connected loop group |
| Reuse | Through geometry instancing | Unstitched trim patterns can serve compatible surfaces |
| Weld identity | IDs in a connected weld namespace | Same namespace, obtained through the consuming surface |

Connections need no ordering because each trim node carries complete loops. A loop can contain any supported number of curve segments. Loop membership and curve order are data, not connection order.

The inline encoding minimizes exporter bookkeeping. Separate nodes make loop groups independently editable. Neither encoding has an assumed memory or rendering advantage; those costs need measurement.

## Shared 3D Edges Are a Separate Extension

The earlier [Option 3: `edge` Nodes](trim-curves-edges.md) also exported a model edge's 3D curve. It is not a third place to store trim data. A 3D curve could accompany either packaging option and either weld-identity encoding.

A trim curve describes a boundary in one surface's parameter domain. A weld declaration states which boundaries belong together. A model-edge curve supplies additional geometry. Keeping these roles separate lets an exporter preserve topology without exporting redundant curves.

## Decisions to Settle

The trim decision is whether exporters and editors need independent loop-group nodes. The [weld decision](shared-boundaries.md#alternatives-and-trade-offs) is how to encode shared identity and boundary uses. Optional model-edge geometry should be considered only when a consumer needs that geometry.
