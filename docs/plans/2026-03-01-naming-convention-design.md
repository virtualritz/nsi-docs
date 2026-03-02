# NSI Naming Convention Design

Status: Draft (brainstorming in progress)

## Why Hyphens, Not Underscores

Attribute names use **hyphens** (`-`) as word separators, not underscores (`_`). This is a deliberate choice: almost no programming language allows hyphens in identifiers (`variable-name` is invalid in C, C++, Python, Rust, Lua, etc.), so attribute name strings are instantly distinguishable from code identifiers in any language. When you see `reflection.ray-depth-max` in source code, it can only be an attribute name — never a variable, function, or type.

## Core Convention

- `.` (dots) separate hierarchy levels — these correspond to what would be groups/rollouts/sections in UI/attribute editor.
- `-` (hyphens) separate words within a single label.
- Singular nouns when used as modifiers in compound names (English compound noun rule).
  - Example: `point-grid` not `points-grid` — "point" modifies "grid".
- Plain English over jargon (governing principle — R9).
  - Example `field-of-view` not `fov`.
- Compound node type names also use hyphens: `vdb-particles`, `output-driver`, `output-layer`, `face-set`, `perspective-camera`, `fisheye-camera`, etc.
- Example: `subdivision.corner-sharpness` — group "Subdivision", label "Corner Sharpness".

## Rulings

### R1: Type-first grouping for ray settings

Ray depth/length settings on the `global` node are grouped by ray type, since each type has multiple related attributes (depth + length):

```
reflection.ray-depth-max
reflection.ray-length-max
diffuse.ray-depth-max
diffuse.ray-length-max
```

### R2: 2+ related attributes required to form a dot-group

Only use dot-separated hierarchy when there are 2 or more related attributes that form a logical group. Single standalone attributes use flat hyphenated naming:

**Groups (dot-separated):**

```
subdivision.scheme
subdivision.corner-index
subdivision.corner-sharpness
visibility.camera
visibility.diffuse
visibility.reflection
```

**Flat (hyphen-separated):**

```
vertex-count
hole-count
clockwise
reference-time
quadratic-motion
```

### R3: The grouping level is context-dependent, not concept-fixed

The same concept (e.g., "reflection") can be a **group** in one context and a **leaf** in another. The rule is: whichever level has 2+ siblings becomes the group.

**On the `global` node** — each ray type has 2+ settings (depth + length), so the ray type is the group:

```
reflection.ray-depth-max
reflection.ray-length-max
```

**On the `attributes` node** — each ray type has only ONE visibility flag, but "visibility" has 8+ flags, so visibility is the group:

```
visibility.reflection
visibility.diffuse
visibility.camera
```

The alternative (type-first everywhere: `reflection.visibility`, `diffuse.visibility`, etc.) would create 8 singleton groups, violating R2. The 2+ rule takes precedence over concept consistency.

### R4: Node type is an implicit top-level group

The node type itself provides context, so attribute names should not redundantly include the node type. On a `curves` node, the attribute is `basis`, not `curve-basis`. On a `particles` node, the attribute is `id`, not `particle-id`.

### R5: Rename everything, including legacy single-letter names

No grandfather clause for industry-standard abbreviations:

- `P` → `position`
- `N` → `normal`
- `nvertices` → `vertex-count`
- `nholes` → `hole-count`

Single-word names that are already clear stay as-is: `width`, `basis`, `id`, `matte`, `clockwise`.

### R6: Hyphen-separate compound domain terms

No concatenated words. All multi-word terms get hyphens:

- `depthoffield` → `depth-of-field`
- `fstop` → `f-stop`
- `focallength` → `focal-length`
- `focaldistance` → `focal-distance`

This applies within both group names and leaf labels:

```
depth-of-field.enable
depth-of-field.f-stop
depth-of-field.focal-length
depth-of-field.aperture.enable    ← sub-group (3 attrs: enable, sides, angle)
depth-of-field.aperture.sides
depth-of-field.aperture.angle
```

### R7: Connection attribute plurality matches cardinality

If a connection attribute accepts multiple connections, use plural. If it accepts only one, use singular.

**Plural** (multi-connection):

```
objects              (root, transform — multiple geometry nodes)
attributes           (root, transform — multiple attribute nodes)
members              (set — multiple objects)
screens              (camera — multiple screen nodes)
output-layers        (screen — multiple layer nodes)
output-drivers       (output-layer — multiple driver nodes)
```

**Singular** (single-connection):

```
shader.surface       (attributes — one surface shader)
shader.displacement  (attributes — one displacement shader)
shader.volume        (attributes — one volume shader)
background-layer     (output-layer — one background layer)
```

### R8: Group by concern, not by concept

Attributes are grouped by what kind of setting they are, not by what rendering concept they relate to. This keeps groups semantically coherent:

- **`quality.*`** = how much effort the renderer spends (sampling counts, performance)
- **`shading.*`** = which shading features are enabled/disabled (feature toggles)
- **`{type}.*`** = per-ray-type limits (depth, length)

```
quality.shading-samples           ← sampling effort
quality.volume-samples            ← sampling effort
quality.denoise                   ← quality toggle
quality.volume-emission-sampling  ← quality toggle
quality.preview.global-update     ← preview/IPR quality
quality.preview.interpolate       ← preview/IPR quality
quality.preview.speed-multiplier  ← preview/IPR quality

shading.displacement              ← feature toggle
shading.atmosphere                ← feature toggle
shading.multiple-scattering       ← feature toggle
shading.osl-subsurface            ← feature toggle

volume.ray-depth-max              ← ray limit
volume.ray-length-max             ← ray limit
```

This avoids scattering quality-related attrs across concept groups (which would make it hard to find "all the knobs that affect render speed").

### R9: Plain English over jargon (governing principle)

This is a **governing principle** that applies across all naming decisions. When choosing between a technical abbreviation/jargon term and a plain English equivalent, always prefer plain English. Names should be understandable without domain-specific knowledge.

- `ipr` → `preview` (Interactive Progressive Rendering → just "preview")
- `fov` → `field-of-view`
- `fstop` → `f-stop` (kept because it's the actual name of the unit, not jargon)

The group `quality.ipr.*` becomes `quality.preview.*`:

```
quality.preview.global-update
quality.preview.interpolate
quality.preview.speed-multiplier
```

### R10: Use `.enable` suffix for booleans in mixed groups

When a boolean on/off attribute belongs to a group that also has non-boolean attrs, append `.enable` to distinguish the toggle from the group:

```
depth-of-field.enable         ← mixed group (has f-stop, focal-length, etc.)
depth-of-field.f-stop
depth-of-field.focal-length

cryptomatte.enable            ← mixed group (has level)
cryptomatte.level
```

When the group is all-toggles or the boolean is standalone, no `.enable` needed:

```
shading.displacement          ← all-toggle group, obviously a toggle
shading.atmosphere

quality.denoise               ← obviously a toggle from context
```

### R11: Unify callbacks under `callback.*` group

All callback/handler function pointers across the API follow a consistent pattern: `callback.{purpose}` for the function pointer and `callback.{purpose}.data` for the associated userdata.

This applies across different API calls — the `callback` group is a cross-cutting convention:

```
# NSIBegin
callback.error               ← error handler function (was: errorhandler)
callback.error.data          ← error handler userdata (was: errorhandler.data)

# NSIRenderControl
callback.stop                ← stopped callback function (was: stoppedcallback)
callback.stop.data           ← stopped callback userdata (was: stoppedcallbackdata)
```

### R12: Singular nouns as modifiers in compound names

When a noun serves as a modifier (adjective) in a compound name, use its singular form. This follows standard English compound noun formation: "dog house" not "dogs house", "vertex count" not "vertices count".

```
vertex-count         ✓  (not vertices-count)
hole-count           ✓  (not holes-count)
face-index           ✓  (not faces-index)
point-grid           ✓  (not points-grid)
object-index         ✓  (not objects-index)
```

Plurals are reserved for R7 (connection cardinality), where the attribute name IS the thing, not a modifier:

```
objects              ✓  (the attribute is multiple objects, not a modifier)
members              ✓
output-layers        ✓
```

## Complete Attribute Mapping

Every attribute across all node types, with current → new name and the ruling(s) that apply. Attributes where current = new are omitted.

### `global` node

| Current                        | New                                | Rules                                  |
| ------------------------------ | ---------------------------------- | -------------------------------------- |
| `numberofthreads`              | `thread-count`                     | R2 (1 attr, flat), R5, R6              |
| `texturememory`                | `texture-memory`                   | R2 (1 attr, flat), R6                  |
| `networkcache.size`            | `network-cache.size`               | R6                                     |
| `networkcache.directory`       | `network-cache.directory`          | R6                                     |
| `networkcache.mipmap`          | `network-cache.mipmap`             | R6                                     |
| `networkcache.write`           | `network-cache.write`              | R6                                     |
| `renderatlowpriority`          | `low-priority`                     | R6, R9                                 |
| `bucketorder`                  | `bucket-order`                     | R6                                     |
| `hidemessages`                 | `messages.hide`                    | R2 (2 message attrs: hide + timestamp) |
| `maximumraydepth.diffuse`      | `diffuse.ray-depth-max`            | R1                                     |
| `maximumraydepth.hair`         | `hair.ray-depth-max`               | R1                                     |
| `maximumraydepth.reflection`   | `reflection.ray-depth-max`         | R1                                     |
| `maximumraydepth.refraction`   | `refraction.ray-depth-max`         | R1                                     |
| `maximumraydepth.volume`       | `volume.ray-depth-max`             | R1                                     |
| `maximumraylength.diffuse`     | `diffuse.ray-length-max`           | R1                                     |
| `maximumraylength.hair`        | `hair.ray-length-max`              | R1                                     |
| `maximumraylength.reflection`  | `reflection.ray-length-max`        | R1                                     |
| `maximumraylength.refraction`  | `refraction.ray-length-max`        | R1                                     |
| `maximumraylength.specular`    | `specular.ray-length-max`          | R1 (pattern consistency)               |
| `maximumraylength.volume`      | `volume.ray-length-max`            | R1                                     |
| `quality.denoise`              | `quality.denoise`                  | R8                                     |
| `quality.iprglobalupdate`      | `quality.preview.global-update`    | R8, R9                                 |
| `quality.iprinterpolate`       | `quality.preview.interpolate`      | R8, R9                                 |
| `quality.iprspeedmultiplier`   | `quality.preview.speed-multiplier` | R8, R9                                 |
| `quality.shadingsamples`       | `quality.shading-samples`          | R8, R6                                 |
| `quality.volumesamples`        | `quality.volume-samples`           | R8, R6                                 |
| `quality.samplevolumeemission` | `quality.volume-emission-sampling` | R8, R6                                 |
| `referencetime`                | `reference-time`                   | R6                                     |
| `show.displacement`            | `shading.displacement`             | R8                                     |
| `show.atmosphere`              | `shading.atmosphere`               | R8                                     |
| `show.multiplescattering`      | `shading.multiple-scattering`      | R8, R6                                 |
| `show.osl.subsurface`          | `shading.osl-subsurface`           | R8, R6                                 |
| `exclusiveshading`             | `exclusive-shading`                | R6                                     |
| `messages.timestamp`           | `messages.timestamp`               | —                                      |

**Unchanged:** `license.server`, `license.wait`, `license.hold`, `frame`, `statistics.progress`, `statistics.filename`, `verbose`

### `root` node

| Current              | New          | Rules                        |
| -------------------- | ------------ | ---------------------------- |
| `geometryattributes` | `attributes` | R6, R7 (multi-conn → plural) |

**Unchanged:** `objects`

### `set` node

**Unchanged:** `members`

### `mesh` node

| Current                           | New                            | Rules                           |
| --------------------------------- | ------------------------------ | ------------------------------- |
| `P`                               | `position`                     | R5                              |
| `nvertices`                       | `vertex-count`                 | R5, R6                          |
| `nholes`                          | `hole-count`                   | R5, R6                          |
| `clockwisewinding`                | `clockwise`                    | R6 (simplification)             |
| `subdivision.cornervertices`      | `subdivision.corner.index`     | R2 (3 corner attrs → sub-group) |
| `subdivision.cornersharpness`     | `subdivision.corner.sharpness` | R2                              |
| `subdivision.smoothcreasecorners` | `subdivision.corner.automatic` | R2                              |
| `subdivision.creasevertices`      | `subdivision.crease.index`     | R2 (2 crease attrs → sub-group) |
| `subdivision.creasesharpness`     | `subdivision.crease.sharpness` | R2                              |
| `referencetime`                   | `reference-time`               | R6                              |
| `quadraticmotion`                 | `quadratic-motion`             | R6                              |
| `outlinecreasethreshold`          | `outline-crease-threshold`     | R6                              |

**Unchanged:** `subdivision.scheme`

### `face-set` node

| Current | New          | Rules            |
| ------- | ------------ | ---------------- |
| `faces` | `face-index` | R9 (descriptive) |

### `curves` node

| Current     | New            | Rules  |
| ----------- | -------------- | ------ |
| `nvertices` | `vertex-count` | R5, R6 |
| `P`         | `position`     | R5     |

**Unchanged:** `width`, `basis`, `extrapolate`

### `particles` node

| Current              | New                   | Rules |
| -------------------- | --------------------- | ----- |
| `P`                  | `position`            | R5    |
| `N`                  | `normal`              | R5    |
| `reverseorientation` | `reverse-orientation` | R6    |
| `quadraticmotion`    | `quadratic-motion`    | R6    |

**Unchanged:** `width`, `id`

### `procedural` node

| Current       | New            | Rules |
| ------------- | -------------- | ----- |
| `boundingbox` | `bounding-box` | R6    |

### `environment` node

**Unchanged:** `angle`

### `shader` node

| Current          | New        | Rules                           |
| ---------------- | ---------- | ------------------------------- |
| `shaderfilename` | `filename` | R4 (node type provides context) |
| `shaderobject`   | `object`   | R4                              |

### `attributes` (geometry) node

| Current                     | New                         | Rules                           |
| --------------------------- | --------------------------- | ------------------------------- |
| `surfaceshader`             | `shader.surface`            | R2, R7 (single-conn → singular) |
| `displacementshader`        | `shader.displacement`       | R2, R7                          |
| `volumeshader`              | `shader.volume`             | R2, R7                          |
| `visibility.set.subsurface` | `visibility.subsurface-set` | R6                              |
| `regularemission`           | `emission.regular`          | R2 (2 emission attrs → group)   |
| `quantizedemission`         | `emission.quantized`        | R2                              |

**Unchanged:** `ATTR.priority`, `visibility.camera`, `visibility.diffuse`, `visibility.hair`, `visibility.reflection`, `visibility.refraction`, `visibility.shadow`, `visibility.specular`, `visibility.volume`, `visibility`, `matte`, `bounds`

### `transform` node

| Current                | New                 | Rules  |
| ---------------------- | ------------------- | ------ |
| `transformationmatrix` | `matrix`            | R4     |
| `geometryattributes`   | `attributes`        | R6, R7 |
| `shaderattributes`     | `shader-attributes` | R6     |

**Unchanged:** `objects`

### `instances` node

| Current                  | New              | Rules               |
| ------------------------ | ---------------- | ------------------- |
| `sourcemodels`           | `objects`        | R7 (multi-conn), R9 |
| `transformationmatrices` | `matrices`       | R4, R6              |
| `modelindices`           | `object-index`   | R6, R9              |
| `disabledinstances`      | `disabled-index` | R6                  |

### `output-driver` node

| Current           | New                | Rules |
| ----------------- | ------------------ | ----- |
| `drivername`      | `driver-name`      | R6    |
| `imagefilename`   | `filename`         | R4    |
| `embedstatistics` | `embed-statistics` | R6    |

### `output-layer` node

| Current           | New                | Rules                           |
| ----------------- | ------------------ | ------------------------------- |
| `variablename`    | `variable-name`    | R6                              |
| `variablesource`  | `variable-source`  | R6                              |
| `layername`       | `layer-name`       | R6                              |
| `scalarformat`    | `scalar-format`    | R6                              |
| `layertype`       | `layer-type`       | R6                              |
| `colorprofile`    | `color-profile`    | R6                              |
| `withalpha`       | `with-alpha`       | R6                              |
| `sortkey`         | `sort-key`         | R6                              |
| `lightset`        | `light-set`        | R6                              |
| `lightsetname`    | `light-set-name`   | R6                              |
| `outputdrivers`   | `output-drivers`   | R6, R7                          |
| `filterwidth`     | `filter.width`     | R2 (2 filter attrs → group)     |
| `filter`          | `filter.name`      | R2                              |
| `backgroundvalue` | `background.value` | R2 (2 background attrs → group) |
| `backgroundlayer` | `background.layer` | R2, R7 (single-conn)            |
| `lightdepth`      | `light-depth`      | R6                              |

**Unchanged:** `dithering`, `cryptomatte.enable`, `cryptomatte.level`

### `screen` node

| Current                  | New                        | Rules  |
| ------------------------ | -------------------------- | ------ |
| `outputlayers`           | `output-layers`            | R6, R7 |
| `prioritywindow`         | `priority-window`          | R6     |
| `screenwindow`           | `screen-window`            | R6     |
| `pixelaspectratio`       | `pixel-aspect-ratio`       | R6     |
| `staticsamplingpattern`  | `static-sampling-pattern`  | R6     |
| `importancesamplefilter` | `importance-sample-filter` | R6     |

**Unchanged:** `resolution`, `oversampling`, `crop`, `overscan`

### `vdb-particles` node

| Current                 | New                       | Rules                         |
| ----------------------- | ------------------------- | ----------------------------- |
| `vdbfilename`           | `filename`                | R4                            |
| `pointsgrid`            | `point-grid`              | R6, R12                       |
| `velocityreferencetime` | `velocity.reference-time` | R2 (2 velocity attrs → group) |
| `velocityscale`         | `velocity.scale`          | R2                            |
| `enablepscale`          | `use-point-scale`         | R9 (plain English)            |
| `widthscale`            | `width-scale`             | R6                            |

**Unchanged:** `width`

### `volume` node

| Current                 | New                       | Rules                     |
| ----------------------- | ------------------------- | ------------------------- |
| `vdbfilename`           | `filename`                | R4                        |
| `densitygrid`           | `grid.density`            | R2 (6 grid attrs → group) |
| `colorgrid`             | `grid.color`              | R2                        |
| `emissiongrid`          | `grid.emission`           | R2                        |
| `emissionintensitygrid` | `grid.emission-intensity` | R2, R6                    |
| `temperaturegrid`       | `grid.temperature`        | R2                        |
| `velocitygrid`          | `grid.velocity`           | R2                        |
| `velocityreferencetime` | `velocity.reference-time` | R2                        |
| `velocityscale`         | `velocity.scale`          | R2                        |

### Camera nodes (`perspective-camera`, `fisheye-camera`, `cylindrical-camera`)

**Common (all cameras):**

| Current          | New               | Rules                        |
| ---------------- | ----------------- | ---------------------------- |
| `screens`        | `screens`         | R7                           |
| `shutterrange`   | `shutter.range`   | R2 (2 shutter attrs → group) |
| `shutteropening` | `shutter.opening` | R2                           |
| `clippingrange`  | `clipping-range`  | R6                           |

**`perspective-camera`:**

| Current                         | New                                 | Rules   |
| ------------------------------- | ----------------------------------- | ------- |
| `fov`                           | `field-of-view`                     | R9      |
| `depthoffield.enable`           | `depth-of-field.enable`             | R6, R10 |
| `depthoffield.fstop`            | `depth-of-field.f-stop`             | R6      |
| `depthoffield.focallength`      | `depth-of-field.focal-length`       | R6      |
| `depthoffield.focallengthratio` | `depth-of-field.focal-length-ratio` | R6      |
| `depthoffield.focaldistance`    | `depth-of-field.focal-distance`     | R6      |
| `depthoffield.aperture.enable`  | `depth-of-field.aperture.enable`    | R6, R10 |
| `depthoffield.aperture.sides`   | `depth-of-field.aperture.sides`     | R6      |
| `depthoffield.aperture.angle`   | `depth-of-field.aperture.angle`     | R6      |
| `unitlengthmillimeters`         | `unit-length-millimeters`           | R6      |

**`fisheye-camera`:**

| Current | New             | Rules |
| ------- | --------------- | ----- |
| `fov`   | `field-of-view` | R9    |

**Unchanged:** `mapping`

**`cylindrical-camera`:**

| Current         | New                        | Rules                        |
| --------------- | -------------------------- | ---------------------------- |
| `fov`           | `field-of-view.vertical`   | R2 (2 fov attrs → group), R9 |
| `horizontalfov` | `field-of-view.horizontal` | R2, R6, R9                   |
| `eyeoffset`     | `eye-offset`               | R6                           |

## API Parameter Mapping

### `NSIBegin`

| Current                 | New                       | Rules                        |
| ----------------------- | ------------------------- | ---------------------------- |
| `streamfilename`        | `stream.filename`         | R2 (4 stream attrs → group)  |
| `streamformat`          | `stream.format`           | R2                           |
| `streamcompression`     | `stream.compression`      | R2                           |
| `streampathreplacement` | `stream.path-replacement` | R2, R6                       |
| `separateprocess`       | `separate-process`        | R6                           |
| `errorhandler`          | `callback.error`          | R11 (unified callback group) |
| `errorhandler.data`     | `callback.error.data`     | R11                          |
| `executeprocedurals`    | `evaluate-replace`        | R9                           |

**Unchanged:** `type`

### `NSIDelete`

**Unchanged:** `recursive`

### `NSIConnect`

**Unchanged:** `value`, `priority`, `strength`

### `NSIEvaluate`

| Current          | New               | Rules |
| ---------------- | ----------------- | ----- |
| `backgroundload` | `background-load` | R6    |

**Unchanged:** `type`, `filename`, `script`, `buffer`, `size`

### `NSIRenderControl`

| Current               | New                  | Rules                        |
| --------------------- | -------------------- | ---------------------------- |
| `stoppedcallback`     | `callback.stop`      | R11 (unified callback group) |
| `stoppedcallbackdata` | `callback.stop.data` | R11                          |

**Unchanged:** `action`, `progressive`, `interactive`, `frame`
