# Decision 3: Scope and Contract

This decision asks two questions that are about behaviour, not about names. Which types need a second width at all? And what happens when a caller supplies the wrong one?

It governs how much [Decision 2](type-names-vocabulary.md) matters. If the renderer converts between widths, an exporter author stops having to track a width per attribute, and the spelling becomes a matter of taste.

## Which types need a second width

The specification types about 28 attributes as `double` and about 14 as `float`. No principle separates them.

There is a weak habit. Time and world-space lengths tend to be `double`: `frame`, `referencetime`, `shutterrange`, `velocityreferencetime`, `clippingrange`, `depthoffield.*`. Per-vertex data and values bound to ᴏsʟ tend to be `float`. The habit has counterexamples in both directions:

| Wide          | Narrow          | Both are                       |
| ------------- | --------------- | ------------------------------ |
| `angle`       | `fov`           | an angle in degrees            |
| `screenwindow` | `crop`          | a normalised pair on one node  |
| `vdbparticles.width` | `particles.width` | a width on a particle type |

`screenwindow` and `crop` sit on the same page of the specification, on the same node, and disagree.

One case is genuine. Matrices are consistently wide: `transform.transformationmatrix` and `instances.transformationmatrices` are both `doublematrix`. Precedent agrees, since USD types transforms as `matrix4d` and Alembic uses `M44d`.

The narrow matrix is meanwhile a dead type. No attribute in the specification is typed `matrix`, `nsi.hpp` defines no `MatrixArg`, and the only use in this book was an error. `NSITypeMatrix` can be retired, or `matrix` can be redefined as the 64-bit type at no cost.

## What a mismatch should do

The renderer refuses a mismatch today, in both directions, and keeps the previous value. Three contracts are available:

| Contract | A caller must | An arbitrary `float` against `double` choice is |
| --- | --- | --- |
| **Reject**, as today | match the declared width exactly | a trap that costs a dropped attribute |
| **Convert** | supply any width of the right kind | invisible, and harmless |
| **Normalise** | supply any width | absent, because the API declares one width per kind |

Rejection is the strictest and the most predictable. It also means every arbitrary choice in the table above is a defect that an exporter author has to discover. The Python binding makes this concrete: it types a bare Python float as `NSITypeDouble`, so every `float` attribute silently drops one.

Conversion removes the trap, at the cost of hiding a real precision loss when a caller sends 64-bit data to a 32-bit attribute. A warning can cover that case.

Normalisation is the most radical. It says the API declares one width per kind, and the renderer stores whatever it likes internally. It removes the width axis from the vocabulary question entirely, and it would retire `double`, `int64`, and `doublematrix` as names. It cannot remove width from `NSIParam_t`, because that field describes the layout of caller-owned memory.

## Questions

1. Is there a demonstrated need for a wide `point`, `normal`, or `color`? Precedent says no.
2. Should `NSITypeMatrix` be retired, or `matrix` redefined as 64-bit?
3. Should the `float` against `double` choices in the current specification be audited and normalised, independently of any renaming?
4. Would conversion with a warning be preferable to the current silent drop?
