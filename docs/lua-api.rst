.. include:: definitions.rst

.. _section:Lua:

The Lua API
-----------

The scripted interface is slightly different than its counterpart
since it has been adapted to take advantage of the niceties of Lua. The
main differences with the C |nbsp| API are:

-  No need to pass a |nsi| context to function calls since it’s already
   embodied in the |nsi| Lua table (which is used as a class).

-  The ``type`` argument can be omitted if the argument is an integer,
   real or string (as with the ``Kd`` and ``filename`` in the example
   below).

-  |nsi| arguments can either be passed as a variable number of
   arguments or as a single argument representing an array of arguments
   (as in the ``"ggx"`` shader below)

-  There is no need to call ``NSIBegin()`` and ``NSIEnd()`` equivalents
   since the Lua script is run in a valid context.

Below is an example shader creation logic in Lua.

.. code-block:: lua
    :caption: shader creation example in Lua
    :linenos:

    nsi.Create( "lambert", "shader" );
    nsi.SetAttribute(
        "lambert", {
           { name = "filename", data = "lambert_material.oso" },
           { name = "Kd", data = 0.55 },
           { name = "albedo", data = { 1, 0.5, 0.3 }, type = nsi.TypeColor }
        }
    );

    nsi.Create( "ggx", "shader" );
    nsi.SetAttribute(
        "ggx", {
            {name = "filename", data = "ggx_material.oso" },
            {name = "anisotropy_direction", data = {0.13, 0 ,1}, type = nsi.TypeVector }
        }
    );

API calls
~~~~~~~~~

All (in a scripting context) useful |nsi| functions are provided and are
listed below. There is also a ``nsi.utilities`` class which, for now, only
contains a :ref:`method to print errors<luaapi:errors>`.

.. table:: |nsi| functions
    :widths: 1 1

    ============================ ===========================
    **Lua Function**             **C equivalent**
    ============================ ===========================
    ``nsi.SetAttribute()``       ``NSISetAttribute()``
    ``nsi.SetAttributeAtTime()`` ``NSISetAttributeAtTime()``
    ``nsi.Create()``             ``NSICreate()``
    ``nsi.Delete()``             ``NSIDelete()``
    ``nsi.DeleteAttribute()``    ``NSIDeleteAttribute()``
    ``nsi.Connect()``            ``NSIConnect()``
    ``nsi.Disconnect()``         ``NSIDisconnect()``
    ``Evaluate()``               ``NSIEvaluate()``
    ============================ ===========================

Optional function arguments format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each single argument is passed as a Lua table containing the following
key values:

-  ``name`` – the name of the argument.

-  ``data`` – the argument data. Either a value (integer, float or
   string) or an array.

-  ``type`` – the type of the argument. Possible values are:

   .. table:: Lua |nsi| argument types
       :widths: 1 1

       =================== ==================
       **Lua Type**        **C equivalent**
       =================== ==================
       ``nsi.TypeFloat``   ``NSITypeFloat``
       ``nsi.TypeInteger`` ``NSITypeInteger``
       ``nsi.TypeString``  ``NSITypeString``
       ``nsi.TypeNormal``  ``NSITypeNormal``
       ``nsi.TypeVector``  ``NSITypeVector``
       ``nsi.TypePoint``   ``NSITypePoint``
       ``nsi.TypeMatrix``  ``NSITypeMatrix``
       =================== ==================

-  ``arraylength`` – length of the array for each element.

   .. Note:
       There is no ``count`` argument in Lua since it can be deduced
       from the size of the provided data, its type and array length.

Here are some example of well formed arguments:

.. code-block:: lua
    :linenos:

    --[[ strings, floats and integers do not need a 'type' specifier ]] --
    p1 = {
        name = "shaderfilename",
        data = "emitter"
    };
    p2 = {
        name = "power",
        data = 10.13
    };
    p3 = {
        name = "toggle",
        data = 1
    };

    --[[ All other types, including colors and points, need a
         type specified for disambiguation. ]]--
    p4 = {
        name = "Cs",
        data = { 1, 0.9, 0.7 },
        type=nsi.TypeColor
    };

    --[[ An array of 2 colors ]] --
    p5 = {
        name = "vertex_color",
        arraylength = 2,
        data= { 1, 1, 1, 0, 0, 0 },
        type= nsi.TypeColor
    };

    --[[ Create a simple mesh and connect it root ]] --
    nsi.Create( "floor", "mesh" )
    nsi.SetAttribute(
        "floor", {
            name = "nvertices",
            data = 4
        }, {
            name = "P",
            type = nsi.TypePoint,
            data = { -2, -1, -1, 2, -1, -1, 2, 0, -3, -2, 0, -3 }
        }
    )
    nsi.Connect( "floor", "", ".root", "objects" )

.. _luaapi:evaluation:

Evaluating a Lua script
~~~~~~~~~~~~~~~~~~~~~~~

Script evaluation is done through C, an |nsi| stream or even another Lua
script. Here is an example using an |nsi| stream:

.. code-block:: shell
    :linenos:

    Evaluate
        "filename" "string" 1 ["test.nsi.lua"]
        "type" "string" 1 ["lua"]

It is also possible to evaluate a Lua script *inline* using the
``script`` argument. For example:

.. code-block:: shell
    :linenos:

    Evaluate
        "script" "string" 1 ["nsi.Create(\"light\", \"shader\");"]
        "type" "string" 1 ["lua"]

Both ``filename`` and ``script`` can be specified to ``NSIEvaluate()``
in one go, in which case the inline script will be evaluated before the
file and both scripts will share the same |nsi| and Lua contexts.

Any error during script parsing or evaluation will be sent to |nsi|'s error
handler.

Some utilities, such as error reporting, are available through the
``nsi.utilities`` class.

.. note::
    All Lua scripts are run in a sandbox in which all Lua system libraries
    are *disabled*.

Passing arguments to a Lua script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All arguments passed to ``NSIEvaluate()`` will appear in the
``nsi.scriptarguments`` table. For example, the following call:

.. code-block:: shell
    :linenos:

    Evaluate
        "filename" "string" 1 ["test.lua"]
        "type" "string" 1 ["lua"]
        "userdata" "color[2]" 1 [1 0 1 2 3 4]

Will register a ``userdata`` entry in the ``nsi.scriptarguments``
table. So executing the following line in the ``test.lua`` script
that the above snippete references:

.. code-block:: lua

    print( nsi.scriptarguments.userdata.data[5] );

Will print:

.. code-block:: shell

    3.0

.. _luaapi:errors:

Reporting errors from a Lua script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``nsi.utilities.ReportError()`` to send error messages to the error
handler defined in the current nsi context. For example:

.. code-block:: lua

    nsi.utilities.ReportError( nsi.ErrWarning, "Watch out!" );

The and are shown in .

.. table:: Lua |nsi| error codes
    :widths: 1 1

    =================== =================
    **Lua Error Codes** **C equivalent**
    =================== =================
    ``nsi.ErrMessage``  ``NSIErrMessage``
    ``nsi.ErrWarning``  ``NSIErrMessage``
    ``nsi.ErrInfo``     ``NSIErrInfo``
    ``nsi.ErrError``    ``NSIErrError``
    =================== =================
