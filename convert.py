#!/usr/bin/env python3
"""Convert NSI docs from Sphinx/RST to mdbook Markdown.

Strategy:
  1. Pre-process: expand substitutions as RST-compatible text, convert
     :ref:/:doc: to unique placeholders, strip directives
  2. Pandoc: RST → GFM markdown (better table support)
  3. Post-process: replace placeholders with Markdown links, fix admonitions
"""

import re
import subprocess
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
BOOK_SRC = Path("book/src")

SKIP_FILES = {"definitions.rst", "index.rst", "genindex.rst", "patchmesh.rst", "quick_tour.rst"}

# Plain-text substitutions (no markdown — these go into RST before pandoc)
PLAIN_SUBSTITUTIONS = {
    "|nsi|": "ɴsɪ",
    "|nbsp|": "\u00a0",
    "|nsp|": "\u200b",
}

# Substitutions that become links — use placeholders pre-pandoc, expand post-pandoc
LINK_SUBSTITUTIONS = {
    "|osl|": ("ᴏsʟ", "https://opensource.imageworks.com/?p=osl"),
    "|OpenVDB|": ("OpenVDB", "https://www.openvdb.org"),
    "|3delight|": ("3Delight", "https://www.3delight.com"),
    "|closure|": ("closure", "https://www.3delight.com/documentation/display/3DSP/3Delight's+OSL+Support"),
    "|closures|": ("closures", "https://www.3delight.com/documentation/display/3DSP/3Delight's+OSL+Support"),
}

# Substitutions that become inline code
CODE_SUBSTITUTIONS = {
    "|NSICreate|": "``NSICreate``",
    "|NSIConnect|": "``NSIConnect``",
    "|attributes|": "``attributes``",
    "|shader|": "``shader``",
}

# Label → file#anchor mapping
LABEL_MAP = {}

DOC_MAP = {
    "nsi.h": "nsi.h.md",
    "nsi.hpp": "nsi.hpp.md",
    "nsi_dynamic.hpp": "nsi_dynamic.hpp.md",
    "nsi.py": "nsi.py.md",
    "nsi_procedural.h": "nsi_procedural.h.md",
    "gear.cpp": "gear.cpp.md",
}

# Placeholder counter for unique link markers
_placeholder_id = 0
_placeholders = {}  # id → (text, url)


def make_placeholder(text: str, url: str) -> str:
    """Create a unique placeholder string that survives pandoc."""
    global _placeholder_id
    _placeholder_id += 1
    pid = f"XREFPLACEHOLDER{_placeholder_id}X"
    _placeholders[pid] = (text, url)
    return pid


def rst_label_to_anchor(label: str) -> str:
    return label.lower().replace(":", "-").replace("_", "-")


def build_label_map():
    for rst_file in DOCS_DIR.glob("*.rst"):
        if rst_file.name in SKIP_FILES:
            continue
        md_name = rst_file.stem + ".md"
        content = rst_file.read_text()
        for m in re.finditer(r"\.\.\s+_([A-Za-z][A-Za-z0-9_:.-]+):", content):
            label = m.group(1)
            after = content[m.end():m.end() + 10].strip()
            if after.startswith("http"):
                continue
            LABEL_MAP[label] = f"{md_name}#{rst_label_to_anchor(label)}"


def preprocess_rst(text: str) -> str:
    """Pre-process RST before pandoc conversion."""
    # Strip include directives
    text = re.sub(r"^\.\.\s+include::\s+definitions\.rst\s*\n", "", text, flags=re.MULTILINE)

    # Strip index directives
    text = re.sub(
        r"^\.\.\s+index::.*?(?=\n(?:\S|\n))",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Remove RST label definitions (but keep URL targets)
    def strip_label(m):
        rest = m.group(2).strip() if m.group(2) else ""
        if rest.startswith("http"):
            return m.group(0)
        return ""

    text = re.sub(
        r"^\.\.\s+_[A-Za-z][A-Za-z0-9_:.-]+:([ \t]*(.*))?\n?",
        strip_label,
        text,
        flags=re.MULTILINE,
    )

    # Expand code substitutions (RST inline code — pandoc handles these fine)
    for key in sorted(CODE_SUBSTITUTIONS.keys(), key=len, reverse=True):
        text = text.replace(key, CODE_SUBSTITUTIONS[key])

    # Expand plain text substitutions
    for key in sorted(PLAIN_SUBSTITUTIONS.keys(), key=len, reverse=True):
        text = text.replace(key, PLAIN_SUBSTITUTIONS[key])

    # Expand link substitutions as placeholders
    for key in sorted(LINK_SUBSTITUTIONS.keys(), key=len, reverse=True):
        display, url = LINK_SUBSTITUTIONS[key]
        placeholder = make_placeholder(display, url)
        text = text.replace(key, placeholder)

    # Convert :ref:`text<label>` to placeholders
    def ref_replacer(m):
        text_part = m.group(1).strip()
        label = m.group(2)
        target = LABEL_MAP.get(label, "")
        if target:
            return make_placeholder(text_part, target)
        return text_part

    text = re.sub(r":ref:`([^<]+)<([^>]+)>`", ref_replacer, text)

    # Convert bare :ref:`label`
    def ref_replacer_bare(m):
        label = m.group(1)
        target = LABEL_MAP.get(label, "")
        if target:
            return make_placeholder(label, target)
        return label

    text = re.sub(r":ref:`([^`<]+)`", ref_replacer_bare, text)

    # Convert :doc:`filename` references
    def doc_replacer(m):
        full = m.group(1)
        m2 = re.match(r"(.+?)\s*<(.+?)>", full)
        if m2:
            display, target = m2.group(1), m2.group(2)
        else:
            display = target = full
        md_file = DOC_MAP.get(target, target + ".md")
        return make_placeholder(display, md_file)

    text = re.sub(r":doc:`([^`]+)`", doc_replacer, text)

    return text


def run_pandoc(rst_text: str) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "rst", "-t", "gfm", "--wrap=none"],
        input=rst_text,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  pandoc stderr: {result.stderr}", file=sys.stderr)
    return result.stdout


def postprocess_md(text: str) -> str:
    """Post-process pandoc output: expand placeholders, fix admonitions."""
    # Replace all placeholders with Markdown links
    for pid, (display, url) in _placeholders.items():
        text = text.replace(pid, f"[{display}]({url})")

    # Fix admonitions — pandoc produces <div class="note/tip/warning"> blocks
    def fix_admonition(m):
        kind = m.group(1).capitalize()
        body = m.group(2).strip()
        # Indent each line with >
        lines = body.split("\n")
        quoted = "\n".join(f"> {line}" if line.strip() else ">" for line in lines)
        return f"> **{kind}:** {lines[0]}\n" + "\n".join(
            f"> {line}" if line.strip() else ">" for line in lines[1:]
        ) if len(lines) > 1 else f"> **{kind}:** {body}"

    text = re.sub(
        r'<div class="(note|warning|caution|tip|important)">\s*\n(.*?)\n</div>',
        fix_admonition,
        text,
        flags=re.DOTALL,
    )

    # Clean up triple+ blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def convert_literalinclude(rst_file: Path) -> str:
    content = rst_file.read_text()
    m = re.search(r"\.\.\s+literalinclude::\s+(\S+)", content)
    if not m:
        return ""

    code_path = DOCS_DIR / m.group(1)
    if not code_path.exists():
        print(f"  WARNING: literalinclude target not found: {code_path}", file=sys.stderr)
        return ""

    ext_to_lang = {".h": "c", ".hpp": "cpp", ".cpp": "cpp", ".py": "python"}
    lang = ext_to_lang.get(code_path.suffix, "")

    title_match = re.match(r"([^\n]+)\n[=\-~]+\n", content)
    title = title_match.group(1).strip() if title_match else code_path.name

    code = code_path.read_text()
    return f"# {title}\n\n```{lang}\n{code}\n```\n"


def convert_file(rst_file: Path) -> str:
    global _placeholder_id, _placeholders
    _placeholder_id = 0
    _placeholders = {}

    content = rst_file.read_text()

    if ".. literalinclude::" in content:
        return convert_literalinclude(rst_file)

    processed = preprocess_rst(content)
    md = run_pandoc(processed)
    md = postprocess_md(md)
    return md


def main():
    build_label_map()
    LABEL_MAP["NSICreate"] = "c-api.md#capi-nsicreate"
    LABEL_MAP["NSIConnect"] = "c-api.md#capi-nsiconnect"
    LABEL_MAP["attributes"] = "nodes.md#node-attributes"
    LABEL_MAP["shader"] = "nodes.md#node-shader"

    print(f"Built label map with {len(LABEL_MAP)} entries")
    BOOK_SRC.mkdir(parents=True, exist_ok=True)

    for rst_file in sorted(DOCS_DIR.glob("*.rst")):
        if rst_file.name in SKIP_FILES:
            continue
        md_name = rst_file.stem + ".md"
        out_path = BOOK_SRC / md_name
        print(f"Converting {rst_file.name} → {md_name} ...", end=" ")
        md_content = convert_file(rst_file)
        out_path.write_text(md_content)
        print(f"({len(md_content)} bytes)")

    print("\nDone!")


if __name__ == "__main__":
    main()
