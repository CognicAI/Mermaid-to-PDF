#!/usr/bin/env python3
"""
main.py – Automated Mermaid-to-PDF pipeline.

Usage:

    python scripts/main.py <input.md>           # Process a single markdown file
    python scripts/main.py <folder>             # Process all .md files in a folder

    # Customise author, logo, or header text:
    python scripts/main.py <input.md> --author "Jane Doe"
    python scripts/main.py <input.md> --logo /path/to/logo.png
    python scripts/main.py <input.md> --header-text "Project Report"

Pipeline:
    1. Extract mermaid blocks → .mmd files          (extract_mermaid.py)
    2. Convert .mmd files    → .png images           (convert_mermaid.py)
    3. Replace mermaid code  → image references       (replace_mermaid.py)
    4. Generate PDF via pandoc

Project layout:
    docs/
    ├── assets/          CognicAI_logo.png, etc.
    ├── scripts/         Python pipeline scripts
    ├── styles/          style-preamble.tex
    ├── output/          Generated .pdf and .md
    └── *.md             Source markdown files
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Project root is one level up from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

from extract_mermaid import process_markdown_file
from convert_mermaid import convert_all
from replace_mermaid import process_file as replace_mermaid_in_file
from remove_backticks import remove_inline_backticks

# Matches most emoji unicode ranges
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U0001F7E0-\U0001F7EB"  # colored circles (🟡🟢🔴 etc.)
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U0001FA70-\U0001FAFF"  # symbols extended-A
    "\U00002702-\U000027B0"  # dingbats
    "\U0000FE00-\U0000FE0F"  # variation selectors
    "\U0000200D"             # zero width joiner
    "\U00002600-\U000026FF"  # misc symbols
    "\U0000231A-\U0000231B"  # watch/hourglass
    "\U00002934-\U00002935"  # arrows
    "\U000025AA-\U000025FE"  # geometric shapes
    "\U00002B05-\U00002B07"  # arrows
    "\U00002B1B-\U00002B1C"  # squares
    "\U00002B50"             # star
    "\U00002B55"             # circle
    "\U0000203C-\U00002049"  # exclamation marks
    "\U00002139"             # info
    "\U0001F004-\U0001F0CF"  # playing cards / mahjong
    "\U0001F170-\U0001F251"  # enclosed characters
    "]+",
    re.UNICODE,
)


def strip_emojis(text: str) -> str:
    """Remove emoji characters from text."""
    return EMOJI_PATTERN.sub("", text)


# ── Defaults (used when CLI flags are omitted) ─────────────────────
DEFAULT_AUTHOR = "Harsha Vardhanu Parnandi"


def _find_logo_in_assets() -> Path | None:
    """Return the first image file found in assets/, or None."""
    assets = PROJECT_ROOT / "assets"
    if not assets.is_dir():
        return None
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.svg"):
        matches = sorted(assets.glob(ext))
        if matches:
            return matches[0]
    return None


def run_pipeline(md_input: Path, *, author: str, logo: Path | None, header_text: str):
    base_name = md_input.stem
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for organized output
    markdown_dir = output_dir / "markdown"
    pdf_dir = output_dir / "pdf"
    temp_dir = output_dir / "temp"  # For intermediate files
    markdown_dir.mkdir(exist_ok=True)
    pdf_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)

    # ── Step 1: Extract mermaid blocks into .mmd files ──────────────────
    print("\n📦 Step 1/4 — Extracting mermaid blocks …")
    process_markdown_file(md_input, temp_dir)

    mmd_files = sorted(temp_dir.glob(f"{base_name}_diagram_*.mmd"))
    has_mermaid = len(mmd_files) > 0
    
    if has_mermaid:
        print(f"   Found {len(mmd_files)} mermaid block(s).\n")

        # ── Step 2: Convert .mmd → .png ─────────────────────────────────────
        print("🖼  Step 2/4 — Converting .mmd files to .png …")
        png_paths = convert_all(mmd_files)
        print()

        # ── Step 3: Replace mermaid code with image references ──────────────
        print("✏️  Step 3/4 — Replacing mermaid blocks with image references …")

        # Use relative paths (just filenames) so pandoc can resolve them from
        # inside the temp/ directory.
        image_names = [p.name for p in png_paths]

        output_md = markdown_dir / md_input.name
        replace_mermaid_in_file(md_input, image_names, output_md)
    else:
        print("⚠  No mermaid blocks found. Proceeding with PDF generation.\n")
        # Just copy the input file to markdown directory
        output_md = markdown_dir / md_input.name
        shutil.copy2(md_input, output_md)

    # Strip emojis from the output markdown (LaTeX can't render them)
    md_text = output_md.read_text(encoding="utf-8")
    md_text = strip_emojis(md_text)

    # Replace → with a LaTeX-safe arrow (Barlow font may lack this glyph)
    md_text = md_text.replace("→", "$\\rightarrow$")

    # Remove inline code backticks (`) from the markdown
    md_text = remove_inline_backticks(md_text)

    # Remove any existing \begin{titlepage}...\end{titlepage} from body
    titlepage_match = re.search(
        r"\\begin\{titlepage\}.*?\\end\{titlepage\}",
        md_text,
        re.DOTALL,
    )
    if titlepage_match:
        md_text = md_text[:titlepage_match.start()] + md_text[titlepage_match.end():]

    # Remove YAML front matter fields we override via flags / preamble
    md_text = re.sub(r'^title:\s*.*$', "", md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^author:\s*.*$', "", md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^date:\s*.*$', "", md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^numbersections:\s*.*$', "", md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^geometry:\s*.*$', "", md_text, flags=re.MULTILINE)
    md_text = re.sub(
        r'^header-includes:\s*\n(?:\s+-\s+.*\n)*',
        "", md_text, flags=re.MULTILINE,
    )

    # Extract document title from first top-level heading (# Title)
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    doc_title = title_match.group(1).strip() if title_match else base_name
    
    # Escape LaTeX special characters in title
    # Use a placeholder for backslash first to prevent its braces from
    # being double-escaped by the subsequent { and } replacements.
    _BKSL = "\x00BKSL\x00"
    doc_title_escaped = doc_title.replace('\\', _BKSL) \
                                  .replace('{', '\\{') \
                                  .replace('}', '\\}') \
                                  .replace('_', '\\_') \
                                  .replace('&', '\\&') \
                                  .replace('%', '\\%') \
                                  .replace('$', '\\$') \
                                  .replace('#', '\\#') \
                                  .replace('^', '\\textasciicircum{}') \
                                  .replace('~', '\\textasciitilde{}') \
                                  .replace(_BKSL, '\\textbackslash{}')

    # Generate a full-page title page with title, author, and date
    titlepage_file = temp_dir / "titlepage.tex"
    logo_path = logo.resolve() if logo else None

    logo_include = (
        rf"\includegraphics[height=40pt]{{{logo_path}}}"
        if logo_path
        else ""
    )
    titlepage_tex = rf"""
\begin{{titlepage}}
\centering

\vspace*{{3cm}}

{{\fontsize{{30}}{{36}}\selectfont\bfseries {doc_title_escaped}\par}}

\vspace{{1.5cm}}

{{\Large {author}\par}}

\vspace{{1cm}}

{{\large \today\par}}

\vfill

{logo_include}

\vspace{{1cm}}
\end{{titlepage}}

\tableofcontents
\newpage
"""
    titlepage_file.write_text(titlepage_tex.strip() + "\n", encoding="utf-8")

    output_md.write_text(md_text, encoding="utf-8")

    print(f"   Written: {output_md}\n")

    # Copy images from assets/ and source dir into temp/ for pandoc
    assets_dir = PROJECT_ROOT / "assets"
    for search_dir in (assets_dir, md_input.parent):
        if not search_dir.exists():
            continue
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.svg"):
            for img in search_dir.glob(ext):
                dest = temp_dir / img.name
                if not dest.exists() or img.stat().st_mtime > dest.stat().st_mtime:
                    shutil.copy2(img, dest)

    # ── Step 4: Generate PDF  (pandoc + xelatex with enhanced styling) ──
    print("📄 Step 4/4 — Generating PDF …")
    output_pdf = pdf_dir / f"{base_name}.pdf"

    # LaTeX preamble with GitHub-like styling
    preamble_path = PROJECT_ROOT / "styles" / "style-preamble.tex"

    # Write a small tex file defining \logopath (if available) and
    # \headertext so the preamble can reference them regardless of CWD.
    paths_tex = temp_dir / "paths.tex"
    paths_lines: list[str] = []
    if logo_path:
        paths_lines.append(f"\\newcommand{{\\logopath}}{{{logo_path}}}")
        paths_lines.append("\\newcommand{\\haslogo}{1}")
    else:
        paths_lines.append("\\newcommand{\\logopath}{}")
    paths_lines.append(f"\\newcommand{{\\headertext}}{{{header_text}}}")
    paths_tex.write_text("\n".join(paths_lines) + "\n", encoding="utf-8")

    pandoc_cmd = [
        "pandoc",
        str(output_md),
        "-f", "markdown+lists_without_preceding_blankline",
        "-o", str(output_pdf),
        "--pdf-engine=xelatex",
        "-V", "mainfont=Barlow",
        "-V", "monofont=Fira Code",
        "-V", "fontsize=12pt",
        "-V", "geometry:margin=0.75in",
        "--number-sections",
        "--toc",
        "--toc-depth=3",
        "--wrap=auto",
        "--columns=85",
        "-H", str(paths_tex),
        "-H", str(preamble_path),
        "--resource-path", str(temp_dir),
    ]

    # Insert titlepage before body (renders before TOC)
    if titlepage_file.exists():
        pandoc_cmd.extend(["-B", str(titlepage_file)])

    result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✖ Pandoc failed:\n{result.stderr.strip()}")
        sys.exit(1)
    print(f"   PDF: {output_pdf}")

    # ── Cleanup: clean up temporary files ─────────────────────────────────
    for f in temp_dir.iterdir():
        if f.is_file():
            f.unlink()

    # ── Done ────────────────────────────────────────────────────────────
    print(f"\n✅ Pipeline complete!")
    print(f"   Markdown: {output_md}")
    print(f"   PDF: {output_pdf}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the pipeline."""
    parser = argparse.ArgumentParser(
        description="Mermaid-to-PDF: convert Markdown with Mermaid diagrams into styled PDFs.",
    )
    parser.add_argument(
        "input",
        help="Path to a .md file or a folder of .md files",
    )
    parser.add_argument(
        "--author",
        default=DEFAULT_AUTHOR,
        help=f"Author name shown on the title page (default: '{DEFAULT_AUTHOR}')",
    )
    parser.add_argument(
        "--logo",
        default=None,
        help="Path to logo image (default: auto-detect first image in assets/)",
    )
    parser.add_argument(
        "--header-text",
        default=None,
        help="Text shown in the top-right page header (default: filename)",
    )
    return parser.parse_args(argv)


def main():
    args = parse_args()
    input_path = Path(args.input).resolve()

    if not input_path.exists():
        print(f"Error: path not found: {input_path}")
        sys.exit(1)

    # Resolve logo: explicit flag > auto-detect from assets/ > None (skip)
    if args.logo is not None:
        logo = Path(args.logo).resolve()
        if not logo.exists():
            print(f"Error: logo not found: {logo}")
            sys.exit(1)
    else:
        logo = _find_logo_in_assets()
        if logo:
            print(f"   Auto-detected logo: {logo.name}")
        else:
            print("   No logo found in assets/ — generating PDF without logo.")

    # Handle folder input - process all .md files
    if input_path.is_dir():
        md_files = sorted(input_path.glob("*.md"))
        if not md_files:
            print(f"Error: no .md files found in: {input_path}")
            sys.exit(1)
        
        print(f"\n🗂  Found {len(md_files)} markdown file(s) in {input_path.name}/")
        for i, md_file in enumerate(md_files, 1):
            print(f"\n{'='*60}")
            print(f"Processing {i}/{len(md_files)}: {md_file.name}")
            print(f"{'='*60}")
            # Use filename as header if not specified, replacing underscores with spaces
            header_text = args.header_text if args.header_text else md_file.stem.replace("_", " ")
            pipeline_kwargs = dict(author=args.author, logo=logo, header_text=header_text)
            run_pipeline(md_file, **pipeline_kwargs)
        
        print(f"\n✅ All {len(md_files)} file(s) processed successfully!")
    
    # Handle single file input
    elif input_path.is_file():
        if input_path.suffix != ".md":
            print(f"Error: expected a .md file, got: {input_path.suffix}")
            sys.exit(1)
        # Use filename as header if not specified, replacing underscores with spaces
        header_text = args.header_text if args.header_text else input_path.stem.replace("_", " ")
        pipeline_kwargs = dict(author=args.author, logo=logo, header_text=header_text)
        run_pipeline(input_path, **pipeline_kwargs)
    
    else:
        print(f"Error: invalid path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
