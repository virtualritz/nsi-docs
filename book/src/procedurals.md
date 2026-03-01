# Dynamic Library Procedurals

and nodes can execute code loaded from a dynamically loaded library that defines a procedural. Executing the procedural is expected to result in a series of ɴsɪ API calls that contribute to the description of the scene. For example, a procedural could read a part of the scene stored in a different file format and translate it directly into ɴsɪ calls.

This section describes how to use the definitions from the \[nsi_procedural.h\](nsi_procedural.h.md) header to write such a library in C or C++. However, the process of compiling and linking it is specific to each operating system and out of the scope of this manual.

## Entry Point

The renderer expects a dynamic library procedural to contain a `NSIProceduralLoad()` symbol, which is an entry point for the library's main function:

```c
struct NSIProcedural_t* NSIProceduralLoad(
    NSIContext_t ctx,
    NSIReport_t report,
    const char* nsi_library_path,
    const char* renderer_version);
```

It will be called only once per render and has the responsibility of initializing the library and returning a description of the functions implemented by the procedural. However, it is not meant to generate nsi calls.

It returns a pointer to an descriptor struct of type `NSIProcedural_t` (see \[below\](procedurals.md#capi-proceduraldescription)).

`NSIProceduralLoad()` receives the following arguments:

<table style="width:14%;">
<caption>NSIProceduralLoad() optional arguments</caption>
<colgroup>
<col style="width: 2%" />
<col style="width: 1%" />
<col style="width: 9%" />
</colgroup>
<tbody>
<tr class="odd">
<td rowspan="2"><blockquote>
<p><strong>Name</strong></p>
</blockquote>
<dl>
<dt>======================</dt>
<dd>
<p><code>ctx</code></p>
</dd>
</dl></td>
<td rowspan="2"><blockquote>
<p><strong>Type</strong></p>
</blockquote>
<dl>
<dt>==================</dt>
<dd>
<p><code>NSIContext_t</code></p>
</dd>
</dl></td>
<td rowspan="2"><blockquote>
<p><strong>Description</strong> |</p>
</blockquote>
<dl>
<dt>==============================================+</dt>
<dd>
<p>The ɴsɪ context into which the procedural | is being loaded. |</p>
</dd>
</dl></td>
</tr>
<tr class="even">
</tr>
<tr class="odd">
<td><code>report</code></td>
<td><code>NSIReport_t</code></td>
<td>A function that can be used to display informational, warning or error messages through the renderer.</td>
</tr>
<tr class="even">
<td><code>nsi_library_path</code></td>
<td><code>const char*</code></td>
<td>The path to the ɴsɪ implementation that is | loading the procedural. This allows the | procedural to explicitly make its ɴsɪ API | calls through the same implementation (for | example, by using defined in | [nsi_dynamic.hpp](nsi_dynamic.hpp.md)). It’s usually not required if only one implementation of ɴsɪ | is installed on the system. |</td>
</tr>
<tr class="odd">
<td><code>renderer_version</code></td>
<td><code>const char*</code></td>
<td>A character string describing the current version of the renderer.</td>
</tr>
</tbody>
</table>

NSIProceduralLoad() optional arguments

## Procedural Description

``{.c caption="definition of`NSIProcedural_t``"}
typedef void (_NSIProceduralUnload_t)(
NSIContext_t ctx,
NSIReport_t report,
struct NSIProcedural_t_ proc);

typedef void (_NSIProceduralExecute_t)(
NSIContext_t ctx,
NSIReport_t report,
struct NSIProcedural_t_ proc,
int n_args,
const struct NSIParam_t\* args);

struct NSIProcedural_t
{
unsigned nsi_version;
NSIProceduralUnload_t unload;
NSIProceduralExecute_t execute;
};

````

The structure returned by `NSIProceduralLoad()` contains information needed by the renderer to use the procedural.

> [!NOTE]
> The allocation of this structure is managed entirely from within the procedural and it will *never* be copied or modified by the renderer.

> [!TIP]
> This means that it is possible for a procedural to extend the structure (by over-allocating memory or subclassing, for example) in order to store any **extra information** that it might need later.

The `nsi_version` member must be set to `NSI_VERSION` (defined in \[nsi.h\](nsi.h.md)), so the renderer is able to determine which version of ɴsɪ was used when compiling the procedural.

The function pointers types used in the definition are :

- `NSIProceduralUnload_t` is a function that cleans-up after the last execution of the procedural. This is the dual of `NSIProceduralLoad()`. In addition to arguments `ctx` and `report`, also received by `NSIProceduralLoad()`, it receives the description of the procedural returned by `NSIProceduralLoad()`.
- `NSIProceduralExecute_t` is a function that contributes to the description of the scene by generating ɴsɪ API calls. Since `NSIProceduralExecute_t` might be called multiple times in the same render, it's important that it uses the context `ctx` it receives as a argument to make its ɴsɪ calls, and not the context previously received by `NSIProceduralLoad()`. It also receives any extra arguments sent to , or any extra attributes set on a node. They are stored in the `args` array (of length `n_args`). `NSIParam_t` is described in .

## Error Reporting

All functions of the procedural called by ɴsɪ receive a argument of type `NSIReport_t`. This is a pointer to a function which should be used by the procedural to report errors or display any informational message.

``` c
typedef void (*NSIReport_t)(
    NSIContext_t ctx, int level, const char* message);
````

It receives the current context, the error level (as described in ) and the message to be displayed. This information will be forwarded to any error handler attached to the current context, along with other regular renderer messages. Using this, instead of a custom error reporting mechanism, will benefit the user by ensuring that all messages are displayed in a consistent manner.

## Preprocessor Macros

Some convenient C preprocessor macros are also defined in `nsi_procedural.h` :

```c
NSI_PROCEDURAL_UNLOAD(name)
```

and

```c
NSI_PROCEDURAL_EXECUTE(name)
```

declare functions of the specified name that match `NSIProceduralUnload_t` and `NSIProceduralExecute_t`, respectively.

```c
NSI_PROCEDURAL_LOAD
```

declares a `NSIProceduralLoad` function.

```c
NSI_PROCEDURAL_INIT(proc, unload_fct, execute_fct)
```

initializes a `NSIProcedural_t` (passed as `proc`) using the addresses of the procedural\'s main functions. It also initializes `proc.nsi_version`.

So, a skeletal dynamic library procedural (that does nothing) could be implemented as in .

Please note, however, that the `proc` static variable in this example contains only constant values, which allows it to be allocated as a static variable. In a more complex implementation, it could have been over-allocated (or subclassed, in C++) to hold additional, variable data ​[^1]. In that case, it would have been better to allocate the descriptor dynamically -- and release it in `NSI_PROCEDURAL_UNLOAD` -- so the procedural could be loaded independently from multiple parallel renders, each using its own instance of the `NSIProcedural_t` descriptor.

```{.c linenos=""}
#include "nsi_procedural.h"

NSI_PROCEDURAL_UNLOAD(min_unload)
{
}

NSI_PROCEDURAL_EXECUTE(min_execute)
{
}

NSI_PROCEDURAL_LOAD
{
    static struct NSIProcedural_t proc;
    NSI_PROCEDURAL_INIT(proc, min_unload, min_execute);
    return &proc;
}
```

---

**Footnotes**

[^1]: A good example of this is available in the _3Delight_ installation, in file \[gear.cpp\](gear.cpp.md).
