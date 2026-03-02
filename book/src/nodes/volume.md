# `volume`

This node represents a volumetric object defined by [OpenVDB](https://www.openvdb.org) data. It has the following attributes:

| Name          | Type       | Default |
| ------------- | ---------- | ------- |
| `vdbfilename` | _`string`_ |         |

The path to an OpenVDB file with the volumetric data.

| Name          | Type       | Default |
| ------------- | ---------- | ------- |
| `densitygrid` | _`string`_ |         |

The name of the OpenVDB grid to use as volume density for the volume shader.

| Name        | Type       | Default |
| ----------- | ---------- | ------- |
| `colorgrid` | _`string`_ |         |

The name of the OpenVDB grid to use as a scattering color multiplier for the volume shader.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `emissiongrid` | _`string`_ |         |

The name of the OpenVDB grid to use directly as emission for the volume shader.

| Name                    | Type       | Default |
| ----------------------- | ---------- | ------- |
| `emissionintensitygrid` | _`string`_ |         |

The name of the OpenVDB grid to use as emission intensity for the volume shader.

| Name              | Type       | Default |
| ----------------- | ---------- | ------- |
| `temperaturegrid` | _`string`_ |         |

The name of the OpenVDB grid to use as temperature for the volume shader.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `velocitygrid` | _`string`_ |         |

The name of the OpenVDB grid to use as motion vectors. This can also name the first of three scalar grids (ie. "velocityX").

| Name                    | Type       | Default |
| ----------------------- | ---------- | ------- |
| `velocityreferencetime` | _`double`_ |         |

The reference time at which the grid data is used directly, without being moved by the velocity grid. Defaults to the [global node](global.md)'s `referencetime` attribute.

| Name            | Type       | Default |
| --------------- | ---------- | ------- |
| `velocityscale` | _`double`_ | `1`     |

A scaling factor applied to the motion vectors.
