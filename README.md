[![Documentation Status](https://readthedocs.org/projects/nsi/badge/?version=latest)](https://nsi.readthedocs.io/en/latest/?badge=latest)
# ɴsɪ Documentation

Documentation for Illumination Research’s Nodal Scene Interface – ɴsɪ.

## Building

Change into the `docs` folder. This contains the
[Sphinx](https://www.sphinx-doc.org/) project.

The root folder of the repository only contains the YML configuration
for [ReadTheDocs](https://nsi.readthedocs.io/) and this readme.
```
cd docs
```

You need Python 3 to build this. Aka: running `pyton` should invoke a
Python 3 interpreter.

For example, on **macOS**, using **Homebrew**:

```
> brew install pyenv 
> pyenv install 3.7.6
> pyenv global 3.7.6
```

Requirements for a `pip` install are in `docs/requirements.txt`.
```
pip install -r requirements.txt
```

### HTML target

```
make html
```
Open `_build/html/index.html` to browse the HTML docs locally.

### EPUB target

```
make epub
```
The result will be in `_build/epub/NSI.epub`.

If you own a *Kindle* or other e-book reader that requires Mobipocket
format, conversion of the EPUB to this format is best done with
Amazon’s native tool,
[kindlegen](https://www.amazon.com/gp/feature.html?docId=1000765211).

This can be ran from the command line directly, e.g. on macOS:
```
/Applications/KindleGen/kindlegen _build/epub/NSI.epub
```
will generate `NSI.mobi`.

If you are on macOS Catalina or later kindlegen will not work since
it’s 32bit only. In this case use Amazon’s 
[Kindle Previewer](https://www.amazon.com/gp/feature.html?docId=1000765261)
tool which, too, can convert from EPUB to Mobipocket format.

### LaTex/LaTexPDF target

You need a Tex installation.

Either *libRSVG* or *Inkscape* is needed to convert the SVGs to PDF via
[sphinxcontrib-svg2pdfconverter](https://github.com/missinglinkelectronics/sphinxcontrib-svg2pdfconverter).

This means you must have `inkscape` or `rsvg-convert` in your `PATH`.
Note that *Inkscape 1.0beta* does not work with
*sphinxcontrib-svg2pdfconverter*. You need an older 0.9x version.

The default in the
[`extensions` section of `docs/conf.py`](https://github.com/virtualritz/nsi-docs/blob/df238d06353cf915c8c1ea33e370e6ba9e81d6f9/docs/conf.py#L34)
is for `rsvg-convert`.

To build the PDF:
```
make latexpdf
```
The result will be in docs/_build/latex/nsi.pdf

This currently looks a tad ugly and needs some love with custom Tex
commands.
