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
nodes in some contexts, such as
:ref:`removing connections<CAPI:nsiconnect>`.

.. _CAPI:dotallattrib:

.. code-block:: c

    #define NSI_ALL_ATTRIBUTES ".all"

The ``NSI_ALL_ATTRIBUTES`` macro defines a special handle to refer to
all attributes in some contexts, such as
:ref:`removing connections<CAPI:nsiconnect>`.


.. index::
    context handling

.. _CAPI:contexthandling:

Context Handling
~~~~~~~~~~~~~~~~

.. code-block:: c

    NSIContext_t NSIBegin(
       int n_args,
       const NSIArg_t *args
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

:ref:`Optional arguments<CAPI:optionalarguments>` may be given to
``NSIBegin()`` to control the creation of the context:

.. table:: NSIBegin() optional arguments
    :widths: 3 1 2 4

    +----------------------------+----------+------------------------------------------------+
    | **Name**                   | **Type** | **Description/Values**                         |
    +============================+==========+================================================+
    | ``type``                   | string   | Sets the type of context to create. The        |
    |                            |          | possibletypes are:                             |
    |                            |          +---------------+--------------------------------+
    |                            |          | ``render``    | Execute the calls directly in  |
    |                            |          |               | the renderer. This is the      |
    |                            |          |               | **default**.                   |
    |                            |          +---------------+--------------------------------+
    |                            |          | ``apistream`` | To write the interface calls   |
    |                            |          |               | to a  stream, for later        |
    |                            |          |               | execution.                     |
    |                            |          |               | The target for writing the     |
    |                            |          |               | stream must be specified in    |
    |                            |          |               | another argument.              |
    +----------------------------+----------+---------------+--------------------------------+
    | ``streamfilename``         | string   | The file to which the stream is to be output,  |
    |                            |          | if the context type is ``apistream``.          |
    | ``stream.filename`` (!)    |          | Specify ``stdout`` to write to standard output |
    |                            |          | and``stderr`` to write to standard error.      |
    +----------------------------+----------+------------------------------------------------+
    | ``streamformat``           | string   | The format of the command stream to write.     |
    |                            |          | Possible formats are:                          |
    | ``stream.format`` (!)      |          +---------------+--------------------------------+
    |                            |          | ``nsi``       | Produces an :ref:`nsi          |
    |                            |          |               | stream<section:nsistream>`     |
    |                            |          +---------------+--------------------------------+
    |                            |          | ``binarynsi`` | Produces a binary encoded      |
    |                            |          |               | :ref:`nsi                      |
    |                            |          |               | stream<section:nsistream>`     |
    +----------------------------+----------+---------------+--------------------------------+
    | ``stream.compression``     | string   | The type of compression to apply to the        |
    |                            |          | written command stream.                        |
    | ``stream.compression`` (!) |          |                                                |
    +----------------------------+----------+------------------------------------------------+
    | ``streampathreplacement``  | int      | Use ``0`` to disable replacement of path       |
    |                            |          | prefixes by references to environment          |
    | ``stream.path.replace``    |          | variables which begin with ``NSI_PATH_`` in an |
    |                            |          | |nsi| stream.                                  |
    |                            |          | This should generally be left enabled to ease  |
    |                            |          | creation of files which can be moved between   |
    |                            |          | systems.                                       |
    +----------------------------+----------+------------------------------------------------+
    | ``errorhandler``           | pointer  | A function which is to be called by the        |
    |                            |          | renderer to report errors. The default handler |
    |                            |          | will print messages to the console.            |
    +----------------------------+----------+------------------------------------------------+
    | ``errorhandler.data``      | pointer  | The ``userdata`` argument of the :ref:`error   |
    |                            |          | reporting function<CAPI:errorcallback>`.       |
    +----------------------------+----------+------------------------------------------------+
    | ``executeprocedurals``     | string   | A list of procedural types that should be      |
    |                            |          | executed immediately when a call to            |
    | ``evaluate.replace``  (!)  |          | :ref:`NSIEvaluate() <CAPI:nsievaluate>` or a   |
    |                            |          | procedural node is encountered and             |
    |                            |          | ``NSIBegin()``'s output ``type`` is            |
    |                            |          | ``apistream``. This will replace any matching  |
    |                            |          | call to ``NSIEvaluate()`` with the results of  |
    |                            |          | the procedural's execution.                    |
    +----------------------------+----------+------------------------------------------------+

Arguments vs. Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~

Arguments are what a user specifies when calling a function of the API.
Each function takes extra, optional arguments.

Attributes are properties of nodes and are only set *through* the
aforementioed optional arguments using the ``NSISetAttribute()`` and
``NSISetAttributeAtTime()`` functions.

Optional Arguments
==================
Any API call can take extra arguments. These are always optional.
What this means the call can do work without the user specifying these
arguments.

Nodes are special as they have mandatory extra **attributes** that are
set *after* the node is created inside the API but which must be set
*before* the geometry or concept the node represents can actually be
created in the scene.

These attributes are passed as extra arguments to the
``NSISetAttribute()`` and ``NSISetAttributeAtTime()`` functions.

.. Note::
    Nodes can also take extra **arguments** when they are created.
    These optional arguments are only meant to add information needed
    to create the node that a particular implementation may need.

    **As of this writing there is no implementation that has any such
    optional arguments on the** ``NSICreate()`` **function.** The
    possibility to specify them is solely there to make the API future
    proof.

.. Caution::
    Nodes do *not* have optional arguments for now. **An optional
    argument on a node is not the same as an attribute on a node.**

Attributes – Describe the Node's Specifics
==========================================

Attributes are *only* for nodes. They must be set using the
``NSISetAttribute()`` or ``NSISetAttributeAtTime()`` functions.

They can **not** be set on the node when it is created with the
``NSICreate()`` function.

.. Caution::
    **Only nodes have attributes.** They are sent to the API
    via optional arguments on the API's attribute functions.

.. _CAPI:optionalarguments:

Passing Optional Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

    struct NSIArg_t
    {
        const char *name;
        const void *data;
        int type;
        int arraylength;
        size_t count;
        int flags;
    };

This structure is used to pass variable argument lists through the
C |nbsp| interface. Most functions accept an array of the structure in
a ``args`` argument along with its length in a ``n_args``
argument.

The meaning of these two arguments will not be documented for every
function. Instead, each function will document the arguments which can
be given in the array.

| ``name``
|   A C string which gives the argument's name.

| ``type``
|   Identifies the argument's type, using one of the following constants:

    .. table:: types of optional arguments
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
        | ``NSITypeMatrix``       | Transformation matrix, in row-major    |
        |                         | order, given as 16 32-bit floating     |
        |                         | point values.                          |
        +-------------------------+----------------------------------------+
        | ``NSITypeDoubleMatrix`` | Transformation matrix, in row-major    |
        |                         | order, given as 16 64-bit floating     |
        |                         | point values.                          |
        +-------------------------+----------------------------------------+
        | ``NSITypePointer``      | C |nbsp| pointer.                      |
        +-------------------------+----------------------------------------+

Tuple types are specified by setting the bit defined by the
``NSIArgIsArray`` constant in the ``flags`` member and the length of
the tuple in the ``arraylength`` member.

.. Tip::
    It helps to view ``arraylength`` as a part of the data type. The
    data type is a tuple with this length when ``NSIArgIsArray`` is set.

.. Note::
    If ``NSIArgIsArray`` is not set, ``arraylength`` is *ignored*.

    The ``NSIArgIsArray`` flag is neccessary to distinguish between
    arguments that happen to be of *length* 1 (set in the ``count``
    member) and tuples that have a *length* of 1 (set in the
    ``arraylength`` member) for the resp. argument.

    .. code-block:: shell
        :caption: A tuple argument of length 1 (and count 1) vs. a (non-tuple) argument of count 1

        "foo" "int[1]" 1 [42]  # The answer to the ultimate question – in an a (single) tuple
        "bar" "int" 1 13       # My favorite Friday

The ``count`` member gives the number of data items given as the value
of the argument.

The ``data`` member is a pointer to the data for the argument. This is
a pointer to a single value or a number values. Depending on ``type``,
``count`` and ``arraylength`` settings.

.. Note::
    When data is an array, the actual number of elements in the array
    is :math:`count\times arraylength\times n`. Where :math:`n` is
    specified implictly through the ``type`` member in the table above.

    For example, if the type is ``NSITypeColor`` (**3** values),
    ``NSIArgIsArray`` is set, ``arraylength`` is **2** and ``count`` is
    **4**, ``data`` is expected to contain **24** 32-bit floating point
    values (:math:`3\times2\times4`).


The ``flags`` member is a bit field with a number of constants used
to communicate more information about the argument:

.. _CAPI:argflags:

.. table:: flags for optional arguments
    :widths: 2 8

    +-------------------------------+----------------------------------+
    | ``NSIArgIsArray``             | to specify that the argument is  |
    |                               | an array type, as explained      |
    |                               | above.                           |
    +-------------------------------+----------------------------------+
    | ``NSIArgPerFace``             | to specify that the argument     |
    |                               | has different values for every   |
    |                               | face of a geometric primitive,   |
    |                               | where this might be ambiguous.   |
    +-------------------------------+----------------------------------+
    | ``NSIArgPerVertex``           | Specify that the argument has    |
    |                               | different values for every       |
    |                               | vertex of a geometric primitive, |
    |                               | where this might be ambiguous.   |
    +-------------------------------+----------------------------------+
    | ``NSIArgInterpolateLinear``   | Specify that the argument is to  |
    |                               | be interpolated linearly instead |
    |                               | of using some other, default     |
    |                               | method.                          |
    +-------------------------------+----------------------------------+

.. Note::
    ``NSIArgPerFace`` or ``NSIArgPerVertex`` are only strictly
    needed in rare circumstances when a geometric primitive's number of
    vertices matches the number of faces. The most simple case is a
    tetrahedral mesh which has exactly four vertices and also four
    faces.

Indirect lookup of arguments is achieved by giving an integer argument
of the same name, with the ``.indices`` suffix added. This is read to
know which values of the other argument to use.

.. index::
    P.indices example
    indexing example

.. code-block:: shell
   :caption: A subdivision mesh using ``P.indices`` to reference the ``P`` argument
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

Node Creation
~~~~~~~~~~~~~

.. code-block:: c

   void NSICreate(
       NSIContext_t context,
       NSIHandle_t handle,
       const char *type,
       int n_args,
       const NSIArg_t *args
   )

This function is used to create a new node. Its arguments are:

| ``context``
|   The context returned by ``NSIBegin()``. See
    :ref:`context handling<CAPI:contexthandling>`.

| ``handle``
|   A node handle. This string will uniquely identify the node in the
    scene.

    If the supplied handle matches an existing node, the function does
    nothing if all other arguments match the call which created that
    node.
    Otherwise, it emits an error. Note that handles need only be unique
    within a given interface context. It is acceptable to reuse the same
    handle inside different contexts. The ``NSIHandle_t`` typedef is
    defined in :doc:`nsi.h`:

    .. code-block:: c

       typedef const char* NSIHandle_t;

| ``type``
|   The type of :ref:`node<chapter:nodes>` to create.

| ``n_args``, ``args``
    This pair describes a list of optional arguments.
    The ``NSIArg_t`` type is
    described in :ref:`this section<CAPI:optionalarguments>`.

.. Caution::
    There are *no* optional arguments defined as of now.

--------------

.. _CAPI:nsidelete:

:ref:`NSIDeleteAttribute()`

.. index::
    NSIDelete()
    deleting nodes
    node deletion

.. code-block:: c

   void NSIDelete(
       NSIContext_t ctx,
       NSIHandle_t handle,
       int n_args,
       const NSIArg_t *args
   )

This function deletes a node from the scene. All connections to and from
the node are also deleted. Note that it is not possible to delete the
:ref:`root<node:root>` or the :ref:`global<node:global>` node.
Its arguments are:

| ``context``
|   The context returned by ``NSIBegin()``. See
    :ref:`context handling<CAPI:contexthandling>`.

| ``handle``
|   A node handle. It identifies the node to be deleted.

It accepts the following optional arguments:

.. index::
    recursive node deletetion

.. table:: NSIDelete() optional arguments
    :widths: 3 1 6

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``recursive``          | int      | Specifies whether deletion is recursive. By        |
    |                        |          | default, only the specified node is deleted.       |
    |                        |          | If a value of ``1`` is given, then nodes which     |
    |                        |          | connect to the specified node are recursively      |
    |                        |          | removed. Unless they meet one of the following     |
    |                        |          | conditions:                                        |
    |                        |          |                                                    |
    |                        |          | * They also have connections which do not          |
    |                        |          |   eventually lead to the specified node.           |
    |                        |          |                                                    |
    |                        |          | * Their connection to the deleted node was created |
    |                        |          |   with a ``strength`` greater than ``0``.          |
    |                        |          |                                                    |
    |                        |          | This  allows, for example, deletion of an entire   |
    |                        |          | shader network in a single call.                   |
    +------------------------+----------+---------------+------------------------------------+

Setting Attributes
~~~~~~~~~~~~~~~~~~

.. code-block:: c

   void NSISetAttribute(
       NSIContext_t ctx,
       NSIHandle_t object,
       int n_args,
       const NSIArg_t *args
   )

This functions sets attributes on a previously node. All :ref:`optional
arguments <CAPI:optionalarguments>` of the function become attributes
of the node.

On a :ref:`shader node<node:shader>`, this function is used to set the
implicitly defined shader arguments.

Setting an attribute using this function replaces any value previously
set by ``NSISetAttribute()`` or ``NSISetAttributeAtTime()``. To reset
an attribute to its default value, use :ref:`NSIDeleteAttribute()
<CAPI:nsidepeteattribute>`.

--------------

.. _CAPI:nsisetattributeattime:

.. code-block:: c

   void NSISetAttributeAtTime(
       NSIContext_t ctx,
       NSIHandle_t object,
       double time,
       int n_args,
       const NSIArg_t *args
   )

This function sets time-varying attributes (i.e. motion blurred). The
``time`` argument specifies at which time the attribute is being
defined.

It is not required to set time-varying attributes in any particular
order. In most uses, attributes that are motion blurred must have the
same specification throughout the time range.

A notable exception is the ``P`` attribute on :ref:`particles
<node:particles>` which can be of different size for each time step
because of appearing or disappearing particles. Setting an attribute
using this function replaces any value previously set by
``NSISetAttribute()``.

--------------

.. _CAPI:nsideleteattribute:

.. code-block:: c

   void NSIDeleteAttribute(
       NSIContext_t ctx,
       NSIHandle_t object,
       const char *name
   )

This function deletes any attribute with a name which matches the
``name`` argument on the specified object. There is no way to delete
an attribute only for a specific time value.

Deleting an attribute resets it to its default value.

For example, after deleting the ``transformationmatrix`` attribute on a
:ref:`transform node <node:transform>`, the transform will be an
identity. Deleting a previously set attribute on a :ref:`shader
node<node:shader>` node will default to whatever is declared inside the
shader.

.. _CAPI:nsiconnect:

Making Connections
~~~~~~~~~~~~~~~~~~

.. code-block:: c

   void NSIConnect(
       NSIContext_t ctx,
       NSIHandle_t from,
       const char *from_attr,
       NSIHandle_t to,
       const char *to_attr,
       int n_args,
       const NSIArg_t *args
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
which the connection is performed must exist. The arguments are:

| ``from``
|   The handle of the node from which the connection is made.

| ``from_attr``
|   The name of the attribute from which the connection is made. If this
    is an empty string then the connection is made from the node instead
    of from a specific attribute of the node.

| ``to``
|   The handle of the node to which the connection is made.                                              |

| ``to_attr``
|   The name of the attribute to which the connection is made. If this
    is an empty string then the connection is made to the node instead
    of to a specific attribute of the node.

``NSIConnect()`` accepts additional optional arguments.

.. table:: NSIConnect() optional arguments
    :widths: 3 1 6

    +------------------------+----------+----------------------------------------------------+
    | **Name**               | **Type** | **Description/Values**                             |
    +========================+==========+====================================================+
    | ``value``              |          | This can be used to change the value of a node's   |
    |                        |          | attribute in some contexts. Refer to               |
    |                        |          | :ref:`guidelines on inter-object                   |
    |                        |          | visibility<section:lightlinking>` for more         |
    |                        |          | information about the utility of this parameter.   |
    +------------------------+----------+----------------------------------------------------+
    | ``priority``           |          | When connecting attribute nodes, indicates in      |
    |                        |          | which order the nodes should be considered when    |
    |                        |          | evaluating the value of an attribute.              |
    +------------------------+----------+----------------------------------------------------+
    | ``strength``           | int (0)  | A connection with a strength greater than ``0``    |
    |                        |          | will *block* the progression of a recursive        |
    |                        |          | ``NSIDelete``.                                     |
    +------------------------+----------+----------------------------------------------------+


Refer to the
for
more information about their utility.

With ``NSIDisconnect()``, the handle for either node may be the special
value :ref:`'.all'<CAPI:dotall>` . This will remove all connections
which match the other three arguments. For example, to disconnect
everything from :ref:`the scene's root<node:root>`:

.. code-block:: c
   :linenos:

   NSIDisconnect( NSI_ALL_NODES, "", NSI_SCENE_ROOT, "objects" );

.. _CAPI:nsievaluate:

.. index::
    archive
    evaluating Lua scripts
    inline archive

Evaluating Procedurals
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   void NSIEvaluate(
       NSIContext_t ctx,
       int n_args,
       const NSIArg_t *args
   )

This function includes a block of interface calls from an external
source into the current scene. It blends together the concepts of a
straight file include, commonly known as an archive, with that of
procedural include which is traditionally a compiled executable. Both
are really the same idea expressed in a different language (note that
for delayed procedural evaluation one should use the :ref:`procedural
node<node:procedural>`).

The |nsi| adds a third option which sits in-between — :ref:`Lua scripts
<section:Lua>`. They are much more powerful than a simple included file
yet they are also much easier to generate as they do not require
compilation. It is, for example, very realistic to export a whole new
script for every frame of an animation. It could also be done for every
character in a frame. This gives great flexibility in how components of
a scene are put together.

The ability to load |nsi| commands straight from memory is also
provided.

The optional arguments accepted by this function are:

.. table:: NSIEvaluate() optional arguments
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
    |                        |          |                    | ``filename`` or               |
    |                        |          |                    | ``buffer``/``size``           |
    |                        |          |                    | arguments to be specified     |
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
    | ``filename``           | string   | The file from which to read the interface stream.  |
    |                        |          |                                                    |
    | ``stream.filename``    |          |                                                    |
    | (!)                    |          |                                                    |
    +------------------------+----------+----------------------------------------------------+
    | ``script``             | string   | A valid :ref:`Lua<section:Lua>` script to execute  |
    |                        |          | when ``type`` is set to ``lua``.                   |
    +------------------------+----------+----------------------------------------------------+
    | ``buffer``             | pointer  | These two arguments define a memory block that     |
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

Error Reporting
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
``NSIBegin()`` function. When it is called, the ``level`` argument is one
of the values defined by the ``NSIErrorLevel`` enum. The ``code``
argument is a numeric identifier for the error message, or 0 when
irrelevant. The ``message`` argument is the text of the message.

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
        int n_args,
        const NSIArg_t *args
    )

This function is the only control function of the API. It is responsible
of starting, suspending and stopping the render. It also allows for
synchronizing the render with interactive calls that might have been
issued. The function accepts :

.. table:: NSIRenderControl() intrinsic argument
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

.. table:: NSIRenderControl() optional arguments
    :widths: 3 1 6

    +-------------------------+----------+---------------------------------------------------+
    | ``progressive``         | integer  | If set to ``1``, render the image in a            |
    |                         |          | progressive fashion.                              |
    +-------------------------+----------+---------------------------------------------------+
    | ``interactive``         | integer  | .. _section:rendering:interactive:                |
    |                         |          |                                                   |
    |                         |          | If set to ``1``, the renderer will accept         |
    |                         |          | commands to edit scene’s state while rendering.   |
    |                         |          | The difference with a normal render is that the   |
    |                         |          | render task will not exit even if rendering is    |
    |                         |          | finished. Interactive renders are by definition   |
    |                         |          | progressive.                                      |
    +-------------------------+----------+---------------------------------------------------+
    | ``frame``               |          | Specifies the frame number of this render.        |
    +-------------------------+----------+---------------------------------------------------+
    | ``stoppedcallback``     | pointer  | A pointer to a user function that should be       |
    |                         |          | called on rendering status changes. This function |
    | ``callback`` (!)        |          | must have no return value and accept a pointer    |
    |                         |          | argument, a |nsi| context argument and an integer |
    |                         |          | argument:                                         |
    |                         |          |                                                   |
    |                         |          | .. code-block:: c                                 |
    |                         |          |                                                   |
    |                         |          |     void StoppedCallback(                         |
    |                         |          |         void* stoppedcallbackdata,                |
    |                         |          |         NSIContext_t ctx,                         |
    |                         |          |         int status                                |
    |                         |          |     )                                             |
    |                         |          |                                                   |
    |                         |          | The third argument is an integer which can take   |
    |                         |          | the following values:                             |
    |                         |          |                                                   |
    |                         |          | *  ``NSIRenderCompleted`` indicates that          |
    |                         |          |    rendering has completed normally.              |
    |                         |          |                                                   |
    |                         |          | *  ``NSIRenderAborted`` indicates that rendering  |
    |                         |          |    was interrupted before completion.             |
    |                         |          |                                                   |
    |                         |          | *  ``NSIRenderSynchronized`` indicates that an    |
    |                         |          |    interactive render has produced an image which |
    |                         |          |    reflects all changes to the scene.             |
    |                         |          |                                                   |
    |                         |          | *  ``NSIRenderRestarted`` indicates that an       |
    |                         |          |    interactive render has received new changes to |
    |                         |          |    the scene and no longer has an up to date      |
    |                         |          |    image.                                         |
    +-------------------------+----------+---------------------------------------------------+
    | ``stoppedcallbackdata`` | pointer  | A pointer that will be passed back to the         |
    |                         |          | ``stoppedcallback`` function.                     |
    | ``callback.data`` (!)   |          |                                                   |
    +-------------------------+----------+---------------------------------------------------+
