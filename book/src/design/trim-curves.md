# Trim Curves: API Alternatives

The [`nurbs`](../nodes/nurbs.md) node is a draft with no implementation yet, which leaves one packaging question genuinely open: **where should trim-curve data live** — inline on the surface node, or in nodes of its own? This section lays out three alternatives with their rationale and trade-offs, as a basis for discussion with implementers. They share the same per-curve data model (counts, orders, knots, control points, hole flags, edge identities); they differ in *granularity*, *ordering semantics*, and *how welds are expressed*.

The criteria worth weighing:

- **Exporter ergonomics** — how much bookkeeping a STEP/IGES exporter needs. Evidence from a real exporter (the STEP → ɴꜱɪ BRep emitter in [monster-step-viewer](https://github.com/virtualritz/monster-step-viewer)) informed these pages.
- **API-call count** — more nodes means more `Create`/`Connect`/`SetAttribute` traffic. Implementer feedback: in an offline renderer this overhead is dwarfed by render time, so it should not by itself decide the design. Memory cost is likewise near-identical across all three.
- **Editability** — can a live session replace one hole without resending the rest?
- **Reuse** — can identical trim geometry be shared across faces?
- **Ordering** — curves within a loop are ordered head-to-tail; connections in ɴꜱɪ are unordered, so any node-based option must carry ordering as data.
- **Stitching fidelity** — how faithfully the CAD weld topology ([Stitching](../nodes/nurbs.md#stitching)) is conserved, and what the renderer can do with it.
- **Precedent** — RenderMan's `RiTrimCurve` was a separate entity from the patch it trimmed (graphics state applied to subsequent `RiNuPatch` calls); 3Delight's existing ɴꜱɪ carries `trimcurves.*` inline; BRep kernels and STEP store edges as first-class shared entities.

## The Options

| Criterion               | [1 — Inline](trim-curves-inline.md)  | [2 — `trim` nodes](trim-curves-nodes.md)    | [3 — `edge` nodes](trim-curves-edges.md)    |
| ----------------------- | ------------------------------------ | ------------------------------------------- | ------------------------------------------- |
| Trim data lives         | on the `nurbs` node                  | on `trim` nodes, connected                  | on the `nurbs` node (as Option 1)           |
| Weld identity           | integer ids                          | integer ids                                 | `edge` node handles                         |
| Nodes per trimmed face  | 1                                    | 1 + trim nodes (1 suffices)                 | 1 + shared edge nodes (~half per face)      |
| Ordering                | explicit arrays                      | whole loops per node — order-free           | explicit arrays                             |
| Independent loop edits  | no — resend the block                | yes — swap one node                         | no — resend the block                       |
| Reuse across faces      | no                                   | yes, for unstitched trims                   | edges shared by construction                |
| Authoritative 3D edge   | no                                   | no                                          | yes — enables crack-free re-tessellation    |
| Exporter complexity     | lowest                               | medium (handles, granularity)               | highest (two curve representations)         |
| Precedent               | 3Delight ɴꜱɪ `trimcurves.*`          | RenderMan `RiTrimCurve`                     | STEP / BRep kernel topology                 |

Options 2 and 3 are not mutually exclusive: 2 repackages the *per-face* data, 3 adds a node for the *shared* entity. Either could be adopted alone, or both together.

## Questions to Settle

1. **Granularity** — is trim data an atomic property of the surface (one blob, Option 1) or scene structure (loop-set nodes, Option 2)? Since call overhead is agreed to be negligible, this is a question of editing model and exporter ergonomics, not performance.
2. **Weld identity** — are welds out-of-band integers (Options 1/2) or graph objects (Option 3)? Integers are trivial to emit; handles cannot collide and can carry geometry.
3. **Is reuse real?** — Option 2's sharing only pays off for identical trim regions on identically parameterized faces (hole patterns, perforated panels), and conflicts with stitching (edge identities are per-use). Is that case common enough to shape the API?
4. **Does the renderer want authoritative 3D edges?** — Option 3 is the only one that lets tessellation and displacement reconcile against a single shared curve instead of reconciling two approximations against each other. If the answer is "eventually", Option 3's `edge` node can be specified now and implemented later — it degrades cleanly to Option 1.
