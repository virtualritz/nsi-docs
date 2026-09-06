# Option C: Width as a Flag

Width leaves the type name. A type names a semantic role and an arity, and a flag states the storage width. This is the move ɴsɪ already made for arity, where `NSIParamIsArray` and `arraylength` hold that axis outside the type name.

| Concept        | C enum                 | C++ class           | Lua constant            | Stream keyword     |
| -------------- | ---------------------- | ------------------- | ----------------------- | ------------------ |
| 32-bit int     | `NSITypeInt`           | `IntArg`            | `nsi.TypeInt`           | `"int"`            |
| 64-bit int     | `NSITypeInt` + wide    | `Int64Arg`          | `nsi.TypeInt` + wide    | `"int64"`          |
| 32-bit float   | `NSITypeFloat`         | `FloatArg`          | `nsi.TypeFloat`         | `"float"`          |
| 64-bit float   | `NSITypeFloat` + wide  | `Float64Arg`        | `nsi.TypeFloat` + wide  | `"float64"`        |
| Matrix         | `NSITypeMatrix`        | `MatrixArg`         | `nsi.TypeMatrix`        | `"matrix"`         |
| Wide matrix    | `NSITypeMatrix` + wide | `Matrix64Arg`       | `nsi.TypeMatrix` + wide | `"matrix64"`       |
| Color          | `NSITypeColor`         | `ColorArg`          | `nsi.TypeColor`         | `"color"`          |
| Point          | `NSITypePoint`         | `PointArg`          | `nsi.TypePoint`         | `"point"`          |
| Weighted point | `NSITypeWeightedPoint` | `WeightedPointArg`  | `nsi.TypeWeightedPoint` | `"weighted-point"` |
| String         | `NSITypeString`        | `StringArg`         | `nsi.TypeString`        | `"string"`         |
| Pointer        | `NSITypePointer`       | `PointerArg`        | `nsi.TypePointer`       | `"pointer"`        |

"Wide" above means a new flag next to the existing ones:

```c
enum
{
    NSIParamIsArray = 1,
    NSIParamPerFace = 2,
    NSIParamPerVertex = 4,
    NSIParamInterpolateLinear = 8,
    NSIParamIsWide = 16
};
```

The value `16` is the `0x10` bit that the enum already uses for the same purpose. It moves from the type field to the flags field, where the other orthogonal axes live.

The table shows the short scalar spellings, `int` and `float`. That choice belongs to the [abbreviation axis](type-names.md#abbreviation-and-word-separation) and not to this option.

`NSITypeDouble`, `NSITypeInt64`, and `NSITypeDoubleMatrix` cease to exist as names. Any type can be wide, including the ones that have no wide form today.

## Two surfaces keep single tokens

The flag is a concern of the in-memory API. The other surfaces do not have to expose it:

- The **stream** keeps one token per type. A writer emits `"float64"`, and the parser sets `NSITypeFloat` with the wide flag. The stream vocabulary therefore looks like Option B.
- The **C++ classes** keep one class per combination, for the same reason. `Float64Arg` sets the flag in `FillNSIParam`, and callers never see it.

Only the C enum and the Lua constants expose the axis directly.

## Rationale

The `0x10` bit says that the API's authors already understood width as orthogonal. Only the names disagreed. This option makes the names say what the encoding has said since version 1.

The gain is that width becomes available to every type at once, rather than to the three types that happened to get a constant. A double-precision point, normal, or rational control point needs no new name and no new enum entry. It needs only the stream token that names its width.

## Pros

- One rule, and the encoding already implements it.
- Any type can be wide. `Point`, `Normal`, `Color`, and `WeightedPoint` gain a 64-bit form for free.
- The enum shrinks from 14 entries to 11, and it stops growing with each width.
- Semantic names stay purely semantic, which is what [geometry-types](geometry-types.md) asks of them.
- It matches how `arraylength` already works, so the API gains no new kind of concept.

## Cons

- `NSITypeSizeOf` breaks. The function in `nsi.h` takes `unsigned t` and returns a size. Under this option the size depends on the flags too, so the signature must change. That is a source break for every caller.
- The type field alone no longer describes the data. Code that switches on `type` must also read `flags`, and code that forgets to will silently misread wide data as narrow.
- It is the largest change to the mental model. Options A and B rename things a user already understands; this option changes what a type *is*.
- Two fields must travel together. Any place that passes a type without its flags, in a binding or a serializer, loses the width.
- The Lua binding gets clumsier. A single constant no longer names a wide type, so a Lua author must set a flag next to `type`.
