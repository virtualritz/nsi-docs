.. include:: definitions.rst

.. _section:nsistream:

The interface stream
--------------------

It is important for a scene description api to be streamable. This
allows saving scene description into files, communicating scene state
between processes and provide extra flexibility when sending commands to
the renderer |nsp| [#]_.

Instead of re-inventing the wheel, the authors have decided to use
exactly the same format as is used by the *RenderMan* Interface
Bytestream (rib). This has several advantages:

-  Well defined ascii and binary formats.

-  The ascii format is human readable and easy to understand.

-  Easy to integrate into existing renderers (writers and readers
   already available).

Note that since Lua is part of the api, one can use Lua files for api
streaming |nsp| [#]_.

--------------

.. rubric:: Footnotes

.. [#]
   The streamable nature of the *RenderMan* API, through RIB, is an
   undeniable advantage. RenderMan is a registered trademark of Pixar.

.. [#]
   Preliminary tests show that the Lua parser is as fast as an optimized
   ASCII RIB parser.

