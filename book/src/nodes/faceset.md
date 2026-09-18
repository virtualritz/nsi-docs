# `faceset`

This node is used to provide a way to attach attributes to some faces of another geometric primitive, such as the mesh node. It has the following attributes:

| Name    | Type    | Default |
| ------- | ------- | ------- |
| `faces` | _`int`_ |         |

This attribute is a list of indices of faces. It identifies which faces of the original geometry will be part of this face set.

A face set is connected to the `facesets` attribute of its geometry. Attributes then attach to the face set as they do to any geometry. This stream defines a face set on a subdivision surface:

```sh
Create "subdiv" "mesh"
SetAttribute "subdiv"
  "nvertices" "int" 4 [ 4 4 4 4 ]
  "P" "point" 9 [
    0 0 0   1 0 0   2 0 0
    0 1 0   1 1 0   2 1 0
    0 2 0   1 2 0   2 2 2 ]
  "P.indices" "int" 16 [
    0 1 4 3   1 2 5 4   3 4 7 6   4 5 8 7 ]
  "subdivision.scheme" "string" 1 "catmull-clark"

Create "set1" "faceset"
SetAttribute "set1"
  "faces" "int" 2 [ 0 3 ]
Connect "set1" "" "subdiv" "facesets"

Connect "attributes1" "" "subdiv" "geometryattributes"
Connect "attributes2" "" "set1" "geometryattributes"
```
