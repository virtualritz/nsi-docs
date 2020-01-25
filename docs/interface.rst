The Interface
=============

The interface abstraction
-------------------------

The Nodal Scene Interface is built around the concept of nodes. Each
node has a unique handle to identify it and a type which describes its
intended function in the scene. Nodes are abstract containers for data
for which the interpretation depends on the node type. Nodes can also be
connected to each other to express relationships.

Data is stored on nodes as attributes. Each attribute has a name which
is unique on the node and a type which describes the kind of data it
holds (strings, integer numbers, floating point numbers, etc).

Relationships and data flow between nodes are represented as
connections. Connections have a source and a destination. Both can be
either a node or a specific attribute of a node. There are no type
restrictions for connections in the interface itself. It is acceptable
to connect attributes of different types or even attributes to nodes.
The validity of such connections depends on the types of the nodes
involved.

What we refer to as the nsi has two major components:

-  Methods to create nodes, attributes and their connections.

-  Node types understood by the renderer. These are described in .

Much of the complexity and expressiveness of the interface comes from
the supported nodes. The first part was kept deliberately simple to make
it easy to support multiple ways of creating nodes. We will list a few
of those in the following sections but this list is not meant to be
final. New languages and file formats will undoubtedly be supported in
the future.

The C API
---------

This section will describe in detail the c implementation of the nsi, as
provided in the ``nsi.h`` file. This will also be a reference for the
interface in other languages as all concepts are the same.

.. code-block:: c

   #define NSI_VERSION 1

The ``NSI_VERSION`` macro exists in case there is a need at some point
to break source compatibility of the c interface.

.. code-block:: c

   #define NSI_SCENE_ROOT ".root"

The ``NSI_SCENE_ROOT`` macro defines the handle of
:ref:`root node<section:rootnode>`.

.. code-block:: c

   #define NSI_ALL_NODES ".all"

The ``NSI_ALL_NODES`` macro defines a special handle to refer to all
nodes in some contexts, such as when
:ref:`removing connections<CAPI:nsiconnect>`.

.. _CAPI:contexthandling:

Context handling
~~~~~~~~~~~~~~~~

.. code-block:: c

   NSIContext_t NSIBegin(
      int nparams,
      const NSIParam_t *params
   )

.. code-block:: c

   void NSIEnd(
      NSIContext_t ctx
   )

These two functions control creation and destruction of a nsi context,
identified by a handle of type ``NSIContext_t``. A context must be given
explicitly when calling all other functions of the interface. Contexts
may be used in multiple threads at once. The ``NSIContext_t`` is a
convenience typedef and is defined as:

.. code-block:: c

   typedef int NSIContext_t;

If ``NSIBegin`` fails for some reason, it returns ``NSI_BAD_CONTEXT``
which is defined in ``nsi.h``:

.. code-block:: c

   #define NSI_BAD_CONTEXT ((NSIContext_t)0)

Optional parameters may be given to ``NSIBegin()`` to control the
creation of the context:

.. table::
   :widths: 2 1 2 5

   +------------------------+---------+-------------------------------------------------------+
   | ``type``               | string  | Sets the type of context to create. The possible      |
   |                        |         | types are:                                            |
   +------------------------+---------+---------------+---------------------------------------+
   |                        |         | ``render``    | Execute the calls directly in the     |
   |                        |         |               | renderer.                             |
   |                        |         +---------------+---------------------------------------+
   |                        |         | ``apistream`` | To write the interface calls to a     |
   |                        |         |               | stream, for later execution.          |
   |                        |         |               | The target for writing the stream     |
   |                        |         |               | must be specified in another          |
   |                        |         |               | parameter.                            |
   +------------------------+---------+---------------+---------------------------------------+
   | ``streamfilename``     | string  | The file to which the stream is to be output, if the  |
   |                        |         | context type is ``apistream``.                        |
   |                        |         | Specify ``stdout`` to write to standard output and    |
   |                        |         | ``stderr`` to write to standard error.                |
   +------------------------+---------+-------------------------------------------------------+
   | ``streamformat``       | string  | The format of the command stream to write. Possible   |
   |                        |         | formats are:                                          |
   |                        |         +---------------+---------------------------------------+
   |                        |         | ``nsi``       | Produces an                           |
   |                        |         |               | :ref:`nsi stream<section:nsistream>`  |
   |                        |         +---------------+---------------------------------------+
   |                        |         | ``binarynsi`` | Produces a binary encoded             |
   |                        |         |               | :ref:`nsi stream<section:nsistream>`  |
   +------------------------+---------+---------------+---------------------------------------+
   | ``streamcompression``  | string  | The type of compression to apply to the written       |
   |                        |         | command stream.                                       |
   +------------------------+---------+-------------------------------------------------------+
   | ``errorhandler``       | pointer | A function which is to be called by the renderer to   |
   |                        |         | report errors. The default handler will print         |
   |                        |         | messages to the console.                              |
   +------------------------+---------+-------------------------------------------------------+
   | ``errorhandlerdata``   | pointer | The ``userdata`` parameter of the error reporting     |
   |                        |         | function.                                             |
   +------------------------+---------+-------------------------------------------------------+
   | ``executeprocedurals`` | string  | A list of procedural types that should be executed    |
   |                        |         | immediately when a call to or a procedural node is    |
   |                        |         | encountered and ``NSIBegin()``'s output ``type`` is   |
   |                        |         | ``apistream``. This will replace any matching call    |
   |                        |         | to ``NSIEvaluate()`` with the results of the          |
   |                        |         | procedural's execution.                               |
   +------------------------+---------+-------------------------------------------------------+

.. _CAPI:optionalparam:

Passing optional parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   struct NSIParam_t
   {
       const char *name;
       const void *data;
       int type;
       int arraylength;
       size_t count;
       int flags;
   };

This structure is used to pass variable parameter lists through the c
interface. Most functions accept an array of the structure in a
``params`` parameter along with its length in a ``nparams`` parameter.
The meaning of these two parameters will not be documented for every
function. Instead, they will document the parameters which can be given
in the array.

The ``name`` member is a c string which gives the parameter’s name. The
``type`` member identifies the parameter’s type, using one of the
following constants:

-  ``NSITypeFloat`` for a single 32-bit floating point value.

-  ``NSITypeDouble`` for a single 64-bit floating point value.

-  ``NSITypeInteger`` for a single 32-bit integer value.

-  ``NSITypeString`` for a string value, given as a pointer to a c
   string.

-  ``NSITypeColor`` for a color, given as three 32-bit floating point
   values.

-  ``NSITypePoint`` for a point, given as three 32-bit floating point
   values.

-  ``NSITypeVector`` for a vector, given as three 32-bit floating point
   values.

-  ``NSITypeNormal`` for a normal vector, given as three 32-bit floating
   point values.

-  ``NSITypeMatrix`` for a transformation matrix, given as 16 32-bit
   floating point values.

-  ``NSITypeDoubleMatrix`` for a transformation matrix, given as 16
   64-bit floating point values.

-  ``NSITypePointer`` for a c pointer.

Array types are specified by setting the bit defined by the
``NSIParamIsArray`` constant in the ``flags`` member and the length of
the array in the ``arraylength`` member. The ``count`` member gives the
number of data items given as the value of the parameter. The ``data``
member is a pointer to the data for the parameter. The ``flags`` member
is a bit field with a number of constants defined to communicate more
information about the parameter: [Interface:parameterflags]

-  ``NSIParamIsArray`` to specify that the parameter is an array type,
   as explained previously.

-  ``NSIParamPerFace`` to specify that the parameter has different
   values for every face of a geometric primitive, where this might be
   ambiguous.

-  ``NSIParamPerVertex`` to specify that the parameter has different
   values for every vertex of a geometric primitive, where this might be
   ambiguous.

-  ``NSIParamInterpolateLinear`` to specify that the parameter is to be
   interpolated linearly instead of using some other default method.

[parameter:indirect] Indirect lookup of parameters is achieved by giving
an integer parameter of the same name, with the ``.indices`` suffix
added. This is read to know which values of the other parameter to use.

.. _CAPI:nsicreate:

Node creation
~~~~~~~~~~~~~

.. code-block:: c

   void NSICreate(
       NSIContext_t context,
       NSIHandle_t handle,
       const char *type,
       int nparams,
       const NSIParam_t *params
   )

This function is used to create a new node. Its parameters are:


``context``
      The context returned by ``NSIBegin()``. See
      :ref:`context handling<CAPI:contexthandling>`.

``handle``
   A node handle. This string will uniquely identify the node in the
   scene.

   If the supplied handle matches an existing node, the function does
   nothing if all other parameters match the call which created that
   node.
   Otherwise, it emits an error. Note that handles need only be unique
   within a given interface context. It is acceptable to reuse the same
   handle inside different contexts. The ``NSIHandle_t`` typedef is
   defined in `nsi.h`:

   .. code-block:: c

      typedef const char* NSIHandle_t;

``type``
   The type of :ref:`node<section:nodes>` to create.

``nparams``, ``params``
   This pair describes a list of optional parameters. *There are no
   optional parameters defined as of now*. The ``NSIParam_t`` type is
   described in .

--------------

.. code-block:: c

   void NSIDelete(
       NSIContext_t ctx,
       NSIHandle_t handle,
       int nparams,
       const NSIParam_t *params
   )

This function deletes a node from the scene. All connections to and from
the node are also deleted. Note that it is not possible to delete the or
the node. Its parameters are:

The context returned by ``NSIBegin()``. See
:ref:`context handling<CAPI:contexthandling>`.

A node handle. It identifies the node to be deleted.

It accepts the following optional parameters:

Specifies whether deletion is recursive. By default, only the specified
node is deleted. If a value of 1 is given, then nodes which connect to
the specified node are recursively removed, unless they also have
connections which do not eventually lead to the specified node. This
allows, for example, deletion of an entire shader network in a single
call.

Setting attributes
~~~~~~~~~~~~~~~~~~

.. code-block:: c

   void NSISetAttribute(
       NSIContext_t ctx,
       NSIHandle_t object,
       int nparams,
       const NSIParam_t *params
   )

This functions sets attributes on a previously node. All of the function
become attributes of the node. On a node, this function is used to set
the implicitly defined shader parameters. Setting an attribute using
this function replaces any value previously set by
``NSISetAttribute()`` or ``NSISetAttributeAtTime()``. To reset an
attribute to its default value, use .

--------------

::

   void NSISetAttributeAtTime(
       NSIContext_t ctx,
       NSIHandle_t object,
       double time,
       int nparams,
       const NSIParam_t *params );

This function sets time-varying attributes (i.e. motion blurred). The
``time`` parameter specifies at which time the attribute is being
defined. It is not required to set time-varying attributes in any
particular order. In most uses, attributes that are motion blurred must
have the same specification throughout the time range. A notable
exception is the ``P`` attribute on which can be of different size for
each time step because of appearing or disappearing particles. Setting
an attribute using this function replaces any value previously set by
``NSISetAttribute``.

--------------

[CAPI:nsideleteattribute]

::

   void NSIDeleteAttribute(
       NSIContext_t ctx,
       NSIHandle_t object,
       const char *name );

This function deletes any attribute with a name which matches the
``name`` parameter on the specified object. There is no way to delete an
attribute only for a specific time value.

Deleting an attribute resets it to its default value. For example, after
deleting the ``transformationmatrix`` attribute on a node, the transform
will be an identity. Deleting a previously set attribute on a node will
default to whatever is declared inside the shader.

.. _CAPI:nsiconnect:

Making connections
~~~~~~~~~~~~~~~~~~

[CAPI:nsidisconnect]

::

   void NSIConnect(
       NSIContext_t ctx,
       NSIHandle_t from,
       const char *from_attr,
       NSIHandle_t to,
       const char *to_attr,
       int nparams,
       const NSIParam_t *params );

   void NSIDisconnect(
       NSIContext_t ctx,
       NSIHandle_t from,
       const char *from_attr,
       NSIHandle_t to,
       const char *to_attr );

These two functions respectively create or remove a connection between
two elements. It is not an error to create a connection which already
exists or to remove a connection which does not exist but the nodes on
which the connection is performed must exist. The parameters are:

The handle of the node from which the connection is made.

The name of the attribute from which the connection is made. If this is
an empty string then the connection is made from the node instead of
from a specific attribute of the node.

The handle of the node to which the connection is made.

The name of the attribute to which the connection is made. If this is an
empty string then the connection is made to the node instead of to a
specific attribute of the node.

``NSIConnect`` accepts additional optional parameters. Refer to for more
about their utility.

With ``NSIDisconnect``, the handle for either node may be the special
value . This will remove all connections which match the other three
parameters. For example, to disconnect everything from the :

::

   NSIDisconnect( NSI_ALL_NODES, "", NSI_SCENE_ROOT, "objects" );

.. _CAPI:nsievaluate:

Evaluating procedurals
~~~~~~~~~~~~~~~~~~~~~~

::

   void NSIEvaluate(
       NSIContext_t ctx,
       int nparams,
       const NSIParam_t *params );

This function includes a block of interface calls from an external
source into the current scene. It blends together the concepts of a
straight file include, commonly known as an archive, with that of
procedural include which is traditionally a compiled executable. Both
are really the same idea expressed in a different language (note that
for delayed procedural evaluation one should use the node).

The nsi adds a third option which sits in-between—Lua scripts (). They
are much more powerful than a simple included file yet they are also
much easier to generate as they do not require compilation. It is, for
example, very realistic to export a whole new script for every frame of
an animation. It could also be done for every character in a frame. This
gives great flexibility in how components of a scene are put together.

The ability to load nsi command straight from memory is also provided.

The optional parameters accepted by this function are:

The type of file which will generate the interface calls. This can be
one of:

:math:`\rightarrow` To read in a . This requires either ``filename``,
``script`` or\ ``buffer/size`` to be provided as source for nsi
commands.

:math:`\rightarrow` To execute a Lua script, either from file or inline.
See and more specifically .

:math:`\rightarrow` To execute native compiled code in a loadable
library. See for about the implementation of such a library.

The name of the file which contains the interface calls to include.

A valid Lua script to execute when ``type`` is set to ``"lua"``.

These two parameters define a memory block that contain nsi commands to
execute.

If this is nonzero, the object may be loaded in a separate thread, at
some later time. This requires that further interface calls not directly
reference objects defined in the included file. The only guarantee is
that the file will be loaded before rendering begins.

.. _subsection:errors:

Error reporting
~~~~~~~~~~~~~~~

::

   enum NSIErrorLevel
   {
       NSIErrMessage = 0,
       NSIErrInfo = 1,
       NSIErrWarning = 2,
       NSIErrError = 3
   };

   typedef void (*NSIErrorHandler_t)(
       void *userdata, int level, int code, const char *message );

This defines the type of the error handler callback given to the
``NSIBegin`` function. When it is called, the ``level`` parameter is one
of the values defined by the ``NSIErrorLevel`` enum. The ``code``
parameter is a numeric identifier for the error message, or 0 when
irrelevant. The ``message`` parameter is the text of the message.

The text of the message will not contain the numeric identifier nor any
reference to the error level. It is usually desirable for the error
handler to present these values together with the message. The
identifier exists to provide easy filtering of messages.

The intended meaning of the error levels is as follows:

-  ``NSIErrMessage`` for general messages, such as may be produced by
   printf in shaders. The default error handler will print this type of
   messages without an eol terminator as it’s the duty of the caller to
   format the message.

-  ``NSIErrInfo`` for messages which give specific information. These
   might simply inform about the state of the renderer, files being
   read, settings being used and so on.

-  ``NSIErrWarning`` for messages warning about potential problems.
   These will generally not prevent producing images and may not require
   any corrective action. They can be seen as suggestions of what to
   look into if the output is broken but no actual error is produced.

-  ``NSIErrError`` for error messages. These are for problems which will
   usually break the output and need to be fixed.

.. _section:rendering:

Rendering
~~~~~~~~~

::

   void NSIRenderControl(
       NSIContext_t ctx,
       int nparams,
       const NSIParam_t *params );

This function is the only control function of the api. It is responsible
of starting, suspending and stopping the render. It also allows for
synchronizing the render with interactive calls that might have been
issued. The function accepts :

Specifies the operation to be performed, which should be one of the
following:

:math:`\rightarrow` This starts rendering the scene in the provided
context. The render starts in parallel and the control flow is not
blocked.

:math:`\rightarrow` Wait for a render to finish.

:math:`\rightarrow` For an interactive render, apply all the buffered
calls to scene’s state.

:math:`\rightarrow` Suspends render in the provided context.

:math:`\rightarrow` Resumes a previously suspended render.

:math:`\rightarrow` Stops rendering in the provided context without
destroying the scene

If set to 1, render the image in a progressive fashion.

[interactive render] If set to 1, the renderer will accept commands to
edit scene’s state while rendering. The difference with a normal render
is that the render task will not exit even if rendering is finished.
Interactive renders are by definition progressive.

Specifies the frame number of this render.

A pointer to a user function that should be called on rendering status
changes. This function must have no return value and accept a pointer
argument, a nsi context argument and an integer argument :

::

   void StoppedCallback(
       void* stoppedcallbackdata,
       NSIContext_t ctx,
       int status);

The third parameter is an integer which can take the following values:

-  ``NSIRenderCompleted`` indicates that rendering has completed
   normally.

-  ``NSIRenderAborted`` indicates that rendering was interrupted before
   completion.

-  ``NSIRenderSynchronized`` indicates that an interactive render has
   produced an image which reflects all changes to the scene.

-  ``NSIRenderRestarted`` indicates that an interactive render has
   received new changes to the scene and no longer has an up to date
   image.

A pointer that will be passed back to the ``stoppedcallback`` function.

.. _section:Lua:

The Lua API
-----------

The scripted interface is slightly different than its C counterpart
since it has been adapted to take advantage of the niceties of Lua. The
main differences with the C api are:

-  No need to pass a nsi context to function calls since it’s already
   embodied in the nsi Lua table (which is used as a class).

-  The ``type`` parameter specified can be omitted if the parameter is
   an integer, real or string (as with the ``Kd`` and ``filename`` in
   the example below).

-  nsi parameters can either be passed as a variable number of arguments
   or as a single argument representing an array of parameters (as in
   the ``"ggx"`` shader below)

-  There is no need to call ``NSIBegin`` and ``NSIEnd`` equivalents
   since the Lua script is run in a valid context.

shows an example shader creation logic in Lua

::

   nsi.Create( "lambert", "shader" );
   nsi.SetAttribute(
       "lambert",
       {name="filename", data="lambert_material.oso"},
       {name="Kd", data=.55},
       {name="albedo", data={1, 0.5, 0.3}, type=nsi.TypeColor} );

   nsi.Create( "ggx", "shader" );
   nsi.SetAttribute(
       "ggx",
       {
           {name="filename", data="ggx_material.oso"},
           {name="anisotropy_direction", data={0.13, 0 ,1}, type=nsi.TypeVector}
       } );

API calls
~~~~~~~~~

All useful (in a scripting context) nsi functions are provided and are
listed in . There is also a ``nsi.utilities`` class which, for now, only
contains a method to print errors. See .

.. table:: nsi functions

   ====================== =====================
   **Lua Function**       **C equivalent**
   ====================== =====================
   nsi.SetAttribute       NSISetAttribute
   nsi.SetAttributeAtTime NSISetAttributeAtTime
   nsi.Create             NSICreate
   nsi.Delete             NSIDelete
   nsi.DeleteAttribute    NSIDeleteAttribute
   nsi.Connect            NSIConnect
   nsi.Disconnect         NSIDisconnect
   Evaluate               NSIEvaluate
   ====================== =====================

Function parameters format
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each single parameter is passed as a Lua table containing the following
key values:

-  name - contains the name of the parameter.

-  data - The actual parameter data. Either a value (integer, float or
   string) or an array.

-  type - specifies the type of the parameter. Possible values are shown
   in .

   .. table:: nsi types

      =============== ================
      **Lua Type**    **C equivalent**
      =============== ================
      nsi.TypeFloat   NSITypeFloat
      nsi.TypeInteger NSITypeInteger
      nsi.TypeString  NSITypeString
      nsi.TypeNormal  NSITypeNormal
      nsi.TypeVector  NSITypeVector
      nsi.TypePoint   NSITypePoint
      nsi.TypeMatrix  NSITypeMatrix
      =============== ================

-  arraylength - specifies the length of the array for each element.

      note — There is no count parameter in Lua since it can be obtained
      from the size of the provided data, its type and array length.

Here are some example of well formed parameters:

::

   --[[ strings, floats and integers do not need a 'type' specifier ]] --
   p1 = {name="shaderfilename", data="emitter"};
   p2 = {name="power", data=10.13};
   p3 = {name="toggle", data=1};

   --[[ All other types, including colors and points, need a
        type specified for disambiguation. ]]--
   p4 = {name="Cs", data={1, 0.9, 0.7}, type=nsi.TypeColor};

   --[[ An array of 2 colors ]] --
   p5 = {name="vertex_color", arraylength=2,
       data={1, 1, 1, 0, 0, 0}, type=nsi.TypeColor};

   --[[ Create a simple mesh and connect it root ]] --
   nsi.Create( "floor", "mesh" )
   nsi.SetAttribute( "floor",
       {name="nvertices", data=4},
       {name="P", type=nsi.TypePoint,
           data={-2, -1, -1, 2, -1, -1, 2, 0, -3, -2, 0, -3}} )
   nsi.Connect( "floor", "", ".root", "objects" )

.. _subsection:luaevaluation:

Evaluating a Lua script
~~~~~~~~~~~~~~~~~~~~~~~

Script evaluation is started using in C, nsi stream or even another Lua
script. Here is an example using nsi stream:

   ::

      Evaluate
          "filename" "string" 1 ["test.nsi.lua"]
          "type" "string" 1 ["lua"]

It is also possible to evaluate a Lua script *inline* using the
``script`` parameter. For example:

   ::

      Evaluate
          "script" "string" 1 ["nsi.Create(\"light\", \"shader\");"]
          "type" "string" 1 ["lua"]

Both “filename” and “script” can be specified to ``NSIEvaluate`` in one
go, in which case the inline script will be evaluated before the file
and both scripts will share the same nsi and Lua contexts. Any error
during script parsing or evaluation will be sent to nsi\ ’s error
handler. Note that all Lua scripts are run in a sandbox in which all Lua
system libraries are disabled. Some utilities, such as error reporting,
are available through the ``nsi.utilities`` class.

Passing parameters to a Lua script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All parameters passed to ``NSIEvaluate`` will appear in the
``nsi.scriptparameters`` table. For example, the following call:

   ::

      Evaluate
          "filename" "string" 1 ["test.lua"]
          "type" "string" 1 ["lua"]
          "userdata" "color[2]" 1 [1 0 1 2 3 4]

Will register a ``userdata`` entry in the ``nsi.scriptparameters``
table. So executing the following line in ``test.lua``:

   ::

      print( nsi.scriptparameters.userdata.data[5] );

Will print 3.0.

.. _subsection:luaerrors:

Reporting errors from a Lua script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``nsi.utilities.ReportError`` to send error messages to the error
handler defined in the current nsi context. For example:

   ::

      nsi.utilities.ReportError( nsi.ErrWarning, "Watch out!" );

The and are shown in .

.. table:: NSI error codes

   =================== ================
   **Lua Error Codes** **C equivalent**
   =================== ================
   nsi.ErrMessage      NSIErrMessage
   nsi.ErrWarning      NSIErrMessage
   nsi.ErrInfo         NSIErrInfo
   nsi.ErrError        NSIErrError
   =================== ================

The C++ API wrappers
--------------------

The ``nsi.hpp`` file provides C++ wrappers which are less tedious to use
than the low level C interface. All the functionality is inline so no
additional libraries are needed and there are no abi issues to consider.

Creating a context
~~~~~~~~~~~~~~~~~~

The core of these wrappers is the ``NSI::Context`` class. Its default
construction will require linking with the renderer.

::

   #include "nsi.hpp"

   NSI::Context nsi;

[dynamicapi] The ``nsi_dynamic.hpp`` file provides an alternate api
source which will load the renderer at runtime and thus requires no
direct linking.

::

   #include "nsi.hpp"
   #include "nsi_dynamic.hpp"

   NSI::DynamicAPI nsi_api;
   NSI::Context nsi(nsi_api);

In both cases, a new nsi context can then be created with the ``Begin``
method.

::

   nsi.Begin();

This will be bound to the ``NSI::Context`` object and released when the
object is deleted. It is also possible to bind the object to a handle
from the c api, in which case it will not be released unless the ``End``
method is explicitly called.

Argument passing
~~~~~~~~~~~~~~~~

The ``NSI::Context`` class has methods for all the other nsi calls. The
optional parameters of those can be set by several accessory classes and
given in many ways. The most basic is a single argument.

::

   nsi.SetAttribute("handle", NSI::FloatArg("fov", 45.0f));

It is also possible to provide static lists:

::

   nsi.SetAttribute("handle",(
       NSI::FloatArg("fov", 45.0f),
       NSI::DoubleArg("depthoffield.fstop", 4.0)
       ));

And finally a class supports dynamically building a list.

::

   NSI::ArgumentList args;
   args.Add(new NSI::FloatArg("fov", 45.0f));
   args.Add(new NSI::DoubleArg("depthoffield.fstop", 4.0));
   nsi.SetAttribute("handle", args);

The ``NSI::ArgumentList`` object will delete all the objects added to it
when it is deleted.

Argument classes
~~~~~~~~~~~~~~~~

To be continued …

.. _section:Python:

The Python API
--------------

The ``nsi.py`` file provides a python wrapper to the C interface. It is
compatible with both python 2.7 and python 3. An example of how to us it
is provided in ``python/examples/live_edit/live_edit.py``

.. _section:nsistream:

The interface stream
--------------------

It is important for a scene description api to be streamable. This
allows saving scene description into files, communicating scene state
between processes and provide extra flexibility when sending commands to
the renderer [1]_.

Instead of re-inventing the wheel, the authors have decided to use
exactly the same format as is used by the *RenderMan* Interface
Bytestream (rib). This has several advantages:

-  Well defined ascii and binary formats.

-  The ascii format is human readable and easy to understand.

-  Easy to integrate into existing renderers (writers and readers
   already available).

Note that since Lua is part of the api, one can use Lua files for api
streaming [2]_. [section:rib]

.. _section:dllprocedurals:

Dynamic library procedurals
---------------------------

and nodes can execute code loaded from a dynamically loaded library that
defines a procedural. Executing the procedural is expected to result in
a series of nsi api calls that contribute to the description of the
scene. For example, a procedural could read a part of the scene stored
in a different file format and translate it directly into nsi calls.

This section describes how to use the definitions from the
``nsi_procedural.h`` header to write such a library in C or C++.
However, the process of compiling and linking it is specific to each
operating system and out of the scope of this manual.

Entry point
~~~~~~~~~~~

The renderer expects a dynamic library procedural to contain a
``NSIProceduralLoad`` symbol, which is an entry point for the library’s
main function:

::

   struct NSIProcedural_t* NSIProceduralLoad(
       NSIContext_t ctx,
       NSIReport_t report,
       const char* nsi_library_path,
       const char* renderer_version);

It will be called only once per render and has the responsibility of
initializing the library and returning a description of the functions
implemented by the procedural. However, it is not meant to generate nsi
calls.

It returns a pointer to an descriptor object of type
``struct NSIProcedural_t`` (see ).

``NSIProceduralLoad`` receives the following parameters:

The nsi context into which the procedural is being loaded.

A function that can be used to display informational, warning or error
messages through the renderer.

The path to the nsi implementation that is loading the procedural. This
allows the procedural to explicitly make its nsi api calls through the
same implementation (for example, by using defined in
``nsi_dynamic.hpp``). It’s usually not required if only one
implementation of nsi is installed on the system.

A character string describing the current version of the renderer.

Procedural description
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   typedef void (*NSIProceduralUnload_t)(
       NSIContext_t ctx,
       NSIReport_t report,
       struct NSIProcedural_t* proc);

   typedef void (*NSIProceduralExecute_t)(
       NSIContext_t ctx,
       NSIReport_t report,
       struct NSIProcedural_t* proc,
       int nparams,
       const struct NSIParam_t* params);

   struct NSIProcedural_t
   {
       unsigned nsi_version;
       NSIProceduralUnload_t unload;
       NSIProceduralExecute_t execute;
   };

The structure returned by ``NSIProceduralLoad`` contains information
needed by the renderer to use the procedural. Note that its allocation
is managed entirely from within the procedural and it will never be
copied or modified by the renderer. This means that it’s possible for a
procedural to extend the structure (by over-allocating memory or
subclassing, for example) in order to store any extra information that
it might need later.

The ``nsi_version`` member must be set to ``NSI_VERSION`` (defined in
``nsi.h``), so the renderer is able to determine which version of nsi
was used when compiling the procedural.

The function pointers types used in the definition are :

-  ``NSIProceduralUnload_t`` is a function that cleans-up after the last
   execution of the procedural. This is the dual of
   ``NSIProceduralLoad``. In addition to parameters ``ctx`` and
   ``report``, also received by ``NSIProceduralLoad``, it receives the
   description of the procedural returned by ``NSIProceduralLoad``.

-  ``NSIProceduralExecute_t`` is a function that contributes to the
   description of the scene by generating nsi api calls. Since
   ``NSIProceduralExecute_t`` might be called multiple times in the same
   render, it’s important that it uses the context ``ctx`` it receives
   as a parameter to make its nsi calls, and not the context previously
   received by ``NSIProceduralLoad``. It also receives any extra
   parameters sent to , or any extra attributes set on a node. They are
   stored in the ``params`` array (of length ``nparams``).
   ``NSIParam_t`` is described in .

Error reporting
~~~~~~~~~~~~~~~

All functions of the procedural called by nsi receive a parameter of
type ``NSIReport_t``. It’s a pointer to a function which should be used
by the procedural to report errors or display any informational message.

.. code-block:: c

   typedef void (*NSIReport_t)(
       NSIContext_t ctx, int level, const char* message);

It receives the current context, the error level (as described in ) and
the message to be displayed. This information will be forwarded to any
error handler attached to the current context, along with other regular
renderer messages. Using this, instead of a custom error reporting
mechanism, will benefit the user by ensuring that all messages are
displayed in a consistent manner.

Preprocessor macros
~~~~~~~~~~~~~~~~~~~

Some convenient C preprocessor macros are also defined in
``nsi_procedural.h`` :

-  ::

      NSI_PROCEDURAL_UNLOAD(name)

   and

   ::

      NSI_PROCEDURAL_EXECUTE(name)

   declare functions of the specified name that match
   ``NSIProceduralUnload_t`` and ``NSIProceduralExecute_t``,
   respectively.

-  ::

      NSI_PROCEDURAL_LOAD

   declares a ``NSIProceduralLoad`` function.

-  ::

      NSI_PROCEDURAL_INIT(proc, unload_fct, execute_fct)

   initializes a ``NSIProcedural_t`` (passed as ``proc``) using the
   addresses of the procedural’s main functions. It also initializes
   ``proc.nsi_version``.

So, a skeletal dynamic library procedural (that does nothing) could be
implemented as in .

Please note, however, that the ``proc`` static variable in this example
contains only constant values, which allows it to be allocated as a
static variable. In a more complex implementation, it could have been
over-allocated (or subclassed, in C++) to hold additional, variable
data [3]_. In that case, it would have been better to allocate the
descriptor dynamically – and release it in ``NSI_PROCEDURAL_UNLOAD`` –
so the procedural could be loaded independently from multiple parallel
renders, each using its own instance of the ``NSIProcedural_t``
descriptor.

::

   #include "nsi_procedural.h"

   NSI_PROCEDURAL_UNLOAD(min_unload)
   {
   }

   NSI_PROCEDURAL_EXECUTE(min_execute)
   {
   }

   NSI_PROCEDURAL_LOAD
   {
       static struct NSIProcedural_t proc;
       NSI_PROCEDURAL_INIT(proc, min_unload, min_execute);
       return &proc;
   }

.. _chapter:Nodes: