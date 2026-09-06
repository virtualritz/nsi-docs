# Repository Guidelines

This file gives guidance to Claude Code and other AI agents that work in this repository.

## Project Context

This repository holds the documentation for the Nodal Scene Interface (ɴꜱɪ), the 3D rendering API of Illumination Research. It is a documentation repository. It contains no application code.

- `book/src/` -- the mdbook source. Every page is Markdown.
- `book/src/SUMMARY.md` -- the table of contents. A new page must be listed here or mdbook will not build it.
- `book/src/nodes/` -- the node reference. One page per node type.
- `book/src/design/` -- design drafts that compare API alternatives, for discussion with implementers.
- `book/src/naming-convention.md` -- the attribute and node naming rules the drafts follow.
- `docs/` -- the legacy Sphinx/reStructuredText tree and the LaTeX PDF build.

## Build and Development Commands

```bash
just book          # build the book HTML into book/build/
just book-serve    # serve locally with live reload
just pdf           # build the PDF from the legacy docs/ tree
just install       # install mdbook and its preprocessors
```

Run `just book` after any change under `book/src/`. It is the only check this repository has.

## Blueprint References

For cross-project standards, see `.blueprints/`.

### Core Rules (MUST READ)

- [Agent Behavior Rules](.blueprints/base/AGENTS.md)
- [Microtypography](.blueprints/base/microtypography.md) -- dashes, slashes, quotes, ellipses, ASCII-first. Applies to every page, commit message, and chat reply.
- [Writing Style (ASD-STE100)](.blueprints/base/writing-style.md) -- use Simplified Technical English for technical facts and instructions, in docs and in chat.
- [Documentation Structure](.blueprints/base/doc-structure.md) -- Diátaxis. Read it **before** you write or restructure a page. Node pages are reference; design pages are explanation.
- [Context Economy](.blueprints/base/context-economy.md)
- [Git Safety](.blueprints/base/git-safety.md)

### Reference

- [Documentation Standards](.blueprints/base/documentation.md)
- [Commit Messages](.blueprints/base/commit-messages.md)
- [Domain Glossary](.blueprints/domain/glossary.md)

The language and testing blueprints do not apply here. This repository has no source code.

## Project-Specific Rules

- **Small caps for acronyms.** The book writes ɴsɪ and ᴏsʟ with Unicode small-capital letters. Note the plain lowercase `s` in both. Keep that exact spelling; do not substitute the small-capital S, U+A731. This convention is the one deliberate exception to the ASCII-first rule.
- **Mathematical notation.** Continuity classes keep their Unicode superscripts, as in C² and G¹.
- **Emphasis.** The book uses `*asterisks*` for emphasis and `_underscores_` around inline code for type names, as in _`float[2]`_. Do not let a formatter swap them.
- **A global prettier hook runs on every Write and Edit.** It reflows Markdown tables and rewrites emphasis markers, neither of which matches this repository. Edit pages through the shell instead when that matters.
- **Attribute tables.** Keep the column padding of a table you edit. Do not reflow rows you did not change.
- **Draft nodes.** A node page for an unimplemented node carries a blockquote that says so, and follows the [naming convention](book/src/naming-convention.md) rather than the legacy names.
