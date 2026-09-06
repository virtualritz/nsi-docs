# Type Names: API Alternatives

`NSIType_t` grew one type at a time. Width entered the vocabulary three times, and each time it took a different form. This section briefs implementers. It rules on nothing.

An earlier version of this draft compared three schemes in one matrix. That was a mistake: the schemes differed on unrelated axes, so a criteria row could not compare them. The draft now separates three decisions. Each can be settled on its own, and each has its own pages.

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

## What the renderer does today

Any proposal must start from the current behaviour. These results come from `renderdl` of 3Delight 2.9.

**Width is type identity, and the renderer converts nothing.** A mismatch in either direction is refused, and the attribute keeps its previous value:

```
.global.frame           (double)    given float     -> E6007, dropped
.global.numberofthreads (int)       given double    -> E6007, dropped
screen.crop             (float[2])  given double[2] -> E6007, dropped
screen.screenwindow     (double[2]) given float[2]  -> E6007, dropped
```

Arity is identity too. A `float` of count 4 does not satisfy a `float[2]`.

**`"integer"` is not a second spelling of `"int"`. It is a syntax error.** The parser reports `E1000 ... has invalid type 'integer'` and skips the whole call.

**The encoding already reserves room for wide semantic types.** `NSITypeSizeOf` in `nsi.h` carries table slots 20 to 23, which are `Color|0x10` through `Normal|0x10`. All four hold zero. The bit pattern exists; only the names and the sizes are missing.

Two consequences follow. ɴsɪ is already schema-fixed in the sense USD is: the node specification fixes the width, and the caller must match it. The width of an attribute is also a hard contract. An arbitrary choice between `float` and `double` is therefore a trap for exporter authors, not a cosmetic detail.

## Six surfaces, six vocabularies

| Concept       | C enum                | C++ class         | Lua constant      | Python `Type`  | Stream keyword   | Renderer message |
| ------------- | --------------------- | ----------------- | ----------------- | -------------- | ---------------- | ---------------- |
| 32-bit int    | `NSITypeInteger`      | `IntegerArg`      | `nsi.TypeInteger` | `Type.Integer` | `"int"`          | `'int'`          |
| 64-bit int    | `NSITypeInt64`        | `Int64Arg`        | none              | none           | `"int64"`        | `'int64'`        |
| 32-bit float  | `NSITypeFloat`        | `FloatArg`        | `nsi.TypeFloat`   | `Type.Float`   | `"float"`        | `'float'`        |
| 64-bit float  | `NSITypeDouble`       | `DoubleArg`       | none              | `Type.Double`  | `"double"`       | `'double'`       |
| 32-bit matrix | `NSITypeMatrix`       | none              | `nsi.TypeMatrix`  | `Type.Matrix`  | `"matrix"`       | `'matrix'`       |
| 64-bit matrix | `NSITypeDoubleMatrix` | `DoubleMatrixArg` | none              | `Type.DoubleMatrix` | `"doublematrix"` | `'doublematrix'` |

The wide types are the ones that surfaces forget. No Lua constant names any of them, and the Python `Type` class omits `Int64` although it defines `Double` and `DoubleMatrix`.

## An in-spec precedent

The `scalarformat` attribute of the [`outputlayer`](../nodes/outputlayer.md) node already names a family of widths:

```
int8  uint8  int16  uint16  int32  uint32  half  float
```

That vocabulary abbreviates the integer word and states its width as a number. It keeps the C word for the two float widths. ɴsɪ therefore already contains an answer to part of the vocabulary question, and `int32` is house style.

## The three decisions

| | Decides | Pages |
| --- | --- | --- |
| **1. Encoding** | Where the width lives in `NSIParam_t` | [composite constants](type-names-composite.md), [a named bit](type-names-named-bit.md), [a flag](type-names-flag.md) |
| **2. Vocabulary** | How a name spells the width, and whether it abbreviates | [one page, one matrix](type-names-vocabulary.md) |
| **3. Scope and contract** | Which types get a second width, and whether a mismatch converts or drops | [one page](type-names-scope.md) |

Decision 2 applies whatever Decision 1 settles, because the stream still needs one token per type. Decision 3 governs how much Decision 2 matters to a user. If the renderer converts, an exporter author stops having to track a width per attribute.

## Three axes in one name

A type name carries up to three independent facts. Only one is expressed consistently:

| Axis                | Where it lives today                                      | Consistent? |
| ------------------- | --------------------------------------------------------- | ----------- |
| Storage width       | the name, as `Double`, as `64`, or as a `Double` prefix    | no          |
| Arity               | partly the name (`Color`, `Matrix`), partly `arraylength`  | no          |
| Transform semantics | the name (`Point`, `Vector`, `Normal`)                     | yes         |

The [Geometry in the Type System](geometry-types.md) page settles the third axis. It is not reopened here.

## Questions to Settle

1. **Does anything need a 64-bit geometry type?** Precedent says no. USD offers `point3d` but types the `points` attribute as `point3f[]`. Alembic stores `P` as `V3f`. glTF has no double at all. The 64-bit point that Decision 1 would enable has no demonstrated customer.
2. **Is width part of a type's identity, or part of its storage?** The renderer answers "identity" today, and refuses every mismatch. A change here is a change of behaviour, not of naming.
3. **Should the renderer convert between widths?** This is the highest-value question on this page. It decides whether the arbitrary `float` against `double` choices in the current specification stay a trap.
4. **Does a third width ever arrive?** `scalarformat` already lists `half`. A scheme that can express only two widths forecloses that.
5. **What happens to the old names?** Every option can keep the current constants as deprecated aliases, since the enum values do not move. That choice is independent of the three decisions.
