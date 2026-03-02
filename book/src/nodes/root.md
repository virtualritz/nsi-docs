# `root`

The root node is much like a transform node with the particularity that it is the end connection for all renderable scene elements (see [basic scene anatomy](../guidelines.md#basic-scene-anatomy)). A node can exist in an ɴsɪ context without being connected to the root note but in that case it won't affect the render in any way. The root node has the reserved handle name `.root` and doesn't need to be created using `NSICreate`. The root node has two defined attributes: `objects` and `geometryattributes`. Both are explained in [the transform node](transform.md).
