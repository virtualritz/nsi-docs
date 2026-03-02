# Nodes

The following sections describe available nodes in technical terms. Refer to [the rendering guidelines](guidelines.md) for usage details.

| Node                                  | Function                                                                          |
| ------------------------------------- | --------------------------------------------------------------------------------- |
| [root](nodes/root.md)                 | Scene's root                                                                      |
| [global](nodes/global.md)             | Global settings node                                                              |
| [set](nodes/set.md)                   | To express relationships of groups of nodes                                       |
| [shader](nodes/shader.md)             | [ᴏsʟ](https://opensource.imageworks.com/?p=osl) shader or layer in a shader group |
| [attributes](nodes/attributes.md)     | Container for generic attributes (e.g. visibility)                                |
| [transform](nodes/transform.md)       | Transformation to place objects in the scene                                      |
| [mesh](nodes/mesh.md)                 | Polygonal mesh or subdivision surface                                             |
| [plane](nodes/plane.md)               | Infinite plane                                                                    |
| [faceset](nodes/faceset.md)           | Assign attributes to part of a mesh                                               |
| [curves](nodes/curves.md)             | Linear, B-spline and Catmull-Rom curves                                           |
| [particles](nodes/particles.md)       | Collection of particles                                                           |
| [procedural](nodes/procedural.md)     | Geometry to be loaded in delayed fashion                                          |
| [environment](nodes/environment.md)   | Geometry type to define environment lighting                                      |
| [vdbparticles](nodes/vdbparticles.md) | Particles defined by [OpenVDB](https://www.openvdb.org) data                      |
| [volume](nodes/volume.md)             | Volumetric object defined by [OpenVDB](https://www.openvdb.org) data              |
| [outputdriver](nodes/outputdriver.md) | Location where to output rendered pixels                                          |
| [outputlayer](nodes/outputlayer.md)   | Describes one render layer to be connected to an outputdriver node                |
| [screen](nodes/screen.md)             | Describes how the view from a camera will be rasterized into an outputlayer node  |
| [\*camera](nodes/camera-nodes.md)     | Set of nodes to create viewing cameras                                            |
