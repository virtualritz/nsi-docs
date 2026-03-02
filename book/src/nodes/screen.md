# `screen`

This node describes how the view from a camera node will be rasterized into an [output layer](outputlayer.md) node. It can be connected to the `screens` attribute of a camera node.

| Name           | Type             | Default |
| -------------- | ---------------- | ------- |
| `outputlayers` | _`<connection>`_ |         |

This connection accepts [output layer](outputlayer.md) nodes which will receive a rendered image of the scene as seen by the camera.

| Name         | Type           | Default |
| ------------ | -------------- | ------- |
| `resolution` | _`integer[2]`_ |         |

Horizontal and vertical resolution of the rendered image, in pixels.

| Name           | Type        | Default |
| -------------- | ----------- | ------- |
| `oversampling` | _`integer`_ |         |

The total number of samples (i.e. camera rays) to be computed for each pixel in the image.

| Name   | Type             | Default |
| ------ | ---------------- | ------- |
| `crop` | _`2 × float[2]`_ |         |

The region of the image to be rendered. It's defined by a list of exactly 2 pairs of floating-point number. Each pair represents a point in ɴᴅᴄ space:

- Top-left corner of the crop region
- Bottom-right corner of the crop region

| Name             | Type           | Default |
| ---------------- | -------------- | ------- |
| `prioritywindow` | _`2 × int[2]`_ |         |

For progressive renders, this is the region of the image to be rendered first. It is two pairs of integers. Each represents pixel coordinates:

- Top-left corner of the high priority region
- Bottom-right corner of the high priority region

| Name           | Type              | Default |
| -------------- | ----------------- | ------- |
| `screenwindow` | _`2 × double[2]`_ |         |

Specifies the screen space region to be rendered. Each pair represents a 2D point in screen space:

- Bottom-left corner of the region
- Top-right corner of the region

Note that the default screen window is set implicitly by the frame aspect ratio:
screenwindow = [-f, -1], [f, 1] for f = xres/yres

| Name       | Type           | Default |
| ---------- | -------------- | ------- |
| `overscan` | _`2 × int[2]`_ |         |

Specifies how many extra pixels to render around the image. The four values represent the amount of overscan on the left, top, right and bottom of the image.

| Name               | Type      | Default |
| ------------------ | --------- | ------- |
| `pixelaspectratio` | _`float`_ |         |

Ratio of the physical width to the height of a single pixel. A value of 1.0 corresponds to square pixels.

| Name                    | Type    | Default |
| ----------------------- | ------- | ------- |
| `staticsamplingpattern` | _`int`_ | `0`     |

This controls whether or not the sampling pattern used to produce the image change for every frame. A nonzero value will cause the same pattern to be used for all frames. A value of zero will cause the pattern to change with the `frame` attribute of the [global node](global.md).

| Name                     | Type    | Default |
| ------------------------ | ------- | ------- |
| `importancesamplefilter` | _`int`_ | `0`     |

This enables a rendering mode where the pixel filter is importance sampled. Quality will be reduced and the same filter will be used for all output layers of the screen. Filters with negative lobes (eg. sinc) are unsupported.
