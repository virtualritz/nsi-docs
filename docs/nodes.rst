.. _section:nodes:

Nodes
=====

The following sections describe available nodes in technical terms.
Refer to for usage details.

.. table:: nsi nodes overview

   +--------------+-------------------------------------+---------------+
   | **Node**     | **Function**                        | **Reference** |
   +==============+=====================================+===============+
   | root         | Scene’s root                        |               |
   +--------------+-------------------------------------+---------------+
   | global       | Global settings node                |               |
   +--------------+-------------------------------------+---------------+
   | set          | To express relationships to groups  |               |
   |              | of nodes                            |               |
   +--------------+-------------------------------------+---------------+
   | shader       | osl shader or layer in a shader     |               |
   |              | group                               |               |
   +--------------+-------------------------------------+---------------+
   | attributes   | Container for generic attributes    |               |
   |              | (e.g. visibility)                   |               |
   +--------------+-------------------------------------+---------------+
   | transform    | Transformation to place objects in  |               |
   |              | the scene                           |               |
   +--------------+-------------------------------------+---------------+
   | mesh         | Polygonal mesh or subdivision       |               |
   |              | surface                             |               |
   +--------------+-------------------------------------+---------------+
   | faceset      | Assign attributes to part of a mesh |               |
   +--------------+-------------------------------------+---------------+
   | cubiccurves  | B-spline and Catmull-Rom curves     |               |
   +--------------+-------------------------------------+---------------+
   | linearcurves | Linearly interpolated curves        |               |
   +--------------+-------------------------------------+---------------+
   | particles    | Collection of particles             |               |
   +--------------+-------------------------------------+---------------+
   | procedural   | Geometry to be loaded in delayed    |               |
   |              | fashion                             |               |
   +--------------+-------------------------------------+---------------+
   | environment  | Geometry type to define environment |               |
   |              | lighting                            |               |
   +--------------+-------------------------------------+---------------+
   | \*camera     | Set of nodes to create viewing      |               |
   |              | cameras                             |               |
   +--------------+-------------------------------------+---------------+
   | outputdriver | Location where to output rendered   |               |
   |              | pixels                              |               |
   +--------------+-------------------------------------+---------------+
   | outputlayer  | Describes one render layer to be    |               |
   |              | connected to an ``outputdriver``    |               |
   |              | node                                |               |
   +--------------+-------------------------------------+---------------+
   | screen       | Describes how the view from a       |               |
   |              | camera will be rasterized into an   |               |
   |              | ``outputlayer`` node                |               |
   +--------------+-------------------------------------+---------------+

.. _section:rootnode:

The root node
-------------

The root node is much like a transform node with the particularity that
it is the end connection for all renderable scene elements (see ). A
node can exist in an nsi context without being connected to the root
note but in that case it won’t affect the render in any way. The root
node has the reserved handle name ``.root`` and doesn’t need to be
created using ``NSICreate``. The root node has two defined attributes:
``objects`` and ``geometryattributes``. Both are explained in .

.. _section:globalnode:

The global node
---------------

This node contains various global settings for a particular nsi context.
Note that these attributes are for the most case implementation
specific. This node has the reserved handle name ``.global`` and doesn’t
need to be created using ``NSICreate``. The following attributes are
recognized by *3Delight*:

Specifies the total number of threads to use for a particular render:

-  A value of zero lets the render engine choose an optimal thread
   value. This is the default behaviour.

-  Any positive value directly sets the total number of render threads.

-  A negative value will start as many threads as optimal *plus* the
   specified value. This allows for an easy way to decrease the total
   number of render threads.

Specifies the approximate maximum memory size, in megabytes, the
renderer will allocate to accelerate texture access.

Specifies the maximum network cache size, in gigabytes, the renderer
will use to cache textures on a local drive to accelerate data access.

Specifies the directory in which textures will be cached. A good default
value is /var/tmp/3DelightCache on Linux systems.

Enables caching for image write operations. This alleviates pressure on
networks by first rendering images to a local temporary location and
copying them to their final destination at the end of the render. This
replaces many small network writes by more efficient larger operations.

Specifies the name or address of the license server to be used.

When no license is available for rendering, the renderer will wait until
a license is available if this attribute is set to ``1``, but will stop
immediately if it’s set to ``0``. The latter setting is useful when
managing a renderfarm and other work could be scheduled instead.

By default, the renderer will get new licenses for every render and
release them once it’s done. This can be undesirable if several frames
are rendered in sequence from the same process. If this option is set to
``1``, the licenses obtained for the first frame are held until the last
frame is finished.

If set to 1, start the render with a lower process priority. This can be
useful if there are other applications that must run during rendering.

Specifies in what order the buckets are rendered. The available values
are:

:math:`\rightarrow` row by row, left to right and top to bottom.

:math:`\rightarrow` column by column, top to bottom and left to right.

:math:`\rightarrow` row by row, left to right on even rows and right to
left on odd rows.

:math:`\rightarrow` in a clockwise spiral from the centre of the image.

:math:`\rightarrow` in concentric circles from the centre of the image.

Provides a frame number to be used as a seed for the sampling pattern.
See the .

Specifies the maximum bounce depth a diffuse ray can reach. A depth of 1
specifies one additional bounce compared to purely local illumination.

Specifies the maximum bounce depth a hair ray can reach. Note that hair
are akin to volumetric primitives and might need elevated ray depth to
properly capture the illumination.

Specifies the maximum bounce depth a reflection ray can reach. Setting
the reflection depth to 0 will only compute local illumination meaning
that only emissive surfaces will appear in the reflections.

Specifies the maximum bounce depth a refraction ray can reach. A value
of 4 allows light to shine through a properly modeled object such as a
glass.

Specifies the maximum bounce depth a volume ray can reach.

Limits the distance a ray emitted from a diffuse material can travel.
Using a relatively low value for this attribute might improve
performance without significantly affecting the look of the resulting
image, as it restrains the extent of global illumination. Setting it to
a negative value disables the limitation.

Limits the distance a ray emitted from a hair closure can travel.
Setting it to a negative value disables the limitation.

Limits the distance a ray emitted from a reflective material can travel.
Setting it to a negative value disables the limitation.

Limits the distance a ray emitted from a refractive material can travel.
Setting it to a negative value disables the limitation.

Limits the distance a ray emitted from a specular (glossy) material can
travel. Setting it to a negative value disables the limitation.

Limits the distance a ray emitted from a volume can travel. Setting it
to a negative value disables the limitation.

Controls the quality of bsdf sampling. Larger values give less visible
noise.

Controls the quality of volume sampling. Larger values give less visible
noise.

When set to ``1``, enables displacement shading. Otherwise, it must be
set to ``0``, which forces the renderer to ignore any displacement
shader in the scene.

When set to ``1``, enables the ``subsurface()`` osl closure. Otherwise,
it must be set to ``0``, which will ignore this closure in osl shaders.

When set to ``1``, prints rendering progress as a percentage of
completed pixels.

Full path of the file where rendering statistics will be written. An
empty string will write statistics to standard output. The name ``null``
will not output statistics.

.. _section:setnode:

The set node
------------

This node can be used to express relationships between objects. An
example is to connect many lights to such a node to create a *light set*
and then to connect this node to ``outputlayer.lightset`` ( and ). It
has the following attributes:

This connection accepts all nodes that are members of the set.

.. _section:meshnode:

The mesh node
-------------

This node represents a polygon mesh. It has the following required
attributes:

The positions of the object’s vertices. Typically, this attribute will
be through a ``P.indices`` attribute.

The number of vertices for each face of the mesh. The number of values
for this attribute specifies total face number (unless ``nholes`` is
defined).

It also has optional attributes:

The number of holes in the polygons. When this attribute is defined, the
total number of faces in the mesh is defined by the number of values for
``nholes`` rather than for ``nvertices``. For each face, there should be
(``nholes``\ +1) values in ``nvertices``: the respective first value
specifies the number of vertices on the outside perimeter of the face,
while additional values describe the number of vertices on perimeters of
holes in the face. shows the definition of a polygon mesh consisting of
3 square faces, with one triangular hole in the first one and square
holes in the second one.

A value of 1 specifies that polygons with a clockwise winding order are
front facing. The default is 0, making counterclockwise polygons front
facing.

A value of ``"catmull-clark"`` will cause the mesh to render as a
Catmull-Clark subdivision surface.

This attribute is a list of vertices which are sharp corners. The values
are indices into the ``P`` attribute, like ``P.indices``.

This attribute is the sharpness of each specified sharp corner. It must
have a value for each value given in ``subdivision.cornervertices``.

This attribute is a list of crease edges. Each edge is specified as a
pair of indices into the ``P`` attribute, like ``P.indices``.

This attribute is the sharpness of each specified crease. It must have a
value for each pair of values given in ``subdivision.creasevertices``.

::

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

.. _section:facesetnode:

The faceset node
----------------

This node is used to provide a way to attach attributes to some faces of
another geometric primitive, such as the ``mesh`` node, as shown in . It
has the following attributes:

This attribute is a list of indices of faces. It identifies which faces
of the original geometry will be part of this face set.

::

   Create "subdiv" "mesh"
   SetAttribute "subdiv"
     "nvertices" "int" 4 [ 4 4 4 4 ]
     "P" "i point" 9 [
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

.. _section:curvesnode:

The curves node
---------------

This node represents a group of curves. It has the following required
attributes:

The number of vertices for each curve. This must be at least 4 for cubic
curves and 2 for linear curves. There can be either a single value or
one value per curve.

The positions of the curve vertices. The number of values provided,
divided by ``nvertices``, gives the number of curves which will be
rendered.

The width of the curves.

The basis functions used for curve interpolation. Possible choices are:

:math:`\rightarrow` B-spline interpolation.

:math:`\rightarrow` Catmull-Rom interpolation.

:math:`\rightarrow` Linear interpolation.

By default, cubic curves will not be drawn to their end vertices as the
basis functions require an extra vertex to define the curve. If this
attribute is set to 1, an extra vertex is automatically extrapolated so
the curves reach their end vertices, as with linear interpolation.

Attributes may also have a single value, one value per curve, one value
per vertex or one value per vertex of a single curve, reused for all
curves. Attributes which fall in that last category must always specify
. Note that a single curve is considered a face as far as use of is
concerned.

.. _section:particlesnode:

The particles node
------------------

This geometry node represents a collection of *tiny* particles.
Particles are represented by either a disk or a sphere. This primitive
is not suitable to render large particles as these should be represented
by other means (e.g. instancing).

A mandatory attribute that specifies the center of each particle.

A mandatory attribute that specifies the width of each particle. It can
be specified for the entire particles node (only one value provided),
per-particle or through a ``width.indices`` attribute.

The presence of a normal indicates that each particle is to be rendered
as an oriented disk. The orientation of each disk is defined by the
provided normal which can be constant or a per-particle attribute. Each
particle is assumed to be a sphere if a normal is not provided.

This attribute, of the same size as ``P``, assigns a unique identifier
to each particle which must be constant throughout the entire shutter
range. Its presence is necessary in the case where particles are motion
blurred and some of them could appear or disappear during the motion
interval. Having such identifiers allows the renderer to properly render
such transient particles. This implies that the number of *id*\ s might
vary for each time step of a motion-blurred particle cloud so the use of
is mandatory by definition.

.. _section:proceduralnode:

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

.. _section:environmentnode:

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
sampled. The angle is measured around the :math:`\mathrm{Z+}` axis [4]_.
If the angle is set to :math:`0`, the environment describes a
directional light. Refer to for more about how to specify light sources.

.. _section:shadernode:

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

.. _section:attributesnode:

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

.. _section:transformnode:

The transform node
------------------

This node represents a geometric transformation. Transform nodes can be
chained together to express transform concatenation, hierarchies and
instances. Transform nodes also accept attributes to implement . It has
the following attributes:

This is a 4x4 matrix which describes the node’s transformation. Matrices
in nsi post-multiply column vectors so are of the form:

.. math::

   \left[ \begin{array}{cccc}
         w_{1_1} & w_{1_2} & w_{1_3} & 0  \\
         w_{2_1} & w_{2_2} & w_{2_3} & 0  \\
         w_{3_1} & w_{3_2} & w_{3_3} & 0  \\
         Tx & Ty & Tz & 1 \end{array} \right]

This is where the transformed objects are connected to. This includes
geometry nodes, other transform nodes and camera nodes.

This is where may be connected to affect any geometry transformed by
this node. Refer to and for explanation on how this connection is used.

.. _section:instancesnode:

The instances nodes
-------------------

This node is an efficient way to specify a large number of instances. It
has the following attributes:

The instanced models should connect to this attribute. Connections must
have an integer ``index`` attribute if there are several, so the models
effectively form an ordered list.

A transformation matrix for each instance.

An optional model selector for each instance.

An optional list of indices of instances which are not to be rendered.

.. _section:outputdrivernode:

The outputdriver node
---------------------

An output driver defines how an image is transferred to an output
destination. The destination could be a file (e.g. “exr” output driver),
frame buffer or a memory address. It can be connected to the
``outputdrivers`` attribute of an node. It has the following attributes:

This is the name of the driver to use. The api of the driver is
implementation specific and is not covered by this documentation.

Full path to a file for a file-based output driver or some meaningful
identifier depending on the output driver.

A value of 1 specifies that statistics will be embedded into the image
file.

Any extra attributes are also forwarded to the output driver which may
interpret them however it wishes.

.. _section:outputlayernode:

The outputlayer node
--------------------

This node describes one specific layer of render output data. It can be
connected to the ``outputlayers`` attribute of a screen node. It has the
following attributes:

This is the name of a variable to output.

Indicates where the variable to be output is read from. Possible values
are:

:math:`\rightarrow` computed by a shader and output through an osl
closure (such as ``outputvariable()`` or ``debug()``) or the ``Ci``
global variable.

:math:`\rightarrow` retrieved directly from an attribute with a matching
name attached to a geometric primitive.

:math:`\rightarrow` generated automatically by the renderer (e.g. "z",
"alpha", "N.camera", "P.world").

This will be name of the layer as written by the output driver. For
example, if the output driver writes to an EXR file then this will be
the name of the layer inside that file.

Specifies the format in which data will be encoded (quantized) prior to
passing it to the output driver. Possible values are:

:math:`\rightarrow` signed 8-bit integer

:math:`\rightarrow` unsigned 8-bit integer

:math:`\rightarrow` signed 16-bit integer

:math:`\rightarrow` unsigned 16-bit integer

:math:`\rightarrow` signed 32-bit integer

:math:`\rightarrow` unsigned 32-bit integer

:math:`\rightarrow` ieee 754 half-precision binary floating point
(binary16)

:math:`\rightarrow` ieee 754 single-precision binary floating point
(binary32)

Specifies the type of data that will be written to the layer. Possible
values are:

:math:`\rightarrow` A single quantity. Useful for opacity ("alpha") or
depth ("Z") information.

:math:`\rightarrow` A 3-component color.

:math:`\rightarrow` A 3D point or vector. This will help differentiate
the data from a color in further processing.

:math:`\rightarrow` A sequence of 4 values, where the fourth value is
not an alpha channel.

Each component of those types is stored according to the
``scalarformat`` attribute set on the same ``outputlayer`` node.

The name of an ocio color profile to apply to rendered image data prior
to quantization.

If set to 1, dithering is applied to integer scalars [5]_. Otherwise, it
must be set to 0.

If set to 1, an alpha channel is included in the output layer.
Otherwise, it must be set to 0.

This attribute is used as a sorting key when ordering multiple output
layer nodes connected to the same node. Layers with the lowest
``sortkey`` attribute appear first.

This connection accepts either or nodes to which lights are connected.
In this case only listed lights will affect the render of the output
layer. If nothing is connected to this attribute then all lights are
rendered.

This connection accepts nodes to which the layer’s image will be sent.

The type of filter to use when reconstructing the final image from
sub-pixel samples. Possible values are: "box", "triangle",
"catmull-rom", "bessel", "gaussian", "sinc", "mitchell",
"blackman-harris", "zmin" and "zmax".

Diameter in pixels of the reconstruction filter. It is not applied when
filter is "box" or "zmin".

The value given to pixels where nothing is rendered.

Any extra attributes are also forwarded to the output driver which may
interpret them however it wishes.

.. _section:screennode:

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

.. _section:volumenode:

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

.. _section:camera:

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

.. _section:orthographiccamera:

The orthographiccamera node
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This node defines an orthographic camera with a view direction towards
the :math:`\mathrm{Z-}` axis. This camera has no specific attributes.

.. _section:perspectivecameranode:

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

.. _section:fisheyecameranode:

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

.. _section:sphericalcamera:

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
