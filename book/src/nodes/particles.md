# `particles`

This geometry node represents a collection of _tiny_ particles. Particles are represented by either a disk or a sphere. This primitive is not suitable to render large particles as these should be represented by other means (e.g. instancing).

| Name | Type      | Default |
| ---- | --------- | ------- |
| `P`  | _`point`_ |         |

A mandatory attribute that specifies the center of each particle.

| Name    | Type      | Default |
| ------- | --------- | ------- |
| `width` | _`float`_ |         |

A mandatory attribute that specifies the width of each particle. It can be specified for the entire particles node (only one value provided) or per-particle.

| Name | Type       | Default |
| ---- | ---------- | ------- |
| `N`  | _`normal`_ |         |

The presence of a normal indicates that each particle is to be rendered as an oriented disk. The orientation of each disk is defined by the provided normal which can be constant or a per-particle attribute. Each particle is assumed to be a sphere if a normal is not provided.

| Name                 | Type    | Default |
| -------------------- | ------- | ------- |
| `reverseorientation` | _`int`_ | `0`     |

Setting this to 1 will reverse the orientation of spherical particles. Specifically, their u parametric direction is reversed, which also reverses their normal so it points inwards. It has no effect on particles for which N is provided.

| Name | Type    | Default |
| ---- | ------- | ------- |
| `id` | _`int`_ |         |

This attribute, of the same size as P, assigns a unique identifier to each particle which must be constant throughout the entire shutter range. Its presence is necessary in the case where particles are motion blurred and some of them could appear or disappear during the motion interval. Having such identifiers allows the renderer to properly render such transient particles. This implies that the number of _ids_ might vary for each time step of a motion-blurred particle cloud so the use of `NSISetAttributeAtTime` is mandatory by definition.

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `quadraticmotion` | _`int`_ | `0`     |

A value of 1 will enable curved deformation blur if three equally spaced time samples are provided for the P attribute. Linear deformation is used otherwise.
