# Help Wanted

The ɴsɪ API is used in the [3Delight](https://3delight.com/) renderer. More and more users of this renderer are switching their pipelines from using the _RenderMan Interface™_ to ɴsɪ.

Aka: this _is_ being used in production.

## Naming

There are many things that lack coherence & stringency in naming of parts of the API.

The current documentation has new naming suggestions for some arguments, attributes and nodes that are marked with exclamation marks **(!)**.

If you see a name written differently below the current name and marked with **(!)** this is a change suggestion.

Feedback on these is welcome. Please go to the [GitHub repository](https://github.com/virtualritz/nsi-docs/) for this documentation and open a [ticket](https://github.com/virtualritz/nsi-docs/issues) or comment on an existing one.

## Spelling, Grammar & Content {#spelling-grammar-content}

If you find typos, grammar mistakes or think something should be changed or added to improve this documentation, do not hesitate to go ahead and open a pull request with your changes.

Each page has an `Edit on GitHub`{.interpreted-text role="guilabel"} button on the top right corner to make this process as painless as possible.

## Language Bindings

The actual API is **C** which makes it easy to bind ɴsɪ to many different languages.

Currently the 3Delight renderer ships with free ɴsɪ bindings for **C++**, **Python** and **Lua**. There is also a [Rust binding](https:://crates.io/crates/nsi).

More bindings are always welcome!
