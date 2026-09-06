# Type Names: API Alternatives

The `NSIType_t` enum grew one type at a time. Width entered the vocabulary three times, and each time it took a different form. This section lays out three alternatives, as a basis for discussion with implementers. It rules on none of them.

## One axis, three spellings

The enum in `nsi.h` already encodes width as an orthogonal bit:

```c
NSITypeFloat   = 1,   NSITypeDouble       = NSITypeFloat   | 0x10,
NSITypeInteger = 2,   NSITypeInt64        = NSITypeInteger | 0x10,
NSITypeMatrix  = 8,   NSITypeDoubleMatrix = NSITypeMatrix  | 0x10,
```

The `0x10` bit means "64 bits wide". The names do not agree on how to say that:

| Narrow    | Wide           | How the name states the width                                              |
| --------- | -------------- | -------------------------------------------------------------------------- |
| `Float`   | `Double`       | The base word changes. The C spelling of the wider type replaces it.        |
| `Integer` | `Int64`        | A postfix states the width. The base word also shortens, `Integer` to `Int`. |
| `Matrix`  | `DoubleMatrix` | A prefix states the width, and it borrows the float word.                   |

`Double` means "a 64-bit float". `DoubleMatrix` means "a matrix of 64-bit floats". The word does different work in each name. No `Int64Matrix` exists, so nothing forces a reader to notice the difference.

## The same type, four spellings

Each type appears on four surfaces. They disagree:

| Concept       | C enum                | C++ class         | Lua constant      | Stream keyword          |
| ------------- | --------------------- | ----------------- | ----------------- | ----------------------- |
| 32-bit int    | `NSITypeInteger`      | `IntegerArg`      | `nsi.TypeInteger` | `"int"` and `"integer"` |
| 64-bit int    | `NSITypeInt64`        | `Int64Arg`        | none              | `"int64"`               |
| 32-bit float  | `NSITypeFloat`        | `FloatArg`        | `nsi.TypeFloat`   | `"float"`               |
| 64-bit float  | `NSITypeDouble`       | `DoubleArg`       | none              | `"double"`              |
| 32-bit matrix | `NSITypeMatrix`       | none              | `nsi.TypeMatrix`  | `"matrix"`              |
| 64-bit matrix | `NSITypeDoubleMatrix` | `DoubleMatrixArg` | none              | `"doublematrix"`        |

Three observations follow from that table:

- The stream keyword and the C constant disagree for the commonest type of all. The specification uses `"int"` on pages 34, 35 and 61, and `"integer"` on pages 44, 45, 49 and 50, for the same 32-bit integer.
- The 32-bit matrix has no C++ convenience class, although `DoubleMatrixArg` exists. The asymmetric names hide the asymmetric coverage.
- The wide types are exactly the ones that surfaces forget. No Lua constant names any of them.

## Three axes in one name

A type name in ɴsɪ carries up to three independent facts. Only one of them is expressed consistently:

| Axis                | Where it lives today                                    | Consistent? |
| ------------------- | ------------------------------------------------------- | ----------- |
| Storage width       | the name, as `Double`, as `64`, or as a `Double` prefix  | no          |
| Arity               | partly the name (`Color`, `Matrix`), partly `arraylength` | no          |
| Transform semantics | the name (`Point`, `Vector`, `Normal`)                   | yes         |

The [Geometry in the Type System](geometry-types.md) page settles the third axis. It is not reopened here.

The first axis is the subject of this section. ɴsɪ has a precedent for the move that Option C makes. `NSIParamIsArray` and `arraylength` already hold the arity axis outside the type name. The [C API](../c-api.md) even tells readers to view `arraylength` as a part of the data type.

## The Options

| Criterion                | [A -- Explicit width](type-names-explicit.md) | [B -- Bare means 32-bit](type-names-postfix.md) | [C -- Width as a flag](type-names-flag.md) |
| ------------------------ | --------------------------------------------- | ----------------------------------------------- | ------------------------------------------ |
| 32-bit int               | `NSITypeInt32`                                | `NSITypeInt`                                    | `NSITypeInt`                               |
| 64-bit int               | `NSITypeInt64`                                | `NSITypeInt64`                                  | `NSITypeInt` + wide flag                   |
| 64-bit matrix            | `NSITypeMatrix64`                             | `NSITypeMatrix64`                               | `NSITypeMatrix` + wide flag                |
| 64-bit point             | `NSITypePoint64`                              | no name exists                                  | `NSITypePoint` + wide flag                 |
| Enum entries             | 14                                            | 14                                              | 11                                         |
| Constants renamed        | all                                           | three                                           | three removed                              |
| Width readable from name | always                                        | by absence                                      | never                                      |
| `NSITypeSizeOf` survives | yes                                           | yes                                             | no                                         |

Counts include the draft `weighted-point` type and `NSITypeInvalid`.

## The rational point

The `weighted-point` type of the [geometry-types](geometry-types.md) draft discriminates the three options, so it is worth stating separately.

- Under **Option A** it becomes `NSITypeWeightedPoint32`. The rule admits no exception, so a semantic name gains a width postfix. That mixes the two axes the geometry-types page separated.
- Under **Option B** it stays `NSITypeWeightedPoint`. It cannot widen. A double-precision rational control point has no name, and CAD data is the one place that plausibly wants one.
- Under **Option C** it widens for free. No new constant is needed, because width is not part of the name.

The same reasoning applies to `point`, `vector`, `normal`, and `color`. Option C is the only option under which a 64-bit member of that family can exist without a new enum entry each.

## Questions to Settle

1. **Does anything need a 64-bit geometry type?** No pipeline may ever ask for a double-precision point. If none does, the value of Option C falls away, and the choice reduces to A against B. CAD import is the case to test this against.
2. **Is width part of a type's identity, or part of its storage?** Option A and Option B answer "identity". Option C answers "storage". It makes width mean what `arraylength` already means: a fact about layout, held outside the name.
3. **What does `NSITypeSizeOf` become?** The function in `nsi.h` takes the type alone. Under Option C the size is no longer a function of the type, so the signature must change. Is that break acceptable?
4. **Do the stream keywords follow the C constants?** The two disagree today, and no option repairs that by itself. A rule that derives one from the other would settle `"int"` against `"integer"` permanently.
5. **What happens to the old names?** Every option can keep the current constants as deprecated aliases, since the enum values do not move. That choice is independent of which option wins.
