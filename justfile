# List available recipes.
default:
    @just --list

# Build the book HTML (output: book/build/).
book:
    mdbook build book

# Serve the book locally with live reload and open it in the browser.
book-serve:
    mdbook serve book --open

# Convert SVGs in book/src/image/ to PDFs into docs/build/images/, and
# create placeholder PDFs for figures referenced by nsi.tex but not
# shipped in the repo (e.g. the SSS images that live only in $DELIGHT).
_pdf-images:
    #!/usr/bin/env bash
    set -euo pipefail
    src=book/src/image
    dst=docs/build/images
    mkdir -p "$dst"
    if ! command -v inkscape >/dev/null 2>&1; then
        echo "inkscape not found; install it to convert SVGs to PDFs." >&2
        exit 1
    fi
    for svg in "$src"/*.svg; do
        [[ -f "$svg" ]] || continue
        name=$(basename "$svg" .svg)
        out="$dst/$name.pdf"
        if [[ ! -f "$out" || "$svg" -nt "$out" ]]; then
            inkscape --export-filename="$out" "$svg" >/dev/null 2>&1
        fi
    done
    if [[ ! -f "$dst/placeholder.pdf" ]]; then
        tmp=$(mktemp -d)
        cat > "$tmp/p.tex" <<'EOL'
    \documentclass{article}
    \usepackage[paperwidth=4cm,paperheight=3cm,margin=0pt]{geometry}
    \pagestyle{empty}
    \begin{document}
    \fbox{\parbox{3.6cm}{\centering\small\itshape image\\placeholder}}
    \end{document}
    EOL
        (cd "$tmp" && pdflatex -interaction=nonstopmode p.tex >/dev/null 2>&1)
        cp "$tmp/p.pdf" "$dst/placeholder.pdf"
        rm -rf "$tmp"
    fi
    needed=$(rg -o '\\includegraphics(\[[^\]]*\])?\{([^}]+)\}' -r '$2' docs/nsi.tex | sort -u)
    for name in $needed; do
        out="$dst/$name.pdf"
        [[ -f "$out" ]] || cp "$dst/placeholder.pdf" "$out"
    done

# Build a PDF from docs/nsi.tex into docs/build/. Requires latexmk + TeX Live.
pdf: _pdf-images
    cd docs && TEXINPUTS=.:build/images:: latexmk -pdf -outdir=build nsi.tex

# Install latexmk + a minimal TeX Live set sufficient to build docs/nsi.tex.
install:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v brew >/dev/null 2>&1; then
        brew install --cask mactex-no-gui
    elif command -v apt-get >/dev/null 2>&1; then
        sudo apt install -y latexmk texlive-latex-base texlive-latex-recommended \
            texlive-latex-extra texlive-pictures texlive-fonts-recommended
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y latexmk texlive-scheme-medium
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --needed texlive-binextra texlive-basic texlive-latexextra \
            texlive-latexrecommended texlive-pictures texlive-fontsrecommended
    elif command -v winget >/dev/null 2>&1; then
        winget install -e --id MiKTeX.MiKTeX
    elif command -v choco >/dev/null 2>&1; then
        choco install -y miktex
    elif command -v scoop >/dev/null 2>&1; then
        scoop install latex
    else
        echo "No supported package manager detected (brew/apt/dnf/pacman/winget/choco/scoop)." >&2
        exit 1
    fi

# Install the full TeX Live distribution (~6 GB).
install-full:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v brew >/dev/null 2>&1; then
        brew install --cask mactex
    elif command -v apt-get >/dev/null 2>&1; then
        sudo apt install -y texlive-full
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y texlive-scheme-full
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --needed texlive-meta
    elif command -v choco >/dev/null 2>&1; then
        choco install -y texlive
    elif command -v scoop >/dev/null 2>&1; then
        scoop bucket add extras
        scoop install extras/texlive
    elif command -v winget >/dev/null 2>&1; then
        echo "winget has no full TeX Live package; falling back to MiKTeX (auto-completes packages on demand)." >&2
        winget install -e --id MiKTeX.MiKTeX
    else
        echo "No supported package manager detected (brew/apt/dnf/pacman/choco/scoop/winget)." >&2
        exit 1
    fi
