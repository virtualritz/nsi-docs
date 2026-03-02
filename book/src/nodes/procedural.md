# `procedural`

This node acts as a proxy for geometry that could be defined at a later time than the node's definition, using a procedural supported by `NSIEvaluate`. Since the procedural is evaluated in complete isolation from the rest of the scene, it can be done either lazily (depending on its `boundingbox` attribute) or in parallel with other procedural nodes.

The procedural node supports, as its attributes, all the parameters of the `NSIEvaluate` API call, meaning that procedural types accepted by that API call (NSI archives, dynamic libraries, LUA scripts) are also supported by this node. Those attributes are used to call a procedural that is expected to define a sub-scene, which has to be independent from the other nodes in the scene. The procedural node will act as the sub-scene's local root and, as such, also supports all the attributes of a regular transform node. In order to connect the nodes it creates to the sub-scene's root, the procedural simply has to connect them to the regular [root node](root.md) `.root`.

In the context of an [interactive render](global.md), the procedural will be executed again after the node's attributes have been edited. All nodes previously connected by the procedural to the sub-scene's root will be deleted automatically before the procedural's re-execution.

Additionally, this node has the following optional attribute:

| Name          | Type         | Default |
| ------------- | ------------ | ------- |
| `boundingbox` | _`point[2]`_ |         |

Specifies a bounding box for the geometry where `boundingbox[0]` and `boundingbox[1]` correspond, respectively, to the "minimum" and the "maximum" corners of the box.
