Cookbook
========

The Nodal Scene Interface (NSI) is a simple yet expressive API to
describe a scene to a renderer. From geometry declaration, to
instancing, to attribute inheritance and shader assignments,
everything fits in 12 API calls. The following recipes demonstrate
how to achieve most common manipulations.

Geometry Creation
-----------------

Creating geometry nodes is simple. The content of each node is filled
using the `NSISetAttribute` call.

.. code-block:: cpp
    :linenos:

    /**
    Polygonal meshes can be created minimally by specifying "P".
    NSI's C++ API provides an easy interface to pass parameters to all NSI
    API calls through the Args class.
    */
    const char *k_poly_handle = "simple polygon"; /* avoids typos */

    nsi.Create( k_poly_handle, "mesh" );

    NSI::ArgumentList mesh_args;
    float points[3*4] = { -1, 1, 0,  1, 1, 0, 1, -1, 0, -1, -1, 0 };
    mesh_args.Add(
        NSI::Argument::New( "P" )
            ->SetType( NSITypePoint )
            ->SetCount( 4 )
            ->SetValuePointer( points ) );
    nsi.SetAttribute( k_poly_handle, mesh_args );


.. code-block:: rib
    :linenos:

    ## Polygonal meshes can be created minimally by specifying "P".
    ## NSI's C++ API provides an easy interface to pass parameters to all NSI
    ## API calls through the Args class.

    Create "simple polygon" "mesh"
    SetAttribute "simple polygon"
        "P" "point" 1 [ -1  1  0   1  1  0   1 -1  0   -1 -1  0 ]
