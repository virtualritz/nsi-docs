# Lens shaders

A lens shader is an ᴏsʟ network connected to a camera through the `lensshader` connection. Such shaders receive the position and the direction of each tracer ray and can either change or completely discard the traced ray. This allows to implement distortion maps and cut maps. The following shader variables are provided:

- `P` — Contains ray's origin.
- `I` — Contains ray's direction. Setting this variable to zero instructs the renderer not to trace the corresponding ray sample.
- `time` — The time at which the ray is sampled.
- `(u, v)` — Coordinates, in screen space, of the ray being traced.
