.. _section:background:

Background
==========

The Nodal Scene Interface (nsi) was developed to replace existing api\ s
in our renderer which are showing their age. Having been designed in the
80s and extended several times since, they include features which are no
longer relevant and design decisions which do not reflect modern needs.
This makes some features more complex to use than they should be and
prevents or greatly increases the complexity of implementing other
features.

The design of the nsi was shaped by multiple goals:

Simplicity
   The interface itself should be simple to understand and use, even if
   complex things can be done with it. This simplicity is carried into
   everything which derives from the interface.

Interactive rendering and scene edits
   Scene edit operations should not be a special case. There should be
   no difference between scene *description* and scene *edits*. In other
   words, a scene description is a series of edits and vice versa.

Tight integration with *Open Shading Language*
   osl integration is not superficial and affects scene definition. For
   example, there are no explicit light sources in nsi: light sources
   are created by connected shaders with an ``emission()`` closure to a
   geometry.

Scripting
   The interface should be accessible from a platform independent,
   efficient and easily accessible scripting language. Scripts can be
   used to add render time intelligence to a given scene description.

Performance and multi-threading
   All api design decisions are made with performance in mind and this
   includes the possibility to run all api calls in a concurrent,
   multi-threaded environment. Nearly all software today which deals
   with large data sets needs to use multiple threads at some point. It
   is important for the interface to support this directly so it does
   not become a single thread communication bottleneck. This is why
   commands are self-contained and do not rely on a current state.
   Everything which is needed to perform an action is passed in on every
   call.

Support for serialization
   The interface calls should be serializable. This implies a mostly
   unidirectional dataflow from the client application to the renderer
   and allows greater implementation flexibility.

Extensibility
   The interface should have as few assumptions as possible built-in
   about which features the renderer supports. It should also be
   abstract enough that new features can be added without looking out of
   place.
