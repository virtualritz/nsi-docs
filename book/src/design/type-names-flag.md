# Encoding 3: A Flag in `flags`

Width leaves the `type` field entirely. A type names a semantic role and an arity. A flag next to `NSIParamIsArray` states the storage width.

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

`NSITypeDouble`, `NSITypeInt64`, and `NSITypeDoubleMatrix` cease to exist. Any type can be wide.

## Rationale

ɴsɪ already holds one orthogonal axis outside the type name. `NSIParamIsArray` and `arraylength` carry arity, and the [C API](../c-api.md) tells readers to view `arraylength` as a part of the data type. This option treats width the same way.

The result is the smallest type enumeration of the three encodings, and the one where the two axes never multiply.

## Pros

- The enum stops growing with width. Eleven entries cover every combination.
- Any type gains a wide form, including `point`, `normal`, `color`, and the draft `weighted-point`.
- Width sits with the other per-parameter facts, which is where a reader of `NSIParam_t` already looks for layout modifiers.
- The composition rule is stated in one place, rather than implied by enum values.

## Cons

- `NSITypeSizeOf` breaks. The function takes `unsigned t` and returns a size, so under this option the size stops being a function of its argument. That is a source break for every caller.
- The type no longer describes the data. Two fields must travel together, and any binding or serializer that passes a type without its flags loses the width silently.
- The `arraylength` analogy is weaker than it looks. The renderer treats `float[2]` as a distinct type when it matches attributes. Arity held outside the name is therefore still part of the contract, not a free modifier.
- A boolean cannot express a third width. `scalarformat` already names `half`, and this encoding forecloses it.
- Lua and Python gain a second argument beside `type`, where today one constant suffices.
