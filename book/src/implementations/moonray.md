# MoonRay

[MoonRay](https://openmoonray.org/) is DreamWorks' open-source production renderer. It has no ɴsɪ interface of its own. The [nsi-moonray](https://github.com/virtualritz/nsi-moonray) backend translates ɴsɪ calls into a MoonRay scene and ships as a library that exports the ɴsɪ C API. The items on this page are recorded in that project's specifications and were observed with MoonRay commit `eef67ae`, with 3Delight 2.9.209 as the reference for comparisons.

## Extensions

- **ᴏsʟ shader networks run in MoonRay.** An ɴsɪ shader network becomes one ᴏsʟ shader group, evaluated by three MoonRay plug-ins: `Osl` for surfaces, `OslDisplacement` and `OslMap`. The backend must be built with ᴏsʟ available; without it, each shader is replaced by a `UsdPreviewSurface` with parameters read from 3Delight's shaders, and displacement is dropped with a report.
- **3Delight's ᴏsʟ closures are understood.** `layer_closures`, `outputvariable` and `outputconstant` are registered, and `microfacet`'s `realeta`/`complexeta` build a conductor. The MaterialX closures (`dielectric_bsdf`, `conductor_bsdf`, `generalized_schlick_bsdf`, `sheen_bsdf`, `subsurface_bssrdf`, `uniform_edf`, `layer` and others) are mapped too.
- **Per-lobe AOVs.** An output variable that names a lobe becomes a MoonRay light-path expression. 3Delight's variable names are translated, for example `reflection` to `specular` and `incandescence` to `emission`.
- **Output drivers without ndspy.** An output driver named `ferris_f32` (or `_u32`, `_i32`, `_u16`, `_i16`, `_u8`, `_i8`) calls Rust closures passed as `callback.open`, `callback.write` and `callback.finish`.
- **Scene export.** `$NSI_MOONRAY_SCENE` writes the translated scene as MoonRay `.rdla`. The `mnry` command renders, converts and watches `.nsi` files.

## Limitations

- **At most two motion samples per attribute**, on one shutter for the whole scene. More samples are reported, not rendered, and each object's motion is resampled onto the scene's shutter.
- **Moving instances translate only.** Rotation or scale of an `instances` node across the shutter is reported, not rendered.
- **`suspend` and `resume` are not supported.** Restarting a MoonRay frame loses the samples taken so far.
- **`volumeshader` is not used.** ᴏsʟ volume closures are unmapped; VDB volumes render with MoonRay's own volume shader. A scalar emission grid is refused, and the volume with it.
- **`vdbparticles` is not supported.** MoonRay has no geometry that reads a point-data grid.
- **`environment` carries no texture.** It becomes a MoonRay environment light with default color and intensity.
- **ᴏsʟ details that are dropped:** colored transparency becomes one scalar presence; MaterialX tints become their luminance; `occlusion()` and the `microfacet` keywords `gamma`, `thinfilmthickness`, `thinfilmeta` and `mediumeta` are ignored with a warning; scoped `getattribute("scope", "name", ...)` is not answered.
- **An emissive mesh cannot also have a non-emissive material**, such as glowing metal.
- **One renderer per process.** A second concurrent render is refused; use a second process.
- **An orthographic camera renders empty** through the in-process progressive path. It renders through the spawned `moonray` program.
- **Output-driver callbacks need one shared build.** Rust closures work only when the application and the backend use the same `nsi-ffi-wrap`.

## Behavior That Differs From 3Delight

- **Pixels are pulled, not pushed.** MoonRay renders progressively but does not deliver buckets. The backend polls it and sends each changed rectangle to the output driver.
- **Channels are named after the layer.** The beauty output has the channels `Ci.R`, `Ci.G` and `Ci.B`, without alpha, not RGBA.
- **A plain `mesh` is not subdivided.** MoonRay's mesh subdivides by default; the backend turns that off unless `subdivision.scheme` is set.
- **Lights are recognized by shader name.** Geometry wearing one of 3Delight's light shaders (`areaLight`, `pointLight`, `spotLight`, `distantLight`) becomes a mesh light. Other emissive geometry is visible but lights nothing, because MoonRay's ᴏsʟ `emission()` affects only camera rays.
- **ᴏsʟ `+` adds closures.** Only `layer()` and `layer_closures` layer them with attenuation.
- **A disconnected object is switched off**, not removed, in an interactive session.
- **A scene without a camera gets a default one**, and geometry without a shader gets a default material.
- **`fov` is vertical**, matching 3Delight's framing to within a pixel.

## Known MoonRay Bugs

Found while writing the backend; none is filed upstream yet.

- A scene without a camera crashes MoonRay. The backend adds a default camera.
- Changing visibility re-tessellates the geometry instead of only rebuilding the acceleration structure, so hiding and showing is not cheap in an interactive session.
- A mesh light needs a material from the separate `moonshine_dwa` package; a MoonRay-only build fails. The backend provides a stand-in.
- A material without a vectorized shading function renders black in MoonRay's default mode. The backend forces scalar mode.
- A mesh light with a map shader crashes when its geometry is in no geometry set. The backend adds one.

## Setup

- The library is `libnsi_moonray.so` (`.dylib` on macOS, `nsi_moonray.dll` on Windows). It exports the ɴsɪ C API.
- `$NSI_MOONRAY_DSO` must name MoonRay's plug-in directory. Without it, no scene class is found and the render is empty, without an error.
- The backend links MoonRay when built with the `rdl2` feature. Otherwise it writes `.rdla` and runs the `moonray` program.
- MoonRay is licensed under Apache-2.0; nsi-moonray under MIT, Apache-2.0 or Zlib.
