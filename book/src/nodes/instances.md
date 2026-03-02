# `instances`

This node is an efficient way to specify a large number of instances. It has the following attributes:

| Name           | Type             | Default |
| -------------- | ---------------- | ------- |
| `sourcemodels` | _`<connection>`_ |         |

The instanced models should connect to this attribute. Connections must have an integer `index` attribute if there are several, so the models effectively form an ordered list.

| Name                     | Type             | Default |
| ------------------------ | ---------------- | ------- |
| `transformationmatrices` | _`doublematrix`_ |         |

A transformation matrix for each instance.

| Name           | Type    | Default |
| -------------- | ------- | ------- |
| `modelindices` | _`int`_ | `0`     |

An optional model selector for each instance. The value used is matched to the `index` attribute of the model connection. A negative value will cause an instance to not be rendered.

| Name                | Type    | Default |
| ------------------- | ------- | ------- |
| `disabledinstances` | _`int`_ |         |

An optional list of indices of instances which are not to be rendered.
