# 3Delight

[3Delight](https://www.3delight.com/) by Illumination Research is the reference implementation of ɴsɪ. The observations on this page were made with 3Delight 2.9.210 unless a version is named.

## Extensions

- **ᴏsʟ extensions.** 3Delight resolves intersecting subsurface-scattering volumes with intersection priorities and merge sets. See [ᴏsʟ Extensions](../osl-extensions.md).
- **A binary stream format.** `streamformat` `binarynsi` writes an undocumented binary encoding. `autonsi`, which is the behavior for a `streamfilename` that does not end in `.nsia`, selects it. A binary stream starts with the bytes `cc 00`. `renderdl -cat` converts it to text.
- **Lua scenes.** `NSIEvaluate` with `type` `lua` runs a script with an `nsi` table. See the [Lua API](../lua-api.md) and its limitations below.
- **Display drivers.** An [output driver](../nodes/outputdriver.md)'s `drivername` selects an ndspy display driver. 3Delight looks for `<drivername>.dpy` in the working directory, then in `$DELIGHT/displays` and `$DELIGHT/lib`. No environment variable extends that path. A built-in driver name, such as `png`, cannot be replaced by a file of the same name.
- **Cryptomatte built-ins.** With [`cryptomatte.enable`](../nodes/outputlayer.md) at its default of 1, the built-in variables `id.geometry`, `id.scenepath`, `id.surfaceshader` and `id.asset` are written in Cryptomatte format.
- **Tools.** `renderdl` renders a stream or a Lua script. `renderdl -cat` writes a stream back as text, and `renderdl -lua -cat` runs a Lua script and writes the calls it makes as a stream.

## Limitations

- **Lua cannot pass 64-bit values.** `nsi.TypeInt64`, `nsi.TypeDouble` and `nsi.TypePointer` are `nil`. A value that names one of them is re-typed without an error: an `int64` becomes the `int` 1, a `double` becomes a `float`. See the [FAQ](../faq.md#can-a-lua-script-pass-an-int64-or-a-double).
- **A connection `priority` on `geometryattributes` has no effect.** Only a `priority` on a shader connection, such as `surfaceshader`, ranks it. Use `ATTR.priority` on the attributes node instead. See the [FAQ](../faq.md).
- **Calls on one context run one at a time.** Several threads may call into one context, but they are serialized: 20,000 `SetAttribute` calls take 11.8 ms from one thread and 21.4 ms from sixteen.
- **`hpoint` needs 2.9.210.** A [`nurbs`](../nodes/nurbs.md) surface's `Pw` must have the type `hpoint`. The same data as flat `float`s is rejected (`E6007`), and the surface is then dropped (`E6020`). 3Delight 2.9.208 has neither the type nor the node.
- **Displacement needs `displacementbound`.** A `displacementshader` has no effect unless the attributes also set `displacementbound`, a `float`: how far, at most, the displacement moves the surface. The manual does not mention it. The library also knows a `displacementboundspace`, whose behavior is unverified. See the [attributes node](../nodes/attributes.md#displacement-bound).
- **The `hobby` curve basis is not supported.** A [`curves`](../nodes/curves.md) node with `basis` `hobby` warns `E6036` and falls back to the default basis.

## Behavior the Specification Leaves Open

- **Equal-priority definitions resolve in connection order.** When two attributes nodes on one node define the same attribute at the same priority, the one connected first applies, for plain attributes and for shaders. 3Delight prints no warning about the definitions it drops. See the [attributes node](../nodes/attributes.md#geometry-attributes).
- **A lone `ATTR.priority` is a definition** of `ATTR` at its default value. The priority must be exactly one `int`; any other type or count is ignored.
- **Specificity ranks before proximity.** At equal priority, a far `visibility.camera` wins over a nearer `visibility`.
- **Values are read loosely.** On `visibility`, a `float` 0.4 is visible, an `int64` 0 hides, and a `string` reads as true. A value of the wrong type is still a definition.
- **`set` nodes are attribute sources**, for `geometryattributes` and `shaderattributes`, with direct membership only.
- **A wrong-typed motion sample unsets the attribute** and discards every sample before it (`E6007`).
- **`${VAR}` in a string value expands at use**, for any variable, when the value is used -- for example when a file is opened. A stream reader keeps it as written.
- **The stream reader is lenient about type spellings.** `"i point"` reads as `point`.

## Setup

- The library is `lib3delight` in `$DELIGHT/lib`. The `renderdl` tool is in `$DELIGHT/bin`.
- Without a license, 3Delight renders with a watermark in the image background. The license server (`licserver`) must be running to use a node-locked license.
