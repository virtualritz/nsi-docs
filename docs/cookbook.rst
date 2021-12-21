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

.. code-block:: shell
    :caption: **Geometry Creation**
    :linenos:

    ## Polygonal meshes can be created minimally by specifying "P".
    ## NSI's C++ API provides an easy interface to pass parameters to all NSI
    ## API calls through the Args class.

    Create "simple polygon" "mesh"
    SetAttribute "simple polygon"
        "P" "point" 1 [ -1  1  0   1  1  0   1 -1  0   -1 -1  0 ]



.. container:: toggle

    .. container:: header

        **Geometry Creation in C++**

    .. code-block:: cpp
        :linenos:

        /*
            Polygonal meshes can be created minimally by specifying "P".
            NSI's C++ API provides an easy interface to pass parameters
            to all NSI API calls through the Args class.
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

----

Specifying normals and other texture coordinates follows the same
logic. Constant attributes can be declared in a concise form too:

.. code-block:: shell
    :caption: **Adding constant attributes**
    :linenos:

    SetAttribute "simple polygon"
        "subdivision.scheme" "string" 1 ["catmull-clark"]

.. container:: toggle

    .. container:: header

        **Adding constant attributes in C++**

    .. code-block:: cpp
        :linenos:

        /** Turn our mesh into a subdivision surface */
        nsi.SetAttribute( k_poly_handle,
            NSI::CStringPArg("subdivision.scheme", "catmull-clark") );

----

Transforming Geometry
---------------------

In NSI, a geometry is rendered only if connected to the scene's root
(which has the special handle ".root"). It is possible to directly
connect a geometry node (such as the simple polygon above) to scene's
root but it wouldn't be very useful. To place/instance a geometry
anywhere in the 3D world a transform node is used as in the code
snippet below.


.. code-block:: shell
    :caption: **Adding constant attributes**
    :linenos:

    Create "my translation" "transform"
    Connect "translation"  "" ".root" "objects"
    Connect "simple polygon" "" "translation" "objects" );

    # Transalte 1 unit in Y
    SetAttribute "my translation"
        "transformationmatrix" "matrix" 1 [
        1 0 0 0
        0 1 0 0
        0 0 1 0
        0 1 0 1]

.. container:: toggle

    .. container:: header

        **Adding constant attributes in C++**

    .. code-block:: cpp
        :linenos:

        const char *k_instance1 = "my translation";

        nsi.Create( k_instance1, "transform" );
        nsi.Connect( k_instance1, "", NSI_SCENE_ROOT, "objects" );
        nsi.Connect( k_poly_handle, "", k_instance1, "objects" );

        /*
            Matrices in NSI are in double format to allow for greater
            range and precision.
        */
        double trs[16] =
        {
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            0., 1., 0., 1. /* transalte 1 unit in Y */
        };

        nsi.SetAttribute( k_instance1,
            NSI::DoubleMatrixArg("transformationmatrix", trs) );

----

Instancing is as simple as connecting a geometry to different
attributes. Instances of instances do work as expected too.

.. code-block:: cpp
    :linenos:

    const char *k_instance2 = "another translation";
    trs[13] += 1.0; /* translate in Y+ */

    nsi.Create( k_instance2, "transform" );
    nsi.Connect( k_poly_handle, "", k_instance2, "objects" );
    nsi.Connect( k_instance2, "", NSI_SCENE_ROOT, "objects" );

    /* We know have two instances of the same polygon in the scene */
