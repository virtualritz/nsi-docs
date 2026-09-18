# Implementer FAQ

Questions an implementer of ɴsɪ runs into when the specification is silent, or when it says one thing and 3Delight does another. Each answer gives the rule, what was observed, and what an implementation should do.

Unless stated otherwise, the observations come from 3Delight 2.9.207. Each was rendered, not read from documentation: a small scene, rendered twice with one change between the renders.

## Attributes and Priority

### Two attributes nodes on one node set the same attribute at the same priority. Which one applies?

**Answer.** The node connected *first* applies. The order of the `NSIConnect()` calls is part of the scene.

**Observed.** A plane with two sibling attributes nodes, one with `visibility.camera` 0 and one with 1. The plane is visible when the visible node is connected first, and hidden when the hidden node is connected first. Handle names and creation order run against the connection order, so they do not decide. The same rule applies to shaders: with a red and a green shader on two sibling attributes nodes, the plane takes the colour of the node connected first. 3Delight prints no warning in either case.

**For implementers.** Resolve the tie in connection order. Also *warn*, and list the definitions that were dropped: a scene whose look depends on call order is almost never intentional. The author can remove the ambiguity with `ATTR.priority`, or with a `priority` on the shader connection. See the [attributes node](nodes/attributes.md#geometry-attributes).

### Does a `priority` on a `geometryattributes` connection change which attributes node wins?

**Answer.** No. The `priority` of a connection has an effect only on shader connections, such as `surfaceshader`. To rank an attributes node, set `ATTR.priority` on that node.

**Observed.** The specification says both things. The `NSIConnect()` argument table says `priority` "indicates in which order the nodes should be considered". The attributes node page says connections can be assigned priorities "(for shaders, essentially)". 3Delight follows the second sentence:

```sh
Connect "near" "" "mesh" "geometryattributes"
Connect "far" "" "xf" "geometryattributes" "priority" "int" 1 [ 10 ]
SetAttribute "near" "visibility" "int" 1 [ 0 ]
SetAttribute "far" "visibility" "int" 1 [ 1 ]
```

The mesh stays hidden: `near` wins, and the connection priority has no effect. Replace the connection argument with `"visibility.priority" "int" 1 [ 10 ]` on `far` and the mesh is visible. `renderdl -cat` echoes the connection argument back, so the renderer parses it and then ignores it.

**For implementers.** Read the connection `priority` for the three shader slots. Ignore it on `geometryattributes`.

### An attributes node sets `ATTR.priority` but not `ATTR`. Does it define anything?

**Answer.** Yes. It defines `ATTR` at its default value, and that definition ranks with the given priority like any other.

**Observed.** An attributes node with only `visibility.priority` makes the geometry visible over a farther `visibility 0`, at priority 10 and also at priority 0. The same node two levels up, at priority 10, also wins over a `visibility 0` on the node attached to the geometry itself. So it does not win only because it is nearer. A node with no attributes defines nothing.

**For implementers.** Treat a lone `ATTR.priority` as a definition of `ATTR` with its default value.

### Which types does `ATTR.priority` accept?

**Answer.** Exactly one `int`. 3Delight ignores the priority when it has any other type or count, and then the definition ranks at priority 0.

**Observed.** An `int64` priority of 10 loses to a nearer definition with no priority. A priority written `"int" 2 [ 10 10 ]` or `"int[2]" 1 [ 10 10 ]` is also ignored.

**For implementers.** Accept a single `int`. Do not take the first value of a longer array, and do not convert an `int64`.

### Which wins: a far `visibility.camera` or a nearer `visibility`?

**Answer.** At equal priority, the far `visibility.camera`. The more specific attribute wins before proximity is compared.

**For implementers.** Rank the candidates by priority first, then by specificity (per-ray before `visibility`), then by distance from the geometry, then by connection order.

### Is an attribute value read strictly by its type?

**Answer.** No. 3Delight reads a value much more loosely than a priority. On `visibility`, a `float` 0.4 is visible and a `float` 0 is hidden, an `int64` 0 hides, and a `string` reads as *true*. A value of the wrong type is still a definition: it wins its ranking, so the renderer does not look further up the path.

**For implementers.** Do not treat a value of an unexpected type as "not defined". That shows the object where the renderer hides it, or the reverse.

### Are `set` nodes a source of attributes?

**Answer.** Yes, for `geometryattributes` and for `shaderattributes`, although the gathering rule names only geometry and transform nodes. Only direct membership counts.

**Observed.** For each node on the path from the geometry to the root, the order is:

1. The node's own attributes nodes.
2. The attributes nodes on the sets the node is directly a member of, in the order of the memberships.
3. The next node up the path.

A set inside another set contributes nothing. A set that holds two nodes of the path counts once, at the nearer node. `ATTR.priority` still ranks above all of this.

**For implementers.** Gather set containers at each level, with direct membership only.

### A geometry has two parents. Which attributes apply?

**Answer.** Each path to the root applies its own attributes. Connecting a geometry to two transforms draws it twice, and each copy gathers attributes along its own path.

**Observed.** One parent with `visibility 1` and one with `visibility 0` draws one copy, not two and not none.

**For implementers.** Resolve attributes per path, not per geometry.

## Types and Motion

### What happens to motion samples when one sample has the wrong type?

**Answer.** The wrong sample *unsets* the attribute and discards every sample before it. Only the samples set after it remain.

**Observed.** A good `doublematrix` at `t=0`, a `float` at `t=1` and a good `doublematrix` at `t=2` draw a static object at the `t=2` matrix. 3Delight warns `E6007`. Without the `float`, the object moves across the frame.

**For implementers.** Do not skip the bad sample and keep the others. That shows motion blur that the renderer does not draw.

### Is `"double" 16 [...]` a matrix?

**Answer.** No. `transformationmatrix` must be a `doublematrix`. With sixteen `double` values, 3Delight warns `E6007` and draws the node at the identity transform. In a stream, the type name for an integer is `int`: `"integer"` is rejected with `E1000` and the call is skipped.

### Can a Lua script pass an `int64` or a `double`?

**Answer.** Not in 3Delight 2.9.210. `nsi.TypeInt64`, `nsi.TypeDouble` and `nsi.TypePointer` are `nil`, so an argument that names one of them has no type. The renderer then infers a type and changes the value without an error.

**Observed.** With `renderdl -lua -cat`, `data=9007199254740993, type=nsi.TypeInt64` is written as `"int" 1 1`, and `data=0.1, type=nsi.TypeDouble` is written as a `float`.

**For implementers.** Define all type constants in the Lua binding, including the 64-bit ones. A value that cannot be represented should be an error, not a silent conversion. See the [Lua API](lua-api.md).

## The Stream Format

### Is the stream line-based?

**Answer.** No. The stream is a sequence of tokens. A complete scene on one line parses. A parameter list ends at the next *bare* token that is a statement keyword. Parameter names are always quoted, so this is not ambiguous. Whitespace runs are free, and `#` starts a comment that ends at the end of the line.

**Observed.** `renderdl -cat` reads `Create "a" "transform" Create "b" "mesh" SetAttribute "b" "fov" "float" 1 45` as separate statements.

### Which escapes does a string accept?

**Answer.** 3Delight writes `\"`, `\\`, `\t` and `\n` by name, each other byte below `0x20` as three octal digits, such as `\001`, and each byte at or above `0x7f` unchanged. It reads octal escapes of one to three digits. There is no `\x`.

**For implementers.** A string is a sequence of bytes, not UTF-8 text. A file name in Latin-1 is valid, so do not reject it.

### Does a reader expand `${VAR}` in a string?

**Answer.** No. The value stays as written in the stream. 3Delight expands the reference when it *uses* the value, for example when it opens a file. Every variable expands, not only variables whose name starts with `NSI_PATH_`. That prefix only controls which paths `streampathreplacement` writes as references.

**Observed.** `renderdl -cat` echoes `${NSI_PATH_TEST}/out.exr` unchanged. A render with that `imagefilename` writes to the expanded path.

**For implementers.** Keep the reference in a stream that you read and write again. Expand it where you open the file.

### Why does a stream I wrote not start with text?

**Answer.** With the `autonsi` format, which is the default, 3Delight writes `binarynsi` unless the file name ends in `.nsia`. The binary encoding is not documented. Its files start with the bytes `cc 00`. To get text, name the file `.nsia` or convert the file with `renderdl -cat`.

## Threads

### Can I make calls on one context from many threads?

**Answer.** 3Delight accepts calls from several threads. But 3Delight 2.9 runs the calls on one context one at a time, so more threads do not make them faster.

**Observed.** 20,000 `SetAttribute` calls on existing meshes take 11.8 ms from one thread and 21.4 ms from sixteen threads. 20,000 `Create` calls take 11.4 ms and 10.8 ms.

**For implementers.** To load a scene faster, do the parsing on other threads and send the calls in order. If calls on your implementation can run concurrently, the order still matters: `Create` before use, and `Connect` calls into one attribute in stream order (see the first question).
