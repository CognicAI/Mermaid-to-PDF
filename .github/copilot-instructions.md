# Copilot Instructions – Mermaid-to-PDF Pipeline

## Architecture Overview

This is a **4-step Python pipeline** that converts Markdown files containing Mermaid diagrams into professionally styled PDFs. The entry point is `main.py` (thin wrapper) → `scripts/main.py` (actual pipeline).

**Pipeline flow** (`run_pipeline()` in `scripts/main.py`):
1. **Extract** – `extract_mermaid.py`: regex-extracts ` ```mermaid ``` ` blocks → `.mmd` files in `output/temp/`
2. **Convert** – `convert_mermaid.py`: runs `mmdc` CLI to render `.mmd` → `.png` (4× scale, 2048px width)
3. **Replace** – `replace_mermaid.py`: substitutes mermaid blocks with `![label](image.png)` references
4. **PDF gen** – pandoc + XeLaTeX with custom title page, TOC, and GitHub-inspired styling from `styles/style-preamble.tex`

## Project Structure

- `main.py` – Root wrapper; adds `scripts/` to path and delegates to `scripts/main.py`
- `scripts/main.py` – Core pipeline orchestration, emoji stripping, LaTeX escaping, pandoc invocation
- `scripts/extract_mermaid.py` – Mermaid block extraction via regex (`MERMAID_BLOCK_REGEX`)
- `scripts/convert_mermaid.py` – `.mmd` → `.png` conversion via `mmdc` CLI
- `scripts/replace_mermaid.py` – Replaces mermaid code blocks with image markdown
- `styles/style-preamble.tex` – LaTeX preamble (colors, headings, headers/footers, code blocks, tables)
- `output/` – Generated artifacts: `markdown/`, `pdf/`, `temp/` (cleaned after each run)
- `reports/` – Sample input markdown files for testing

## Key Conventions

- **No pip dependencies** – All Python code uses standard library only (`pathlib`, `subprocess`, `re`, `shutil`, `sys`)
- **Path handling** – `PROJECT_ROOT = Path(__file__).resolve().parent.parent` anchors all paths; always use `Path` objects, never string concatenation
- **Emoji stripping** – LaTeX cannot render emojis; `strip_emojis()` removes them before PDF generation using a comprehensive Unicode regex
- **Special character escaping** – `→` is replaced with `$\rightarrow$`; LaTeX special chars in titles are escaped individually
- **Title page generation** – Dynamically generated `.tex` file with configurable logo, author name, and `\today`
- **Runtime-injected LaTeX macros** – `paths.tex` defines `\logopath` and `\headertext` so the preamble and title page stay data-driven; never hardcode these values in `.tex` files

## Running the Pipeline

```bash
# Local (requires Python 3.10+, pandoc, mmdc, XeLaTeX, Barlow & Fira Code fonts)
python3 main.py <input.md>          # Single file
python3 main.py <folder>            # All .md files in folder

# Configurable options (all optional, sensible defaults provided):
python3 main.py <input.md> --author "Jane Doe"
python3 main.py <input.md> --logo /path/to/logo.png
python3 main.py <input.md> --header-text "Project Report"

# Docker (recommended – all deps pre-configured)
make build                          # Build image
make run FILE=README.md             # Process file from current dir
make run-custom PATH=/abs/path FILE=file.md  # Custom directory
make test                           # Build + process README.md
make clean                          # Remove image + outputs
```

### CLI Defaults

| Flag | Default | Where it appears |
|------|---------|-------------------|
| `--author` | `Harsha Vardhanu Parnandi` | Title page |
| `--logo` | `assets/CognicAI_logo.png` | Title page + every page header |
| `--header-text` | `Analysis Document` | Top-right page header |

## Modifying the Pipeline

- **Adding new diagram types**: Modify `MERMAID_BLOCK_REGEX` in `extract_mermaid.py` and the corresponding replacement logic in `replace_mermaid.py`
- **Changing PDF styling**: Edit `styles/style-preamble.tex` – uses packages: `fancyhdr`, `titlesec`, `xcolor`, `hyperref`, `mdframed`, `booktabs`; colors defined as `headingblue (#0366d6)`, `codebg (#f6f8fa)`, etc.
- **Adjusting mmdc settings**: Conversion flags are in `convert_mmd_to_png()` – currently `-b transparent -s 4 -w 2048`
- **Pandoc flags**: Configured in `run_pipeline()` – uses `markdown+lists_without_preceding_blankline`, `--pdf-engine=xelatex`, `--number-sections`, `--toc-depth=3`

## Docker Setup

- Base image: `ubuntu:22.04` with TeX Live, Node.js 20, Chromium (for mmdc/Puppeteer), Barlow + Fira Code fonts
- `PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser` is required for mmdc
- Input mounted read-only at `/app/input`, output at `/app/output`
- CI workflow at `.github/workflows/docker.yml` builds and tests on push to `main`/`develop`
