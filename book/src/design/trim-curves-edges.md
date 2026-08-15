# Option 3 — `edge` Nodes

The per-face trim data stays inline exactly as in [Option 1](trim-curves-inline.md) — a parametric curve has one consumer, the surface in whose domain it lives, so nothing is gained by moving it. What becomes a node is the thing that genuinely *is* shared: the **model edge**. This mirrors BRep topology directly: STEP stores each `edge_curve` once, and faces reference it through oriented uses; here each model edge becomes one `edge` node, and faces reference it by handle.

An `edge` node carries a single 3D NURBS curve — the authoritative shape of the edge both faces meet at:

| Attribute                       | Type                        |
| ------------------------------- | --------------------------- |
| `order`                         | _`int`_                     |
| `knot`                          | _`float`_                   |
| `min`, `max`                    | _`float`_                   |
| `position` / `position-weighted`| _`point`_ / _`float[4]`_    |

Identity is the node handle. On the `nurbs` node, the integer ids of the current draft become handle references:

- `trim-curves.edge-id` (_`int`_) → `trim-curves.edge` (_`string`_, one handle per curve, `""` = none)
- `stitch.edge-id` (_`int[4]`_) → `stitch.edge` (_`string[4]`_)
- `trim-curves.edge-orientation` / `stitch.edge-orientation` are unchanged — orientation is relative to the edge curve's parametric direction, which is now explicit.

```
Create "edge_301" "edge"
SetAttribute "edge_301" "order" "int" 1 [4] ...

Create "face_12" "nurbs"
SetAttribute "face_12" ... "trim-curves.edge" "string" 5 ["edge_301" "" ...] ...
Create "face_13" "nurbs"
SetAttribute "face_13" ... "trim-curves.edge" "string" 4 ["edge_301" ...] ...
```

A handle that resolves to no node is legal and acts as a pure identity token — two faces naming the same missing handle are still welded. The scheme therefore *degrades to Option 1* (ids happen to be strings) for exporters that don't emit edge geometry, and renderers may implement resolution incrementally.

When the node exists, its curve is authoritative: where a face's parametric curve (mapped through its surface) and the edge curve disagree, the edge curve defines the true boundary position; the parametric curves define the locus in the parameter domain and the trimmed-region classification.

## What the shared curve buys

This is the only option that changes what a renderer can *do*, rather than how data is packaged:

- **Crack-free tessellation.** Adjacent faces tessellate their shared boundary by sampling the *same* curve instead of two floating-point approximations of it — closing the gaps that trim-tolerance drift opens today (the sampled-trim fallback in the monster-step-viewer exporter is exactly such a drift source).
- **Exact displacement reconciliation.** Welded displacement can be derived once, on the edge curve, and applied to every use.
- **Reusable topology.** The same nodes serve BRep wireframe rendering and exact re-projection, and `t-nurcc` open borders weld against them identically.
- **Collision-free identity.** Handles are unique by construction; integer ids from two exporters feeding one scene can collide silently.

## Pros

- Faithful conservation of CAD topology — the scene graph *shows* that two faces share an edge.
- Everything under "What the shared curve buys" above.
- Additive: it can be specified now and adopted incrementally, since dangling handles reduce to Option 1 semantics.

## Cons

- The heaviest option: exporters emit a second curve representation (3D edge curves in addition to the parametric curves), and roughly one edge node per two face-uses — edge nodes outnumber faces in typical solids.
- Cross-node references by handle-valued *attribute* rather than by connection are a new pattern for ɴꜱɪ; dependency tracking and deletion semantics need explicit rules (or a parallel `Connect` into an `edges` attribute purely for lifetime bookkeeping — to be decided).
- Two sources of truth for the boundary (parametric curve vs edge curve) require the precedence rule above, and tolerance disagreements between them become the exporter's bug to own.
- Renderers must at minimum parse and ignore the references even if they never use the geometry.
