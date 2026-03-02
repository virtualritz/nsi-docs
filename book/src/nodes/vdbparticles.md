# `vdbparticles`

This node represents particles defined by [OpenVDB](https://www.openvdb.org) data. It has the following attributes:

| Name          | Type       | Default |
| ------------- | ---------- | ------- |
| `vdbfilename` | _`string`_ |         |

The path to an OpenVDB file with the particle data.

| Name         | Type       | Default |
| ------------ | ---------- | ------- |
| `pointsgrid` | _`string`_ |         |

The name of the OpenVDB grid to use for particle data. It must be of type PointDataGrid.

| Name                    | Type       | Default |
| ----------------------- | ---------- | ------- |
| `velocityreferencetime` | _`double`_ |         |

The reference time at which the grid data is used directly, without being moved by the velocity attribute. Defaults to the [global node](global.md)'s `referencetime` attribute.

| Name            | Type       | Default |
| --------------- | ---------- | ------- |
| `velocityscale` | _`double`_ | `1`     |

A scaling factor applied to the velocity data.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `enablepscale` | _`int`_ | `1`     |

Enables use of the `pscale` attribute in the grid to specify particle radius.

| Name    | Type       | Default |
| ------- | ---------- | ------- |
| `width` | _`double`_ | `1`     |

The width of particles, if there is no `pscale` attribute in the file to specify their radius or it is disabled by setting `enablepscale` to 0.

| Name         | Type       | Default |
| ------------ | ---------- | ------- |
| `widthscale` | _`double`_ | `1`     |

A scaling factor applied to particle width.

The P, v and pscale grid attributes are used to respectively define particle position, velocity and radius. Other grid attributes may be read by shaders.
