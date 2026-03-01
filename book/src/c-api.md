# The C API

This section describes the C implementation of the ɴsɪ, as provided in the \[nsi.h\](nsi.h.md) file. This will also be a reference for the interface in other languages as all concepts are the same.

```c
#define NSI_VERSION 1
```

The `NSI_VERSION` macro exists in case there is a need at some point to break source compatibility of the C interface.

```c
#define NSI_SCENE_ROOT ".root"
```

The `NSI_SCENE_ROOT` macro defines the handle of the \[root node\](nodes.md#node-root).

```c
#define NSI_ALL_NODES ".all"
```

The `NSI_ALL_NODES` macro defines a special handle to refer to all nodes in some contexts, such as \[removing connections\](c-api.md#capi-nsiconnect).

```c
#define NSI_ALL_ATTRIBUTES ".all"
```

The `NSI_ALL_ATTRIBUTES` macro defines a special handle to refer to all attributes in some contexts, such as \[removing connections\](c-api.md#capi-nsiconnect).

## Context Handling

```c
NSIContext_t NSIBegin(
   int n_params,
   const NSIParam_t *args
)
```

```c
void NSIEnd(
   NSIContext_t ctx
)
```

These two functions control creation and destruction of a ɴsɪ context, identified by a handle of type `NSIContext_t`.

A context must be given explicitly when calling all other functions of the interface. Contexts may be used in multiple threads at once. The `NSIContext_t` is a convenience typedef and is defined as:

```c
typedef int NSIContext_t;
```

If `NSIBegin` fails for some reason, it returns `NSI_BAD_CONTEXT` which is defined in \[nsi.h\](nsi.h.md):

```c
#define NSI_BAD_CONTEXT ((NSIContext_t)0)
```

\[Optional arguments\](c-api.md#capi-optionalarguments) may be given to `NSIBegin()` to control the creation of the context:

<table style="width:14%;">
<caption>NSIBegin() optional arguments</caption>
<colgroup>
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 2%" />
<col style="width: 5%" />
</colgroup>
<tbody>
<tr class="odd">
<td rowspan="4"><blockquote>
<p><strong>Name</strong></p>
</blockquote>
<dl>
<dt>============================</dt>
<dd>
<p><code>type</code></p>
</dd>
</dl></td>
<td rowspan="4"><blockquote>
<p><strong>Type</strong></p>
</blockquote>
<dl>
<dt>==========</dt>
<dd>
<p>string</p>
</dd>
</dl></td>
<td colspan="2" rowspan="2"><blockquote>
<p><strong>Description/Values</strong></p>
</blockquote>
<dl>
<dt>================================================</dt>
<dd>
<p>Sets the type of context to create. The possibletypes are:</p>
</dd>
</dl></td>
</tr>
<tr class="even">
</tr>
<tr class="odd">
<td><code>render</code></td>
<td>Execute the calls directly in the renderer. This is the <strong>default</strong>.</td>
</tr>
<tr class="even">
<td><code>apistream</code></td>
<td>To write the interface calls to a stream, for later execution. The target for writing the stream must be specified in another argument.</td>
</tr>
<tr class="odd">
<td><p><code>streamfilename</code></p>
<p><code>stream.filename</code> (!)</p></td>
<td>string</td>
<td colspan="2">The file to which the stream is to be output, if the context type is <code>apistream</code>. Specify <code>stdout</code> to write to standard output and <code>stderr</code> to write to standard error.</td>
</tr>
<tr class="even">
<td rowspan="3"><p><code>streamformat</code></p>
<p><code>stream.format</code> (!)</p></td>
<td rowspan="3">string</td>
<td colspan="2">The format of the command stream to write. Possible formats are:</td>
</tr>
<tr class="odd">
<td><code>nsi</code></td>
<td>Produces an [nsi | stream](stream-api.md#section-nsistream)</td>
</tr>
<tr class="even">
<td><code>binarynsi</code></td>
<td>Produces a binary encoded | [nsi | stream](stream-api.md#section-nsistream)</td>
</tr>
<tr class="odd">
<td><p><code>stream.compression</code></p>
<p><code>stream.compression</code> (!)</p></td>
<td>string</td>
<td colspan="2">The type of compression to apply to the written command stream.</td>
</tr>
<tr class="even">
<td><p><code>streampathreplacement</code></p>
<p><code>stream.path.replace</code></p></td>
<td>int</td>
<td colspan="2">Use <code>0</code> to disable replacement of path | prefixes by references to environment | variables which begin with <code>NSI_PATH_</code> in an | ɴsɪ stream. | This should generally be left enabled to ease | creation of files which can be moved between | systems. |</td>
</tr>
<tr class="odd">
<td><code>errorhandler</code></td>
<td>pointer</td>
<td colspan="2">A function which is to be called by the renderer to report errors. The default handler will print messages to the console.</td>
</tr>
<tr class="even">
<td><code>errorhandler.data</code></td>
<td>pointer</td>
<td colspan="2">The <code>userdata</code> argument of the [error | reporting function](c-api.md#capi-errorcallback). |</td>
</tr>
<tr class="odd">
<td><p><code>executeprocedurals</code></p>
<p><code>evaluate.replace</code> (!)</p></td>
<td>string</td>
<td colspan="2">A list of procedural types that should be | executed immediately when a call to | [NSIEvaluate() ](c-api.md#capi-nsievaluate) or a | procedural node is encountered and | <code>NSIBegin()</code>'s output <code>type</code> is | <code>apistream</code>. This will replace any matching | call to <code>NSIEvaluate()</code> with the results of | the procedural's execution. |</td>
</tr>
</tbody>
</table>

NSIBegin() optional arguments

## Arguments vs. Attributes {#arguments-vs.-attributes}

Arguments are what a user specifies when calling a function of the API. Each function takes extra, optional arguments.

Attributes are properties of nodes and are only set _through_ the aforementioed optional arguments using the `NSISetAttribute()` and `NSISetAttributeAtTime()` functions.

### Optional Arguments

Any API call can take extra arguments. These are always optional. What this means the call can do work without the user specifying these arguments.

Nodes are special as they have mandatory extra **attributes** that are set _after_ the node is created inside the API but which must be set _before_ the geometry or concept the node represents can actually be created in the scene.

These attributes are passed as extra arguments to the `NSISetAttribute()` and `NSISetAttributeAtTime()` functions.

> [!NOTE]
> Nodes can also take extra **arguments** when they are created. These optional arguments are only meant to add information needed to create the node that a particular implementation may need.
>
> **As of this writing there is no implementation that has any such optional arguments on the** `NSICreate()` **function.** The possibility to specify them is solely there to make the API future proof.

> [!CAUTION]
> Nodes do _not_ have optional arguments for now. **An optional argument on a node is not the same as an attribute on a node.**

### Attributes -- Describe the Node\'s Specifics {#attributes-describe-the-nodes-specifics}

Attributes are _only_ for nodes. They must be set using the `NSISetAttribute()` or `NSISetAttributeAtTime()` functions.

They can **not** be set on the node when it is created with the `NSICreate()` function.

> [!CAUTION]
> **Only nodes have attributes.** They are sent to the API via optional arguments on the API\'s attribute functions.

## Passing Optional Arguments

```c
struct NSIParam_t
{
    const char *name;
    const void *data;
    int type;
    int arraylength;
    size_t count;
    int flags;
};
```

This structure is used to pass variable argument lists through the C   interface. Most functions accept an array of the structure in a `args` argument along with its length in a `n_params` argument.

The meaning of these two arguments will not be documented for every function. Instead, each function will document the arguments which can be given in the array.

`name`  
  A C string which gives the argument\'s name.

`type`  
  Identifies the argument\'s type, using one of the following constants:

> |                       |                                                                                      |
> | --------------------- | ------------------------------------------------------------------------------------ |
> | `NSITypeFloat`        | Single 32-bit floating point value.                                                  |
> | `NSITypeDouble`       | Single 64-bit floating point value.                                                  |
> | `NSITypeInteger`      | Single 32-bit integer value.                                                         |
> | `NSITypeString`       | String value, given as a pointer to a C   string. \|                                 |
> | `NSITypeColor`        | Color, given as three 32-bit floating point values.                                  |
> | `NSITypePoint`        | Point, given as three 32-bit floating point values.                                  |
> | `NSITypeVector`       | Vector, given as three 32-bit floating point values.                                 |
> | `NSITypeNormal`       | Normal vector, given as three 32-bit floating point values.                          |
> | `NSITypeMatrix`       | Transformation matrix, in row-major order, given as 16 32-bit floating point values. |
> | `NSITypeDoubleMatrix` | Transformation matrix, in row-major order, given as 16 64-bit floating point values. |
> | `NSITypePointer`      | C   pointer. \|                                                                      |
>
> types of optional arguments

Tuple types are specified by setting the bit defined by the `NSIArgIsArray` constant in the `flags` member and the length of the tuple in the `arraylength` member.

> [!TIP]
> It helps to view `arraylength` as a part of the data type. The data type is a tuple with this length when `NSIArgIsArray` is set.

> [!NOTE]
> If `NSIArgIsArray` is not set, `arraylength` is _ignored_.
>
> The `NSIArgIsArray` flag is neccessary to distinguish between arguments that happen to be of _length_ 1 (set in the `count` member) and tuples that have a _length_ of 1 (set in the `arraylength` member) for the resp. argument.
>
> ```{.shell caption="A tuple argument of length 1 (and count 1) vs. a (non-tuple) argument of count 1"}
> "foo" "int[1]" 1 [42]  # The answer to the ultimate question – in an a (single) tuple
> "bar" "int" 1 13       # My favorite Friday
> ```

The `count` member gives the number of data items given as the value of the argument.

The `data` member is a pointer to the data for the argument. This is a pointer to a single value or a number values. Depending on `type`, `count` and `arraylength` settings.

> [!NOTE]
> When data is an array, the actual number of elements in the array is $count\times arraylength\times n$. Where $n$ is specified implictly through the `type` member in the table above.
>
> For example, if the type is `NSITypeColor` (**3** values), `NSIArgIsArray` is set, `arraylength` is **2** and `count` is **4**, `data` is expected to contain **24** 32-bit floating point values ($3\times2\times4$).

The `flags` member is a bit field with a number of constants used to communicate more information about the argument:

|                           |                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `NSIArgIsArray`           | to specify that the argument is an array type, as explained above.                                                        |
| `NSIArgPerFace`           | to specify that the argument has different values for every face of a geometric primitive, where this might be ambiguous. |
| `NSIArgPerVertex`         | Specify that the argument has different values for every vertex of a geometric primitive, where this might be ambiguous.  |
| `NSIArgInterpolateLinear` | Specify that the argument is to be interpolated linearly instead of using some other, default method.                     |

flags for optional arguments

> [!NOTE]
> `NSIArgPerFace` or `NSIArgPerVertex` are only strictly needed in rare circumstances when a geometric primitive\'s number of vertices matches the number of faces. The most simple case is a tetrahedral mesh which has exactly four vertices and also four faces.

Indirect lookup of arguments is achieved by giving an integer argument of the same name, with the `.indices` suffix added. This is read to know which values of the other argument to use.

``{.shell caption="A subdivision mesh using`P.indices`to reference the`P`` argument" linenos=""}
Create "subdiv" "mesh"
SetAttribute "subdiv"
"nvertices" "int" 4 [ 4 4 4 4 ]
"P" "point" 9 [
0 0 0 1 0 0 2 0 0
0 1 0 1 1 0 2 1 0
0 2 0 1 2 0 2 2 2 ]
"P.indices" "int" 16 [
0 1 4 3 2 3 5 4 3 4 7 6 4 5 8 7 ]
"subdivision.scheme" "string" 1 "catmull-clark"

````

## Node Creation

``` c
void NSICreate(
    NSIContext_t context,
    NSIHandle_t handle,
    const char *type,
    int n_params,
    const NSIParam_t *args
)
````

This function is used to create a new node. Its arguments are:

`context`  
  The context returned by `NSIBegin()`. See \[context handling\](c-api.md#capi-contexthandling).

`handle`  
  A node handle. This string will uniquely identify the node in the scene.

> If the supplied handle matches an existing node, the function does nothing if all other arguments match the call which created that node. Otherwise, it emits an error. Note that handles need only be unique within a given interface context. It is acceptable to reuse the same handle inside different contexts. The `NSIHandle_t` typedef is defined in \[nsi.h\](nsi.h.md):
>
> ```c
> typedef const char* NSIHandle_t;
> ```

`type`  
  The type of \[node\](nodes.md#chapter-nodes) to create.

`n_params`, `args` This pair describes a list of optional arguments. The `NSIParam_t` type is described in \[this section\](c-api.md#capi-optionalarguments).

> [!CAUTION]
> There are _no_ optional arguments defined as of now.

---

```c
void NSIDelete(
    NSIContext_t ctx,
    NSIHandle_t handle,
    int n_params,
    const NSIParam_t *args
)
```

This function deletes a node from the scene. All connections to and from the node are also deleted. Note that it is not possible to delete the \[root\](nodes.md#node-root) or the \[global\](nodes.md#node-global) node. Its arguments are:

`context`  
  The context returned by `NSIBegin()`. See \[context handling\](c-api.md#capi-contexthandling).

`handle`  
  A node handle. It identifies the node to be deleted.

It accepts the following optional arguments:

<table style="width:15%;">
<caption>NSIDelete() optional arguments</caption>
<colgroup>
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 8%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Name</strong></th>
<th><strong>Type</strong></th>
<th><strong>Description/Values</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><code>recursive</code></td>
<td>int</td>
<td><p>Specifies whether deletion is recursive. By default, only the specified node is deleted. If a value of <code>1</code> is given, then nodes which connect to the specified node are recursively removed. Unless they meet one of the following conditions:</p>
<ul>
<li>They also have connections which do not eventually lead to the specified node.</li>
<li>Their connection to the deleted node was created with a <code>strength</code> greater than <code>0</code>.</li>
</ul>
<p>This allows, for example, deletion of an entire shader network in a single call.</p></td>
</tr>
</tbody>
</table>

NSIDelete() optional arguments

## Setting Attributes

```c
void NSISetAttribute(
    NSIContext_t ctx,
    NSIHandle_t object,
    int n_params,
    const NSIParam_t *args
)
```

This functions sets attributes on a previously node. All \[optional arguments \](c-api.md#capi-optionalarguments) of the function become attributes of the node.

On a \[shader node\](nodes.md#node-shader), this function is used to set the implicitly defined shader arguments.

Setting an attribute using this function replaces any value previously set by `NSISetAttribute()` or `NSISetAttributeAtTime()`. To reset an attribute to its default value, use NSIDeleteAttribute() .

---

```c
void NSISetAttributeAtTime(
    NSIContext_t ctx,
    NSIHandle_t object,
    double time,
    int n_params,
    const NSIParam_t *args
)
```

This function sets time-varying attributes (i.e. motion blurred). The `time` argument specifies at which time the attribute is being defined.

It is not required to set time-varying attributes in any particular order. In most uses, attributes that are motion blurred must have the same specification throughout the time range.

A notable exception is the `P` attribute on \[particles \](nodes.md#node-particles) which can be of different size for each time step because of appearing or disappearing particles. Setting an attribute using this function replaces any value previously set by `NSISetAttribute()`.

---

```c
void NSIDeleteAttribute(
    NSIContext_t ctx,
    NSIHandle_t object,
    const char *name
)
```

This function deletes any attribute with a name which matches the `name` argument on the specified object. There is no way to delete an attribute only for a specific time value.

Deleting an attribute resets it to its default value.

For example, after deleting the `transformationmatrix` attribute on a \[transform node \](nodes.md#node-transform), the transform will be an identity. Deleting a previously set attribute on a \[shader node\](nodes.md#node-shader) node will default to whatever is declared inside the shader.

## Making Connections

```c
void NSIConnect(
    NSIContext_t ctx,
    NSIHandle_t from,
    const char *from_attr,
    NSIHandle_t to,
    const char *to_attr,
    int n_params,
    const NSIParam_t *args
)
```

```c
void NSIDisconnect(
    NSIContext_t ctx,
    NSIHandle_t from,
    const char *from_attr,
    NSIHandle_t to,
    const char *to_attr
)
```

These two functions respectively create or remove a connection between two elements. It is not an error to create a connection which already exists or to remove a connection which does not exist but the nodes on which the connection is performed must exist. The arguments are:

`from`  
  The handle of the node from which the connection is made.

`from_attr`  
  The name of the attribute from which the connection is made. If this is an empty string then the connection is made from the node instead of from a specific attribute of the node.

`to`  
  The handle of the node to which the connection is made. \|

`to_attr`  
  The name of the attribute to which the connection is made. If this is an empty string then the connection is made to the node instead of to a specific attribute of the node.

`NSIConnect()` accepts additional optional arguments.

<table style="width:14%;">
<caption>NSIConnect() optional arguments</caption>
<colgroup>
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 8%" />
</colgroup>
<tbody>
<tr class="odd">
<td rowspan="2"><blockquote>
<p><strong>Name</strong></p>
</blockquote>
<dl>
<dt>========================</dt>
<dd>
<p><code>value</code></p>
</dd>
</dl></td>
<td rowspan="2"><blockquote>
<p><strong>Type</strong></p>
</blockquote>
<hr /></td>
<td rowspan="2"><blockquote>
<p><strong>Description/Values</strong> |</p>
</blockquote>
<dl>
<dt>====================================================+</dt>
<dd>
<p>This can be used to change the value of a node's | attribute in some contexts. Refer to | [guidelines on inter-object | visibility](guidelines.md#section-lightlinking) for more information about the utility of this parameter. |</p>
</dd>
</dl></td>
</tr>
<tr class="even">
</tr>
<tr class="odd">
<td><code>priority</code></td>
<td></td>
<td>When connecting attribute nodes, indicates in which order the nodes should be considered when evaluating the value of an attribute.</td>
</tr>
<tr class="even">
<td><code>strength</code></td>
<td>int (0)</td>
<td>A connection with a strength greater than <code>0</code> will <em>block</em> the progression of a recursive <code>NSIDelete</code>.</td>
</tr>
</tbody>
</table>

NSIConnect() optional arguments

## Severing Connections

With `NSIDisconnect()`, the handle for either node may be the special value \[\'.all\'\](c-api.md#capi-dotall). This will remove all connections which match the other three arguments. For example, to disconnect everything from \[the scene\'s root\](nodes.md#node-root):

```{.c linenos=""}
NSIDisconnect( NSI_ALL_NODES, "", NSI_SCENE_ROOT, "objects" );
```

## Evaluating Procedurals

```c
void NSIEvaluate(
    NSIContext_t ctx,
    int n_params,
    const NSIParam_t *args
)
```

This function includes a block of interface calls from an external source into the current scene. It blends together the concepts of a straight file include, commonly known as an archive, with that of procedural include which is traditionally a compiled executable. Both are really the same idea expressed in a different language (note that for delayed procedural evaluation one should use the \[procedural node\](nodes.md#node-procedural)).

The ɴsɪ adds a third option which sits in-between --- \[Lua scripts \](lua-api.md#section-lua). They are much more powerful than a simple included file yet they are also much easier to generate as they do not require compilation. It is, for example, very realistic to export a whole new script for every frame of an animation. It could also be done for every character in a frame. This gives great flexibility in how components of a scene are put together.

The ability to load ɴsɪ commands straight from memory is also provided.

The optional arguments accepted by this function are:

<table style="width:14%;">
<caption>NSIEvaluate() optional arguments</caption>
<colgroup>
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 2%" />
<col style="width: 5%" />
</colgroup>
<tbody>
<tr class="odd">
<td rowspan="5"><blockquote>
<p><strong>Name</strong></p>
</blockquote>
<dl>
<dt>========================</dt>
<dd>
<p><code>type</code></p>
</dd>
</dl></td>
<td rowspan="5"><blockquote>
<p><strong>Type</strong></p>
</blockquote>
<dl>
<dt>==========</dt>
<dd>
<p>string</p>
</dd>
</dl></td>
<td colspan="2" rowspan="2"><blockquote>
<p><strong>Description/Values</strong></p>
</blockquote>
<dl>
<dt>====================================================</dt>
<dd>
<p>The type of file which will generate the interface calls. This can be one of:</p>
</dd>
</dl></td>
</tr>
<tr class="even">
</tr>
<tr class="odd">
<td><code>apistream</code></td>
<td>Read in an [nsi | stream](stream-api.md#section-nsistream). | This requires either | <code>filename</code> or | <code>buffer</code>/<code>size</code> | arguments to be specified | too. |</td>
</tr>
<tr class="even">
<td><code>lua</code></td>
<td>Execute a | [Lua](lua-api.md#section-lua) | script, either from file or | inline. See also | [how to evaluate a Lua | script](lua-api.md#luaapi-evaluation). |</td>
</tr>
<tr class="odd">
<td><code>dynamiclibrary</code></td>
<td>Execute native compiled code | in a loadable library. See | [dynamic library | procedurals | ](procedurals.md#section-procedurals) for an implementation example. |</td>
</tr>
<tr class="even">
<td><p><code>filename</code></p>
<p><code>stream.filename</code> (!)</p></td>
<td>string</td>
<td colspan="2">The file from which to read the interface stream.</td>
</tr>
<tr class="odd">
<td><code>script</code></td>
<td>string</td>
<td colspan="2">A valid [Lua](lua-api.md#section-lua) script to execute | when <code>type</code> is set to <code>lua</code>. |</td>
</tr>
<tr class="even">
<td><p><code>buffer</code></p>
<p><code>size</code></p></td>
<td><p>pointer</p>
<p>int</p></td>
<td colspan="2">These two arguments define a memory block that | contains ɴsɪ commands to execute. | |</td>
</tr>
<tr class="odd">
<td><code>backgroundload</code></td>
<td>int</td>
<td colspan="2">If this is nonzero, the object may be loaded in a separate thread, at some later time. This requires that further interface calls not directly reference objects defined in the included file. The only guarantee is that the the file will be loaded before rendering begins.</td>
</tr>
</tbody>
</table>

NSIEvaluate() optional arguments

## Error Reporting

```c
enum NSIErrorLevel
{
    NSIErrMessage = 0,
    NSIErrInfo = 1,
    NSIErrWarning = 2,
    NSIErrError = 3
}
```

```c
typedef void (*NSIErrorHandler_t)(
    void *userdata, int level, int code, const char *message
)
```

This defines the type of the error handler callback given to the `NSIBegin()` function. When it is called, the `level` argument is one of the values defined by the `NSIErrorLevel` enum. The `code` argument is a numeric identifier for the error message, or 0 when irrelevant. The `message` argument is the text of the message.

The text of the message will not contain the numeric identifier nor any reference to the error level. It is usually desirable for the error handler to present these values together with the message. The identifier exists to provide easy filtering of messages.

The intended meaning of the error levels is as follows:

|                 |                                                                                                                                                                                                                                                           |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NSIErrMessage` | For general messages, such as may be produced by `printf()` in shaders. The default error handler will print this type of messages without an eol terminator as it's the duty of the caller to format the message.                                        |
| `NSIErrInfo`    | For messages which give specific information. These might simply inform about the state of the renderer, files being read, settings being used and so on.                                                                                                 |
| `NSIErrWarning` | For messages warning about potential problems. These will generally not prevent producing images and may not require any corrective action. They can be seen as suggestions of what to look into if the output is broken but no actual error is produced. |
| `NSIErrError`   | For error messages. These are for problems which will usually break the output and need to be fixed.                                                                                                                                                      |

error levels

## Rendering

```c
void NSIRenderControl(
    NSIContext_t ctx,
    int n_params,
    const NSIParam_t *args
)
```

This function is the only control function of the API. It is responsible of starting, suspending and stopping the render. It also allows for synchronizing the render with interactive calls that might have been issued. The function accepts :

| **Name** | **Type** | **Description/Values**                                                         |                                                                                                                             |
| -------- | -------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `action` | string   | Specifies the operation to be performed, which should be one of the following: |                                                                                                                             |
|          |          | `start`                                                                        | This starts rendering the scene in the provided context. The render starts in parallel and the control flow is not blocked. |
|          |          | `wait`                                                                         | Wait for a render to finish.                                                                                                |
|          |          | `synchronize`                                                                  | For an interactive render, apply all the buffered calls to scene's state.                                                   |
|          |          | `suspend`                                                                      | Suspends render in the provided context.                                                                                    |
|          |          | `resume`                                                                       | Resumes a previously suspended render.                                                                                      |
|          |          | `stop`                                                                         | Stops rendering in the provided context without destroying the scene.                                                       |

NSIRenderControl() intrinsic argument

<table style="width:14%;">
<caption>NSIRenderControl() optional arguments</caption>
<colgroup>
<col style="width: 4%" />
<col style="width: 1%" />
<col style="width: 8%" />
</colgroup>
<tbody>
<tr class="odd">
<td><code>progressive</code></td>
<td>integer</td>
<td>If set to <code>1</code>, render the image in a progressive fashion.</td>
</tr>
<tr class="even">
<td><code>interactive</code></td>
<td>integer</td>
<td><div id="section:rendering:interactive">
<p>If set to <code>1</code>, the renderer will accept commands to edit scene’s state while rendering. The difference with a normal render is that the render task will not exit even if rendering is finished. Interactive renders are by definition progressive.</p>
</div></td>
</tr>
<tr class="odd">
<td><code>frame</code></td>
<td></td>
<td>Specifies the frame number of this render.</td>
</tr>
<tr class="even">
<td><p><code>stoppedcallback</code></p>
<p><code>callback</code> (!)</p></td>
<td>pointer</td>
<td><p>A pointer to a user function that should be called on rendering status changes. This function must have no return value and accept a pointer argument, a ɴsɪ context argument and an integer | argument:</p>
<div class="sourceCode" id="cb1"><pre class="sourceCode c"><code class="sourceCode c"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="dt">void</span> StoppedCallback<span class="op">(</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>    <span class="dt">void</span><span class="op">*</span> stoppedcallbackdata<span class="op">,</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>    NSIContext_t ctx<span class="op">,</span></span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a>    <span class="dt">int</span> status</span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a><span class="op">)</span></span></code></pre></div>
<p>The third argument is an integer which can take the following values:</p>
<ul>
<li><code>NSIRenderCompleted</code> indicates that rendering has completed normally.</li>
<li><code>NSIRenderAborted</code> indicates that rendering was interrupted before completion.</li>
<li><code>NSIRenderSynchronized</code> indicates that an interactive render has produced an image which reflects all changes to the scene.</li>
<li><code>NSIRenderRestarted</code> indicates that an interactive render has received new changes to the scene and no longer has an up to date image.</li>
</ul></td>
</tr>
<tr class="odd">
<td><p><code>stoppedcallbackdata</code></p>
<p><code>callback.data</code> (!)</p></td>
<td>pointer</td>
<td>A pointer that will be passed back to the <code>stoppedcallback</code> function.</td>
</tr>
</tbody>
</table>

NSIRenderControl() optional arguments
