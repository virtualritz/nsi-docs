# Node Types: Naming and Granularity


The [naming convention](../naming-convention.md) renames attributes consistently, but it doesn't resolve a deeper inconsistency in how ɴsɪ models primitives. Three different patterns are in play across the existing node types:

| Primitive | Pattern                        | Examples                                                                                           |
| --------- | ------------------------------ | -------------------------------------------------------------------------------------------------- |
| Meshes    | One node, type attribute       | `mesh` (polygons and Catmull-Clark via `subdivision.scheme`)                                       |
| Volumes   | One node, but only one backend | `volume` (renders OpenVDB exclusively)                                                             |
| Particles | Split by backend               | `particles`, `vdbparticles`                                                                        |
| Cameras   | Split by projection            | `perspectivecamera`, `fisheyecamera`, `cylindricalcamera`, `sphericalcamera`, `orthographiccamera` |
| Surfaces  | One node per representation    | `nurbs` (shipped in 3Delight 2.9.210), [`t-nurcc`](../nodes/t-nurcc.md) (draft)                    |

`mesh` collapses polygons and subdivision surfaces behind a `subdivision.scheme` attribute. Cameras do the opposite -- five separate node types that differ only in their projection function. Volumes name themselves generically while only one backend is implemented. Particles are split by the data format their control points hold, not by what the renderer sees.

Three coherent resolutions, from least to most invasive:

## Option 1 -- Honest names, same shape

Keep one node per concern and rename for honesty. The mapping later in this document already adopts these names:

- `volume` -> `vdb-volume` (it only renders OpenVDB).
- `vdbparticles` -> `vdb-particles` (hyphenated).
- Cameras keep their five hyphenated names (`perspective-camera`, ...).
- `mesh` stays as the one merged exception.

The inconsistency with `mesh` remains. This is a pure rename -- no API change.

## Option 2 -- Collapse to one canonical primitive

Bring volumes, particles, and cameras in line with `mesh`'s "one node, type attribute" pattern:

- `vdb-volume` and `vdb-particles` collapse into a single `vdb` node with `kind = "volume" | "particles"` (or distinguished by which data attribute is supplied).
- The five camera nodes collapse into one `camera` node with `projection = "perspective" | "fisheye" | "cylindrical" | "spherical" | "orthographic"`. Projection-specific attributes live behind the projection's prefix (e.g. `fisheye.mapping`).

Every scene-graph entity ends up with a single canonical primitive. Migration is "rename node type, add a `kind`/`projection` attribute". The renderer's dispatch table has to flatten, but no user-side attribute is lost.

## Option 3 -- Split `mesh` to match the rest

Adopt the honest renames from Option 1 -- `volume` -> `vdb-volume`, `vdbparticles` -> `vdb-particles` -- and additionally replace `mesh` with `polygon-mesh` and `subdivision-mesh`. Each mesh node carries only the attributes meaningful for its surface kind; `subdivision.scheme` disappears entirely.

This is the most invasive option: every existing scene using subdivision surfaces has to re-target the new node, and the `subdivision.*` attributes migrate from prefix-grouped on `mesh` to top-level on `subdivision-mesh`.

## Trade-offs

- **Option 1** is cheapest to deliver; it preserves the inconsistency under prettier names.
- **Option 2** matches the mesh pattern. Requires backend dispatch work but no user-facing data loss.
- **Option 3** is the cleanest in isolation but invalidates the largest existing-asset footprint.

No recommendation in this draft. The decision belongs in the API roadmap, not in a renaming pass.
