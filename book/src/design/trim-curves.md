# Trim Curves: API Alternatives

The [`nurbs`](../nodes/nurbs.md) node is a draft. No implementation exists yet. One packaging question therefore stays open: **where does trim-curve data live**? It can live inline on the surface node, or in nodes of its own. This section gives three alternatives with their rationale and trade-offs, as a basis for discussion with implementers. All three share the same per-curve data model: counts, orders, knots, control points, hole flags, and edge identities. They differ in *granularity*, in *ordering semantics*, and in *how each option expresses welds*.

The criteria worth weighing:

- **Exporter ergonomics** -- how much bookkeeping a STEP/IGES exporter needs. A real exporter informed these pages: the STEP -> ɴsɪ BRep emitter in [monster-step-viewer](https://github.com/virtualritz/monster-step-viewer).
- **API-call count** -- more nodes mean more `Create`/`Connect`/`SetAttribute` traffic. Implementers report that render time dwarfs this overhead in an offline renderer. The overhead must therefore not decide the design alone. Memory cost is also near-identical across all three options.
- **Editability** -- can a live session replace one hole without a resend of the rest?
- **Reuse** -- can two faces share identical trim geometry?
- **Ordering** -- a loop orders its curves head-to-tail. Connections in ɴsɪ have no order. A node-based option must therefore carry the order as data.
- **Stitching fidelity** -- how well the option conserves the CAD weld topology ([Stitching](../nodes/nurbs.md#stitching)), and what the renderer can do with it.
- **Precedent** -- three prior designs differ:
  - RenderMan's `RiTrimCurve` was a separate entity from the patch it trimmed. It set graphics state for the `RiNuPatch` calls that followed.
  - The existing 3Delight ɴsɪ carries `trimcurves.*` inline.
  - BRep kernels and STEP store edges as first-class shared entities.

## The Options

| Criterion               | [1 -- Inline](trim-curves-inline.md) | [2 -- `trim` nodes](trim-curves-nodes.md)   | [3 -- `edge` nodes](trim-curves-edges.md)   |
| ----------------------- | ------------------------------------ | ------------------------------------------- | ------------------------------------------- |
| Trim data lives         | on the `nurbs` node                  | on `trim` nodes, connected                  | on the `nurbs` node (as Option 1)           |
| Weld identity           | integer ids                          | integer ids                                 | `edge` node handles                         |
| Nodes per trimmed face  | 1                                    | 1 + trim nodes (1 suffices)                 | 1 + shared edge nodes (~half per face)      |
| Ordering                | explicit arrays                      | whole loops per node -- order-free          | explicit arrays                             |
| Independent loop edits  | no -- resend the block               | yes -- swap one node                        | no -- resend the block                      |
| Reuse across faces      | no                                   | yes, for unstitched trims                   | edges shared by construction                |
| Authoritative 3D edge   | no                                   | no                                          | yes -- one exact common boundary            |
| Exporter complexity     | lowest                               | medium (handles, granularity)               | highest (two curve representations)         |
| Precedent               | 3Delight ɴsɪ `trimcurves.*`          | RenderMan `RiTrimCurve`                     | STEP/BRep kernel topology                   |

Option 2 and Option 3 are not mutually exclusive. Option 2 repackages the *per-face* data. Option 3 adds a node for the *shared* entity. Adopt either option alone, or both together.

## Questions to Settle

1. **Granularity** -- is trim data an atomic property of the surface (one blob, Option 1) or scene structure (loop-set nodes, Option 2)? Call overhead is negligible, as agreed above. This question is therefore about the editing model and exporter ergonomics, not about performance.
2. **Weld identity** -- are welds out-of-band integers (Option 1 and Option 2) or graph objects (Option 3)? Integers are easy to emit. Handles cannot collide, and they can carry geometry.
3. **Is reuse real?** -- Option 2 shares trim data only between identical trim regions on identically parameterized faces, such as hole patterns and perforated panels. The sharing also conflicts with stitching, because edge identities are per-use. Is that case common enough to shape the API?
4. **Does the renderer want authoritative 3D edges?** -- only Option 3 reconciles boundary evaluation and displacement against a single shared curve. Every other option reconciles two approximations of that curve. Option 3 does so whatever the evaluation strategy. An analytic backend resolves both faces to the exact curve; 3Delight dices only displacement-mapped surfaces. A tessellating backend, such as a GPU renderer, welds its meshes along samples of the same curve. If the answer is "eventually", specify the `edge` node of Option 3 now and implement it later. It degrades cleanly to Option 1.
