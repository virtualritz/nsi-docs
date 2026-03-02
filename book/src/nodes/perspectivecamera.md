# `perspectivecamera`

This node defines a perspective camera. The canonical camera is viewing in the direction of the Z- axis. The node is usually connected into a [transform](transform.md) node for camera placement. It has the following attributes:

| Name  | Type      | Default |
| ----- | --------- | ------- |
| `fov` | _`float`_ |         |

The field of view angle, in degrees.

| Name                  | Type        | Default |
| --------------------- | ----------- | ------- |
| `depthoffield.enable` | _`integer`_ | `0`     |

Enables depth of field effect for this camera.

| Name                 | Type       | Default |
| -------------------- | ---------- | ------- |
| `depthoffield.fstop` | _`double`_ |         |

Relative aperture of the camera.

| Name                       | Type       | Default |
| -------------------------- | ---------- | ------- |
| `depthoffield.focallength` | _`double`_ |         |

Vertical focal length, in scene units, of the camera lens.

| Name                            | Type       | Default |
| ------------------------------- | ---------- | ------- |
| `depthoffield.focallengthratio` | _`double`_ | `1`     |

Ratio of vertical focal length to horizontal focal length. This is the squeeze ratio of an anamorphic lens.

| Name                         | Type       | Default |
| ---------------------------- | ---------- | ------- |
| `depthoffield.focaldistance` | _`double`_ |         |

Distance, in scene units, in front of the camera at which objects will be in focus.

| Name                           | Type        | Default |
| ------------------------------ | ----------- | ------- |
| `depthoffield.aperture.enable` | _`integer`_ | `0`     |

By default, the renderer simulates a circular aperture for depth of field. Enable this feature to simulate aperture "blades" as on a real camera. This feature affects the look in out-of-focus regions of the image.

| Name                          | Type        | Default |
| ----------------------------- | ----------- | ------- |
| `depthoffield.aperture.sides` | _`integer`_ | `5`     |

Number of sides of the camera's aperture. The minimum number of sides is 3.

| Name                          | Type       | Default |
| ----------------------------- | ---------- | ------- |
| `depthoffield.aperture.angle` | _`double`_ | `0`     |

A rotation angle (in degrees) to be applied to the camera's aperture, in the image plane.

| Name                    | Type       | Default |
| ----------------------- | ---------- | ------- |
| `unitlengthmillimeters` | _`double`_ |         |

Physical length, in millimeters, of one scene unit. Since NSI only uses virtual scene units, this has no effect on the rendered images. However, this value can be useful if the renderer has to communicate with other software or file formats using physical units. For example, the focal length of the camera, expressed in millimeters, would be the product `depthoffield.focallength * unitlengthmillimeters`.
