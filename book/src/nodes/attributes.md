# `attributes`

This node is a generic container for attributes. Its exact purpose depends on where it is connected in the scene. There are currently two uses.

### geometry attributes

This node can provide various geometry related rendering attributes that are not _intrinsic_ to a particular node (for example, one can't set the topology of a polygonal mesh using this attributes node). For this use, instances of this node must be connected to the `geometryattributes` attribute of either geometric primitives or transform nodes (to build [attributes hierarchies](../guidelines.md#a-word-or-two-about-attributes)). Attribute values are gathered along the path starting from the geometric primitive, through all the transform nodes it is connected to, until the [scene root](root.md) is reached.

When an attribute is defined multiple times along this path, the definition with the highest priority is selected. In case of conflicting priorities, the definition that is closest to the geometric primitive (i.e. the furthest from the root) is selected. Connections (for shaders, essentially) can also be assigned priorities, which are used in the same way as for regular attributes. Multiple attributes nodes can be connected to the same geometry or transform nodes (e.g. one attributes node can set object visibility and another can set the surface shader) and will all be considered.

In this case, the node has the following attributes:

| Name            | Type             | Default |
| --------------- | ---------------- | ------- |
| `surfaceshader` | _`<connection>`_ |         |

The [shader node](shader.md) which will be used to shade the surface is connected to this attribute. A priority (useful for overriding a shader from higher in the scene graph) can be specified by setting the `priority` attribute of the connection itself.

| Name                 | Type             | Default |
| -------------------- | ---------------- | ------- |
| `displacementshader` | _`<connection>`_ |         |

The [shader node](shader.md) which will be used to displace the surface is connected to this attribute. A priority (useful for overriding a shader from higher in the scene graph) can be specified by setting the `priority` attribute of the connection itself.

| Name           | Type             | Default |
| -------------- | ---------------- | ------- |
| `volumeshader` | _`<connection>`_ |         |

The [shader node](shader.md) which will be used to shade the volume inside the primitive is connected to this attribute.

| Name            | Type    | Default |
| --------------- | ------- | ------- |
| `ATTR.priority` | _`int`_ | `0`     |

Sets the priority of attribute ATTR when gathering attributes in the scene hierarchy.

| Name                    | Type    | Default |
| ----------------------- | ------- | ------- |
| `visibility.camera`     | _`int`_ | `1`     |
| `visibility.diffuse`    | _`int`_ | `1`     |
| `visibility.hair`       | _`int`_ | `1`     |
| `visibility.reflection` | _`int`_ | `1`     |
| `visibility.refraction` | _`int`_ | `1`     |
| `visibility.shadow`     | _`int`_ | `1`     |
| `visibility.specular`   | _`int`_ | `1`     |
| `visibility.volume`     | _`int`_ | `1`     |

These attributes set visibility for each ray type specified in ᴏsʟ. The same effect could be achieved using shader code (using the `raytype()` function) but it is much faster to filter intersections at trace time. A value of 1 makes the object visible to the corresponding ray type, while 0 makes it invisible.

| Name         | Type    | Default |
| ------------ | ------- | ------- |
| `visibility` | _`int`_ | `1`     |

This attribute sets the default visibility for all ray types. When visibility is set both per ray type and with this default visibility, the attribute with the highest priority is used. If their priority is the same, the more specific attribute (i.e. per ray type) is used.

| Name                        | Type             | Default |
| --------------------------- | ---------------- | ------- |
| `visibility.set.subsurface` | _`<connection>`_ |         |

If a [set node](set.md) is connected to this attribute, subsurface rays will only see objects with a connection to that same set node.

| Name    | Type    | Default |
| ------- | ------- | ------- |
| `matte` | _`int`_ | `0`     |

If this attribute is set to 1, the object becomes a matte for camera rays. Its transparency is used to control the matte opacity and all other shading components are ignored.

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `regularemission` | _`int`_ | `1`     |

If this is set to 1, closures not used with `quantize()` will use emission from the objects affected by the attribute. If set to 0, they will not.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `quantizedemission` | _`int`_ | `1`     |

If this is set to 1, quantized closures will use emission from the objects affected by the attribute. If set to 0, they will not.

| Name     | Type             | Default |
| -------- | ---------------- | ------- |
| `bounds` | _`<connection>`_ |         |

When a geometry node (usually a [mesh node](mesh.md)) is connected to this attribute, it will be used to restrict the effect of the attributes node, which will apply only inside the volume defined by the connected geometry object. It is also possible to connect a transform node to this. It is equivalent to connecting all the geometry nodes connected, even indirectly, to the transform.

### shader attributes

This node can be a container for attributes available to shaders. For this purpose, instances of this node must be connected to the `shaderattributes` attribute of geometric primitives, [transform](transform.md) nodes or [set](set.md) nodes. Attribute values are gathered along the path starting from the geometric primitive, through all the transform nodes it is connected to, until the [scene root](root.md) is reached.

Priority is given to nodes attached closest to the geometric primitive, with the highest priority given to attributes set directly on the geometric primitive. Attributes set on this node may only have a single value.
