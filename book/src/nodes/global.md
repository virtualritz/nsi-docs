# `global`

This node contains various global settings for a particular ɴsɪ context. Note that these attributes are for the most case implementation specific. This node has the reserved handle name `.global` and doesn't need to be created using `NSICreate`. The following attributes are recognized by [3Delight](https://www.3delight.com):

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `numberofthreads` | _`int`_ | `0`     |

Specifies the total number of threads to use for a particular render:

- A value of zero lets the render engine choose an optimal thread value. This is the default behaviour.
- Any positive value directly sets the total number of render threads.
- A negative value will start as many threads as optimal _plus_ the specified value. This allows for an easy way to decrease the total number of render threads.

| Name            | Type    | Default |
| --------------- | ------- | ------- |
| `texturememory` | _`int`_ |         |

Specifies the approximate maximum memory size, in megabytes, the renderer will allocate to accelerate texture access.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `networkcache.size` | _`int`_ | `0`     |

Specifies the maximum network cache size, in gigabytes, the renderer will use to cache textures on a local drive to accelerate data access.

| Name                     | Type       | Default |
| ------------------------ | ---------- | ------- |
| `networkcache.directory` | _`string`_ |         |

Specifies the directory in which textures will be cached. A good default value is `/var/tmp/3DelightCache` on Linux systems.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `networkcache.mipmap` | _`int`_ | `1`     |

Enables caching of texture mipmaps separately. This makes more efficient use of available cache space.

| Name                 | Type       | Default |
| -------------------- | ---------- | ------- |
| `networkcache.write` | _`string`_ | `0`     |

Enables caching for image write operations. This alleviates pressure on networks by first rendering images to a local temporary location and copying them to their final destination at the end of the render. This replaces many small network writes by more efficient larger operations.

| Name             | Type       | Default |
| ---------------- | ---------- | ------- |
| `license.server` | _`string`_ |         |

Specifies the name or address of the license server to be used.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `license.wait` | _`int`_ | `1`     |

When no license is available for rendering, the renderer will wait until a license is available if this attribute is set to 1, but will stop immediately if it's set to 0. The latter setting is useful when managing a renderfarm and other work could be scheduled instead.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `license.hold` | _`int`_ | `0`     |

By default, the renderer will get new licenses for every render and release them once it's done. This can be undesirable if several frames are rendered in sequence from the same process. If this option is set to 1, the licenses obtained for the first frame are held until the last frame is finished.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `renderatlowpriority` | _`int`_ | `0`     |

If set to 1, start the render with a lower process priority. This can be useful if there are other applications that must run during rendering.

| Name          | Type       | Default      |
| ------------- | ---------- | ------------ |
| `bucketorder` | _`string`_ | `horizontal` |

Specifies in what order the buckets are rendered. The available values are:

- `horizontal` — row by row, left to right and top to bottom.
- `vertical` — column by column, top to bottom and left to right.
- `zigzag` — row by row, left to right on even rows and right to left on odd rows.
- `spiral` — in a clockwise spiral from the centre of the image.
- `circle` — in concentric circles from the centre of the image.

| Name    | Type       | Default |
| ------- | ---------- | ------- |
| `frame` | _`double`_ | `0`     |

Provides a frame number to be used as a seed for the sampling pattern. See the [screen node](screen.md).

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `hidemessages` | _`int`_ |         |

This specifies error and warning messages which will not be displayed. The attribute values are the message numbers to ignore.

| Name                      | Type    | Default |
| ------------------------- | ------- | ------- |
| `maximumraydepth.diffuse` | _`int`_ | `1`     |

Specifies the maximum bounce depth a diffuse ray can reach. A depth of 1 specifies one additional bounce compared to purely local illumination.

| Name                   | Type    | Default |
| ---------------------- | ------- | ------- |
| `maximumraydepth.hair` | _`int`_ | `4`     |

Specifies the maximum bounce depth a hair ray can reach. Note that hair are akin to volumetric primitives and might need elevated ray depth to properly capture the illumination.

| Name                         | Type    | Default |
| ---------------------------- | ------- | ------- |
| `maximumraydepth.reflection` | _`int`_ | `1`     |

Specifies the maximum bounce depth a reflection ray can reach. Setting the reflection depth to 0 will only compute local illumination meaning that only emissive surfaces will appear in the reflections.

| Name                         | Type    | Default |
| ---------------------------- | ------- | ------- |
| `maximumraydepth.refraction` | _`int`_ | `4`     |

Specifies the maximum bounce depth a refraction ray can reach. A value of 4 allows light to shine through a properly modeled object such as a glass.

| Name                     | Type    | Default |
| ------------------------ | ------- | ------- |
| `maximumraydepth.volume` | _`int`_ | `0`     |

Specifies the maximum bounce depth a volume ray can reach.

| Name                       | Type       | Default |
| -------------------------- | ---------- | ------- |
| `maximumraylength.diffuse` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a diffuse material can travel. Using a relatively low value for this attribute might improve performance without significantly affecting the look of the resulting image, as it restrains the extent of global illumination. Setting it to a negative value disables the limitation.

| Name                    | Type       | Default |
| ----------------------- | ---------- | ------- |
| `maximumraylength.hair` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a hair closure can travel. Setting it to a negative value disables the limitation.

| Name                          | Type       | Default |
| ----------------------------- | ---------- | ------- |
| `maximumraylength.reflection` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a reflective material can travel. Setting it to a negative value disables the limitation.

| Name                          | Type       | Default |
| ----------------------------- | ---------- | ------- |
| `maximumraylength.refraction` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a refractive material can travel. Setting it to a negative value disables the limitation.

| Name                        | Type       | Default |
| --------------------------- | ---------- | ------- |
| `maximumraylength.specular` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a specular (glossy) material can travel. Setting it to a negative value disables the limitation.

| Name                      | Type       | Default |
| ------------------------- | ---------- | ------- |
| `maximumraylength.volume` | _`double`_ | `-1`    |

Limits the distance a ray emitted from a volume can travel. Setting it to a negative value disables the limitation.

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `quality.denoise` | _`int`_ | `1`     |

Enables denoising of output. Currently only supported for interactive renders.

| Name                      | Type    | Default |
| ------------------------- | ------- | ------- |
| `quality.iprglobalupdate` | _`int`_ | `1`     |

Enables a different method of updating the image for interactive renders.

| Name                     | Type    | Default |
| ------------------------ | ------- | ------- |
| `quality.iprinterpolate` | _`int`_ | `1`     |

Enables interpolation of low resolution interactive output, when denoised.

| Name                         | Type       | Default |
| ---------------------------- | ---------- | ------- |
| `quality.iprspeedmultiplier` | _`double`_ | `1`     |

Adjusts targeted render speed when processing multiple scene edits. A higher value will produce faster but lower quality results.

| Name                     | Type    | Default |
| ------------------------ | ------- | ------- |
| `quality.shadingsamples` | _`int`_ | `1`     |

Controls the quality of ʙsᴅꜰ sampling. Larger values give less visible noise.

| Name                    | Type    | Default |
| ----------------------- | ------- | ------- |
| `quality.volumesamples` | _`int`_ | `1`     |

Controls the quality of volume sampling. Larger values give less visible noise.

| Name            | Type       | Default |
| --------------- | ---------- | ------- |
| `referencetime` | _`double`_ |         |

Specifies a reference time for the frame, where deformation data is most valid. This is the default when the same attribute is not set on a geometry node. It is also the default for the `velocityreferencetime` attribute of the [vdbparticles node](vdbparticles.md) and the [volume node](volume.md). If not set, the center of the camera shutter is used.

| Name                           | Type    | Default |
| ------------------------------ | ------- | ------- |
| `quality.samplevolumeemission` | _`int`_ | `1`     |

Enables or disables the higher quality sampling of emission of ᴠᴅʙ volumes. The emission is visible either way, this only affects quality and render time.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `show.displacement` | _`int`_ | `1`     |

When set to 1, enables displacement shading. Otherwise, it must be set to 0, which forces the renderer to ignore any displacement shader in the scene.

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `show.atmosphere` | _`int`_ | `1`     |

When set to 1, enables atmosphere shader(s). Otherwise, it must be set to 0, which forces the renderer to ignore any atmosphere shader in the scene.

| Name                      | Type       | Default |
| ------------------------- | ---------- | ------- |
| `show.multiplescattering` | _`double`_ | `1.0`   |

This is a multiplier on the multiple scattering of ᴠᴅʙ nodes. This parameter is useful to obtain faster draft renders by lowering the value below 1. The range is 0 to 1.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `show.osl.subsurface` | _`int`_ | `1`     |

When set to 1, enables the `subsurface()` ᴏsʟ closure. Otherwise, it must be set to 0, which will ignore this closure in ᴏsʟ shaders.

| Name                  | Type    | Default |
| --------------------- | ------- | ------- |
| `statistics.progress` | _`int`_ | `0`     |

When set to 1, prints rendering progress as a percentage of completed pixels.

| Name                  | Type       | Default |
| --------------------- | ---------- | ------- |
| `statistics.filename` | _`string`_ | `null`  |

Full path of the file where rendering statistics will be written. An empty string will write statistics to standard output. The name `null` will not output statistics.

| Name               | Type             | Default |
| ------------------ | ---------------- | ------- |
| `exclusiveshading` | _`<connection>`_ |         |

When geometry nodes are connected here, all others in the scene will be rendered as black to the camera. This is meant to be used to speed up rendering when adjusting parameters of specific objects during an [interactive render](global.md). Connected shader nodes will behave in a similar way: objects not using them will be rendered as black. If the connected shader nodes are not the root of their shading network (ie: they are not connected to an [attributes node](attributes.md) and their output is used as another shader node's input), the evaluation of the shading network will end there. This allows fine-tune parts of a shading network in isolation.

| Name      | Type    | Default |
| --------- | ------- | ------- |
| `verbose` | _`int`_ | `0`     |

When set to 1, enables additional informative messages before, during and after rendering.

| Name                 | Type    | Default |
| -------------------- | ------- | ------- |
| `messages.timestamp` | _`int`_ | `0`     |

When set to 1, messages output by the renderer will include the local time.
