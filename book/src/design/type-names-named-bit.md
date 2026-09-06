# Encoding 2: A Named Bit

The `0x10` bit stays in the `type` field and gains a name. Composing it with any base type becomes legal and documented.

```c
NSITypeWide = 0x10,        /* 64-bit variant of the base type */

NSITypeFloat  = 1,
NSITypeInt    = 2,
NSITypeMatrix = 8,
```

`NSITypeFloat | NSITypeWide` replaces `NSITypeDouble`. `NSITypePoint | NSITypeWide` becomes legal, and it needs no new constant. The old composite names can stay as aliases, because their values do not move.

## Rationale

The encoding has always been compositional. Only the documentation and the names were not. This option changes what the API *says* rather than what it does, and it is the smallest change that makes a wide semantic type expressible.

The four zeroed slots in `NSITypeSizeOf`, at `Color|0x10` through `Normal|0x10`, are exactly the entries this option fills. The table needs sizes, not a new shape.

## Pros

- A wide variant of any type costs one table entry, not one constant per combination.
- `NSITypeSizeOf` keeps its signature. Width is still in the `type` argument, so a parameter stays self-describing.
- No second field must travel with the type. A serializer that forwards `type` forwards the width with it.
- Existing constants keep their values, so the change is source-compatible if the old names stay as aliases.
- It documents a relationship that already exists, so no implementation has to change to match.

## Cons

- The type field stops being a plain enumeration. A `switch` over it must mask the bit, and code that forgets misreads a wide value as an unknown type.
- Bindings that expose a flat constant list, such as Lua and Python, must expose the bit and the composition rule too.
- It reserves a bit of the type field permanently, which limits how many base types the field can ever hold.
- A third width needs a second bit, or a small width field. The bit alone answers `half` no better than composite constants do.
- The stream still needs one token per combination, so it gains nothing here. That is [Decision 2](type-names-vocabulary.md).
