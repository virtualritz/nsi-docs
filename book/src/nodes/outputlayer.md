# `outputlayer`

This node describes one specific layer of render output data. It can be connected to the `outputlayers` attribute of a screen node. It has the following attributes:

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `variablename` | _`string`_ |         |

This is the name of a variable to output.

| Name             | Type       | Default  |
| ---------------- | ---------- | -------- |
| `variablesource` | _`string`_ | `shader` |

Indicates where the variable to be output is read from. Possible values are:

- `shader` — computed by a shader and output through an ᴏsʟ closure (such as `outputvariable()` or `debug()`) or the `Ci` global variable.
- `attribute` — retrieved directly from an attribute with a matching name attached to a geometric primitive.
- `builtin` — generated automatically by the renderer (e.g. `"z"`, `"alpha"`, `"N.camera"`, `"P.world"`).

| Name        | Type       | Default |
| ----------- | ---------- | ------- |
| `layername` | _`string`_ |         |

This will be name of the layer as written by the output driver. For example, if the output driver writes to an EXR file then this will be the name of the layer inside that file.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `scalarformat` | _`string`_ | `uint8` |

Specifies the format in which data will be encoded (quantized) prior to passing it to the output driver. Possible values are:

- `int8` — signed 8-bit integer
- `uint8` — unsigned 8-bit integer
- `int16` — signed 16-bit integer
- `uint16` — unsigned 16-bit integer
- `int32` — signed 32-bit integer
- `uint32` — unsigned 32-bit integer
- `half` — IEEE 754 half-precision binary floating point (binary16)
- `float` — IEEE 754 single-precision binary floating point (binary32)

| Name        | Type       | Default |
| ----------- | ---------- | ------- |
| `layertype` | _`string`_ | `color` |

Specifies the type of data that will be written to the layer. Possible values are:

- `scalar` — A single quantity. Useful for opacity ("alpha") or depth ("Z") information.
- `color` — A 3-component color.
- `vector` — A 3D point or vector. This will help differentiate the data from a color in further processing.
- `quad` — A sequence of 4 values, where the fourth value is not an alpha channel.

Each component of those types is stored according to the `scalarformat` attribute set on the same outputlayer node.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `colorprofile` | _`string`_ |         |

The name of an OCIO color profile to apply to rendered image data prior to quantization.

| Name        | Type        | Default |
| ----------- | ----------- | ------- |
| `dithering` | _`integer`_ | `0`     |

If set to 1, dithering is applied to integer scalars. Otherwise, it must be set to 0.

| Name        | Type        | Default |
| ----------- | ----------- | ------- |
| `withalpha` | _`integer`_ | `0`     |

If set to 1, an alpha channel is included in the output layer. Otherwise, it must be set to 0.

| Name      | Type        | Default |
| --------- | ----------- | ------- |
| `sortkey` | _`integer`_ |         |

This attribute is used as a sorting key when ordering multiple output layer nodes connected to the same [output driver](outputdriver.md) node. Layers with the lowest `sortkey` attribute appear first.

| Name       | Type             | Default |
| ---------- | ---------------- | ------- |
| `lightset` | _`<connection>`_ |         |

This connection accepts either light sources or [set](set.md) nodes to which lights are connected. In this case only listed lights will affect the render of the output layer. If nothing is connected to this attribute then all lights are rendered.

If an [environment](environment.md) node is connected here, a `component` string attribute can be specified on the connection with a value of either `sun` or `background`. If this is used, only the corresponding part of the environment will contribute to the output layer.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `lightsetname` | _`string`_ |         |

This can be provided as friendly name for the connected light set. Otherwise, a default name is built from the connected node.

| Name            | Type             | Default |
| --------------- | ---------------- | ------- |
| `outputdrivers` | _`<connection>`_ |         |

This connection accepts [output driver](outputdriver.md) nodes to which the layer's image will be sent.

| Name     | Type       | Default           |
| -------- | ---------- | ----------------- |
| `filter` | _`string`_ | `blackman-harris` |

The type of filter to use when reconstructing the final image from sub-pixel samples. Possible values are: `"box"`, `"triangle"`, `"catmull-rom"`, `"bessel"`, `"gaussian"`, `"sinc"`, `"mitchell"`, `"blackman-harris"`, `"zmin"` and `"zmax"`.

| Name          | Type       | Default |
| ------------- | ---------- | ------- |
| `filterwidth` | _`double`_ | `3.0`   |

Diameter in pixels of the reconstruction filter. It is not applied when filter is `"box"` or `"zmin"`.

| Name              | Type      | Default |
| ----------------- | --------- | ------- |
| `backgroundvalue` | _`float`_ | `0`     |

The value given to pixels where nothing is rendered.

| Name              | Type             | Default |
| ----------------- | ---------------- | ------- |
| `backgroundlayer` | _`<connection>`_ |         |

This connection accepts a single output layer node which is meant to be displayed as a background. Not all [output drivers](outputdriver.md) support this behavior, so it might be ignored.

| Name         | Type       | Default |
| ------------ | ---------- | ------- |
| `lightdepth` | _`string`_ | `auto`  |

Allows filtering light contributions according to the number of bounces light has made from a light source to the objects in front of the camera. This is only meaningful when the layer's `variablesource` is set to `shader` (otherwise, it's ignored). Possible values are:

- `direct` — Only light coming directly from light sources to visible objects (ie: with no bounce) is included.
- `indirect` — Only light coming from light sources to visible objects through at least one bounce is shown.
- `both` — All light is included.
- `auto` — Selects the appropriate value for lightdepth according to the value of the `variablename` attribute. If it ends with either `.direct` or `.indirect`, the corresponding light depth will be used, and the suffix will be removed from the effective variable name. Otherwise, it will default to `both`.

| Name                 | Type    | Default |
| -------------------- | ------- | ------- |
| `cryptomatte.enable` | _`int`_ | `0`     |

Setting this attribute to 1 enables Cryptomatte encoding of the layer's data. `cryptomatte.level` should also be set properly.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `cryptomatte.level` | _`int`_ | `0`     |

If this value is negative, the layer will contain a human-readable "Cryptomatte header" image. Otherwise, the value indicates the index of the first Cryptomatte level that will be output. Since Cryptomatte levels are output by pairs, a Cryptomatte file with 4 levels would contain output layers with `cryptomatte.level` set to -1, 0 and 2. This has no effect unless Cryptomatte encoding is enabled using `cryptomatte.enable`.

Any extra attributes are also forwarded to the output driver which may interpret them however it wishes.
