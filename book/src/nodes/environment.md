# `environment`

This geometry node defines a sphere of infinite radius. Its only purpose is to render environment lights, solar lights and directional lights; lights which cannot be efficiently modeled using area lights. In practical terms, this node is no different than a geometry node with the exception of shader execution semantics: there is no surface position P, only a direction I (refer to [lighting guidelines](../guidelines.md#lighting-in-the-nodal-scene-interface) for more practical details). The following node attribute is recognized:

| Name    | Type       | Default |
| ------- | ---------- | ------- |
| `angle` | _`double`_ | `360`   |

Specifies the cone angle representing the region of the sphere to be sampled. The angle is measured around the Z+ axis. If the angle is set to 0, the environment describes a directional light. Refer to [lighting guidelines](../guidelines.md#lighting-in-the-nodal-scene-interface) for more about how to specify light sources.
