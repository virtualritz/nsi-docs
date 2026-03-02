# `mesh`

This node represents a polygon mesh. It has the following required attributes:

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

The positions of the object's vertices. Typically, this attribute will be [addressed indirectly](#passing-optional-arguments) through a `P.indices` attribute.

| Name        | Type    | Default |
| ----------- | ------- | ------- |
| `nvertices` | _`int`_ |         |

The number of vertices for each face of the mesh. The number of values for this attribute specifies total face number (unless `nholes` is defined).

It also has optional attributes:

| Name     | Type    | Default |
| -------- | ------- | ------- |
| `nholes` | _`int`_ |         |

The number of holes in the polygons. When this attribute is defined, the total number of faces in the mesh is defined by the number of values for `nholes` rather than for `nvertices`. For each face, there should be (nholes+1) values in `nvertices`: the respective first value specifies the number of vertices on the outside perimeter of the face, while additional values describe the number of vertices on perimeters of holes in the face.

| Name               | Type    | Default |
| ------------------ | ------- | ------- |
| `clockwisewinding` | _`int`_ | `0`     |

A value of 1 specifies that polygons with a clockwise winding order are front facing. The default is 0, making counterclockwise polygons front facing.

| Name                 | Type       | Default |
| -------------------- | ---------- | ------- |
| `subdivision.scheme` | _`string`_ |         |

A value of `"catmull-clark"` will cause the mesh to render as a Catmull-Clark subdivision surface.

| Name                         | Type    | Default |
| ---------------------------- | ------- | ------- |
| `subdivision.cornervertices` | _`int`_ |         |

This attribute is a list of vertices which are sharp corners. The values are indices into the P attribute, like `P.indices`.

| Name                          | Type      | Default |
| ----------------------------- | --------- | ------- |
| `subdivision.cornersharpness` | _`float`_ |         |

This attribute is the sharpness of each specified sharp corner. It must have a value for each value given in `subdivision.cornervertices`.

| Name                         | Type    | Default |
| ---------------------------- | ------- | ------- |
| `subdivision.creasevertices` | _`int`_ |         |

This attribute is a list of crease edges. Each edge is specified as a pair of indices into the P attribute, like `P.indices`.

| Name                          | Type      | Default |
| ----------------------------- | --------- | ------- |
| `subdivision.creasesharpness` | _`float`_ |         |

This attribute is the sharpness of each specified crease. It must have a value for each pair of values given in `subdivision.creasevertices`.

| Name                              | Type    | Default |
| --------------------------------- | ------- | ------- |
| `subdivision.smoothcreasecorners` | _`int`_ | `1`     |

This attribute controls whether or not the surface uses enhanced subdivision rules on vertices where more than two creased edges meet. With a value of 0, the vertex becomes a sharp corner. With a value of 1, the vertex is subdivided using an extended crease vertex subdivision rule which yields a smooth crease.

| Name            | Type       | Default |
| --------------- | ---------- | ------- |
| `referencetime` | _`double`_ |         |

Specifies a reference time where deformation data is most valid. This is mainly relevant for velocity blur, in which case it should be set to the time at which position data was originally available. If not set, see the same attribute on the [global node](global.md).

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `quadraticmotion` | _`int`_ | `0`     |

A value of 1 will enable curved deformation blur if three equally spaced time samples are provided for the P attribute. Linear deformation is used otherwise.

| Name                     | Type      | Default |
| ------------------------ | --------- | ------- |
| `outlinecreasethreshold` | _`float`_ | `10`    |

Controls how sharp a crease must be to be considered for the creation of outlines.
