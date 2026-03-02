# `fisheyecamera`

Fish eye cameras are useful for a multitude of applications (e.g. virtual reality). This node accepts these attributes:

| Name  | Type      | Default |
| ----- | --------- | ------- |
| `fov` | _`float`_ |         |

Specifies the field of view for this camera node, in degrees.

| Name      | Type       | Default       |
| --------- | ---------- | ------------- |
| `mapping` | _`string`_ | `equidistant` |

Defines one of the supported fisheye [mapping functions](https://en.wikipedia.org/wiki/Fisheye_lens):

- `equidistant` — Maintains angular distances.
- `equisolidangle` — Every pixel in the image covers the same solid angle.
- `orthographic` — Maintains planar illuminance. This mapping is limited to a 180 field of view.
- `stereographic` — Maintains angles throughout the image. Note that stereographic mapping fails to work with field of views close to 360 degrees.
