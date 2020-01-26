.. include:: definitions.rst

.. _section:cppapi:

The C++ API wrappers
====================

The :doc:`nsi.hpp` file provides C++ wrappers which are less tedious to use
than the low level C interface. All the functionality is inline so no
additional libraries are needed and there are no abi issues to consider.

Creating a context
------------------

The core of these wrappers is the ``NSI::Context`` class. Its default
construction will require linking with the renderer.

.. code-block:: cpp
    :linenos:

    #include "nsi.hpp"

    NSI::Context nsi;

The :doc:`nsi_dynamic.hpp` file provides an alternate api source which
will load the renderer at runtime and thus requires no direct linking.

.. code-block:: cpp
    :linenos:

    #include "nsi.hpp"
    #include "nsi_dynamic.hpp"

    NSI::DynamicAPI nsi_api;
    NSI::Context nsi(nsi_api);

In both cases, a new nsi context can then be created with the
``Begin()`` method.

.. code-block:: cpp
    :linenos:

    nsi.Begin();

This will be bound to the ``NSI::Context`` object and released when the
object is deleted. It is also possible to bind the object to a handle
from the C API, in which case it will not be released unless the
``End()`` method is explicitly called.

Argument passing
----------------

The ``NSI::Context`` class has methods for all the other |nsi| calls.
The optional parameters of those can be set by several accessory classes
and given in many ways. The most basic is a single argument.

.. code-block:: cpp
    :linenos:

    nsi.SetAttribute("handle", NSI::FloatArg("fov", 45.0f));

It is also possible to provide static lists:

.. code-block:: cpp
   :linenos:

    nsi.SetAttribute(
        "handle",(
            NSI::FloatArg("fov", 45.0f),
            NSI::DoubleArg("depthoffield.fstop", 4.0)
        )
    );

And finally a class supports dynamically building a list.

.. code-block:: cpp
    :linenos:

     NSI::ArgumentList args;
     args.Add(new NSI::FloatArg("fov", 45.0f));
     args.Add(new NSI::DoubleArg("depthoffield.fstop", 4.0));
     nsi.SetAttribute("handle", args);

The ``NSI::ArgumentList`` object will delete all the objects added to it
when it is deleted.

Argument classes
~~~~~~~~~~~~~~~~

To be continued …
