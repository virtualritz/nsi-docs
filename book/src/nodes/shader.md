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

Either `shaderfilename` or `shaderobject` must be provided. All other attributes on this node are considered parameters of the shader. They may either be given values or connected to attributes of other shader nodes to build shader networks. ᴏsʟ shader networks must form acyclic graphs or they will be rejected. Refer to [creating ᴏsʟ networks](../guidelines.md#creating-osl-networks) for instructions on ᴏsʟ network creation and usage.
