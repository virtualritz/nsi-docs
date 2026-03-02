# `outputdriver`

An output driver defines how an image is transferred to an output destination. The destination could be a file (e.g. "exr" output driver), frame buffer or a memory address. It can be connected to the `outputdrivers` attribute of an [output layer](outputlayer.md) node. It has the following attributes:

| Name         | Type       | Default |
| ------------ | ---------- | ------- |
| `drivername` | _`string`_ |         |

This is the name of the driver to use. The API of the driver is implementation specific and is not covered by this documentation.

| Name            | Type       | Default |
| --------------- | ---------- | ------- |
| `imagefilename` | _`string`_ |         |

Full path to a file for a file-based output driver or some meaningful identifier depending on the output driver.

| Name              | Type    | Default |
| ----------------- | ------- | ------- |
| `embedstatistics` | _`int`_ | `1`     |

A value of 1 specifies that statistics will be embedded into the image file.

Any extra attributes are also forwarded to the output driver which may interpret them however it wishes.
