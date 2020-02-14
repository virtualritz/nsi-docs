.. include:: definitions.rst

.. _chapter:interface:

The Interface
=============

The Interface Abstraction
-------------------------

The Nodal Scene Interface is built around the concept of nodes. Each
node has a unique handle to identify it and a type which describes its
intended function in the scene. Nodes are abstract containers for data.
The interpretation depends on the node type. Nodes can also be
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

What we refer to as the |nsi| has two major components:

-  Methods to create nodes, attributes and their connections.

-  :ref:`Node types<chapter:nodes>` understood by the renderer.

Much of the complexity and expressiveness of the interface comes from
the supported nodes. The first part was kept deliberately simple to make
it easy to support multiple ways of creating nodes. We will list a few
of those in the following sections but this list is not meant to be
final. New languages and file formats will undoubtedly be supported in
the future.

APIs
----

.. toctree::
    :maxdepth: 2

    c-api
    cpp-api
    lua-api
    python-api
    stream-api
    procedurals
