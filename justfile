# List available recipes.
default:
    @just --list

# Build the book HTML (output: book/build/).
book:
    mdbook build book

# Serve the book locally with live reload and open it in the browser.
book-serve:
    mdbook serve book --open

# Build a PDF from docs/nsi.tex into docs/build/. Requires latexmk + TeX Live.
pdf:
    cd docs && TEXINPUTS=.:../book/src/image:: latexmk -pdf -outdir=build nsi.tex
