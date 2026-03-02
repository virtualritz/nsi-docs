# Attribute Names by Node

This table lists all node attributes, sorted by node type. Attributes marked with (!) have a proposed new name for future consistency.

## global

| Current Name                   | Type           | Default    | Proposed Name (!)            |
| ------------------------------ | -------------- | ---------- | ---------------------------- |
| `numberofthreads`              | int            | 0          | `thread.count`               |
| `texturememory`                | int            |            | `texture.memory`             |
| `networkcache.size`            | int            | 0          |                              |
| `networkcache.directory`       | string         |            |                              |
| `networkcache.mipmap`          | int            | 1          |                              |
| `networkcache.write`           | string         | 0          |                              |
| `license.server`               | string         |            |                              |
| `license.wait`                 | int            | 1          |                              |
| `license.hold`                 | int            | 0          |                              |
| `renderatlowpriority`          | int            | 0          | `priority.low`               |
| `bucketorder`                  | string         | horizontal | `bucket.order`               |
| `frame`                        | double         | 0          |                              |
| `hidemessages`                 | int            |            |                              |
| `maximumraydepth.diffuse`      | int            | 1          | `diffuse.ray.depth.max`      |
| `maximumraydepth.hair`         | int            | 4          | `hair.ray.depth.max`         |
| `maximumraydepth.reflection`   | int            | 1          | `reflection.ray.depth.max`   |
| `maximumraydepth.refraction`   | int            | 4          | `refraction.ray.depth.max`   |
| `maximumraydepth.volume`       | int            | 0          | `volume.ray.depth.max`       |
| `maximumraylength.diffuse`     | double         | -1         | `diffuse.ray.length.max`     |
| `maximumraylength.hair`        | double         | -1         | `hair.ray.length.max`        |
| `maximumraylength.reflection`  | double         | -1         | `reflection.ray.length.max`  |
| `maximumraylength.refraction`  | double         | -1         | `refraction.ray.length.max`  |
| `maximumraylength.specular`    | double         | -1         |                              |
| `maximumraylength.volume`      | double         | -1         |                              |
| `quality.denoise`              | int            | 1          |                              |
| `quality.iprglobalupdate`      | int            | 1          |                              |
| `quality.iprinterpolate`       | int            | 1          |                              |
| `quality.iprspeedmultiplier`   | double         | 1          |                              |
| `quality.shadingsamples`       | int            | 1          | `shading.samples`            |
| `quality.volumesamples`        | int            | 1          | `volume.samples`             |
| `referencetime`                | double         |            |                              |
| `quality.samplevolumeemission` | int            | 1          |                              |
| `show.displacement`            | int            | 1          | `shading.displacement`       |
| `show.atmosphere`              | int            | 1          | `shading.atmosphere`         |
| `show.multiplescattering`      | double         | 1.0        | `shading.multiplescattering` |
| `show.osl.subsurface`          | int            | 1          | `shading.osl.subsurface`     |
| `statistics.progress`          | int            | 0          |                              |
| `statistics.filename`          | string         | null       |                              |
| `exclusiveshading`             | \<connection\> |            |                              |
| `verbose`                      | int            | 0          |                              |
| `messages.timestamp`           | int            | 0          |                              |

## root

| Current Name         | Type           | Default | Proposed Name (!) |
| -------------------- | -------------- | ------- | ----------------- |
| `objects`            | \<connection\> |         | `object`          |
| `geometryattributes` | \<connection\> |         | `attribute`       |

## set

| Current Name | Type           | Default | Proposed Name (!) |
| ------------ | -------------- | ------- | ----------------- |
| `members`    | \<connection\> |         | `member`          |

## mesh

| Current Name                      | Type   | Default | Proposed Name (!)                    |
| --------------------------------- | ------ | ------- | ------------------------------------ |
| `P`                               | point  |         |                                      |
| `nvertices`                       | int    |         | `vertex.count` / `face.vertex.count` |
| `nholes`                          | int    |         | `hole.count`                         |
| `clockwisewinding`                | int    | 0       | `clockwise`                          |
| `subdivision.scheme`              | string |         |                                      |
| `subdivision.cornervertices`      | int    |         | `subdivision.corner.index`           |
| `subdivision.cornersharpness`     | float  |         | `subdivision.corner.sharpness`       |
| `subdivision.creasevertices`      | int    |         | `subdivision.crease.index`           |
| `subdivision.creasesharpness`     | float  |         | `subdivision.crease.sharpness`       |
| `subdivision.smoothcreasecorners` | int    | 1       | `subdivision.corner.automatic`       |
| `referencetime`                   | double |         |                                      |
| `quadraticmotion`                 | int    | 0       |                                      |
| `outlinecreasethreshold`          | float  | 10      |                                      |

## faceset

| Current Name | Type | Default | Proposed Name (!) |
| ------------ | ---- | ------- | ----------------- |
| `faces`      | int  |         | `face.index`      |

## curves

| Current Name  | Type   | Default     | Proposed Name (!) |
| ------------- | ------ | ----------- | ----------------- |
| `nvertices`   | int    |             | `vertex.count`    |
| `P`           | point  |             |                   |
| `width`       | float  |             |                   |
| `basis`       | string | catmull-rom |                   |
| `extrapolate` | int    | 0           |                   |

## particles

| Current Name         | Type   | Default | Proposed Name (!) |
| -------------------- | ------ | ------- | ----------------- |
| `P`                  | point  |         |                   |
| `width`              | float  |         |                   |
| `N`                  | normal |         |                   |
| `reverseorientation` | int    | 0       |                   |
| `id`                 | int    |         |                   |
| `quadraticmotion`    | int    | 0       |                   |

## procedural

| Current Name                                                      | Type     | Default | Proposed Name (!) |
| ----------------------------------------------------------------- | -------- | ------- | ----------------- |
| `boundingbox`                                                     | point[2] |         |                   |
| _(plus all NSIEvaluate parameters and transform node attributes)_ |          |         |                   |

## environment

| Current Name | Type   | Default | Proposed Name (!) |
| ------------ | ------ | ------- | ----------------- |
| `angle`      | double | 360     |                   |

## shader

| Current Name     | Type   | Default | Proposed Name (!) |
| ---------------- | ------ | ------- | ----------------- |
| `shaderfilename` | string |         |                   |
| `shaderobject`   | string |         |                   |

## attributes (geometry)

| Current Name                | Type           | Default | Proposed Name (!)     |
| --------------------------- | -------------- | ------- | --------------------- |
| `surfaceshader`             | \<connection\> |         | `shader.surface`      |
| `displacementshader`        | \<connection\> |         | `shader.displacement` |
| `volumeshader`              | \<connection\> |         | `shader.volume`       |
| `ATTR.priority`             | int            | 0       |                       |
| `visibility.camera`         | int            | 1       |                       |
| `visibility.diffuse`        | int            | 1       |                       |
| `visibility.hair`           | int            | 1       |                       |
| `visibility.reflection`     | int            | 1       |                       |
| `visibility.refraction`     | int            | 1       |                       |
| `visibility.shadow`         | int            | 1       |                       |
| `visibility.specular`       | int            | 1       |                       |
| `visibility.volume`         | int            | 1       |                       |
| `visibility`                | int            | 1       |                       |
| `visibility.set.subsurface` | \<connection\> |         |                       |
| `matte`                     | int            | 0       |                       |
| `regularemission`           | int            | 1       | `emission.regular`    |
| `quantizedemission`         | int            | 1       | `emission.quantized`  |
| `bounds`                    | \<connection\> |         |                       |

## transform

| Current Name           | Type           | Default | Proposed Name (!) |
| ---------------------- | -------------- | ------- | ----------------- |
| `transformationmatrix` | doublematrix   |         | `matrix`          |
| `objects`              | \<connection\> |         | `object`          |
| `geometryattributes`   | \<connection\> |         | `attribute`       |
| `shaderattributes`     | \<connection\> |         |                   |

## instances

| Current Name             | Type           | Default | Proposed Name (!) |
| ------------------------ | -------------- | ------- | ----------------- |
| `sourcemodels`           | \<connection\> |         | `object`          |
| `transformationmatrices` | doublematrix   |         | `matrix`          |
| `modelindices`           | int            | 0       | `object.index`    |
| `disabledinstances`      | int            |         | `disable.index`   |

## outputdriver

| Current Name      | Type   | Default | Proposed Name (!) |
| ----------------- | ------ | ------- | ----------------- |
| `drivername`      | string |         |                   |
| `imagefilename`   | string |         | `filename`        |
| `embedstatistics` | int    | 1       |                   |

## outputlayer

| Current Name         | Type           | Default         | Proposed Name (!) |
| -------------------- | -------------- | --------------- | ----------------- |
| `variablename`       | string         |                 |                   |
| `variablesource`     | string         | shader          |                   |
| `layername`          | string         |                 |                   |
| `scalarformat`       | string         | uint8           |                   |
| `layertype`          | string         | color           |                   |
| `colorprofile`       | string         |                 |                   |
| `dithering`          | integer        | 0               |                   |
| `withalpha`          | integer        | 0               |                   |
| `sortkey`            | integer        |                 |                   |
| `lightset`           | \<connection\> |                 |                   |
| `lightsetname`       | string         |                 |                   |
| `outputdrivers`      | \<connection\> |                 | `outputdriver`    |
| `filter`             | string         | blackman-harris |                   |
| `filterwidth`        | double         | 3.0             |                   |
| `backgroundvalue`    | float          | 0               |                   |
| `backgroundlayer`    | \<connection\> |                 |                   |
| `lightdepth`         | string         | auto            |                   |
| `cryptomatte.enable` | int            | 0               |                   |
| `cryptomatte.level`  | int            | 0               |                   |

## screen

| Current Name             | Type           | Default | Proposed Name (!) |
| ------------------------ | -------------- | ------- | ----------------- |
| `outputlayers`           | \<connection\> |         | `outputlayer`     |
| `resolution`             | integer[2]     |         |                   |
| `oversampling`           | integer        |         |                   |
| `crop`                   | 2 × float[2]   |         |                   |
| `prioritywindow`         | 2 × int[2]     |         |                   |
| `screenwindow`           | 2 × double[2]  |         |                   |
| `overscan`               | 2 × int[2]     |         |                   |
| `pixelaspectratio`       | float          |         |                   |
| `staticsamplingpattern`  | int            | 0       |                   |
| `importancesamplefilter` | int            | 0       |                   |

## vdbparticles

| Current Name            | Type   | Default | Proposed Name (!) |
| ----------------------- | ------ | ------- | ----------------- |
| `vdbfilename`           | string |         |                   |
| `pointsgrid`            | string |         |                   |
| `velocityreferencetime` | double |         |                   |
| `velocityscale`         | double | 1       |                   |
| `enablepscale`          | int    | 1       |                   |
| `width`                 | double | 1       |                   |
| `widthscale`            | double | 1       |                   |

## volume

| Current Name            | Type   | Default | Proposed Name (!) |
| ----------------------- | ------ | ------- | ----------------- |
| `vdbfilename`           | string |         |                   |
| `densitygrid`           | string |         |                   |
| `colorgrid`             | string |         |                   |
| `emissiongrid`          | string |         |                   |
| `emissionintensitygrid` | string |         |                   |
| `temperaturegrid`       | string |         |                   |
| `velocitygrid`          | string |         |                   |
| `velocityreferencetime` | double |         |                   |
| `velocityscale`         | double | 1       |                   |

## camera (common)

| Current Name     | Type           | Default | Proposed Name (!) |
| ---------------- | -------------- | ------- | ----------------- |
| `screens`        | \<connection\> |         | `screen`          |
| `shutterrange`   | double         |         |                   |
| `shutteropening` | double         |         |                   |
| `clippingrange`  | double         |         |                   |

## perspectivecamera

| Current Name                     | Type    | Default | Proposed Name (!) |
| -------------------------------- | ------- | ------- | ----------------- |
| `fov`                            | float   |         |                   |
| `depthoffi­eld.enable`           | integer | 0       |                   |
| `depthoffi­eld.fstop`            | double  |         |                   |
| `depthoffi­eld.focallength`      | double  |         |                   |
| `depthoffi­eld.focallengthratio` | double  | 1       |                   |
| `depthoffi­eld.focaldistance`    | double  |         |                   |
| `depthoffi­eld.aperture.enable`  | integer | 0       |                   |
| `depthoffi­eld.aperture.sides`   | integer | 5       |                   |
| `depthoffi­eld.aperture.angle`   | double  | 0       |                   |
| `unitlengthmillimeters`          | double  |         |                   |

## fisheyecamera

| Current Name | Type   | Default     | Proposed Name (!) |
| ------------ | ------ | ----------- | ----------------- |
| `fov`        | float  |             |                   |
| `mapping`    | string | equidistant |                   |

## cylindricalcamera

| Current Name    | Type  | Default | Proposed Name (!) |
| --------------- | ----- | ------- | ----------------- |
| `fov`           | float | 90      |                   |
| `horizontalfov` | float | 360     | `fov.horizontal`  |
| `eyeoffset`     | float |         |                   |
