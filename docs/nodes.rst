.. include:: definitions.rst

.. _chapter:nodes:

Nodes
=====

The following sections describe available nodes in technical terms.
Refer to :ref:`the rendering guidelines<chapter:guidelines>` for usage
details.

.. table:: Overview of nsi nodes
   :widths: 2 8

   +----------------------------------------+--------------------------+
   | **Node**                               | **Function**             |
   +========================================+==========================+
   | :ref:`root<node:root>`                 | The scene's root         |
   +----------------------------------------+--------------------------+
   | :ref:`global<node:global>`             | Global settings node     |
   +----------------------------------------+--------------------------+
   | :ref:`set<node:set>`                   | Expresses relationships  |
   |                                        | of groups of nodes       |
   +----------------------------------------+--------------------------+
   | :ref:`shader<node:shader>`             | osl shader or layer in a |
   |                                        | shader group             |
   +----------------------------------------+--------------------------+
   | :ref:`attributes<node:attributes>`     | Container for generic    |
   |                                        | attributes (e.g.         |
   |                                        | visibility)              |
   +----------------------------------------+--------------------------+
   | :ref:`transform<node:transform>`       | Transformation to place  |
   |                                        | objects in the scene     |
   +----------------------------------------+--------------------------+
   | :ref:`instances<node:instances>`       | Specifies instances of   |
   |                                        | other nodes              |
   +----------------------------------------+--------------------------+
   | :ref:`mesh<node:mesh>`                 | Polygonal mesh or        |
   |                                        | subdivision surface      |
   +----------------------------------------+--------------------------+
   | :ref:`faceset<node:faceset>`           | Assign attributes to     |
   |                                        | part of a mesh           |
   +----------------------------------------+--------------------------+
   | :ref:`curves<node:curves>`             | Linear, b-spline and     |
   |                                        | Catmull-Rom curves       |
   +----------------------------------------+--------------------------+
   | :ref:`particles<node:particles>`       | Collection of particles  |
   +----------------------------------------+--------------------------+
   | :ref:`procedural<node:procedural>`     | Geometry to be loaded    |
   |                                        | or generated in delayed  |
   |                                        | fashion                  |
   +----------------------------------------+--------------------------+
   | :ref:`volume<node:volume>`             | A volume loaded from a   |
   |                                        | VDB file                 |
   +----------------------------------------+--------------------------+
   | :ref:`environment<node:environment>`   | Geometry type to define  |
   |                                        | environment lighting     |
   +----------------------------------------+--------------------------+
   | :ref:`camera<node:camera>`             | Set of nodes to create   |
   |                                        | viewing cameras          |
   +----------------------------------------+--------------------------+
   | :ref:`outputdriver<node:outputdriver>` | A target where to        |
   |                                        | output rendered pixels   |
   +----------------------------------------+--------------------------+
   | :ref:`outputlayer<node:outputlayer>`   | Describes one render     |
   |                                        | layer to be connected    |
   |                                        | to an ``outputdriver``   |
   |                                        | node                     |
   +----------------------------------------+--------------------------+
   | :ref:`screen<node:screen>`             | Describes how the view   |
   |                                        | from acamera will be     |
   |                                        | rasterized into an       |
   |                                        | ``outputlayer`` node     |
   +----------------------------------------+--------------------------+

.. _node:root:

The root node
-------------

The root node is much like a transform node. With the particularity that
it is the :ref:`end connection<section:basicscene>` for all renderable
scene elements. A node can exist in an nsi context without being
connected to the root note but in that case it won't affect the render
in any way. The root node has the reserved handle name ``.root`` and
doesn’t need to be created using ``NSICreate()``. The root node has two
defined attributes: ``objects`` and ``geometryattributes``. Both are
explained under the :ref:`transform node<node:transform>`.

.. _node:global:

The global node
---------------

This node contains various global settings for a particular nsi context.
Note that these attributes are for the most case implementation
specific.

This node has the reserved handle name ``.global`` and doesn't
need to be created using ``NSICreate()``. The following attributes are
recognized by *3Delight*:


.. table:: global node optional attributes
    :widths: 3 1 2 4

    +---------------------------------+----------+--------------------------------------------+
    | **Name**                        | **Type** | **Description/Values**                     |
    +=================================+==========+============================================+
    | ``numberofthreads``             | integer  | Specifies the total number of threads to   |
    | ``render.threads.number`` (!)   |          | use for a particular render:               |
    |                                 |          +--------------------------------------------+
    |                                 |          | -  A value of ``0`` lets the render engine |
    |                                 |          |    choose an optimal thread value.         |
    |                                 |          |    This is is the **default** behaviour.   |
    |                                 |          | -  Any positive value directly sets the    |
    |                                 |          |    total number of                         |
    |                                 |          |    render threads.                         |
    |                                 |          | -  A negative value will start as many     |
    |                                 |          |    threads as optimal *plus* the specified |
    |                                 |          |    value. This allows for an easy way to   |
    |                                 |          |    to decrease the total number of render  |
    |                                 |          |    threads.                                |
    +---------------------------------+----------+--------------------------------------------+
    | ``renderatlowpriority``         | integer  | If set to 1, start the render with a lower |
    | ``render.priority.low`` (!)     |          | process priority. This can be useful if    |
    |                                 |          | there are other applications that must run |
    |                                 |          | during rendering.                          |
    +---------------------------------+----------+--------------------------------------------+
    | ``texturememory``               | integer  | Specifies the approximate maximum memory   |
    | ``texture.memory`` (!)          |          | size, in megabytes, the renderer will      |
    |                                 |          | allocate to accelerate texture access.     |
    +---------------------------------+----------+--------------------------------------------+
    | ``bucketorder``                 | string   | Specifies in what order the buckets are    |
    | ``bucket.order``                |          | rendered. The available values are:        |
    |                                 |          +----------------+---------------------------+
    |                                 |          | ``horizontal`` | Row by row, left to right |
    |                                 |          |                | and top to bottom. This   |
    |                                 |          |                | is the **default**.       |
    |                                 |          +----------------+---------------------------+
    |                                 |          | ``vertical``   | Column by column, top to  |
    |                                 |          |                | bottom and left to right. |
    |                                 |          +----------------+---------------------------+
    |                                 |          | ``zigzag``     | Row by row, left to right |
    |                                 |          |                | on even rows and right to |
    |                                 |          |                | left on odd rows.         |
    |                                 |          +----------------+---------------------------+
    |                                 |          | ``spiral``     | In a clockwise spiral     |
    |                                 |          |                | from the centre of the    |
    |                                 |          |                | image.                    |
    |                                 |          +----------------+---------------------------+
    |                                 |          | ``circle``     | In concentric circles     |
    |                                 |          |                | from the centre of the    |
    |                                 |          |                | image.                    |
    +---------------------------------+----------+----------------+---------------------------+
    | ``frame``                       | integer  | Provides a frame number to be used as a    |
    |                                 |          | seed for the sampling pattern.             |
    |                                 |          | See the :ref:`screen node<node:screen>`.   |
    +---------------------------------+----------+--------------------------------------------+

.. index::
   caching
   disk cache
   disk usage
   network cache
   temporary files

.. table:: global node optional network cache attributes
   :widths: 3 1 6

   +---------------------------------+----------+--------------------------------------------+
   | ``networkcache.size``           | integer  | Specifies the maximum network cache size,  |
   |                                 |          | in gigabytes (*GB*, not *GiB*), the        |
   |                                 |          | renderer will use to cache textures on a   |
   |                                 |          | local drive to accelerate data access.     |
   +---------------------------------+----------+--------------------------------------------+
   | ``networkcache.directory``      | string   | Specifies the directory in which textures  |
   |                                 |          | will be cached. A good default value is    |
   |                                 |          | ``/var/tmp/3DelightCache`` on Linux        |
   |                                 |          | systems.                                   |
   +---------------------------------+----------+--------------------------------------------+
   | ``networkcache.write``          | integer  | Enables caching for image write            |
   |                                 |          | operations. This alleviates pressure on    |
   |                                 |          | networks by first rendering images to a    |
   |                                 |          | local temporary location and copying them  |
   |                                 |          | to their final destination at the end of   |
   |                                 |          | the render. This replaces many small       |
   |                                 |          | network writes by more efficient larger    |
   |                                 |          | operations.                                |
   +---------------------------------+----------+--------------------------------------------+

.. index::
    license
    server

.. table:: global node optional attributes fpr licensing
   :widths: 3 1 6

   +---------------------------------+----------+--------------------------------------------+
   | ``license.server``              | string   | Specifies the name or IP address of the    |
   |                                 |          | license server to be used.                 |
   +---------------------------------+----------+--------------------------------------------+
   | ``license.wait``                | integer  | When no license is available for           |
   |                                 |          | rendering, the renderer will wait until a  |
   |                                 |          | license is available if this attribute is  |
   |                                 |          | set to ``1``, but will stop immediately if |
   |                                 |          | it is set to ``0``.                        |
   |                                 |          | The latter setting is useful when managing |
   |                                 |          | a renderfarm and other work could be       |
   |                                 |          | scheduled instead.                         |
   +---------------------------------+----------+--------------------------------------------+
   | ``license.hold``                | integer  | By default, the renderer will get new      |
   |                                 |          | licenses for every render and release them |
   |                                 |          | once it is done. This can be undesirable   |
   |                                 |          | if several frames are rendered in sequence |
   |                                 |          | from the same process process. If this     |
   |                                 |          | option is set to ``1``, the licenses       |
   |                                 |          | obtained for the first frame are held      |
   |                                 |          | until the last frame is finished.          |
   +---------------------------------+----------+--------------------------------------------+

.. index::
   diffuse ray depth
   diffuse ray length
   reflection ray depth
   reflection ray length
   refraction ray depth
   refraction ray length
   glossy ray length
   specular ray length
   volume ray depth
   volume ray length
   hair ray depth
   hair ray length

.. table:: global node optional attributes governing ray tracing quality
    :widths: 3 1 6

    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraydepth.diffuse``     | integer  | Specifies the maximum bounce depth a ray   |
    | ``diffuse.ray.depth.max``       |          | emitted from a diffuse |closure| can       |
    |                                 |          | reach. A depth of ``1`` specifies one      |
    |                                 |          | additional bounce compared to purely local |
    |                                 |          | illumination.                              |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.diffuse``    | double   | Limits the distance a ray emitted from a   |
    | ``diffuse.ray.length.max``      |          | diffuse |closure| can travel.              |
    |                                 |          |                                            |
    |                                 |          | Using a relatively low value for this      |
    |                                 |          | attribute might improve performance        |
    |                                 |          | without significantly affecting the look   |
    |                                 |          | of the resulting image, as it restrains    |
    |                                 |          | the extent of global illumination.         |
    |                                 |          |                                            |
    |                                 |          | Setting this to a negative value disables  |
    |                                 |          | the limitation.                            |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraydepth.reflection``  | integer  | Specifies the maximum bounce depth a       |
    | ``reflection.ray.depth.max``    |          | reflection ray can reach.                  |
    |                                 |          |                                            |
    |                                 |          |                                            |
    |                                 |          | Setting reflection depth to 0 will only    |
    |                                 |          | compute local illumination resulting in    |
    |                                 |          | only surfaces with an emission |closure|   |
    |                                 |          | to appear in reflections.                  |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.reflection`` | double   | Limits the distance a reflection ray can   |
    | ``reflection.ray.length.max``   |          | travel. Setting this to a negative value   |
    |                                 |          | disables the limitation.                   |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.specular``   | double   | Limits the distance a glossy ray can       |
    | ``glossy.ray.length.max``       |          | travel. Setting this to a negative value   |
    |                                 |          | disables the limitation.                   |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraydepth.refraction``  | integer  | Specifies the maximum bounce depth a       |
    | ``refraction.ray.depth.max``    |          | refraction ray can reach.                  |
    |                                 |          |                                            |
    |                                 |          | The default value of ``4`` allows light to |
    |                                 |          | shine through a properly modeled object    |
    |                                 |          | such as a glass.                           |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.refraction`` | double   | Limits the distance a refraction ray can   |
    | ``refraction.ray.length.max``   |          | travel. Setting this to a negative value   |
    |                                 |          | disables the limitation.                   |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraydepth.hair``        | integer  | Specifies the maximum bounce depth a hair  |
    | ``hair.ray.depth.max``          |          | ray can reach.                             |
    |                                 |          |                                            |
    |                                 |          | Note that hair are akin to volumetric      |
    |                                 |          | primitives and might need elevated ray     |
    |                                 |          | depth to properly capture the              |
    |                                 |          | illumination.                              |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.hair``       | double   | Limits the distance a hair ray can         |
    | ``hair.ray.length.max`` (!)     |          | travel. Setting this to a negative value   |
    |                                 |          | disables the limitation.                   |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraydepth.volume``      | integer  | Specifies the maximum bounce depth a       |
    | ``volume.ray.depth.max`` (!)    |          | volume ray can reach.                      |
    +---------------------------------+----------+--------------------------------------------+
    | ``maximumraylength.volume``     | double   | Limits the distance a volume ray can       |
    | ``volume.ray.length.max`` (!)   |          | travel. Setting this to a negative value   |
    |                                 |          | disables the limitation.                   |
    +---------------------------------+----------+--------------------------------------------+

.. index::
   image quality
   shading rate
   shading samples
   volume samples
   displacement
   subsurface

.. table:: global node optional attributes controlling overall image quality
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | ``quality.shadingsamples``      | integer  | Controls the quality of BSDF sampling.    |
    | ``shading.samples``             |          | Larger values give less visible noise.    |
    +---------------------------------+----------+-------------------------------------------+
    | ``quality.volumesamples``       | integer  | Controls the quality of volume sampling.  |
    | ``volume.samples``              |          | Larger values give less visible noise.    |
    +---------------------------------+----------+-------------------------------------------+
    | ``displacement.show``           | integer  | When set to ``1``, enables displacement   |
    | ``shading.displacement`` (!)    |          | shading. Otherwise, it must be set to     |
    |                                 |          | ignore any displacement shader in the     |
    |                                 |          | scene.                                    |
    +---------------------------------+----------+-------------------------------------------+
    | ``subsurface.show``             | integer  | When set to ``1``, enables the            |
    | ``shading.subsurface`` (!)      |          | ``subsurface()`` osl |closure|.           |
    |                                 |          | Otherwise, it must be set to ``0``, which |
    |                                 |          | will ignore this |closure| in osl         |
    |                                 |          | shaders.                                  |
    +---------------------------------+----------+-------------------------------------------+

For anti-aliasing quality see the :ref:`screen node<node:screen>`.

.. index::
   statistics
   render time

.. table:: global node optional attributes for statistics
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | ``statistics.progress``         | integer  | When set to ``1``, prints rendering       |
    |                                 |          | progress as a percentage of completed     |
    |                                 |          | pixels.                                   |
    +---------------------------------+----------+-------------------------------------------+
    | ``statistics.filename``         | string   | Full path of the file where rendering     |
    |                                 |          | statistics will be written. An empty      |
    |                                 |          | string will write statistics to standard  |
    |                                 |          | output. The name ``null`` will not output |
    |                                 |          | statistics.                               |
    +---------------------------------+----------+-------------------------------------------+

.. index::
    light layer
    light set
    outputlayer
    set

.. _node:set:

The set node
------------

This node can be used to express relationships between objects.

An example is to connect many lights to such a node to create a *light
set* and then to connect this node to ``outputlayer.lightset`` (see
:ref:`outputlayer<node:outputlayer>` and
:ref:`light layers<section:lightlayers>` ).

It has the following attributes:

.. table:: set node optional attributes
    :widths: 3 1 6

    +---------------------------------+--------------+---------------------------------------+
    | **Name**                        | **Type**     | **Description/Values**                |
    +=================================+==============+=======================================+
    | ``objects``                     | <connection> | This connection accepts all nodes     |
    |                                 |              | that are members of the set.          |
    +---------------------------------+--------------+---------------------------------------+

.. _node:mesh:

.. index::
    mesh node

The mesh node
-------------

This node represents a polygon mesh or a subdivision surface. It has the following required
attributes:

.. table:: mesh node required attributes
   :widths: 3 1 6

   +---------------------------------+----------+--------------------------------------------+
   | **Name**                        | **Type** | **Description/Values**                     |
   +=================================+==========+============================================+
   | ``P``                           | point    | The positions of the object’s vertices.    |
   |                                 |          | Typically, this attribute will be indexed  |
   |                                 |          | through a ``P.indices`` attribute.         |
   +---------------------------------+----------+--------------------------------------------+
   | ``nvertices``                   | integer  | The number of vertices for each face of    |
   |                                 |          | the mesh. The number of values for this    |
   | ``vertices.size`` (!)           |          | attribute specifies total face number      |
   |                                 |          | (unless ``nholes`` is defined).            |
   +---------------------------------+----------+--------------------------------------------+

It also has these optional attributes:

.. index::
    subdivision surface
    Catmull-Clark
    crease
    corner
    sharpness
    winding order
    clockwise winding
    counterclockwise winding

.. table:: mesh node optional attributes
   :widths: 3 1 6

   +---------------------------------+----------+--------------------------------------------+
   | **Name**                        | **Type** | **Description/Values**                     |
   +=================================+==========+============================================+
   | ``nholes``                      | integer  | The number of holes in the polygons.       |
   |                                 |          | When this attribute is defined, the total  |
   | ``holes.length`` (1)            |          | number of faces in the mesh is defined by  |
   |                                 |          | the number of values for ``nholes``        |
   |                                 |          | rather than for ``nvertices``. For         |
   |                                 |          | each face, there should be                 |
   |                                 |          | (``holes.length``+1) values in             |
   |                                 |          | ``vertices``: the respective first value   |
   |                                 |          | specifies the number of vertices on the    |
   |                                 |          | outside perimeter of the face, while       |
   |                                 |          | additional values describe the number of   |
   |                                 |          | vertices on perimeters of holes in the     |
   |                                 |          | face. shows the definition of a polygon    |
   |                                 |          | mesh consisting of 3 square faces, with    |
   |                                 |          | one triangular hole in the first one and   |
   |                                 |          | square holes in the second one.            |
   +---------------------------------+----------+--------------------------------------------+
   | ``clockwisewinding``            | integer  | A value of ``1`` specifies that polygons   |
   |                                 |          | with clockwise winding order are front     |
   |                                 |          | facing.                                    |
   |                                 |          |                                            |
   |                                 |          | **The default** is ``0``, making           |
   |                                 |          | counterclockwise polygons front facing.    |
   +---------------------------------+----------+--------------------------------------------+
   | ``subdivision.scheme``          | string   | A value of ``"catmull-clark"`` will cause  |
   |                                 |          | the mesh to render as a Catmull-Clark      |
   |                                 |          | subdivision surface.                       |
   +---------------------------------+----------+--------------------------------------------+
   | ``subdivision.cornervertices``  | integer  | A list of vertices which are sharp         |
   |                                 |          | corners. The values are indices into the   |
   |                                 |          | ``P`` attribute, like ``P.indices``.       |
   +---------------------------------+----------+--------------------------------------------+
   | ``subdivision.cornersharpness`` | float    | The sharpness of each specified sharp      |
   |                                 |          | corner. It must have a value for each      |
   |                                 |          | value given in                             |
   |                                 |          | ``subdivision.cornervertices``.            |
   +---------------------------------+----------+--------------------------------------------+
   | ``subdivision.creasevertices``  | integer  | A list of crease edges. Each edge is       |
   |                                 |          | specified as a pair of indices into the    |
   |                                 |          | ``P`` attribute, like ``P.indices``.       |
   +---------------------------------+----------+--------------------------------------------+
   | ``subdivision.creasesharpness`` | float    | The sharpness of each specified crease. It |
   |                                 |          | must have a value for each pair of values  |
   |                                 |          | given in ``subdivision.creasevertices``.   |
   +---------------------------------+----------+--------------------------------------------+

.. index::
    mesh example

.. code-block:: shell
   :linenos:

   Create "holey" "mesh"
   SetAttribute "holey"
     "nholes" "int" 3 [ 1 2 0 ]
     "nvertices" "int" 6 [
       4 3                 # Square with 1 triangular hole
       4 4 4               # Square with 2 square holes
       4 ]                 # Square with 0 hole
     "P" "point" 23 [
       0 0 0   3 0 0   3 3 0   0 3 0
       1 1 0   2 1 0   1 2 0

       4 0 0   9 0 0   9 3 0   4 3 0
       5 1 0   6 1 0   6 2 0   5 2 0
       7 1 0   8 1 0   8 2 0   7 2 0

       10 0 0   13 0 0   13 3 0   10 3 0 ]


.. _node:faceset:

.. index::
    faceset node
    tagging faces
    shaders on faces
    shaders on curves

The faceset node
----------------

This node is used to provide a way to attach attributes to some faces of
another geometric primitive, such as the :ref:`mesh node<node:mesh>`. It
has the following attributes:

.. table:: set node optional attributes
    :widths: 3 1 6

    +---------------------------------+--------------+---------------------------------------+
    | **Name**                        | **Type**     | **Description/Values**                |
    +=================================+==============+=======================================+
    | ``faces``                       | integer      | A list of indices of faces. It        |
    |                                 |              | identifies which faces of the         |
    |                                 |              | original geometry will be part of     |
    |                                 |              | this face set.                        |
    +---------------------------------+--------------+---------------------------------------+

.. code-block:: shell
   :linenos:

   Create "subdiv" "mesh"
   SetAttribute "subdiv"
     "nvertices" "int" 4 [ 4 4 4 4 ]
     "P" "point" 9 [
       0 0 0    1 0 0    2 0 0
       0 1 0    1 1 0    2 1 0
       0 2 0    1 2 0    2 2 2 ]
     "P.indices" "int" 16 [
       0 1 4 3    2 3 5 4    3 4 7 6    4 5 8 7 ]
     "subdivision.scheme" "string" 1 "catmull-clark"

   Create "set1" "faceset"
   SetAttribute "set1"
     "faces" "int" 2 [ 0 3 ]
   Connect "set1" "" "subdiv" "facesets"

   Connect "attributes1" "" "subdiv" "geometryattributes"
   Connect "attributes2" "" "set1" "geometryattributes"

.. _node:curves:

The curves node
---------------

This node represents a group of curves. It has the following required
attributes:

.. table:: curves node required attributes
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | **Name**                        | **Type** | **Description/Values**                    |
    +=================================+==========+===========================================+
    | ``nverts``                      | integer  | The number of vertices for each curve.    |
    | ``vertices.size`` (!)           |          | This must be at least ``4`` for cubic     |
    |                                 |          | curves and ``2`` for linear curves. There |
    |                                 |          | can be either a single value or one value |
    |                                 |          | per curve.                                |
    +---------------------------------+----------+-------------------------------------------+
    | ``P``                           | point    | The positions of the curve vertices. The  |
    |                                 |          | number of values provided, divided by     |
    |                                 |          | ``nvertices``, gives the number of        |
    |                                 |          | curves which will be rendered.            |
    +---------------------------------+----------+-------------------------------------------+
    | ``width``                       | float    | The width of the curves.                  |
    +---------------------------------+----------+-------------------------------------------+

It also has these optional attributes:

.. index::
    basis
    extrapolate
    optional curve attributes

.. table:: curves node optional attributes
    :widths: 3 1 2 4

    +---------------------------------+----------+-------------------------------------------+
    | ``basis``                       | string   | The basis functions used for curve        |
    |                                 |          | interpolation. Possible choices are:      |
    |                                 |          +-----------------+-------------------------+
    |                                 |          | ``b-spline``    | B-spline interpolation. |
    |                                 |          +-----------------+-------------------------+
    |                                 |          | ``catmull-rom`` | Catmull-Rom             |
    |                                 |          |                 | interpolation. This is  |
    |                                 |          |                 | **the default** value.  |
    |                                 |          +-----------------+-------------------------+
    |                                 |          | ``linear``      | Linear interpolation.   |
    +---------------------------------+----------+-----------------+-------------------------+
    | ``N``                           | normal   | The presence of a normal indicates that   |
    |                                 |          | each curve is to be rendered as an        |
    |                                 |          | oriented ribbon. The orientation of each  |
    |                                 |          | ribbon is defined by the provided normal  |
    |                                 |          | which can be constant, a per-curve or a   |
    |                                 |          | per-vertex attribute.                     |
    |                                 |          | Each ribbon is assumed to alwyas facing   |
    |                                 |          | the camera if a normal is not provided.   |
    +---------------------------------+----------+-------------------------------------------+
    | ``extrapolate``                 | integer  | By default, when this is set to ``0``,    |
    |                                 |          | cubic curves will not be drawn to their   |
    |                                 |          | end vertices as the basis functions       |
    |                                 |          | require an extra vertex to define the     |
    |                                 |          | curve. If this attribute is set to ``1``, |
    |                                 |          | an extra vertex is automatically          |
    |                                 |          | extrapolated so the curves reach their    |
    |                                 |          | end vertices, as with linear              |
    |                                 |          | interpolation.                            |
    +---------------------------------+----------+-------------------------------------------+

Attributes may also have a single value, one value per curve, one value
per vertex or one value per vertex of a single curve, reused for all
curves. Attributes which fall in that last category must always specify
:ref:`NSIParamPerVertex<CAPI:paramflags>`.

.. Note::
    A single curve is considered a face as far as use of
    :ref:`NSIParamPerFace<CAPI:paramflags>` is concerned. See also the
    :ref:`faceset node<node:faceset>`.


.. index::
    particles

.. _node:particles:

The particles node
------------------

This geometry node represents a collection of *tiny* particles.
Particles are represented by either a disk or a sphere. This primitive
is not suitable to render large particles as these should be represented
by other means (e.g. instancing).

.. index::
    particle size

.. table:: particles node required attributes
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | **Name**                        | **Type** | **Description/Values**                    |
    +=================================+==========+===========================================+
    | ``P``                           | point    | The center of each particle.              |
    +---------------------------------+----------+-------------------------------------------+
    | ``width``                       | float    | The width of each particle. It can be     |
    |                                 |          | specified for the entire particles node   |
    |                                 |          | (only one value provided), per-particle   |
    |                                 |          | or indirectly through a ``width.indices`` |
    |                                 |          | attribute.                                |
    +---------------------------------+----------+-------------------------------------------+

It also has these optional attributes:

.. index::
    particle normals
    particle id
    motion blur
    shutter
    optional particle attributes

.. table:: particles node optional attributes
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | ``N``                           | normal   | The presence of a normal indicates that   |
    |                                 |          | each particle is to be rendered as an     |
    |                                 |          | oriented disk. The orientation of each    |
    |                                 |          | disk is defined by the provided normal    |
    |                                 |          | which can be constant or a per-particle   |
    |                                 |          | attribute.                                |
    |                                 |          | Each particle is assumed to be a sphere   |
    |                                 |          | if a normal is not provided.              |
    +---------------------------------+----------+-------------------------------------------+
    | ``id``                          | integer  | This attribute has to be the same length  |
    |                                 |          | as ``P``. It assigns a unique identifier  |
    |                                 |          | to each particle which must be constant   |
    |                                 |          | throughout the entire :ref:`shutter       |
    |                                 |          | range<motionblur>`. Its presence is       |
    |                                 |          | necessary in the case where particles are |
    |                                 |          | motion blurred and some of them could     |
    |                                 |          | appear or disappear during the motion     |
    |                                 |          | interval. Having such identifiers allows  |
    |                                 |          | the renderer to properly render such      |
    |                                 |          | transient particles. This implies that    |
    |                                 |          | the number of ``id``'s might vary for     |
    |                                 |          | each time step of a motion-blurred        |
    |                                 |          | particle cloud so the use of is mandatory |
    |                                 |          | by definition.                            |
    +---------------------------------+----------+-------------------------------------------+

.. _node:procedural:

The procedural node
-------------------

This node acts as a proxy for geometry that could be defined at a later
time than the node’s definition, using a procedural supported by . Since
the procedural is evaluated in complete isolation from the rest of the
scene, it can be done either lazily (depending on its ``boundingbox``
attribute) or in parallel with other procedural nodes.

The procedural node supports, as its attributes, all the parameters of
the api call, meaning that procedural types accepted by that api call
(NSI archives, dynamic libraries, LUA scripts) are also supported by
this node. Those attributes are used to call a procedural that is
expected to define a sub-scene, which has to be independent from the
other nodes in the scene. The procedural node will act as the
sub-scene’s local root and, as such, also supports all the attributes of
a regular node. In order to connect the nodes it creates to the
sub-scene’s root, the procedural simply has to connect them to the
regular "``.root``".

In the context of an , the procedural will be executed again after the
node’s attributes have been edited. All nodes previously connected by
the procedural to the sub-scene’s root will be deleted automatically
before the procedural’s re-execution.

Additionally, this node has the following optional attribute :

Specifies a bounding box for the geometry where ``boundingbox[0]`` and
``boundingbox[1]`` correspond, respectively, to the "minimum" and the
"maximum" corners of the box.

.. _node:environment:

The environment node
--------------------

This geometry node defines a sphere of infinite radius. Its only purpose
is to render environment lights, solar lights and directional lights;
lights which cannot be efficiently modeled using area lights. In
practical terms, this node is no different than a geometry node with the
exception of shader execution semantics: there is no surface position
``P``, only a direction ``I`` (refer to for more practical details). The
following node attribute is recognized:

Specifies the cone angle representing the region of the sphere to be
sampled. The angle is measured around the :math:`\mathrm{Z+}` axis [#]_.
If the angle is set to :math:`0`, the environment describes a
directional light. Refer to for more about how to specify light sources.

.. _node:shader:

The shader node
---------------

This node represents an osl shader, also called layer when part of a
shader group. It has the following required attribute:

This is the name of the file which contains the shader’s compiled code.

All other attributes on this node are considered parameters of the
shader. They may either be given values or connected to attributes of
other shader nodes to build shader networks. osl shader networks must
form acyclic graphs or they will be rejected. Refer to for instructions
on osl network creation and usage.

.. _node:attributes:

The attributes node
-------------------

This node is a container for various geometry related rendering
attributes that are not *intrinsic* to a particular node (for example,
one can’t set the topology of a polygonal mesh using this attributes
node). Instances of this node must be connected to the
``geometryattributes`` attribute of either geometric primitives or nodes
(to build ). Attribute values are gathered along the path starting from
the geometric primitive, through all the transform nodes it is connected
to, until the is reached.

When an attribute is defined multiple times along this path, the
definition with the highest priority is selected. In case of conflicting
priorities, the definition that is the closest to the geometric
primitive (i.e. the furthest from the root) is selected. Connections
(for shaders, essentially) can also be assigned priorities, which are
used in the same way as for regular attributes. Multiple attributes
nodes can be connected to the same geometry or transform nodes (e.g. one
attributes node can set object visibility and another can set the
surface shader) and will all be considered.

This node has the following attributes:

The which will be used to shade the surface is connected to this
attribute. A priority (useful for overriding a shader from higher in the
scene graph) can be specified by setting the ``priority`` attribute of
the connection itself.

The which will be used to displace the surface is connected to this
attribute. A priority (useful for overriding a shader from higher in the
scene graph) can be specified by setting the ``priority`` attribute of
the connection itself.

The which will be used to shade the volume inside the primitive is
connected to this attribute.

Sets the priority of attribute ``ATTR`` when gathering attributes in the
scene hierarchy. [visibilityattributes]

These attributes set visibility for each ray type specified in osl. The
same effect could be achieved using shader code (using the ``raytype()``
function) but it is much faster to filter intersections at trace time. A
value of ``1`` makes the object visible to the corresponding ray type,
while ``0`` makes it invisible.

This attribute sets the default visibility for all ray types. When
visibility is set both per ray type and with this default visibility,
the attribute with the highest priority is used. If their priority is
the same, the more specific attribute (i.e. per ray type) is used.

If this attribute is set to 1, the object becomes a matte for camera
rays. Its transparency is used to control the matte opacity and all
other shading components are ignored.

If this is set to 1, closures not used with ``quantize()`` will use
emission from the objects affected by the attribute. If set to 0, they
will not.

If this is set to 1, quantized closures will use emission from the
objects affected by the attribute. If set to 0, they will not.

When a geometry node (usually a ) is connected to this attribute, it
will be used to restrict the effect of the attributes node, which will
apply only inside the volume defined by the connected geometry object.

.. _node:transform:

The transform node
------------------

This node represents a geometric transformation. Transform nodes can be
chained together to express transform concatenation, hierarchies and
instances.

A transform node also accepts attributes to implement
:ref:`hierarchical attribute assignment and overrides<section:attributes>`.

It has the following attributes:

.. table:: transform node attributes
    :widths: 3 1 6

    +------------------------------+--------------+------------------------------------------+
    | **Name**                     | **Type**     | **Description/Values**                   |
    +==============================+==============+==========================================+
    | ``tranformationmatrix``      | string       | This is a 4×4 matrix which describes     |
    |                              |              | the node's transformation. Matrices      |
    |                              |              | in |nsi| post-multiply so column         |
    | ``matrix`` (!)               |              | vectors are of the form:                 |
    |                              |              |                                          |
    |                              |              | .. math::                                |
    |                              |              |                                          |
    |                              |              |    \left[ \begin{array}{cccc}            |
    |                              |              |    w_{1_1} & w_{1_2} & w_{1_3} & 0  \\   |
    |                              |              |    w_{2_1} & w_{2_2} & w_{2_3} & 0  \\   |
    |                              |              |    w_{3_1} & w_{3_2} & w_{3_3} & 0  \\   |
    |                              |              |    Tx & Ty & Tz & 1 \end{array} \right]  |
    +------------------------------+--------------+------------------------------------------+
    | ``objects``                  | «connection» | This is where the transformed objects    |
    |                              |              | are connected to. This includes          |
    |                              |              | geometry nodes, other transform nodes    |
    |                              |              | and camera nodes.                        |
    +------------------------------+--------------+------------------------------------------+
    | ``geometryattributes``       | «connection» | This is where                            |
    |                              |              | :ref:`attributes nodes<node:attributes>` |
    |                              |              | may be connected to affect any geometry  |
    |                              |              | transformed by this node.                |
    |                              |              |                                          |
    |                              |              | See the guidelines on                    |
    |                              |              | :ref:`attributes<section:attributes>`    |
    |                              |              | and                                      |
    |                              |              | :ref:`instancing<section:instancing>`    |
    |                              |              | for explanations on how this connection  |
    |                              |              | is used.                                 |
    +------------------------------+--------------+------------------------------------------+

.. _node:instances:

The instances nodes
-------------------

This node is an efficient way to specify a large number of instances. It
has the following attributes:

.. table:: instances node attributes
    :widths: 3 1 6

    +-----------------------------+--------------+-------------------------------------------+
    | **Name**                    | **Type**     | **Description/Values**                    |
    +=============================+==============+===========================================+
    | ``sourcemodels``            | «connection» | The instanced models should connect to    |
    |                             |              | this attribute.                           |
    | ``object`` (!)              |              |                                           |
    |                             |              | Connections must have an integer          |
    |                             |              | ``index`` attribute if there are several, |
    |                             |              | so the models effectively form an ordered |
    |                             |              | list.                                     |
    +-----------------------------+--------------+-------------------------------------------+
    | ``transformationmatrices``  | doublematrix | A transformation matrix for each          |
    |                             |              | instance.                                 |
    | ``matrix`` (!)              |              |                                           |
    +-----------------------------+--------------+-------------------------------------------+
    | ``modelindices``            | integer      | An optional model selector for each       |
    |                             |              | instance.                                 |
    | ``object.index`` (!)        |              |                                           |
    +-----------------------------+--------------+-------------------------------------------+
    | ``disabledinstances``       | integer      | An optional list of indices of instances  |
    |                             |              | which are not to be rendered.             |
    +-----------------------------+--------------+-------------------------------------------+


.. _node:outputdriver:

The outputdriver node
---------------------

An output driver defines how an image is transferred to an output
destination. The destination could be a file (e.g. “exr” output driver),
frame buffer or a memory address. It can be connected to the
``outputdrivers`` attribute of an node. It has the following attributes:

.. table:: outputdriver node attributes
    :widths: 3 1 6

    +---------------------------------+----------+-------------------------------------------+
    | **Name**                        | **Type** | **Description/Values**                    |
    +=================================+==========+===========================================+
    | ``drivername``                  | string   | This is the name of the driver to use.    |
    |                                 |          | The api of the driver is implementation   |
    |                                 |          | specific and is not covered by this       |
    |                                 |          | documentation.                            |
    +---------------------------------+----------+-------------------------------------------+
    | ``imagefilename``               | string   | Full path to a file for a file-based      |
    |                                 |          | output driver or some meaningful          |
    |                                 |          | identifier depending on the output        |
    |                                 |          | driver.                                   |
    +---------------------------------+----------+-------------------------------------------+
    | ``embedstatistics``             | integer  | A value of 1 specifies that statistics    |
    |                                 |          | will be embedded into the image file.     |
    +---------------------------------+----------+-------------------------------------------+

Any extra attributes are also forwarded to the output driver which may
interpret them however it wishes.

.. _node:outputlayer:

The outputlayer node
--------------------

This node describes one specific layer of render output data. It can be
connected to the ``outputlayers`` attribute of a screen node. It has the
following attributes:

.. table:: outputlayer node attributes
    :widths: 3 1 2 4

    +---------------------------------+--------------+-------------------------------------------+
    | **Name**                        | **Type**     | **Description/Values**                    |
    +=================================+==============+===========================================+
    | ``variablename``                | string       | This is the name of a variable to output. |
    +---------------------------------+--------------+-------------------------------------------+
    | ``variablesource``              | string       | Indicates where the variable to be output |
    |                                 |              | is read from. Possible values are:        |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``shader``     | computed by a shader     |
    |                                 |              |                | and output through an    |
    |                                 |              |                | |osl| closure (such as   |
    |                                 |              |                | ``outputvariable()``     |
    |                                 |              |                | or ``debug()``) or the   |
    |                                 |              |                | ``Ci`` global variable.  |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``attribute``  | retrieved directly from  |
    |                                 |              |                | an attribute with a      |
    |                                 |              |                | matching name attached   |
    |                                 |              |                | to a geometric           |
    |                                 |              |                | primitive.               |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``builtin``    | generated automatically  |
    |                                 |              |                | by the renderer (e.g.    |
    |                                 |              |                | ``z``, ``alpha``         |
    |                                 |              |                | ``N.camera``,            |
    |                                 |              |                | ``P.world``).            |
    +---------------------------------+--------------+----------------+--------------------------+
    | ``layername``                   | string       | This will be name of the layer as written |
    |                                 |              | by the output driver. For example, if the |
    |                                 |              | output driver writes to an EXR file then  |
    |                                 |              | this will be the name of the layer inside |
    |                                 |              | that file.                                |
    +---------------------------------+--------------+-------------------------------------------+
    | ``scalarformat``                | string       | Specifies the format in which data will   |
    |                                 |              | be encoded (quantized) prior to passing   |
    |                                 |              | it to the output driver. Possible values  |
    |                                 |              | are:                                      |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``int8``       | Signed 8-bit integer.    |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``uint8``      | Unsigned 8-bit integer.  |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``int16``      | Signed 16-bit integer.   |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``uint16``     | Unsigned 16-bit integer. |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``int32``      | Signed 32-bit integer.   |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``half``       | IEEE 754 half-precision  |
    |                                 |              |                | binary floating point    |
    |                                 |              |                | (binary16).              |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``float``      | IEEE 754                 |
    |                                 |              |                | single-precision binary  |
    |                                 |              |                | floating point           |
    |                                 |              |                | (binary32).              |
    +---------------------------------+--------------+----------------+--------------------------+
    | ``layertype``                   | string       | Specifies the type of data that will be   |
    |                                 |              | written to the layer. Possible values     |
    |                                 |              | are:                                      |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``scalar``     | A single quantity.       |
    |                                 |              |                | Useful for opacity       |
    |                                 |              |                | (``alpha``) or depth     |
    |                                 |              |                | (``Z``) information.     |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``color``      | A 3-component color.     |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``vector``     | A 3D point or vector.    |
    |                                 |              |                | This will help           |
    |                                 |              |                | differentiate the data   |
    |                                 |              |                | from a color in further  |
    |                                 |              |                | processing.              |
    |                                 |              +----------------+--------------------------+
    |                                 |              | ``quad``       | A sequence of 4 values,  |
    |                                 |              |                | where the fourth value   |
    |                                 |              |                | is *not* an alpha        |
    |                                 |              |                | channel.                 |
    |                                 |              +----------------+--------------------------+
    |                                 |              | Each component of those types is stored   |
    |                                 |              | according to the ``scalarformat``         |
    |                                 |              | attribute set on the same ``outputlayer`` |
    |                                 |              | node.                                     |
    +---------------------------------+--------------+-------------------------------------------+
    | ``colorprofile``                | string       | The name of an OCIO color profile to      |
    |                                 |              | apply to rendered image data prior to     |
    |                                 |              | quantization.                             |
    +---------------------------------+--------------+-------------------------------------------+
    | ``dithering``                   | integer      | If set to 1, dithering is applied to      |
    |                                 |              | integer scalars [#]_.                     |
    |                                 |              | Otherwise, it must  be set to 0.          |
    +---------------------------------+--------------+-------------------------------------------+
    | ``withalpha``                   | integer      | If set to 1, an alpha channel is included |
    |                                 |              | in the output layer.                      |
    |                                 |              | Otherwise, it must be set to 0.           |
    +---------------------------------+--------------+-------------------------------------------+
    | ``sortkey``                     | integer      | This attribute is used as a sorting key   |
    |                                 |              | when ordering multiple output layer nodes |
    |                                 |              | connected to the same node.               |
    |                                 |              | Layers with the lowest ``sortkey``        |
    |                                 |              | attribute appear first.                   |
    +---------------------------------+--------------+-------------------------------------------+
    | ``lightset``                    | «connection» | This connection accepts either or nodes   |
    |                                 |              | to which lights are connected. In this    |
    |                                 |              | case only listed lights will affect the   |
    |                                 |              | crender of the output layer. If nothing   |
    |                                 |              | is connected to this attribute then all   |
    |                                 |              | lights are rendered.                      |
    +---------------------------------+--------------+-------------------------------------------+
    | ``outputdrivers``               | «connection» | This connection accepts nodes to which    |
    |                                 |              | the layer’s image will be sent.           |
    +---------------------------------+--------------+-------------------------------------------+
    | ``filter``                      | string       | The type of filter to use when            |
    |                                 |              | reconstructing the final image from       |
    |                                 |              | sub-pixel samples. Possible values are:   |
    |                                 |              | * ``box``                                 |
    |                                 |              | * ``triangle``                            |
    |                                 |              | * ``catmull-rom``                         |
    |                                 |              | * ``bessel``                              |
    |                                 |              | * ``gaussian``                            |
    |                                 |              | * ``sinc``                                |
    |                                 |              | * ``mitchell`                             |
    |                                 |              | * ``blackman-harris`` **(default)**       |
    |                                 |              | * ``zmin``                                |
    |                                 |              | * ``zmax``                                |
    +---------------------------------+--------------+-------------------------------------------+
    | ``filterwidth``                 | double       | Diameter in pixels of the reconstruction  |
    |                                 |              | filter. It ignored when filter is ``box`` |
    |                                 |              | or ``zmin``.                              |
    +---------------------------------+--------------+-------------------------------------------+
    | ``backgroundvalue``             | float        | The value given to pixels where nothing   |
    |                                 |              | is rendered.                              |
    +---------------------------------+--------------+-------------------------------------------+

Any extra attributes are also forwarded to the output driver which may
interpret them however it wishes.

.. _node:screen:

The screen node
---------------

This node describes how the view from a camera node will be rasterized
into an node. It can be connected to the ``screens`` attribute of a
camera node.

This connection accepts nodes which will receive a rendered image of the
scene as seen by the camera.

Horizontal and vertical resolution of the rendered image, in pixels.

The total number of samples (i.e. camera rays) to be computed for each
pixel in the image.

The region of the image to be rendered. It’s defined by a list of
exactly 2 pairs of floating-point number. Each pair represents a point
in ndc space:

-  ``Top-left`` corner of the crop region

-  ``Bottom-right`` corner of the crop region

For progressive renders, this is the region of the image to be rendered
first. It is two pairs of integers. Each represents pixel coordinates:

-  ``Top-left`` corner of the high priority region

-  ``Bottom-right`` corner of the high priority region

Specifies the screen space region to the rendered. Each pair represents
a 2D point in ``screen`` space:

-  ``Bottom-left`` corner of the region

-  ``Top-right`` corner of the region

Note that the default screen window is set implicitely by the frame
aspect ratio:

.. math::

   screenwindow = \begin{bmatrix}-f && -1\end{bmatrix}, \begin{bmatrix}f && 1\end{bmatrix} \text{for } f=\dfrac{xres}{yres}\\

Ratio of the physical width to the height of a single pixel. A value of
1.0 corresponds to square pixels.

This controls whether or not the sampling pattern used to produce the
image change for every frame. A nonzero value will cause the same
pattern to be used for all frames. A value of zero will cause the
pattern to change with the frame attribute of the .

.. _node:volume:

The volume node
---------------

This node represents a volumetric object defined by
`OpenVDB <http:/www.openvdb.org>`__ data. It has the following
attributes:

The path to an OpenVDB file with the volumetric data.

The name of the OpenVDB grid to use as volume density for the volume
shader.

The name of the OpenVDB grid to use as emission intensity for the volume
shader.

The name of the OpenVDB grid to use as temperature for the volume
shader.

The name of the OpenVDB grid to use as motion vectors. This can also
name the first of three scalar grids (ie. "velocityX").

A scaling factor applied to the motion vectors.

.. _node:camera:

Camera Nodes
------------

All camera nodes share a set of common attributes. These are listed
below.

This connection accepts nodes which will rasterize an image of the scene
as seen by the camera. Refer to for more information.

Time interval during which the camera shutter is at least partially
open. It’s defined by a list of exactly two values:

-  Time at which the shutter starts ``opening``.

-  Time at which the shutter finishes ``closing``.

A *normalized* time interval indicating the time at which the shutter is
fully open (a) and the time at which the shutter starts to close (b).
These two values define the top part of a trapezoid filter. The end goal
of this feature it to simulate a mechanical shutter on which open and
close movements are not instantaneous. shows the geometry of such a
trapezoid filter.

Distance of the near and far clipping planes from the camera. It’s
defined by a list of exactly two values:

-  Distance to the ``near`` clipping plane, in front of which scene
   objects are clipped.

-  Distance to the ``far`` clipping plane, behind which scene objects
   are clipped.

.. _node:orthographiccamera:

The orthographiccamera node
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This node defines an orthographic camera with a view direction towards
the :math:`\mathrm{Z-}` axis. This camera has no specific attributes.

.. _node:perspectivecamera:

The perspectivecamera node
~~~~~~~~~~~~~~~~~~~~~~~~~~

This node defines a perspective camera. The canonical camera is viewing
in the direction of the :math:`\mathrm{Z-}` axis. The node is usually
connected into a node for camera placement. It has the following
attributes:

The field of view angle, in degrees.

Enables depth of field effect for this camera.

Relative aperture of the camera.

Focal length, in scene units, of the camera lens.

Distance, in scene units, in front of the camera at which objects will
be in focus.

By default, the renderer simulates a circular aperture for depth of
field. Enable this feature to simulate aperture “blades” as on a real
camera. This feature affects the look in out-of-focus regions of the
image.

Number of sides of the camera’s aperture. The mininum number of sides is
3.

A rotation angle (in degrees) to be applied to the camera’s aperture, in
the image plane.

.. _node:fisheyecamera:

The fisheyecamera node
~~~~~~~~~~~~~~~~~~~~~~

Fish eye cameras are useful for a multitude of applications
(e.g. virtual reality). This node accepts these attributes:

Specifies the field of view for this camera node, in degrees.

Defines one of the supported fisheye `mapping
functions <https://en.wikipedia.org/wiki/Fisheye_lens>`__:

:math:`\rightarrow` Maintains angular distances.

:math:`\rightarrow` Every pixel in the image covers the same solid
angle.

:math:`\rightarrow` Maintains planar illuminance. This mapping is
limited to a 180 field of view.

:math:`\rightarrow` Maintains angles throughout the image. Note that
stereographic mapping fails to work with field of views close to 360
degrees.

.. _node:cylindricalcamera:

The cylindricalcamera node
~~~~~~~~~~~~~~~~~~~~~~~~~~

This node specifies a cylindrical projection camera and has the
following attibutes: [section:cylindricalcamera]

Specifies the *vertical* field of view, in degrees. The default value is
90.

Specifies the horizontal field of view, in degrees. The default value is
360.

This offset allows to render stereoscopic cylindrical images by
specifying an eye offset

.. _node:sphericalcamera:

The sphericalcamera node
~~~~~~~~~~~~~~~~~~~~~~~~

This node defines a spherical projection camera. This camera has no
specific attributes.

Lens shaders
~~~~~~~~~~~~

A lens shader is an osl network connected to a camera through the
``lensshader`` connection. Such shaders receive the position and the
direction of each tracer ray and can either change or completely discard
the traced ray. This allows to implement distortion maps and cut maps.
The following shader variables are provided:

``P`` — Contains ray’s origin.

``I`` — Contains ray’s direction. Setting this variable to zero
instructs the renderer not to trace the corresponding ray sample.

``time`` — The time at which the ray is sampled.

``(u, v)`` — Coordinates, in screen space, of the ray being traced.

--------------

.. rubric:: Footnotes

.. [#]
   To position the environment dome one must connect the node to a
   :ref:`transform node<node:transform>` and apply the desired rotation.

.. [#]
   It is sometimes desirable to turn off dithering, for example, when
   outputting object IDs.