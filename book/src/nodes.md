# Nodes

The following sections describe available nodes in technical terms. Refer to [the rendering guidelines](guidelines.md) for usage details.

| Node                                   | Function                                                                          |
| -------------------------------------- | --------------------------------------------------------------------------------- |
| [root](#the-root-node)                 | Scene's root                                                                      |
| [global](#the-global-node)             | Global settings node                                                              |
| [set](#the-set-node)                   | To express relationships of groups of nodes                                       |
| [shader](#the-shader-node)             | [ᴏsʟ](https://opensource.imageworks.com/?p=osl) shader or layer in a shader group |
| [attributes](#the-attributes-node)     | Container for generic attributes (e.g. visibility)                                |
| [transform](#the-transform-node)       | Transformation to place objects in the scene                                      |
| [mesh](#the-mesh-node)                 | Polygonal mesh or subdivision surface                                             |
| [plane](#the-plane-node)               | Infinite plane                                                                    |
| [faceset](#the-faceset-node)           | Assign attributes to part of a mesh                                               |
| [curves](#the-curves-node)             | Linear, B-spline and Catmull-Rom curves                                           |
| [particles](#the-particles-node)       | Collection of particles                                                           |
| [procedural](#the-procedural-node)     | Geometry to be loaded in delayed fashion                                          |
| [environment](#the-environment-node)   | Geometry type to define environment lighting                                      |
| [vdbparticles](#the-vdbparticles-node) | Particles defined by [OpenVDB](https://www.openvdb.org) data                      |
| [volume](#the-volume-node)             | Volumetric object defined by [OpenVDB](https://www.openvdb.org) data              |
| [outputdriver](#the-outputdriver-node) | Location where to output rendered pixels                                          |
| [outputlayer](#the-outputlayer-node)   | Describes one render layer to be connected to an outputdriver node                |
| [screen](#the-screen-node)             | Describes how the view from a camera will be rasterized into an outputlayer node  |
| [\*camera](#camera-nodes)              | Set of nodes to create viewing cameras                                            |

## Common attributes

`nicename` — string

This is an optional identifier which may be used by the renderer instead of the node handle for various identification purposes.

## The `root` node

The root node is much like a transform node with the particularity that it is the end connection for all renderable scene elements (see [basic scene anatomy](guidelines.md#basic-scene-anatomy)). A node can exist in an ɴsɪ context without being connected to the root note but in that case it won't affect the render in any way. The root node has the reserved handle name `.root` and doesn't need to be created using `NSICreate`. The root node has two defined attributes: `objects` and `geometryattributes`. Both are explained in [the transform node](#the-transform-node).

## The `global` node

This node contains various global settings for a particular ɴsɪ context. Note that these attributes are for the most case implementation specific. This node has the reserved handle name `.global` and doesn't need to be created using `NSICreate`. The following attributes are recognized by [3Delight](https://www.3delight.com):

`numberofthreads` — int (0)\
`thread.count` (!)

Specifies the total number of threads to use for a particular render:

- A value of zero lets the render engine choose an optimal thread value. This is the default behaviour.
- Any positive value directly sets the total number of render threads.
- A negative value will start as many threads as optimal _plus_ the specified value. This allows for an easy way to decrease the total number of render threads.

`texturememory` — int\
`texture.memory` (!)

Specifies the approximate maximum memory size, in megabytes, the renderer will allocate to accelerate texture access.

`networkcache.size` — int (0)

Specifies the maximum network cache size, in gigabytes, the renderer will use to cache textures on a local drive to accelerate data access.

`networkcache.directory` — string

Specifies the directory in which textures will be cached. A good default value is `/var/tmp/3DelightCache` on Linux systems.

`networkcache.mipmap` — int (1)

Enables caching of texture mipmaps separately. This makes more efficient use of available cache space.

`networkcache.write` — string (0)

Enables caching for image write operations. This alleviates pressure on networks by first rendering images to a local temporary location and copying them to their final destination at the end of the render. This replaces many small network writes by more efficient larger operations.

`license.server` — string

Specifies the name or address of the license server to be used.

`license.wait` — int (1)

When no license is available for rendering, the renderer will wait until a license is available if this attribute is set to 1, but will stop immediately if it's set to 0. The latter setting is useful when managing a renderfarm and other work could be scheduled instead.

`license.hold` — int (0)

By default, the renderer will get new licenses for every render and release them once it's done. This can be undesirable if several frames are rendered in sequence from the same process. If this option is set to 1, the licenses obtained for the first frame are held until the last frame is finished.

`renderatlowpriority` — int (0)\
`priority.low` (!)

If set to 1, start the render with a lower process priority. This can be useful if there are other applications that must run during rendering.

`bucketorder` — string (horizontal)\
`bucket.order` (!)

Specifies in what order the buckets are rendered. The available values are:

- `horizontal` — row by row, left to right and top to bottom.
- `vertical` — column by column, top to bottom and left to right.
- `zigzag` — row by row, left to right on even rows and right to left on odd rows.
- `spiral` — in a clockwise spiral from the centre of the image.
- `circle` — in concentric circles from the centre of the image.

`frame` — double (0)

Provides a frame number to be used as a seed for the sampling pattern. See the [screen node](#the-screen-node).

`hidemessages` — int

This specifies error and warning messages which will not be displayed. The attribute values are the message numbers to ignore.

`maximumraydepth.diffuse` — int (1)\
`diffuse.ray.depth.max` (!)

Specifies the maximum bounce depth a diffuse ray can reach. A depth of 1 specifies one additional bounce compared to purely local illumination.

`maximumraydepth.hair` — int (4)\
`hair.ray.depth.max` (!)

Specifies the maximum bounce depth a hair ray can reach. Note that hair are akin to volumetric primitives and might need elevated ray depth to properly capture the illumination.

`maximumraydepth.reflection` — int (1)\
`reflection.ray.depth.max` (!)

Specifies the maximum bounce depth a reflection ray can reach. Setting the reflection depth to 0 will only compute local illumination meaning that only emissive surfaces will appear in the reflections.

`maximumraydepth.refraction` — int (4)\
`refraction.ray.depth.max` (!)

Specifies the maximum bounce depth a refraction ray can reach. A value of 4 allows light to shine through a properly modeled object such as a glass.

`maximumraydepth.volume` — int (0)\
`volume.ray.depth.max` (!)

Specifies the maximum bounce depth a volume ray can reach.

`maximumraylength.diffuse` — double (-1)\
`diffuse.ray.length.max` (!)

Limits the distance a ray emitted from a diffuse material can travel. Using a relatively low value for this attribute might improve performance without significantly affecting the look of the resulting image, as it restrains the extent of global illumination. Setting it to a negative value disables the limitation.

`maximumraylength.hair` — double (-1)\
`hair.ray.length.max` (!)

Limits the distance a ray emitted from a hair closure can travel. Setting it to a negative value disables the limitation.

`maximumraylength.reflection` — double (-1)\
`reflection.ray.length.max` (!)

Limits the distance a ray emitted from a reflective material can travel. Setting it to a negative value disables the limitation.

`maximumraylength.refraction` — double (-1)\
`refraction.ray.length.max` (!)

Limits the distance a ray emitted from a refractive material can travel. Setting it to a negative value disables the limitation.

`maximumraylength.specular` — double (-1)

Limits the distance a ray emitted from a specular (glossy) material can travel. Setting it to a negative value disables the limitation.

`maximumraylength.volume` — double (-1)

Limits the distance a ray emitted from a volume can travel. Setting it to a negative value disables the limitation.

`quality.denoise` — int (1)

Enables denoising of output. Currently only supported for interactive renders.

`quality.iprglobalupdate` — int (1)

Enables a different method of updating the image for interactive renders.

`quality.iprinterpolate` — int (1)

Enables interpolation of low resolution interactive output, when denoised.

`quality.iprspeedmultiplier` — double (1)

Adjusts targeted render speed when processing multiple scene edits. A higher value will produce faster but lower quality results.

`quality.shadingsamples` — int (1)\
`shading.samples` (!)

Controls the quality of ʙsᴅꜰ sampling. Larger values give less visible noise.

`quality.volumesamples` — int (1)\
`volume.samples` (!)

Controls the quality of volume sampling. Larger values give less visible noise.

`referencetime` — double

Specifies a reference time for the frame, where deformation data is most valid. This is the default when the same attribute is not set on a geometry node. It is also the default for the `velocityreferencetime` attribute of the [vdbparticles node](#the-vdbparticles-node) and the [volume node](#the-volume-node). If not set, the center of the camera shutter is used.

`quality.samplevolumeemission` — int (1)

Enables or disables the higher quality sampling of emission of ᴠᴅʙ volumes. The emission is visible either way, this only affects quality and render time.

`show.displacement` — int (1)\
`shading.displacement` (!)

When set to 1, enables displacement shading. Otherwise, it must be set to 0, which forces the renderer to ignore any displacement shader in the scene.

`show.atmosphere` — int (1)\
`shading.atmosphere` (!)

When set to 1, enables atmosphere shader(s). Otherwise, it must be set to 0, which forces the renderer to ignore any atmosphere shader in the scene.

`show.multiplescattering` — double (1.0)\
`shading.multiplescattering` (!)

This is a multiplier on the multiple scattering of ᴠᴅʙ nodes. This parameter is useful to obtain faster draft renders by lowering the value below 1. The range is 0 to 1.

`show.osl.subsurface` — int (1)\
`shading.osl.subsurface` (!)

When set to 1, enables the `subsurface()` ᴏsʟ closure. Otherwise, it must be set to 0, which will ignore this closure in ᴏsʟ shaders.

`statistics.progress` — int (0)

When set to 1, prints rendering progress as a percentage of completed pixels.

`statistics.filename` — string (null)

Full path of the file where rendering statistics will be written. An empty string will write statistics to standard output. The name `null` will not output statistics.

`exclusiveshading` — \<connection\>

When geometry nodes are connected here, all others in the scene will be rendered as black to the camera. This is meant to be used to speed up rendering when adjusting parameters of specific objects during an [interactive render](#the-global-node). Connected shader nodes will behave in a similar way: objects not using them will be rendered as black. If the connected shader nodes are not the root of their shading network (ie: they are not connected to an [attributes node](#the-attributes-node) and their output is used as another shader node's input), the evaluation of the shading network will end there. This allows fine-tune parts of a shading network in isolation.

`verbose` — int (0)

When set to 1, enables additional informative messages before, during and after rendering.

`messages.timestamp` — int (0)

When set to 1, messages output by the renderer will include the local time.

## The `set` node

This node can be used to express relationships between objects. An example is to connect many lights to such a node to create a _light set_ and then to connect this node to `outputlayer.lightset` ([outputlayer](#the-outputlayer-node) and [light layers](guidelines.md#light-layers)). It has the following attributes:

`members` — \<connection\>\
`member` (!)

This connection accepts all nodes that are members of the set.

## The `plane` node

This node represents an infinite plane, centered at the origin and pointing towards Z+. It has no required attributes. The UV coordinates are defined as the X and Y coordinates of the plane.

## The `mesh` node

This node represents a polygon mesh. It has the following required attributes:

`P` — point

The positions of the object's vertices. Typically, this attribute will be [addressed indirectly](#passing-optional-arguments) through a `P.indices` attribute.

`nvertices` — int\
`vertex.count` (!)\
`face.vertex.count` (!)

The number of vertices for each face of the mesh. The number of values for this attribute specifies total face number (unless `nholes` is defined).

It also has optional attributes:

`nholes` — int\
`hole.count` (!)

The number of holes in the polygons. When this attribute is defined, the total number of faces in the mesh is defined by the number of values for `nholes` rather than for `nvertices`. For each face, there should be (nholes+1) values in `nvertices`: the respective first value specifies the number of vertices on the outside perimeter of the face, while additional values describe the number of vertices on perimeters of holes in the face.

`clockwisewinding` — int (0)\
`clockwise` (!)

A value of 1 specifies that polygons with a clockwise winding order are front facing. The default is 0, making counterclockwise polygons front facing.

`subdivision.scheme` — string

A value of `"catmull-clark"` will cause the mesh to render as a Catmull-Clark subdivision surface.

`subdivision.cornervertices` — int\
`subdivision.corner.index` (!)

This attribute is a list of vertices which are sharp corners. The values are indices into the P attribute, like `P.indices`.

`subdivision.cornersharpness` — float\
`subdivision.corner.sharpness` (!)

This attribute is the sharpness of each specified sharp corner. It must have a value for each value given in `subdivision.cornervertices`.

`subdivision.creasevertices` — int\
`subdivision.crease.index` (!)

This attribute is a list of crease edges. Each edge is specified as a pair of indices into the P attribute, like `P.indices`.

`subdivision.creasesharpness` — float\
`subdivision.crease.sharpness` (!)

This attribute is the sharpness of each specified crease. It must have a value for each pair of values given in `subdivision.creasevertices`.

`subdivision.smoothcreasecorners` — int (1)\
`subdivision.corner.automatic` (!)

This attribute controls whether or not the surface uses enhanced subdivision rules on vertices where more than two creased edges meet. With a value of 0, the vertex becomes a sharp corner. With a value of 1, the vertex is subdivided using an extended crease vertex subdivision rule which yields a smooth crease.

`referencetime` — double

Specifies a reference time where deformation data is most valid. This is mainly relevant for velocity blur, in which case it should be set to the time at which position data was originally available. If not set, see the same attribute on the [global node](#the-global-node).

`quadraticmotion` — int (0)

A value of 1 will enable curved deformation blur if three equally spaced time samples are provided for the P attribute. Linear deformation is used otherwise.

`outlinecreasethreshold` — float (10)

Controls how sharp a crease must be to be considered for the creation of outlines.

## The `faceset` node

This node is used to provide a way to attach attributes to some faces of another geometric primitive, such as the mesh node. It has the following attributes:

`faces` — int\
`face.index` (!)

This attribute is a list of indices of faces. It identifies which faces of the original geometry will be part of this face set.

## The `curves` node

This node represents a group of curves. It has the following required attributes:

`nvertices` — int\
`vertex.count` (!)

The number of vertices for each curve. This must be at least 4 for cubic curves and 2 for linear curves. There can be either a single value or one value per curve.

`P` — point

The positions of the curve vertices. The number of values provided, divided by `nvertices`, gives the number of curves which will be rendered.

`width` — float

The width of the curves.

`basis` — string (catmull-rom)

The basis functions used for curve interpolation. Possible choices are:

- `b-spline` — B-spline interpolation.
- `catmull-rom` — Catmull-Rom interpolation.
- `linear` — Linear interpolation.
- `hobby` (!) — Hobby interpolation.

`extrapolate` — int (0)

By default, cubic curves will not be drawn to their end vertices as the basis functions require an extra vertex to define the curve. If this attribute is set to 1, an extra vertex is automatically extrapolated so the curves reach their end vertices, as with linear interpolation.

Attributes may also have a single value, one value per curve, one value per vertex or one value per vertex of a single curve, reused for all curves. Attributes which fall in that last category must always specify `NSIParamPerVertex`. Note that a single curve is considered a face as far as use of `NSIParamPerFace` is concerned.

## The `particles` node

This geometry node represents a collection of _tiny_ particles. Particles are represented by either a disk or a sphere. This primitive is not suitable to render large particles as these should be represented by other means (e.g. instancing).

`P` — point

A mandatory attribute that specifies the center of each particle.

`width` — float

A mandatory attribute that specifies the width of each particle. It can be specified for the entire particles node (only one value provided) or per-particle.

`N` — normal

The presence of a normal indicates that each particle is to be rendered as an oriented disk. The orientation of each disk is defined by the provided normal which can be constant or a per-particle attribute. Each particle is assumed to be a sphere if a normal is not provided.

`reverseorientation` — int (0)

Setting this to 1 will reverse the orientation of spherical particles. Specifically, their u parametric direction is reversed, which also reverses their normal so it points inwards. It has no effect on particles for which N is provided.

`id` — int

This attribute, of the same size as P, assigns a unique identifier to each particle which must be constant throughout the entire shutter range. Its presence is necessary in the case where particles are motion blurred and some of them could appear or disappear during the motion interval. Having such identifiers allows the renderer to properly render such transient particles. This implies that the number of _ids_ might vary for each time step of a motion-blurred particle cloud so the use of `NSISetAttributeAtTime` is mandatory by definition.

`quadraticmotion` — int (0)

A value of 1 will enable curved deformation blur if three equally spaced time samples are provided for the P attribute. Linear deformation is used otherwise.

## The `procedural` node

This node acts as a proxy for geometry that could be defined at a later time than the node's definition, using a procedural supported by `NSIEvaluate`. Since the procedural is evaluated in complete isolation from the rest of the scene, it can be done either lazily (depending on its `boundingbox` attribute) or in parallel with other procedural nodes.

The procedural node supports, as its attributes, all the parameters of the `NSIEvaluate` API call, meaning that procedural types accepted by that API call (NSI archives, dynamic libraries, LUA scripts) are also supported by this node. Those attributes are used to call a procedural that is expected to define a sub-scene, which has to be independent from the other nodes in the scene. The procedural node will act as the sub-scene's local root and, as such, also supports all the attributes of a regular transform node. In order to connect the nodes it creates to the sub-scene's root, the procedural simply has to connect them to the regular [root node](nodes.md#the-root-node) `.root`.

In the context of an [interactive render](#the-global-node), the procedural will be executed again after the node's attributes have been edited. All nodes previously connected by the procedural to the sub-scene's root will be deleted automatically before the procedural's re-execution.

Additionally, this node has the following optional attribute:

`boundingbox` — point[2]

Specifies a bounding box for the geometry where `boundingbox[0]` and `boundingbox[1]` correspond, respectively, to the "minimum" and the "maximum" corners of the box.

## The `environment` node

This geometry node defines a sphere of infinite radius. Its only purpose is to render environment lights, solar lights and directional lights; lights which cannot be efficiently modeled using area lights. In practical terms, this node is no different than a geometry node with the exception of shader execution semantics: there is no surface position P, only a direction I (refer to [lighting guidelines](guidelines.md#lighting-in-the-nodal-scene-interface) for more practical details). The following node attribute is recognized:

`angle` — double (360)

Specifies the cone angle representing the region of the sphere to be sampled. The angle is measured around the Z+ axis. If the angle is set to 0, the environment describes a directional light. Refer to [lighting guidelines](guidelines.md#lighting-in-the-nodal-scene-interface) for more about how to specify light sources.

## The `shader` node

This node represents an ᴏsʟ shader, also called layer when part of a shader group. It has the following attributes:

`shaderfilename` — string

This is the name of the file which contains the shader's compiled code.

`shaderobject` — string

This contains the complete compiled shader code. It allows providing custom shaders without going through files.

Either `shaderfilename` or `shaderobject` must be provided. All other attributes on this node are considered parameters of the shader. They may either be given values or connected to attributes of other shader nodes to build shader networks. ᴏsʟ shader networks must form acyclic graphs or they will be rejected. Refer to [creating ᴏsʟ networks](guidelines.md#creating-osl-networks) for instructions on ᴏsʟ network creation and usage.

## The `attributes` node

This node is a generic container for attributes. Its exact purpose depends on where it is connected in the scene. There are currently two uses.

### geometry attributes

This node can provide various geometry related rendering attributes that are not _intrinsic_ to a particular node (for example, one can't set the topology of a polygonal mesh using this attributes node). For this use, instances of this node must be connected to the `geometryattributes` attribute of either geometric primitives or transform nodes (to build [attributes hierarchies](guidelines.md#a-word-or-two-about-attributes)). Attribute values are gathered along the path starting from the geometric primitive, through all the transform nodes it is connected to, until the [scene root](#the-root-node) is reached.

When an attribute is defined multiple times along this path, the definition with the highest priority is selected. In case of conflicting priorities, the definition that is closest to the geometric primitive (i.e. the furthest from the root) is selected. Connections (for shaders, essentially) can also be assigned priorities, which are used in the same way as for regular attributes. Multiple attributes nodes can be connected to the same geometry or transform nodes (e.g. one attributes node can set object visibility and another can set the surface shader) and will all be considered.

In this case, the node has the following attributes:

`surfaceshader` — \<connection\>\
`shader.surface` (!)

The [shader node](#the-shader-node) which will be used to shade the surface is connected to this attribute. A priority (useful for overriding a shader from higher in the scene graph) can be specified by setting the `priority` attribute of the connection itself.

`displacementshader` — \<connection\>\
`shader.displacement` (!)

The [shader node](#the-shader-node) which will be used to displace the surface is connected to this attribute. A priority (useful for overriding a shader from higher in the scene graph) can be specified by setting the `priority` attribute of the connection itself.

`volumeshader` — \<connection\>\
`shader.volume` (!)

The [shader node](#the-shader-node) which will be used to shade the volume inside the primitive is connected to this attribute.

`ATTR.priority` — int (0)

Sets the priority of attribute ATTR when gathering attributes in the scene hierarchy.

`visibility.camera` — int (1)\
`visibility.diffuse` — int (1)\
`visibility.hair` — int (1)\
`visibility.reflection` — int (1)\
`visibility.refraction` — int (1)\
`visibility.shadow` — int (1)\
`visibility.specular` — int (1)\
`visibility.volume` — int (1)

These attributes set visibility for each ray type specified in ᴏsʟ. The same effect could be achieved using shader code (using the `raytype()` function) but it is much faster to filter intersections at trace time. A value of 1 makes the object visible to the corresponding ray type, while 0 makes it invisible.

`visibility` — int (1)

This attribute sets the default visibility for all ray types. When visibility is set both per ray type and with this default visibility, the attribute with the highest priority is used. If their priority is the same, the more specific attribute (i.e. per ray type) is used.

`visibility.set.subsurface` — \<connection\>

If a [set node](#the-set-node) is connected to this attribute, subsurface rays will only see objects with a connection to that same set node.

`matte` — int (0)

If this attribute is set to 1, the object becomes a matte for camera rays. Its transparency is used to control the matte opacity and all other shading components are ignored.

`regularemission` — int (1)\
`emission.regular` (!)

If this is set to 1, closures not used with `quantize()` will use emission from the objects affected by the attribute. If set to 0, they will not.

`quantizedemission` — int (1)\
`emission.quantized` (!)

If this is set to 1, quantized closures will use emission from the objects affected by the attribute. If set to 0, they will not.

`bounds` — \<connection\>

When a geometry node (usually a [mesh node](#the-mesh-node)) is connected to this attribute, it will be used to restrict the effect of the attributes node, which will apply only inside the volume defined by the connected geometry object. It is also possible to connect a transform node to this. It is equivalent to connecting all the geometry nodes connected, even indirectly, to the transform.

### shader attributes

This node can be a container for attributes available to shaders. For this purpose, instances of this node must be connected to the `shaderattributes` attribute of geometric primitives, [transform](#the-transform-node) nodes or [set](#the-set-node) nodes. Attribute values are gathered along the path starting from the geometric primitive, through all the transform nodes it is connected to, until the [scene root](#the-root-node) is reached.

Priority is given to nodes attached closest to the geometric primitive, with the highest priority given to attributes set directly on the geometric primitive. Attributes set on this node may only have a single value.

## The `transform` node

This node represents a geometric transformation. Transform nodes can be chained together to express transform concatenation, hierarchies and instances. Transform nodes also accept attributes to implement [hierarchical attribute assignment and overrides](guidelines.md#a-word-or-two-about-attributes). It has the following attributes:

`transformationmatrix` — doublematrix\
`matrix` (!)

This is a 4x4 matrix which describes the node's transformation. Matrices in ɴsɪ post-multiply column vectors so are of the form:

```
| w11  w12  w13  0 |
| w21  w22  w23  0 |
| w31  w32  w33  0 |
| Tx   Ty   Tz   1 |
```

`objects` — \<connection\>\
`object` (!)

This is where the transformed objects are connected to. This includes geometry nodes, other transform nodes and camera nodes.

`geometryattributes` — \<connection\>\
`attribute` (!)

This is where [attributes nodes](#the-attributes-node) may be connected to affect any geometry transformed by this node. Refer to [attributes](guidelines.md#a-word-or-two-about-attributes) and [instancing](guidelines.md#instancing) for explanation on how this connection is used.

`shaderattributes` — \<connection\>

This is where [attributes nodes](#the-attributes-node) may be connected to provide shader attributes for any geometry transformed by this node.

## The `instances` node

This node is an efficient way to specify a large number of instances. It has the following attributes:

`sourcemodels` — \<connection\>\
`object` (!)

The instanced models should connect to this attribute. Connections must have an integer `index` attribute if there are several, so the models effectively form an ordered list.

`transformationmatrices` — doublematrix\
`matrix` (!)

A transformation matrix for each instance.

`modelindices` — int (0)\
`object.index` (!)

An optional model selector for each instance. The value used is matched to the `index` attribute of the model connection. A negative value will cause an instance to not be rendered.

`disabledinstances` — int\
`disable.index` (!)

An optional list of indices of instances which are not to be rendered.

## The `outputdriver` node

An output driver defines how an image is transferred to an output destination. The destination could be a file (e.g. "exr" output driver), frame buffer or a memory address. It can be connected to the `outputdrivers` attribute of an [output layer](#the-outputlayer-node) node. It has the following attributes:

`drivername` — string

This is the name of the driver to use. The API of the driver is implementation specific and is not covered by this documentation.

`imagefilename` — string\
`filename` (!)

Full path to a file for a file-based output driver or some meaningful identifier depending on the output driver.

`embedstatistics` — int (1)

A value of 1 specifies that statistics will be embedded into the image file.

Any extra attributes are also forwarded to the output driver which may interpret them however it wishes.

## The `outputlayer` node

This node describes one specific layer of render output data. It can be connected to the `outputlayers` attribute of a screen node. It has the following attributes:

`variablename` — string

This is the name of a variable to output.

`variablesource` — string (shader)

Indicates where the variable to be output is read from. Possible values are:

- `shader` — computed by a shader and output through an ᴏsʟ closure (such as `outputvariable()` or `debug()`) or the `Ci` global variable.
- `attribute` — retrieved directly from an attribute with a matching name attached to a geometric primitive.
- `builtin` — generated automatically by the renderer (e.g. `"z"`, `"alpha"`, `"N.camera"`, `"P.world"`).

`layername` — string

This will be name of the layer as written by the output driver. For example, if the output driver writes to an EXR file then this will be the name of the layer inside that file.

`scalarformat` — string (uint8)

Specifies the format in which data will be encoded (quantized) prior to passing it to the output driver. Possible values are:

- `int8` — signed 8-bit integer
- `uint8` — unsigned 8-bit integer
- `int16` — signed 16-bit integer
- `uint16` — unsigned 16-bit integer
- `int32` — signed 32-bit integer
- `uint32` — unsigned 32-bit integer
- `half` — IEEE 754 half-precision binary floating point (binary16)
- `float` — IEEE 754 single-precision binary floating point (binary32)

`layertype` — string (color)

Specifies the type of data that will be written to the layer. Possible values are:

- `scalar` — A single quantity. Useful for opacity ("alpha") or depth ("Z") information.
- `color` — A 3-component color.
- `vector` — A 3D point or vector. This will help differentiate the data from a color in further processing.
- `quad` — A sequence of 4 values, where the fourth value is not an alpha channel.

Each component of those types is stored according to the `scalarformat` attribute set on the same outputlayer node.

`colorprofile` — string

The name of an OCIO color profile to apply to rendered image data prior to quantization.

`dithering` — integer (0)

If set to 1, dithering is applied to integer scalars. Otherwise, it must be set to 0.

`withalpha` — integer (0)

If set to 1, an alpha channel is included in the output layer. Otherwise, it must be set to 0.

`sortkey` — integer

This attribute is used as a sorting key when ordering multiple output layer nodes connected to the same [output driver](#the-outputdriver-node) node. Layers with the lowest `sortkey` attribute appear first.

`lightset` — \<connection\>

This connection accepts either light sources or [set](#the-set-node) nodes to which lights are connected. In this case only listed lights will affect the render of the output layer. If nothing is connected to this attribute then all lights are rendered.

If an [environment](#the-environment-node) node is connected here, a `component` string attribute can be specified on the connection with a value of either `sun` or `background`. If this is used, only the corresponding part of the environment will contribute to the output layer.

`lightsetname` — string

This can be provided as friendly name for the connected light set. Otherwise, a default name is built from the connected node.

`outputdrivers` — \<connection\>\
`outputdriver` (!)

This connection accepts [output driver](#the-outputdriver-node) nodes to which the layer's image will be sent.

`filter` — string (blackman-harris)

The type of filter to use when reconstructing the final image from sub-pixel samples. Possible values are: `"box"`, `"triangle"`, `"catmull-rom"`, `"bessel"`, `"gaussian"`, `"sinc"`, `"mitchell"`, `"blackman-harris"`, `"zmin"` and `"zmax"`.

`filterwidth` — double (3.0)

Diameter in pixels of the reconstruction filter. It is not applied when filter is `"box"` or `"zmin"`.

`backgroundvalue` — float (0)

The value given to pixels where nothing is rendered.

`backgroundlayer` — \<connection\>

This connection accepts a single output layer node which is meant to be displayed as a background. Not all [output drivers](#the-outputdriver-node) support this behavior, so it might be ignored.

`lightdepth` — string (auto)

Allows filtering light contributions according to the number of bounces light has made from a light source to the objects in front of the camera. This is only meaningful when the layer's `variablesource` is set to `shader` (otherwise, it's ignored). Possible values are:

- `direct` — Only light coming directly from light sources to visible objects (ie: with no bounce) is included.
- `indirect` — Only light coming from light sources to visible objects through at least one bounce is shown.
- `both` — All light is included.
- `auto` — Selects the appropriate value for lightdepth according to the value of the `variablename` attribute. If it ends with either `.direct` or `.indirect`, the corresponding light depth will be used, and the suffix will be removed from the effective variable name. Otherwise, it will default to `both`.

`cryptomatte.enable` — int (0)

Setting this attribute to 1 enables Cryptomatte encoding of the layer's data. `cryptomatte.level` should also be set properly.

`cryptomatte.level` — int (0)

If this value is negative, the layer will contain a human-readable "Cryptomatte header" image. Otherwise, the value indicates the index of the first Cryptomatte level that will be output. Since Cryptomatte levels are output by pairs, a Cryptomatte file with 4 levels would contain output layers with `cryptomatte.level` set to -1, 0 and 2. This has no effect unless Cryptomatte encoding is enabled using `cryptomatte.enable`.

Any extra attributes are also forwarded to the output driver which may interpret them however it wishes.

## The `screen` node

This node describes how the view from a camera node will be rasterized into an [output layer](#the-outputlayer-node) node. It can be connected to the `screens` attribute of a camera node.

`outputlayers` — \<connection\>\
`outputlayer` (!)

This connection accepts [output layer](#the-outputlayer-node) nodes which will receive a rendered image of the scene as seen by the camera.

`resolution` — integer[2]

Horizontal and vertical resolution of the rendered image, in pixels.

`oversampling` — integer

The total number of samples (i.e. camera rays) to be computed for each pixel in the image.

`crop` — 2 × float[2]

The region of the image to be rendered. It's defined by a list of exactly 2 pairs of floating-point number. Each pair represents a point in ɴᴅᴄ space:

- Top-left corner of the crop region
- Bottom-right corner of the crop region

`prioritywindow` — 2 × int[2]

For progressive renders, this is the region of the image to be rendered first. It is two pairs of integers. Each represents pixel coordinates:

- Top-left corner of the high priority region
- Bottom-right corner of the high priority region

`screenwindow` — 2 × double[2]

Specifies the screen space region to be rendered. Each pair represents a 2D point in screen space:

- Bottom-left corner of the region
- Top-right corner of the region

Note that the default screen window is set implicitly by the frame aspect ratio:
screenwindow = [-f, -1], [f, 1] for f = xres/yres

`overscan` — 2 × int[2]

Specifies how many extra pixels to render around the image. The four values represent the amount of overscan on the left, top, right and bottom of the image.

`pixelaspectratio` — float

Ratio of the physical width to the height of a single pixel. A value of 1.0 corresponds to square pixels.

`staticsamplingpattern` — int (0)

This controls whether or not the sampling pattern used to produce the image change for every frame. A nonzero value will cause the same pattern to be used for all frames. A value of zero will cause the pattern to change with the `frame` attribute of the [global node](#the-global-node).

`importancesamplefilter` — int (0)

This enables a rendering mode where the pixel filter is importance sampled. Quality will be reduced and the same filter will be used for all output layers of the screen. Filters with negative lobes (eg. sinc) are unsupported.

## The `vdbparticles` node

This node represents particles defined by [OpenVDB](https://www.openvdb.org) data. It has the following attributes:

`vdbfilename` — string

The path to an OpenVDB file with the particle data.

`pointsgrid` — string

The name of the OpenVDB grid to use for particle data. It must be of type PointDataGrid.

`velocityreferencetime` — double

The reference time at which the grid data is used directly, without being moved by the velocity attribute. Defaults to the [global node](#the-global-node)'s `referencetime` attribute.

`velocityscale` — double (1)

A scaling factor applied to the velocity data.

`enablepscale` — int (1)

Enables use of the `pscale` attribute in the grid to specify particle radius.

`width` — double (1)

The width of particles, if there is no `pscale` attribute in the file to specify their radius or it is disabled by setting `enablepscale` to 0.

`widthscale` — double (1)

A scaling factor applied to particle width.

The P, v and pscale grid attributes are used to respectively define particle position, velocity and radius. Other grid attributes may be read by shaders.

## The `volume` node

This node represents a volumetric object defined by [OpenVDB](https://www.openvdb.org) data. It has the following attributes:

`vdbfilename` — string

The path to an OpenVDB file with the volumetric data.

`densitygrid` — string

The name of the OpenVDB grid to use as volume density for the volume shader.

`colorgrid` — string

The name of the OpenVDB grid to use as a scattering color multiplier for the volume shader.

`emissiongrid` — string

The name of the OpenVDB grid to use directly as emission for the volume shader.

`emissionintensitygrid` — string

The name of the OpenVDB grid to use as emission intensity for the volume shader.

`temperaturegrid` — string

The name of the OpenVDB grid to use as temperature for the volume shader.

`velocitygrid` — string

The name of the OpenVDB grid to use as motion vectors. This can also name the first of three scalar grids (ie. "velocityX").

`velocityreferencetime` — double

The reference time at which the grid data is used directly, without being moved by the velocity grid. Defaults to the [global node](#the-global-node)'s `referencetime` attribute.

`velocityscale` — double (1)

A scaling factor applied to the motion vectors.

## Camera Nodes

All camera nodes share a set of common attributes. These are listed below.

`screens` — \<connection\>\
`screen` (!)

This connection accepts [screen](#the-screen-node) nodes which will rasterize an image of the scene as seen by the camera. Refer to [defining output drivers and layers](guidelines.md#defining-output-drivers-and-layers) for more information.

`shutterrange` — double

Time interval during which the camera shutter is at least partially open. It's defined by a list of exactly two values:

- Time at which the shutter starts **opening**.
- Time at which the shutter finishes **closing**.

`shutteropening` — double

A _normalized_ time interval indicating the time at which the shutter is fully open (a) and the time at which the shutter starts to close (b). These two values define the top part of a trapezoid filter. The end goal of this feature it to simulate a mechanical shutter on which open and close movements are not instantaneous.

![An example shutter opening configuration](image/shutter.svg)

`clippingrange` — double

Distance of the near and far clipping planes from the camera. It's defined by a list of exactly two values:

- Distance to the `near` clipping plane, in front of which scene objects are clipped.
- Distance to the `far` clipping plane, behind which scene objects are clipped.

### The orthographiccamera node

This node defines an orthographic camera with a view direction towards the Z- axis. This camera has no specific attributes.

### The perspectivecamera node

This node defines a perspective camera. The canonical camera is viewing in the direction of the Z- axis. The node is usually connected into a [transform](#the-transform-node) node for camera placement. It has the following attributes:

`fov` — float

The field of view angle, in degrees.

`depthoffi­eld.enable` — integer (0)

Enables depth of field effect for this camera.

`depthoffi­eld.fstop` — double

Relative aperture of the camera.

`depthoffi­eld.focallength` — double

Vertical focal length, in scene units, of the camera lens.

`depthoffi­eld.focallengthratio` — double (1)

Ratio of vertical focal length to horizontal focal length. This is the squeeze ratio of an anamorphic lens.

`depthoffi­eld.focaldistance` — double

Distance, in scene units, in front of the camera at which objects will be in focus.

`depthoffi­eld.aperture.enable` — integer (0)

By default, the renderer simulates a circular aperture for depth of field. Enable this feature to simulate aperture "blades" as on a real camera. This feature affects the look in out-of-focus regions of the image.

`depthoffi­eld.aperture.sides` — integer (5)

Number of sides of the camera's aperture. The minimum number of sides is 3.

`depthoffi­eld.aperture.angle` — double (0)

A rotation angle (in degrees) to be applied to the camera's aperture, in the image plane.

`unitlengthmillimeters` — double

Physical length, in millimeters, of one scene unit. Since NSI only uses virtual scene units, this has no effect on the rendered images. However, this value can be useful if the renderer has to communicate with other software or file formats using physical units. For example, the focal length of the camera, expressed in millimeters, would be the product `depthoffi­eld.focallength * unitlengthmillimeters`.

### The fisheyecamera node

Fish eye cameras are useful for a multitude of applications (e.g. virtual reality). This node accepts these attributes:

`fov` — float

Specifies the field of view for this camera node, in degrees.

`mapping` — string (equidistant)

Defines one of the supported fisheye [mapping functions](https://en.wikipedia.org/wiki/Fisheye_lens):

- `equidistant` — Maintains angular distances.
- `equisolidangle` — Every pixel in the image covers the same solid angle.
- `orthographic` — Maintains planar illuminance. This mapping is limited to a 180 field of view.
- `stereographic` — Maintains angles throughout the image. Note that stereographic mapping fails to work with field of views close to 360 degrees.

### The cylindricalcamera node

This node specifies a cylindrical projection camera and has the following attributes:

`fov` — float (90)

Specifies the _vertical_ field of view, in degrees.

`horizontalfov` — float (360)\
`fov.horizontal` (!)

Specifies the horizontal field of view, in degrees.

`eyeoffset` — float

This offset allows to render stereoscopic cylindrical images by specifying an eye offset.

### The sphericalcamera node

This node defines a spherical projection camera. This camera has no specific attributes.

### Lens shaders

A lens shader is an ᴏsʟ network connected to a camera through the `lensshader` connection. Such shaders receive the position and the direction of each tracer ray and can either change or completely discard the traced ray. This allows to implement distortion maps and cut maps. The following shader variables are provided:

- `P` — Contains ray's origin.
- `I` — Contains ray's direction. Setting this variable to zero instructs the renderer not to trace the corresponding ray sample.
- `time` — The time at which the ray is sampled.
- `(u, v)` — Coordinates, in screen space, of the ray being traced.
