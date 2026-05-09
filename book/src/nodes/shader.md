# `shader`

This node represents an ᴏsʟ shader, also called layer when part of a shader group. It has the following attributes:

| Name             | Type       | Default |
| ---------------- | ---------- | ------- |
| `shaderfilename` | _`string`_ |         |

This is the name of the file which contains the shader's compiled code.

| Name           | Type       | Default |
| -------------- | ---------- | ------- |
| `shaderobject` | _`string`_ |         |

This contains the complete compiled shader code. It allows providing custom shaders without going through files.

| Name               | Type       | Default |
| ------------------ | ---------- | ------- |
| `materialxnodedef` | _`string`_ |         |

The name of the MaterialX node definition to use.

| Name               | Type       | Default |
| ------------------ | ---------- | ------- |
| `materialxversion` | _`string`_ |         |

The MaterialX library version to use to find the node. If unspecified, the most up to date version is used.

Either `shaderfilename`, `shaderobject` or `materialxnodedef` must be provided. All other attributes on this node are considered parameters of the shader. They may either be given values or connected to attributes of other shader nodes to build shader networks. ᴏsʟ shader networks must form acyclic graphs or they will be rejected. Refer to [creating ᴏsʟ networks](../guidelines.md#creating-osl-networks) for instructions on ᴏsʟ network creation and usage.
