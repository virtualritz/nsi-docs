# Option B: Bare Means 32-Bit

A bare name means the 32-bit type. A `64` postfix marks the wide type, and marks nothing else. This is the smallest change that makes the width axis consistent.

| Concept        | C enum                  | C++ class           | Lua constant            | Stream keyword     |
| -------------- | ----------------------- | ------------------- | ----------------------- | ------------------ |
| 32-bit int     | `NSITypeInt`            | `IntArg`            | `nsi.TypeInt`           | `"int"`            |
| 64-bit int     | `NSITypeInt64`          | `Int64Arg`          | `nsi.TypeInt64`         | `"int64"`          |
| 32-bit float   | `NSITypeFloat`          | `FloatArg`          | `nsi.TypeFloat`         | `"float"`          |
| 64-bit float   | `NSITypeFloat64`        | `Float64Arg`        | `nsi.TypeFloat64`       | `"float64"`        |
| Matrix         | `NSITypeMatrix`         | `MatrixArg`         | `nsi.TypeMatrix`        | `"matrix"`         |
| Wide matrix    | `NSITypeMatrix64`       | `Matrix64Arg`       | `nsi.TypeMatrix64`      | `"matrix64"`       |
| Color          | `NSITypeColor`          | `ColorArg`          | `nsi.TypeColor`         | `"color"`          |
| Point          | `NSITypePoint`          | `PointArg`          | `nsi.TypePoint`         | `"point"`          |
| Vector         | `NSITypeVector`         | `VectorArg`         | `nsi.TypeVector`        | `"vector"`         |
| Normal         | `NSITypeNormal`         | `NormalArg`         | `nsi.TypeNormal`        | `"normal"`         |
| Weighted point | `NSITypeWeightedPoint`  | `WeightedPointArg`  | `nsi.TypeWeightedPoint` | `"weighted-point"` |
| String         | `NSITypeString`         | `StringArg`         | `nsi.TypeString`        | `"string"`         |
| Pointer        | `NSITypePointer`        | `PointerArg`        | `nsi.TypePointer`       | `"pointer"`        |

Three constants change: `Integer` becomes `Int`, `Double` becomes `Float64`, and `DoubleMatrix` becomes `Matrix64`. Everything else keeps its name.

## Rationale

The 32-bit types carry almost all traffic. Shader parameters, vertex data, and colors are 32-bit, and a scene may contain no wide value at all. A convention that leaves the common case unmarked keeps the common case short.

The scheme also settles the `"int"` against `"integer"` split in the specification. It settles it in favour of the spelling that the stream examples already use. `NSITypeInt` and `"int"` finally name the same thing with the same word.

## Pros

- The smallest change of the three. Three constants move, and every other name stays.
- The C name and the stream keyword agree, once `Integer` becomes `Int`.
- Short names for the common case. A shader parameter list stays readable.
- The postfix marks the exception, which is what a reader wants to notice.
- Semantic types stay clean. `WeightedPoint` keeps naming a transform rule and nothing else, as [geometry-types](geometry-types.md) argues it should.

## Cons

- The default is implicit. A reader must learn that a bare name means 32 bits, and nothing in the name says so.
- The rule is asymmetric. Two widths exist, and only one of them is ever written down.
- A 64-bit point, normal, or color has no name. Adding one later means inventing `Point64`, which then makes the bare `Point` retroactively mean "the narrow one", a meaning it never announced.
- `Float` and `Float64` do not sort together, so the pair is not visible in an alphabetical list.
- It preserves the shape of the problem it fixes. Width is still part of the name, so every future width needs a new constant on every surface.
