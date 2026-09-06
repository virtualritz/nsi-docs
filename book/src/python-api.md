# The Python API

The [`nsi.py`](nsi.py.md) file provides a python wrapper to the C interface. It is compatible with both Python 2.7 and Python 3.

An example of how to us it is provided in `python/examples/live_edit/live_edit.py`.

## Precision of Untyped Arguments

The wrapper infers a type when you do not give one. A Python `float` becomes
`NSITypeDouble`, and a Python `int` becomes `NSITypeInteger`
([`nsi.py`](nsi.py.md), `_GetArgNSIType`).

The renderer matches attribute types exactly. It does not convert between
widths. An attribute declared `float` therefore rejects a bare Python float,
and warns:

```
3DL WARNING E6007 wrong type for attribute 'fov' on node 'c' of type
'perspectivecamera' (expected type 'float', got 'double')
```

The call is dropped, and the attribute keeps its previous value. Pass a
`FloatArg` for any attribute that the node reference documents as `float`:

```python
nsi.SetAttribute("c", fov=nsi.FloatArg(35))
```

The shipped `live_edit.py` example does this for `fov`, and passes
`shutterrange` bare because that attribute is declared `double`.
