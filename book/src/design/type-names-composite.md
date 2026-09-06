# Encoding 1: Composite Constants

Each combination of a base type and a width keeps its own constant, as it has since version 1. `NSITypeDouble`, `NSITypeInt64`, and `NSITypeDoubleMatrix` remain distinct enum entries. Only their names come up for discussion, and that discussion is [Decision 2](type-names-vocabulary.md).

```c
NSITypeFloat   = 1,   NSITypeDouble       = NSITypeFloat   | 0x10,
NSITypeInteger = 2,   NSITypeInt64        = NSITypeInteger | 0x10,
NSITypeMatrix  = 8,   NSITypeDoubleMatrix = NSITypeMatrix  | 0x10,
```

## Rationale

The encoding works. `NSITypeSizeOf` maps a constant to a byte count, parameters stay self-describing, and every binding needs one constant per case. A rename under Decision 2 fixes the inconsistency that users actually meet, which is the spelling.

The `0x10` bit stays an implementation detail of the enum values. Nothing outside `nsi.h` needs to know it exists.

## Pros

- No ABI change, and no source change beyond names.
- `NSITypeSizeOf` keeps its signature. A parameter still describes its own layout.
- One constant names one layout. A `switch` over the type is complete and a compiler can check it.
- Every binding stays a flat list of constants, which is what Lua and Python already expose.
- It is the only encoding that needs no new concept in the specification.

## Cons

- A wide semantic type needs a new constant for each: `NSITypeWidePoint`, `NSITypeWideNormal`, `NSITypeWideColor`, `NSITypeWideWeightedPoint`. The enum grows as the product of the two axes.
- The reserved slots stay empty. `NSITypeSizeOf` has held zeroed entries for `Color|0x10` through `Normal|0x10` since version 1, and this option leaves them zeroed.
- A third width multiplies the enum again. `scalarformat` already names `half`, so the case is not hypothetical.
- The orthogonality stays hidden. A reader learns the `0x10` relationship only by reading the enum values.
