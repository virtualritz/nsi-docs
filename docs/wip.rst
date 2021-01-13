.. include:: definitions.rst

Help Wanted
===========

The |nsi| API isused in the `3Delight <https://3delight.com/>`__
renderer. More and more users of this renderer are switching their
pipelines from using the *RenderMan Interface™* to |nsi|.

Aka: this *is* being used in production.

Naming
------

There are many things that lack coherence & stringency in naming of
parts of the API.

The current documentation has new naming suggestions for some
arguments, attributes and nodes that are marked with exclamation
marks **(!)**.

If you see a name written differently below the current name and marked
with **(!)** this is a change suggestion.

Feedback on these is welcome. Please go to the `GitHub repository
<https://github.com/virtualritz/nsi-docs/>`__ for this documentation
and open a `ticket <https://github.com/virtualritz/nsi-docs/issues>`__
or comment on an existing one.

Spelling, Grammar & Content
---------------------------

If you find typos, grammar mistakes or think something should be changed
or added to improve this documentation, do not hesitate to go ahead and
open a pull request with your changes.

Each page has an :guilabel:`Edit on GitHub` button on the top right
corner to make this process as painless as possible.

Language Bindings
-----------------

The actual API is **C** which makes it easy to bind |nsi| to many
different languages.

Currently the 3Delight renderer ships with free |nsi| bindings for
**C++**, **Python** and **Lua**.
There is also a `Rust binding <https:://crates.io/crates/nsi>.

More bindings are always welcome!
