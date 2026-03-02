# `transform`

This node represents a geometric transformation. Transform nodes can be chained together to express transform concatenation, hierarchies and instances. Transform nodes also accept attributes to implement [hierarchical attribute assignment and overrides](../guidelines.md#a-word-or-two-about-attributes). It has the following attributes:

| Name                   | Type             | Default |
| ---------------------- | ---------------- | ------- |
| `transformationmatrix` | _`doublematrix`_ |         |

This is a 4x4 matrix which describes the node's transformation. Matrices in ɴsɪ post-multiply column vectors so are of the form:

```
| w11  w12  w13  0 |
| w21  w22  w23  0 |
| w31  w32  w33  0 |
| Tx   Ty   Tz   1 |
```

| Name      | Type             | Default |
| --------- | ---------------- | ------- |
| `objects` | _`<connection>`_ |         |

This is where the transformed objects are connected to. This includes geometry nodes, other transform nodes and camera nodes.

| Name                 | Type             | Default |
| -------------------- | ---------------- | ------- |
| `geometryattributes` | _`<connection>`_ |         |

This is where [attributes nodes](attributes.md) may be connected to affect any geometry transformed by this node. Refer to [attributes](../guidelines.md#a-word-or-two-about-attributes) and [instancing](../guidelines.md#instancing) for explanation on how this connection is used.

| Name               | Type             | Default |
| ------------------ | ---------------- | ------- |
| `shaderattributes` | _`<connection>`_ |         |

This is where [attributes nodes](attributes.md) may be connected to provide shader attributes for any geometry transformed by this node.
