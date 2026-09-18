# Type Rename: Role, Components, Width

This draft proposes one naming scheme for every ɴsɪ type. A name has three parts, always in the same order:

1. The **role**: what the value is, in mathematical terms. `Integer`, `Real`, `Color`, `Point`, `Vector`, `Normal`, `Matrix`, `String`, `Pointer`.
2. The **component count**: how many scalars make one value. A matrix gives its size, 4 for 4×4. A scalar number gives none.
3. The **machine type** of one scalar: `F32`, `F64`, `I32` or `I64`.

The scheme is the one the Rust binding already uses for its attribute types, such as `Color3F32`, `Point4F32` and `Matrix4F64`. It is a further option for [Decision 2: Vocabulary](type-names-vocabulary.md). It rules on nothing.

## The mapping

| Constant today        | Stream name today | Proposed     |
| --------------------- | ----------------- | ------------ |
| `NSITypeFloat`        | `float`           | `RealF32`    |
| `NSITypeDouble`       | `double`          | `RealF64`    |
| `NSITypeInteger`      | `int`             | `IntegerI32` |
| `NSITypeInt64`        | `int64`           | `IntegerI64` |
| `NSITypeColor`        | `color`           | `Color3F32`  |
| `NSITypePoint`        | `point`           | `Point3F32`  |
| `NSITypeHPoint`       | `hpoint`          | `Point4F32`  |
| `NSITypeVector`       | `vector`          | `Vector3F32` |
| `NSITypeNormal`       | `normal`          | `Normal3F32` |
| `NSITypeMatrix`       | `matrix`          | `Matrix4F32` |
| `NSITypeDoubleMatrix` | `doublematrix`    | `Matrix4F64` |
| `NSITypeString`       | `string`          | `String`     |
| `NSITypePointer`      | `pointer`         | `Pointer`    |

An array keeps its length as it does today: `IntegerI32[2]` for the current `int[2]`.

The role and the machine type look redundant for scalars -- a `Real` is always stored as `F32` or `F64` -- but they answer different questions. The role says what the value means, as `Color` or `Normal` does. The suffix says how it is stored. Every name has both parts, so no name is an exception.

## What the scheme makes possible

The same three parts name types that ɴsɪ does not have yet, without a new rule for each:

- `Color4F32`: a color with alpha.
- `Point2F32`: a point in a 2D space. Compare the `parametric-point` role that [Geometry in the Type System](geometry-types.md) reserves for this.
- `Point3F64`, `Vector3F64`, `Normal3F64`: double-precision geometry, one of the cases [Decision 3](type-names-scope.md) weighs.
- `Matrix3F32`: a 3×3 matrix.

## For

- **Every name states all three facts.** Today the width is in the name for `double` and `int64`, in a prefix for `doublematrix`, and absent everywhere else. The component count is never in the name: `color` is 3 floats because the specification says so.
- **One rule, no exceptions.** A reader who knows one name can derive all the others.
- **The Rust binding already uses it.** A name read in the specification is the name written in Rust.
- **Width is visible where it matters.** A `RealF32` sent to an attribute that expects `RealF64` is a visible mismatch in the name. Today it is `float` against `double`, which many readers take as synonyms. See [What the renderer does today](type-names.md#what-the-renderer-does-today).

## Against

- **`Point4F32` states the size, not the behavior.** [Geometry in the Type System](geometry-types.md) rejected `point-4d` for this reason: the name does not say that the four components are *homogeneous* and transform as one unit. `hpoint` says it; `weighted-point` says it. Under this scheme the behavior is in the documentation, not in the name. A way out is a role for it, such as `HPoint4F32`, at the cost of one exception to "the role is what the data is".
- **The case does not match the rest of the API.** Attribute names are lowercase with hyphens under the [naming convention](../naming-convention.md). CamelCase type names in a stream, such as `"Color3F32"`, would be the only mixed-case tokens in it. The lowercase form, `"color3f32"`, is harder to read.
- **`Integer` and `Real` are new vocabulary here.** Every other API in the precedent table of [Decision 2](type-names-vocabulary.md#precedent) calls these `int` and `float`. They are the mathematical names, as `Color`, `Point` and `Normal` already are.
- **Every existing stream and every binding changes.** The stream parser would have to accept both vocabularies for as long as old files exist.

## Questions to settle

1. Does the role name the behavior (`HPoint4F32`) or only the kind of data (`Point4F32`)?
2. Which case in streams and in the C constants: `Color3F32` or `color3f32`, and `NSITypeColor3F32`?
3. Is `Pointer` a role, given that it has no components and no width? The Rust binding calls it `Reference`.
