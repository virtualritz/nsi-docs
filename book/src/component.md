| **Name** | **Type** | **Description/Values**                                                                                                                                                                                     |
| -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index`  | integer  | A list of indices of components. It identifies which component of the original geometry will be part of this component set.                                                                                |
| `level`  | integer  | Specifies hierarchical depth of the component this node targets. The only node that supports a depth higher than 0 is the [curves]{.title-ref} node. The meaning depends on the node this is connected to. |
|          |          | mesh node                                                                                                                                                                                                  |
|          |          | curves node                                                                                                                                                                                                |
|          |          | particles node                                                                                                                                                                                             |
|          |          | patchmesh node                                                                                                                                                                                             |
|          |          | procedural node                                                                                                                                                                                            |

component node optional attributes

Proceduaral nodes need to tag the level using the `__componentlevel` attribute.

Let\'s take for example a procedural tree node.
