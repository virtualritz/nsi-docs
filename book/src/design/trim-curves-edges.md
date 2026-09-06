# Option 3: `edge` Nodes

The per-face trim data stays inline, exactly as in [Option 1](trim-curves-inline.md). A parametric curve has one consumer, the surface in whose domain it lives, so a move to a node gains nothing. The thing that genuinely *is* shared becomes a node: the **model edge**. This mirrors BRep topology directly. STEP stores each `edge_curve` once, and faces reference it through oriented uses. Here each model edge becomes one `edge` node, and faces reference it by handle.

An `edge` node carries a single 3D NURBS curve. That curve is the authoritative shape of the edge both faces meet at:

| Attribute                       | Type                           |
| ------------------------------- | ------------------------------ |
| `order`                         | _`int`_                        |
| `knot`                          | _`float`_                      |
| `min`, `max`                    | _`float`_                      |
| `position`/`position-weighted`  | _`point`_/_`weighted-point`_   |

The node handle is the identity. On the `nurbs` node, the integer ids of the current draft become handle references:

- `trim-curves.edge-id` (_`int`_) -> `trim-curves.edge` (_`string`_, one handle per curve, `""` = none)
- `stitch.edge-id` (_`int[4]`_) -> `stitch.edge` (_`string[4]`_)
- `trim-curves.edge-orientation`/`stitch.edge-orientation` do not change. Orientation is relative to the parametric direction of the edge curve, which is now explicit.

```
Create "edge_301" "edge"
SetAttribute "edge_301" "order" "int" 1 [4] ...

Create "face_12" "nurbs"
SetAttribute "face_12" ... "trim-curves.edge" "string" 5 ["edge_301" "" ...] ...
Create "face_13" "nurbs"
SetAttribute "face_13" ... "trim-curves.edge" "string" 4 ["edge_301" ...] ...
```

A handle that resolves to no node is legal. It acts as a pure identity token, so two faces that name the same missing handle are still welded. The scheme therefore *degrades to Option 1* for exporters that do not emit edge geometry; the ids simply happen to be strings. Renderers may implement resolution incrementally.

When the node exists, its curve is authoritative. A face's parametric curve, mapped through its surface, can disagree with the edge curve. The edge curve then defines the true boundary position. The parametric curves define the locus in the parameter domain and the trimmed-region classification.

## What the shared curve buys

Only this option changes what a renderer can *do*, rather than how the API packages data:

- **One boundary, whatever the evaluation strategy.** Backends differ in how they realize a NURBS surface. 3Delight renders it analytically, and dices only a surface that carries displacement. A GPU backend would tessellate everything. The obligation of stitching is visual watertightness, and it must hold under both strategies. A shared edge curve serves both. An analytic renderer resolves the common boundary of the two faces to the same exact curve. A tessellating backend welds its meshes along samples of that same curve. Neither backend must reconcile two floating-point approximations that drift apart. The sampled-trim fallback in the monster-step-viewer exporter is exactly such a drift source.
- **Exact displacement reconciliation.** Derive the welded displacement once, on the edge curve, and apply it to every use.
- **Reusable topology.** The same nodes serve BRep wireframe rendering and exact re-projection. Open borders of a `t-nurcc` node weld against them identically.
- **Collision-free identity.** Handles are unique by construction. Integer ids from two exporters that feed one scene can collide silently.

## Pros

- Faithful conservation of CAD topology -- the scene graph *shows* that two faces share an edge.
- Everything under "What the shared curve buys" above.
- Additive: specify it now and adopt it incrementally, because dangling handles reduce to Option 1 semantics.

## Cons

- The heaviest option. Exporters emit a second curve representation: 3D edge curves in addition to the parametric curves. They also emit roughly one edge node per two face-uses, so edge nodes outnumber faces in typical solids.
- Cross-node references by a handle-valued *attribute*, rather than by a connection, are a new pattern for ɴsɪ. Dependency tracking and deletion semantics need explicit rules. A parallel `Connect` into an `edges` attribute, purely for lifetime bookkeeping, is one alternative. This point is undecided.
- The boundary gets two sources of truth, the parametric curve and the edge curve. They need the precedence rule above, and the exporter owns any tolerance disagreement between them.
- Renderers must at least parse and ignore the references, even if they never use the geometry.
