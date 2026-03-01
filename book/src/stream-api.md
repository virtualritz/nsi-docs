# The Interface Stream

It is important for a scene description API to be streamable. This allows saving scene description into files, communicating scene state between processes and provide extra flexibility when sending commands to the renderer ​[^1].

Instead of re-inventing the wheel, the authors have decided to use exactly the same format as is used by the _RenderMan_ Interface Bytestream (RIB). This has several advantages:

- Well defined ASCII and binary formats.
- The ASCII format is human readable and easy to understand.
- Easy to integrate into existing renderers (writers and readers already available).

Note that since Lua is part of the API, one can use Lua files for API streaming ​[^2].

---

**Footnotes**

[^1]: The streamable nature of the _RenderMan_ API, through RIB, is an undeniable advantage. RenderMan is a registered trademark of Pixar.

[^2]: Preliminary tests show that the Lua parser is as fast as an optimized ASCII RIB parser.
