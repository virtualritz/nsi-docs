.. include:: definitions.rst

.. index::
    C API

.. _section:capi:

The C API
---------

This section describes the C implementation of the |nsi|, as provided
in the :doc:`nsi.h` file. This will also be a reference for the
interface in other languages as all concepts are the same.

.. code-block:: c

    #define NSI_VERSION 1

The ``NSI_VERSION`` macro exists in case there is a need at some point
to break source compatibility of the C interface.

.. _CAPI:dotroot:

.. code-block:: c

    #define NSI_SCENE_ROOT ".root"

The ``NSI_SCENE_ROOT`` macro defines the handle of the
:ref:`root node<node:root>`.

.. _CAPI:dotall:

.. code-block:: c

    #define NSI_ALL_NODES ".all"

The ``NSI_ALL_NODES`` macro defines a special handle to refer to all
nodes in some contexts, such as when
:ref:`removing connections<CAPI:nsiconnect>`.

.. index::
    context handling

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

These two functions control creation and destruction of a |nsi| context,
identified by a handle of type ``NSIContext_t``.

A context must be given explicitly when calling all other functions of
the interface. Contexts may be used in multiple threads at once. The
``NSIContext_t`` is a convenience typedef and is defined as:

.. code-block:: c

    typedef int NSIContext_t;

If ``NSIBegin`` fails for some reason, it returns ``NSI_BAD_CONTEXT``
which is defined in :doc:`nsi.h`:

.. code-block:: c

    #define NSI_BAD_CONTEXT ((NSIContext_t)0)

:ref:`Optional parameters<CAPI:optionalparameters>` may be given to
``NSIBegin()`` to control the creation of the context:

.. table:: NSIBegin() optional parameters
    :widths: 3 1 2 4

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``type``               | string   | Sets the type of context to create. The possible   |
    |                        |          | types are:                                         |
    |                        |          +---------------+------------------------------------+
    |                        |          | ``render``    | Execute the calls directly in the  |
    |                        |          |               | renderer. This is the **default**. |
    |                        |          +---------------+------------------------------------+
    |                        |          | ``apistream`` | To write the interface calls to a  |
    |                        |          |               | stream, for later execution.       |
    |                        |          |               | The target for writing the stream  |
    |                        |          |               | must be specified in another       |
    |                        |          |               | parameter.                         |
    +------------------------+----------+---------------+------------------------------------+
    | ``stream.filename``    | string   | The file to which the stream is to be output, if   |
    |                        |          | the context type is ``apistream``.                 |
    |                        |          | Specify ``stdout`` to write to standard output and |
    |                        |          | ``stderr`` to write to standard error.             |
    +------------------------+----------+----------------------------------------------------+
    | ``stream.format``      | string   | The format of the command stream to write.         |
    |                        |          | Possible formats are:                              |
    |                        |          +---------------+------------------------------------+
    |                        |          | ``nsi``       | Produces an :ref:`nsi              |
    |                        |          |               | stream<section:nsistream>`         |
    |                        |          +---------------+------------------------------------+
    |                        |          | ``binarynsi`` | Produces a binary encoded          |
    |                        |          |               | :ref:`nsi                          |
    |                        |          |               | stream<section:nsistream>`         |
    +------------------------+----------+---------------+------------------------------------+
    | ``stream.compression`` | string   | The type of compression to apply to the written    |
    |                        |          | command stream.                                    |
    +------------------------+----------+----------------------------------------------------+
    | ``errorhandler``       | pointer  | A function which is to be called by the renderer   |
    |                        |          | to report errors. The default handler will print   |
    |                        |          | messages to the console.                           |
    +------------------------+----------+----------------------------------------------------+
    | ``errorhandler.data``  | pointer  | The ``userdata`` parameter of the :ref:`error      |
    |                        |          | reporting function<CAPI:errorcallback>`.           |
    +------------------------+----------+----------------------------------------------------+
    | ``executeprocedurals`` | string   | A list of procedural types that should be executed |
    |                        |          | immediately when a call to or a procedural node is |
    |                        |          | encountered and ``NSIBegin()``'s output ``type``   |
    |                        |          | is ``apistream``. This will replace any matching   |
    |                        |          | call to ``NSIEvaluate()`` with the results of the  |
    |                        |          | procedural's execution.                            |
    +------------------------+----------+----------------------------------------------------+

.. _CAPI:optionalparameters:

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

This structure is used to pass variable parameter lists through the
C |nbsp| interface. Most functions accept an array of the structure in
a ``params`` parameter along with its length in a ``nparams``
parameter.

The meaning of these two parameters will not be documented for every
function. Instead, they will document the parameters which can be given
in the array.

The ``name`` member is a C string which gives the parameter's name.

The ``type`` member identifies the parameter's type, using one of the
following constants:

.. table:: types of optional parameters
    :widths: 2 8

    +-------------------------+----------------------------------------+
    | ``NSITypeFloat``        | Single 32-bit floating point value.    |
    +-------------------------+----------------------------------------+
    | ``NSITypeDouble``       | Single 64-bit floating point value.    |
    +-------------------------+----------------------------------------+
    | ``NSITypeInteger``      | Single 32-bit integer value.           |
    +-------------------------+----------------------------------------+
    | ``NSITypeString``       | String value, given as a pointer to a  |
    |                         | C |nbsp| string.                       |
    +-------------------------+----------------------------------------+
    | ``NSITypeColor``        | Color, given as three 32-bit floating  |
    |                         | point values.                          |
    +-------------------------+----------------------------------------+
    | ``NSITypePoint``        | Point, given as three 32-bit floating  |
    |                         | point values.                          |
    +-------------------------+----------------------------------------+
    | ``NSITypeVector``       | Vector, given as three 32-bit floating |
    |                         | point values.                          |
    +-------------------------+----------------------------------------+
    | ``NSITypeNormal``       | Normal vector, given as three 32-bit   |
    |                         | floating point values.                 |
    +-------------------------+----------------------------------------+
    | ``NSITypeMatrix``       | Transformation matrix, given as 16     |
    |                         | 32-bit floating point values.          |
    +-------------------------+----------------------------------------+
    | ``NSITypeDoubleMatrix`` | Transformation matrix, given as 16     |
    |                         | 64-bit floating point values.          |
    +-------------------------+----------------------------------------+
    | ``NSITypePointer``      | C |nbsp| pointer.                      |
    +-------------------------+----------------------------------------+

Array types are specified by setting the bit defined by the
``NSIParamIsArray`` constant in the ``flags`` member and the length of
the array in the ``arraylength`` member.

.. Tip::
    It helps to view ``arraylength`` as a part of the data type.

The ``count`` member gives the number of data items given as the value
of the parameter.

The ``data`` member is a pointer to the data for the parameter.

The ``flags`` member is a bit field with a number of constants defined
to communicate more information about the parameter:

.. _CAPI:paramflags:

.. table:: flags for optional parameters
    :widths: 2 8

    +-------------------------------+----------------------------------+
    | ``NSIParamIsArray``           | to specify that the parameter is |
    |                               | an array type, as explained      |
    |                               | previously.                      |
    +-------------------------------+----------------------------------+
    | ``NSIParamPerFace``           | to specify that the parameter    |
    |                               | has different values for every   |
    |                               | face of a geometric primitive,   |
    |                               | where this might be ambiguous.   |
    +-------------------------------+----------------------------------+
    | ``NSIParamPerVertex``         | Specify that the parameter has   |
    |                               | different values for every       |
    |                               | vertex of a geometric primitive, |
    |                               | where this might be ambiguous.   |
    +-------------------------------+----------------------------------+
    | ``NSIParamInterpolateLinear`` | Specify that the parameter is to |
    |                               | be interpolated linearly instead |
    |                               | of using some other default      |
    |                               | method.                          |
    +-------------------------------+----------------------------------+

.. Tip::
    ``NSIParamPerFace`` or ``NSIParamPerVertex`` are only strictly
    needed in rare circumstances when a geometric primitive's number of
    vertices matches the number of faces. The most simple case is a
    tetrahedral mesh which has exactly four vertices and also four
    faces.

Indirect lookup of parameters is achieved by giving an integer parameter
of the same name, with the ``.indices`` suffix added. This is read to
know which values of the other parameter to use.

.. index::
    P.indices example
    indexing example

.. code-block:: shell
   :caption: A subdivision mesh using ``P.indices`` to reference the ``P`` parameter
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

.. index::
    NSICreate()
    creating nodes
    node creation

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

| ``context``
|   The context returned by ``NSIBegin()``. See
    :ref:`context handling<CAPI:contexthandling>`.

| ``handle``
|   A node handle. This string will uniquely identify the node in the
    scene.

    If the supplied handle matches an existing node, the function does
    nothing if all other parameters match the call which created that
    node.
    Otherwise, it emits an error. Note that handles need only be unique
    within a given interface context. It is acceptable to reuse the same
    handle inside different contexts. The ``NSIHandle_t`` typedef is
    defined in :doc:`nsi.h`:

    .. code-block:: c

       typedef const char* NSIHandle_t;

| ``type``
|   The type of :ref:`node<chapter:nodes>` to create.

| ``nparams``, ``params``
    This pair describes a list of optional parameters. *There are no
    optional parameters defined as of now*. The ``NSIParam_t`` type is
    described in :ref:`this section<CAPI:optionalparameters>`.

--------------

.. index::
    NSIDelete()
    deleting nodes
    node deletion

.. code-block:: c

   void NSIDelete(
       NSIContext_t ctx,
       NSIHandle_t handle,
       int nparams,
       const NSIParam_t *params
   )

This function deletes a node from the scene. All connections to and from
the node are also deleted. Note that it is not possible to delete the
:ref:`root<node:root>` or the :ref:`global<node:global>` node.
Its parameters are:

| ``context``
|   The context returned by ``NSIBegin()``. See
    :ref:`context handling<CAPI:contexthandling>`.

| ``handle``
|   A node handle. It identifies the node to be deleted.

It accepts the following optional parameters:

.. index::
    recursive node deletetion

.. table:: NSIDelete() optional parameters
    :widths: 3 1 2 4

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``recursive``          | int      | Specifies whether deletion is recursive. By        |
    |                        |          | default, only the specified node is deleted.       |
    |                        |          | If a value of 1 is given, then nodes which connect |
    |                        |          | to the specified node are recursively removed,     |
    |                        |          | unless they also have connections which do not     |
    |                        |          | eventually lead to the specified node. This        |
    |                        |          | allows, for example, deletion of an entire shader  |
    |                        |          | network in a single call.                          |
    +------------------------+----------+---------------+------------------------------------+

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

: _CAPI:nsisetattributeattime:

.. code-block:: c

   void NSISetAttributeAtTime(
       NSIContext_t ctx,
       NSIHandle_t object,
       double time,
       int nparams,
       const NSIParam_t *params
   )

This function sets time-varying attributes (i.e. motion blurred). The
``time`` parameter specifies at which time the attribute is being
defined. It is not required to set time-varying attributes in any
particular order. In most uses, attributes that are motion blurred must
have the same specification throughout the time range. A notable
exception is the ``P`` attribute on which can be of different size for
each time step because of appearing or disappearing particles. Setting
an attribute using this function replaces any value previously set by
``NSISetAttribute()``.

--------------

.. code-block:: c

   void NSIDeleteAttribute(
       NSIContext_t ctx,
       NSIHandle_t object,
       const char *name
   )

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

.. code-block:: c

   void NSIConnect(
       NSIContext_t ctx,
       NSIHandle_t from,
       const char *from_attr,
       NSIHandle_t to,
       const char *to_attr,
       int nparams,
       const NSIParam_t *params
   )

.. code-block:: c

   void NSIDisconnect(
       NSIContext_t ctx,
       NSIHandle_t from,
       const char *from_attr,
       NSIHandle_t to,
       const char *to_attr
   )

These two functions respectively create or remove a connection between
two elements. It is not an error to create a connection which already
exists or to remove a connection which does not exist but the nodes on
which the connection is performed must exist. The parameters are:

.. table:: NSIConnect()/NSIDisconnect() optional parameters
    :widths: 3 1 6

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``from``               | string   | The handle of the node from which the connection   |
    |                        |          | is made.                                           |
    +------------------------+----------+----------------------------------------------------+
    | ``from attr``          | string   | The name of the attribute from which the           |
    |                        |          | connection is made. If this is an empty string     |
    | ``from.attribute`` (!) |          | then the connection is made from the node instead  |
    |                        |          | of from a specific attribute of the node.          |
    +------------------------+----------+----------------------------------------------------+
    | ``to``                 | string   | The handle of the node to which the connection is  |
    |                        |          | made.                                              |
    +------------------------+----------+----------------------------------------------------+
    | ``to``                 | string   | The name of the attribute to which the connection  |
    |                        |          | is made. If this is an empty string then the       |
    | ``to.attribute`` (!)   |          | connection is made to the node instead of to a     |
    |                        |          | specific attribute of the node.                    |
    +------------------------+----------+----------------------------------------------------+

``NSIConnect()`` accepts additional optional parameters. Refer to the
:ref:`guidelines on inter-object visibility<section:lightlinking>` for
more information about their utility.

With ``NSIDisconnect()``, the handle for either node may be the special
value :ref:`'.all'<CAPI:dotall>` . This will remove all connections
which match the other three parameters. For example, to disconnect
everything from :ref:`the scene's root<node:root>`:

.. code-block:: c
   :linenos:

   NSIDisconnect( NSI_ALL_NODES, "", NSI_SCENE_ROOT, "objects" );

.. _CAPI:nsievaluate:

.. index::
    archive
    evaluating Lua scripts
    inline archive

Evaluating procedurals
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   void NSIEvaluate(
       NSIContext_t ctx,
       int nparams,
       const NSIParam_t *params
   )

This function includes a block of interface calls from an external
source into the current scene. It blends together the concepts of a
straight file include, commonly known as an archive, with that of
procedural include which is traditionally a compiled executable. Both
are really the same idea expressed in a different language (note that
for delayed procedural evaluation one should use the :ref:`procedural
node<node:procedural>`).

The |nsi| adds a third option which sits in-between—Lua scripts (). They
are much more powerful than a simple included file yet they are also
much easier to generate as they do not require compilation. It is, for
example, very realistic to export a whole new script for every frame of
an animation. It could also be done for every character in a frame. This
gives great flexibility in how components of a scene are put together.

The ability to load |nsi| command straight from memory is also provided.

The optional parameters accepted by this function are:

.. table:: NSIEvaluate() optional parameters
    :widths: 3 1 2 4

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``type``               | string   | The type of file which will generate the interface |
    |                        |          | calls. This can be one of:                         |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``apistream``      | Read in an :ref:`nsi          |
    |                        |          |                    | stream<section:nsistream>`.   |
    |                        |          |                    | This requires either          |
    |                        |          |                    | ``stream.filename`` or        |
    |                        |          |                    | ``buffer``/``size``           |
    |                        |          |                    | parameters to be specified    |
    |                        |          |                    | too.                          |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``lua``            | Execute a                     |
    |                        |          |                    | :ref:`Lua<section:Lua>`       |
    |                        |          |                    | script, either from file or   |
    |                        |          |                    | inline. See also              |
    |                        |          |                    | :ref:`how to evaluate a Lua   |
    |                        |          |                    | script<luaapi:evaluation>`.   |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``dynamiclibrary`` | Execute native compiled code  |
    |                        |          |                    | in a loadable library. See    |
    |                        |          |                    | :ref:`dynamic library         |
    |                        |          |                    | procedurals                   |
    |                        |          |                    | <section:procedurals>` for    |
    |                        |          |                    | an implementation example.    |
    +------------------------+----------+--------------------+-------------------------------+
    | ``stream.filename``    | string   | The file from which to read the interface stream.  |
    +------------------------+----------+----------------------------------------------------+
    | ``script``             | string   | A valid :ref:`Lua<section:Lua>` script to execute  |
    |                        |          | when ``type`` is set to ``lua``.                   |
    +------------------------+----------+----------------------------------------------------+
    | ``buffer``             | pointer  | These two parameters define a memory block that    |
    |                        |          | contains |nsi| commands to execute.                |
    | ``size``               | int      |                                                    |
    +------------------------+----------+----------------------------------------------------+
    | ``backgroundload``     | int      | If this is nonzero, the object may be loaded       |
    |                        |          | in a separate thread, at some later time.          |
    |                        |          | This requires that further interface calls not     |
    |                        |          | directly reference objects defined in the included |
    |                        |          | file. The only guarantee is that the the file will |
    |                        |          | be loaded before rendering begins.                 |
    +------------------------+----------+----------------------------------------------------+

.. _CAPI:errorcallback:

.. index::
    error reporting
    enum error levels

Error reporting
~~~~~~~~~~~~~~~

.. code-block:: c

   enum NSIErrorLevel
   {
       NSIErrMessage = 0,
       NSIErrInfo = 1,
       NSIErrWarning = 2,
       NSIErrError = 3
   }

.. code-block:: c

   typedef void (*NSIErrorHandler_t)(
       void *userdata, int level, int code, const char *message
   )

This defines the type of the error handler callback given to the
``NSIBegin()`` function. When it is called, the ``level`` parameter is one
of the values defined by the ``NSIErrorLevel`` enum. The ``code``
parameter is a numeric identifier for the error message, or 0 when
irrelevant. The ``message`` parameter is the text of the message.

The text of the message will not contain the numeric identifier nor any
reference to the error level. It is usually desirable for the error
handler to present these values together with the message. The
identifier exists to provide easy filtering of messages.

The intended meaning of the error levels is as follows:

.. table:: error levels
    :widths: 2 8

    +-------------------------+---------------------------------------------------+
    | ``NSIErrMessage``       | For general messages, such as may be produced by  |
    |                         | ``printf()`` in shaders. The default error        |
    |                         | handler will print this type of messages without  |
    |                         | an eol terminator as it’s the duty of the caller  |
    |                         | to format the message.                            |
    +-------------------------+---------------------------------------------------+
    | ``NSIErrInfo``          | For messages which give specific information.     |
    |                         | These might simply inform about the state of the  |
    |                         | renderer, files being read, settings being used   |
    |                         | and so on.                                        |
    +-------------------------+---------------------------------------------------+
    | ``NSIErrWarning``       | For messages warning about potential problems.    |
    |                         | These will generally not prevent producing images |
    |                         | and may not require any corrective action. They   |
    |                         | can be seen as suggestions of what to look into   |
    |                         | if the output is broken but no actual error is    |
    |                         | produced.                                         |
    +-------------------------+---------------------------------------------------+
    | ``NSIErrError``         | For error messages. These are for problems which  |
    |                         | will usually break the output and need to be      |
    |                         | fixed.                                            |
    +-------------------------+---------------------------------------------------+

.. _section:rendering:

.. index::
    NSIRenderControl()
    controlling rendering
    rendering
    starting a render
    suspending a render
    pausing a render
    stopping a render
    resuming a render
    terminating a render
    synchronizing a render
    interactive rendering

Rendering
~~~~~~~~~

.. code-block:: c

    void NSIRenderControl(
        NSIContext_t ctx,
        int nparams,
        const NSIParam_t *params
    )

This function is the only control function of the API. It is responsible
of starting, suspending and stopping the render. It also allows for
synchronizing the render with interactive calls that might have been
issued. The function accepts :

.. table:: NSIRenderControl() optional parameters
    :widths: 3 1 2 4

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``action``             | string   | Specifies the operation to be performed, which     |
    |                        |          | should be one of the following:                    |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``start``          | This starts rendering the     |
    |                        |          |                    | scene in the provided         |
    |                        |          |                    | context. The render starts in |
    |                        |          |                    | parallel and the control flow |
    |                        |          |                    | is not blocked.               |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``wait``           | Wait for a render to finish.  |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``synchronize``    | For an interactive render,    |
    |                        |          |                    | apply all the buffered calls  |
    |                        |          |                    | to scene’s state.             |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``suspend``        | Suspends render in the        |
    |                        |          |                    | provided context.             |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``resume``         | Resumes a previously          |
    |                        |          |                    | suspended render.             |
    |                        |          +--------------------+-------------------------------+
    |                        |          | ``stop``           | Stops rendering in the        |
    |                        |          |                    | provided context without      |
    |                        |          |                    | destroying the scene.         |
    +------------------------+----------+--------------------+-------------------------------+
    | ``progressive``        | integer  | If set to ``1``, render the image in a progressive |
    |                        |          | fashion.                                           |
    +------------------------+----------+----------------------------------------------------+
    | ``interactive``        | integer  | .. _section:rendering:interactive:                 |
    |                        |          |                                                    |
    |                        |          | If set to ``1``, the renderer will accept commands |
    |                        |          | to edit scene’s state while rendering.             |
    |                        |          | The difference with a normal render is that the    |
    |                        |          | render task will not exit even if rendering is     |
    |                        |          | finished. Interactive renders are by definition    |
    |                        |          | progressive.                                       |
    +------------------------+----------+----------------------------------------------------+
    | ``frame``              |          | Specifies the frame number of this render.         |
    +------------------------+----------+----------------------------------------------------+
    | ``stoppedcallback``    | pointer  | A pointer to a user function that should be        |
    |                        |          | called on rendering status changes. This function  |
    | ``callback`` (!)       |          | must have no return value and accept a pointer     |
    |                        |          | argument, a |nsi| context argument and an integer  |
    |                        |          | argument:                                          |
    |                        |          |                                                    |
    |                        |          | .. code-block:: c                                  |
    |                        |          |                                                    |
    |                        |          |     void StoppedCallback(                          |
    |                        |          |         void* stoppedcallbackdata,                 |
    |                        |          |         NSIContext_t ctx,                          |
    |                        |          |         int status                                 |
    |                        |          |     )                                              |
    |                        |          |                                                    |
    |                        |          | The third parameter is an integer which can take   |
    |                        |          | the following values:                              |
    |                        |          |                                                    |
    |                        |          | *  ``NSIRenderCompleted`` indicates that           |
    |                        |          |    rendering has completed normally.               |
    |                        |          |                                                    |
    |                        |          | *  ``NSIRenderAborted`` indicates that rendering   |
    |                        |          |    was interrupted before completion.              |
    |                        |          |                                                    |
    |                        |          | *  ``NSIRenderSynchronized`` indicates that an     |
    |                        |          |    interactive render has produced an image which  |
    |                        |          |    reflects all changes to the scene.              |
    |                        |          |                                                    |
    |                        |          | *  ``NSIRenderRestarted`` indicates that an        |
    |                        |          |    interactive render has received new changes to  |
    |                        |          |    the scene and no longer has an up to date       |
    |                        |          |    image.                                          |
    +------------------------+----------+----------------------------------------------------+
    | callback.data          | pointer  | A pointer that will be passed back to the          |
    |                        |          | ``stoppedcallback`` function.                      |
    +------------------------+----------+----------------------------------------------------+