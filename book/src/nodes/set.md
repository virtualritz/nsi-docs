# `set`

This node can be used to express relationships between objects. An example is to connect many lights to such a node to create a _light set_ and then to connect this node to `outputlayer.lightset` ([outputlayer](outputlayer.md) and [light layers](../guidelines.md#light-layers)). It has the following attributes:

| Name      | Type             | Default |
| --------- | ---------------- | ------- |
| `members` | _`<connection>`_ |         |

This connection accepts all nodes that are members of the set.
