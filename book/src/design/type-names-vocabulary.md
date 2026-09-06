# Decision 2: Vocabulary

Whatever [Decision 1](type-names.md#the-three-decisions) settles, the stream needs one token per type, and every binding needs a name. This page compares the spellings. A spelling is a table, not an architecture, so all four sit here rather than on pages of their own.

Two choices combine. The first is how a name states the width. The second is whether the name abbreviates.

## How the name states the width

| Concept        | A. Numeric, explicit | B. Numeric, 32 elided | C. `double-` prefix      | D. Short          |
| -------------- | -------------------- | --------------------- | ------------------------ | ----------------- |
| 32-bit int     | `int32`              | `int`                 | `int`                    | `i32`             |
| 64-bit int     | `int64`              | `int64`               | `double-int`             | `i64`             |
| 32-bit float   | `float32`            | `float`               | `float`                  | `f32`             |
| 64-bit float   | `float64`            | `float64`             | `double`                 | `f64`             |
| Matrix         | `matrix32`           | `matrix`              | `matrix`                 | `m32`             |
| Wide matrix    | `matrix64`           | `matrix64`            | `double-matrix`          | `m64`             |
| Point          | `point32`            | `point`               | `point`                  | `p32`             |
| Rational point | `weighted-point32`   | `weighted-point`      | `weighted-point`         | `h32` or `w32`    |
| String         | `string`             | `string`              | `string`                 | `string`          |

**A** is regular without exception, and it matches the vocabulary of NumPy, Arrow, Alembic, and ONNX. It erases `double`, so the C inconsistency disappears without anyone having to argue about `int`. Its cost is that a width postfix reaches the semantic types, where it re-mixes the axis that [geometry-types](geometry-types.md) separated. A variant puts the width on scalars only and fixes the compounds by rule.

**B** changes three names and no more. A bare name means 32 bits. The rule is asymmetric, because two widths exist and only one is ever written. A bare `point` also becomes "the narrow one" retroactively, the day `point64` appears.

**C** promotes the existing `doublematrix` pattern to a rule and hyphenates it per R6. It is not uniform as it stands: `float` to `double` replaces the word, while `int` to `double-int` prefixes it. The uniform form is `double-float`, which nobody will write. `double-int` is also etymologically sound and pragmatically confusing, since a reader takes it for twice an integer. Its honest description is "hyphenate `doublematrix` and stop", which makes it the minimal-change option.

**D** is defensible for `i32` and `f32`, which every programmer reads. It is not defensible for `c32`, `p32`, `n32`, or `h32`. Those are inventions. They contradict the ᴏsʟ words that the same person writes in a shader, and they are jargon in exactly the sense R9 forbids. A `.nsi` stream is read by humans when they debug an exporter, and these tokens make it opaque. The hesitation between `h32` and `w32` for the same type shows the scheme has no natural letter for a new semantic type.

## Whether the name abbreviates

Under a numeric-width scheme the only abbreviations left are `int` and `float`. Both consistent answers satisfy the rule that a vocabulary abbreviates all of its names or none:

| | ᴏsʟ words | Plain words |
| --- | --- | --- |
| Integer | `int` | `integer` |
| Float | `float` | `real` |

`int` and `float` are the words ᴏsʟ uses, and a user of this renderer writes them in every shader. The `scalarformat` attribute already uses `int32` and `float` in this specification. `real` is Fortran and Pascal vocabulary; the only precedent in ɴsɪ is the prose "integer, real or string" on page 18 of the specification.

The current half-abbreviated state is not a chosen style. `"integer"` is a syntax error the parser rejects, so there is only one spelling in the stream today, and it is `int`.

## Precedent

| API | Scalar vocabulary | Semantic types |
| --- | --- | --- |
| USD | `float`, `double`, `int`, `int64` | `point3f`, `matrix4d` -- width in the name |
| Alembic | `Float32`, `Int64` | POD plus extent plus an interpretation string |
| glTF | `componentType`, an enumeration | role in the attribute name, width fixed per role |
| ᴏsʟ | `int`, `float` | `point`, `vector`, `normal`, `color` |
| ɴsɪ `scalarformat` | `int32`, `uint32`, `half`, `float` | not applicable |

All of them state the width explicitly somewhere. None leaves it to the reader.
