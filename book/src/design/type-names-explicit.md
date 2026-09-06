# Option A: Explicit Width

Every type that has a storage width states that width in its name. This is the vocabulary of Rust (`i32`, `f64`), of WGSL, and of most APIs designed after 2010. No name relies on a default.

| Concept       | C enum                    | C++ class              | Lua constant             | Stream keyword      |
| ------------- | ------------------------- | ---------------------- | ------------------------ | ------------------- |
| 32-bit int    | `NSITypeInt32`            | `Int32Arg`             | `nsi.TypeInt32`          | `"int32"`           |
| 64-bit int    | `NSITypeInt64`            | `Int64Arg`             | `nsi.TypeInt64`          | `"int64"`           |
| 32-bit float  | `NSITypeFloat32`          | `Float32Arg`           | `nsi.TypeFloat32`        | `"float32"`         |
| 64-bit float  | `NSITypeFloat64`          | `Float64Arg`           | `nsi.TypeFloat64`        | `"float64"`         |
| Matrix        | `NSITypeMatrix32`         | `Matrix32Arg`          | `nsi.TypeMatrix32`       | `"matrix32"`        |
| Wide matrix   | `NSITypeMatrix64`         | `Matrix64Arg`          | `nsi.TypeMatrix64`       | `"matrix64"`        |
| Color         | `NSITypeColor32`          | `Color32Arg`           | `nsi.TypeColor32`        | `"color32"`         |
| Point         | `NSITypePoint32`          | `Point32Arg`           | `nsi.TypePoint32`        | `"point32"`         |
| Vector        | `NSITypeVector32`         | `Vector32Arg`          | `nsi.TypeVector32`       | `"vector32"`        |
| Normal        | `NSITypeNormal32`         | `Normal32Arg`          | `nsi.TypeNormal32`       | `"normal32"`        |
| Weighted point| `NSITypeWeightedPoint32`  | `WeightedPoint32Arg`   | `nsi.TypeWeightedPoint32`| `"weighted-point32"`|
| String        | `NSITypeString`           | `StringArg`            | `nsi.TypeString`         | `"string"`          |
| Pointer       | `NSITypePointer`          | `PointerArg`           | `nsi.TypePointer`        | `"pointer"`         |

`String` and `Pointer` have no width to state, so they keep their bare names.

## Rationale

A reader never has to know a default. `NSITypeInt32` says what it holds, and so does `NSITypeInt64`. The pair reads as a pair, which `Integer` and `Int64` do not. The rule extends to any future width without a further decision: a half-precision color would be `NSITypeColor16`.

The scheme also erases the worst ambiguity in the current names. `Double` disappears, so no name uses a float word to describe a matrix.

## Pros

- No defaults to memorize. Every numeric name is complete on its own.
- Uniform across all four surfaces, because one rule generates every name.
- Matches the vocabulary that most users already know from Rust, WGSL, and NumPy.
- Extends to new widths without a new convention.
- Names sort together. `Int32` and `Int64` are adjacent in any alphabetical list, unlike `Double` and `Float`.

## Cons

- Every existing constant changes. No current name survives except `String` and `Pointer`.
- The width postfix reaches the semantic types, where it carries little information. Every point in ɴsɪ is 32-bit today, so `Point32` states a fact that has never varied.
- `NSITypeWeightedPoint32` is 24 characters to describe four floats. The names get long exactly where the [geometry-types](geometry-types.md) page argues the name should be about behavior.
- It re-mixes the two axes that the geometry-types page separated. A width postfix on `WeightedPoint` says storage; the base word says transform rule. The name now carries both again.
- A softer variant carves the geometry types out of the rule, and leaves them bare. That variant is Option B with more renaming.
