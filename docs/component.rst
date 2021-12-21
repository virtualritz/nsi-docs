
.. table:: component node optional attributes
    :widths: 3 1 6

    +---------------------------------+----------+--------------------------------------------+
    | **Name**                        | **Type** | **Description/Values**                     |
    +=================================+==========+============================================+
    | ``index``                       | integer  | A list of indices of components. It        |
    |                                 |          | identifies which component of the original |
    |                                 |          | geometry will be part of this component    |
    |                                 |          | set.                                       |
    +---------------------------------+----------+--------------------------------------------+
    | ``level``                       | integer  | Specifies hierarchical depth of the        |
    |                                 |          | component this node targets.               |
    |                                 |          | The only node that supports a depth higher |
    |                                 |          | than 0 is the `curves` node.               |
    |                                 |          | The meaning depends on the node this is    |
    |                                 |          | connected to.                              |
    |                                 |          +-----------------+--------------------------+
    |                                 |          | mesh node       | The `index` attribute    |
    |                                 |          |                 | refers to an individual  |
    |                                 |          |                 | face.                    |
    |                                 |          +-----------------+--------------------------+
    |                                 |          | curves node     | `0` – The `index`        |
    |                                 |          |                 | attribute refers to an   |
    |                                 |          |                 | individual curve.        |
    |                                 |          |                 |                          |
    |                                 |          |                 | `1` – The `index`        |
    |                                 |          |                 | attribute refers to a    |
    |                                 |          |                 | span on an individual    |
    |                                 |          |                 | curve.                   |
    |                                 |          +-----------------+--------------------------+
    |                                 |          | particles node  | The `index` attribute    |
    |                                 |          |                 | refers to an individual  |
    |                                 |          |                 | particle.                |
    |                                 |          +-----------------+--------------------------+
    |                                 |          | patchmesh node  | The `index` attribute    |
    |                                 |          |                 | refers to an individual  |
    |                                 |          |                 | subpatch. Sub-patches    |
    |                                 |          |                 | are numbered per column  |
    |                                 |          |                 | per row. I.e. the first  |
    |                                 |          |                 | row indices 0, 1, 2 ...  |
    |                                 |          +-----------------+--------------------------+
    |                                 |          | procedural node | Procedural nodes         |
    |                                 |          |                 |                          |
    +---------------------------------+----------+-----------------+--------------------------+

Proceduaral nodes need to tag the level using the ``__componentlevel`` attribute.

Let's take for example a procedural tree node.

