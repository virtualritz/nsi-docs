# Script Objects

It is a design goal to provide an easy to use and flexible scripting language for ɴsɪ.

The [Lua](https://www.lua.org/) language has been selected for such a task because of its performance, lightness and features[^1]. A flexible scripting interface greatly reduces the need to have API extensions.

For example, what is known as 'conditional evaluation' and 'Ri filters' in the _RenderMan_ API are superseded by the scripting features of ɴsɪ.

> [!NOTE]
> Although they go hand in hand, scripting objects are not to be confused with the Lua binding.
>
> The binding allows for calling ɴsɪ functions in Lua while scripting objects allow for scene inspection and decision making in Lua. Script objects can make Lua binding calls to make modifications to the scene.

---

To be continued ...

**Footnotes**

[^1]: Lua is also portable and streamable.
