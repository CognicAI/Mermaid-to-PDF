<div align="center">
  <img src="assets/CognicAI.png" alt="Cognic AI Logo" width="800"/>
  <p><em>Developed by Cognic AI</em></p>
</div>

# Documentation Pipeline

Automated Mermaid-to-PDF pipeline for converting Markdown files with embedded Mermaid diagrams into professionally styled PDFs.

## ✨ What's New (February 2026)

- **🗂️ Custom Path Support**: Process markdown files from any directory on your system
- **⚡ Enhanced Makefile**: New `run-custom` and `run-custom-all` commands for flexible file processing
- **🍎 macOS Compatibility**: Automatic Docker path detection resolves "command not found" errors
- **📦 Docker Compose Override**: Easy configuration for custom paths via override files
- **📚 Comprehensive Documentation**: Updated with real-world examples and troubleshooting guides

## 🐋 Docker Quick Start (Recommended)

**The easiest way to use this pipeline is with Docker** - all dependencies are pre-configured!

```bash
# 1. Run the setup script
./setup.sh              # macOS/Linux
# OR
setup.bat               # Windows

# 2. Process a markdown file from current directory
make run FILE=README.md

# 3. Process files from a custom directory
make run-custom-all PATH=/path/to/your/folder

# 4. Process specific file from custom directory
make run-custom PATH=/path/to/your/folder FILE=yourfile.md
```

For detailed Docker instructions, see:
- 📘 [Docker Guide](DOCKER.md) - Complete Docker documentation
- 📋 [Quick Reference](DOCKER_QUICK_REF.md) - Command cheat sheet

## Overview

This pipeline processes Markdown files and generates high-quality PDFs with:
- **Mermaid diagram support**: Automatically extracts and renders Mermaid diagrams as images
- **Professional styling**: GitHub-inspired typography with custom fonts and LaTeX formatting
- **Organized output**: Separate directories for markdown and PDF files
- **Batch processing**: Process individual files or entire folders from any location
- **Flexible path handling**: Process files from current directory or any custom path
- **Docker-based**: Zero dependency installation with consistent cross-platform results
- **Custom title pages**: Auto-generated title pages with logo, author, and date
- **Table of contents**: Automatically generated with configurable depth

## Requirements

### Software Dependencies

- **Python 3.x** (3.7 or higher recommended)
- **Pandoc** (with XeLaTeX support)
- **Mermaid CLI** (`mmdc` or `mermaid-cli`)
- **LaTeX Distribution** (e.g., MacTeX, TeX Live, MiKTeX)

### Package Managers (Optional but Recommended)

**Windows:**
- [Chocolatey](https://chocolatey.org/) - Windows package manager
- [Scoop](https://scoop.sh/) - Command-line installer for Windows

**macOS:**
- [Homebrew](https://brew.sh/) - The missing package manager for macOS

**Linux:**
- Built-in package managers (apt, yum, dnf, pacman, etc.)

### Required Fonts

- **Barlow** (main font)
- **Fira Code** (monospace font)

### Python Modules

All standard library modules are used (no additional `pip install` required):
- `pathlib`
- `subprocess`
- `shutil`
- `re`
- `sys`

## Installation

### 1. Install Pandoc

```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows (using Chocolatey)
choco install pandoc

# Windows (using Scoop)
scoop install pandoc

# Or download installer from https://pandoc.org/installing.html
```

### 2. Install LaTeX

```bash
# macOS
brew install --cask mactex

# Linux (Debian/Ubuntu)
sudo apt-get install texlive-full

# Windows
# Download and install MiKTeX from https://miktex.org/download
# Or TeX Live from https://www.tug.org/texlive/windows.html

# Windows (using Chocolatey)
choco install miktex

# Or download from https://www.latex-project.org/get/
```

### 3. Install Mermaid CLI

**Prerequisites:** Node.js and npm must be installed

```bash
# All platforms (macOS, Linux, Windows)
npm install -g @mermaid-js/mermaid-cli

# Windows: If you don't have Node.js, install it first:
# Download from https://nodejs.org/
# Or using Chocolatey:
choco install nodejs

# Or using Scoop:
scoop install nodejs
```

### 4. Install Fonts

**macOS:**
1. Download fonts from Google Fonts
2. Double-click the font files and click "Install Font"
3. Restart your terminal

**Linux:**
```bash
# Install Barlow and Fira Code
sudo apt-get install fonts-firacode
# For Barlow, download from Google Fonts and copy to ~/.fonts/
```

**Windows:**
1. Download fonts:
   - [Barlow Font](https://fonts.google.com/specimen/Barlow)
   - [Fira Code Font](https://fonts.google.com/specimen/Fira+Code)
2. Extract the ZIP files
3. Right-click each font file and select "Install" or "Install for all users"
4. Restart your terminal/PowerShell

**Alternative (Windows - Chocolatey):**
```powershell
choco install firacode
# Note: Barlow may need manual installation from Google Fonts
```

## Docker Installation (Recommended)

The easiest way to use this pipeline is with Docker, which includes all dependencies pre-configured. **Docker installation eliminates the need for manual installation of Pandoc, LaTeX, Mermaid CLI, and fonts.**

### Prerequisites

- Docker Desktop installed and running ([Download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- Make (optional, but recommended for easiest usage)
  - macOS/Linux: Pre-installed
  - Windows: Install via [Chocolatey](https://community.chocolatey.org/packages/make) or [GnuWin32](http://gnuwin32.sourceforge.net/packages/make.htm)

### Quick Start with Docker

#### Option 1: Using Makefile (Recommended)

The Makefile provides the simplest interface:

```bash
# Build the image
make build

# Process file from current directory
make run FILE=README.md

# Process all files in current directory
make run-all

# Process files from custom directory
make run-custom PATH=/path/to/folder FILE=file.md
make run-custom-all PATH=/path/to/folder
```

**Example - Process Reports from another project:**
```bash
make run-custom-all PATH=/Users/username/Documents/GitHub/MyProject/reports
```

The output files will be generated in the `output/` directory.

#### Option 2: Using Docker Compose

```bash
# Process a single file from current directory
docker-compose run docs-pipeline python3 main.py /app/input/README.md

# Process all markdown files in current directory
docker-compose run docs-pipeline python3 main.py /app/input
```

**For custom paths:** Create a `docker-compose.override.yml` file:
```yaml
version: '3.8'
services:
  docs-pipeline:
    volumes:
      - /path/to/your/folder:/app/input:ro
      - ./output:/app/output
```

Then run:
```bash
docker-compose run docs-pipeline python3 main.py /app/input
```

#### Option 3: Using Docker directly

**Process files from current directory:**
```bash
# Build the image
docker build -t docs-pipeline .

# Process a single file
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input/README.md

# Process all markdown files
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input
```

**Process files from custom directory:**
```bash
# macOS/Linux - Process all files in a custom folder
docker run --rm \
  -v /path/to/your/folder:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input

# Example with specific path
docker run --rm \
  -v /Users/username/Documents/GitHub/SequelSpeak/temp/Reports/Markdown:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input
```

**Windows PowerShell:**
```powershell
# Current directory
docker run --rm `
  -v ${PWD}:/app/input:ro `
  -v ${PWD}/output:/app/output `
  docs-pipeline python3 main.py /app/input/README.md

# Custom directory
docker run --rm `
  -v C:\Users\username\Documents\myfiles:/app/input:ro `
  -v ${PWD}\output:/app/output `
  docs-pipeline python3 main.py /app/input
```

### Docker Benefits

- ✅ All dependencies pre-installed (Pandoc, LaTeX, Mermaid CLI, Fonts)
- ✅ Consistent environment across all platforms
- ✅ No need to install system packages
- ✅ Isolated from your system
- ✅ Easy to share and reproduce builds

### Makefile Commands Reference

The Makefile provides convenient shortcuts for all operations:

```bash
# Setup and Testing
make build                    # Build the Docker image
make test                     # Test with README.md
make help                     # Show all available commands

# Process files from current directory
make run FILE=README.md       # Process a specific file
make run-all                  # Process all .md files

# Process files from custom directory (NEW)
make run-custom PATH=/path/to/folder FILE=yourfile.md  # Process specific file
make run-custom-all PATH=/path/to/folder               # Process all files

# Utilities
make bash                     # Open shell in container
make clean                    # Remove image and outputs
make clean-output             # Remove only output files
```

**Real-World Custom Path Examples:**
```bash
# Process all reports from another project
make run-custom-all PATH=/Users/username/Documents/GitHub/SequelSpeak/temp/Reports/Markdown

# Process a specific file from Desktop
make run-custom PATH=/Users/username/Desktop/documents FILE=report.md

# Process files from a Windows share (macOS)
make run-custom-all PATH=/Volumes/SharedDrive/Documents/Reports

# Process files from external drive
make run-custom-all PATH=/Volumes/USB_Drive/markdown_files
```

> **Note:** The Makefile automatically detects the Docker installation path on macOS, resolving common "docker: command not found" errors.

### Stopping and Cleanup Commands

Properly stop containers and clean up resources when needed:

**Stop Running Containers:**
```bash
# List running containers
docker ps

# Stop a specific container by ID or name
docker stop <container_id_or_name>

# Stop all running containers
docker stop $(docker ps -q)

# Force stop (if container won't stop gracefully)
docker kill <container_id_or_name>
```

**Docker Compose:**
```bash
# Stop and remove containers
docker-compose down

# Stop without removing containers
docker-compose stop

# Stop and remove containers, networks, volumes
docker-compose down -v
```

**Cleanup Docker Resources:**
```bash
# Remove the docs-pipeline image
make clean

# Or manually:
docker rmi docs-pipeline

# Clean only output files (keep Docker image)
make clean-output

# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove all unused volumes
docker volume prune

# Clean everything (containers, images, networks, build cache)
docker system prune -a
```

**Emergency Stop:**
```bash
# If a container is stuck or unresponsive:
docker ps  # Get the container ID
docker kill <container_id>

# Or stop all docs-pipeline containers:
docker ps | grep docs-pipeline | awk '{print $1}' | xargs docker kill
```

> **💡 Tip:** The `--rm` flag in our Docker commands automatically removes containers after they finish, so you typically don't need to manually clean up containers.

## Project Structure

```
docs/
├── main.py                 # Wrapper script (run from docs/)
├── README.md              # This file
├── assets/
│   └── CognicAI_logo.png  # Logo for title page
├── scripts/
│   ├── main.py            # Main pipeline script
│   ├── extract_mermaid.py # Extracts mermaid blocks
│   ├── convert_mermaid.py # Converts .mmd to .png
│   └── replace_mermaid.py # Replaces mermaid with images
├── styles/
│   └── style-preamble.tex # LaTeX styling configuration
└── output/
    ├── markdown/          # Processed markdown files
    ├── pdf/              # Generated PDF files
    └── temp/             # Temporary files (auto-cleaned)
```

## Usage

### Recommended: Docker with Makefile

The easiest and most reliable way to use the pipeline:

```bash
# Process files in current directory
make run FILE=README.md

# Process files from any location
make run-custom-all PATH=/path/to/your/markdown/files
```

### Alternative: Direct Python Execution

If you have all dependencies installed locally:

```bash
# macOS/Linux
cd docs/
python3 main.py <path/to/file.md>
python3 main.py <path/to/folder>  # Process all .md files

# Windows (Command Prompt or PowerShell)
cd docs
python main.py <path/to/file.md>
python main.py <path/to/folder>   # Process all .md files
```

**Example:**
```bash
# macOS/Linux
python3 main.py ../temp/Reports/Markdown/Epic_Plan.md
python3 main.py ../temp/Reports/Markdown  # All files

# Windows
python main.py ..\temp\Reports\Markdown\Epic_Plan.md
python main.py ..\temp\Reports\Markdown   # All files
```

> **💡 Tip:** Using Docker eliminates dependency management issues and ensures consistent results across different systems.

## Pipeline Steps

### Step 1: Extract Mermaid Blocks
- Scans the markdown file for mermaid code blocks
- Extracts each diagram into a separate `.mmd` file
- Files are named: `{basename}_diagram_{index}.mmd`

### Step 2: Convert Diagrams to Images
- Uses Mermaid CLI to render each `.mmd` file as `.png`
- Only runs if mermaid blocks are found
- Images are optimized for print quality

### Step 3: Replace Mermaid Code with Images
- Replaces mermaid code blocks with image references
- Uses relative paths for portability
- If no mermaid blocks exist, copies the original file

### Step 4: Generate PDF
- Removes emoji characters (LaTeX incompatible)
- Escapes special LaTeX characters in titles
- Generates custom title page with logo
- Creates table of contents
- Compiles to PDF using XeLaTeX via Pandoc
- Cleans up temporary files

## Output Organization

After processing, files are organized in the `output/` directory:

```
output/
├── markdown/
│   ├── file1.md
│   ├── file2.md
│   └── file3.md
├── pdf/
│   ├── file1.pdf
│   ├── file2.pdf
│   └── file3.pdf
└── temp/
    └── (empty - auto-cleaned)
```

## Features

### Automatic Title Extraction
The pipeline extracts the document title from the first level-1 heading (`# Title`) and uses it for:
- The title page
- PDF metadata
- Fallback to filename if no heading is found

### LaTeX Special Character Handling
Automatically escapes special characters in titles:
- Underscores (`_`)
- Dollar signs (`$`)
- Ampersands (`&`)
- Percent signs (`%`)
- Hash symbols (`#`)
- Braces (`{`, `}`)
- And more...

### Custom Styling
The pipeline applies professional styling via `styles/style-preamble.tex`:
- Custom fonts (Barlow, Fira Code)
- Code syntax highlighting
- Proper spacing and margins
- GitHub-inspired design

### Title Page Components
Each generated PDF includes:
- Document title (large, bold)
- Author name (Harsha Vardhanu Parnandi)
- Current date (auto-generated)
- CognicAI logo
- Table of contents

## Examples

### Example 1: Single File with Mermaid Diagrams

```bash
# macOS/Linux
python3 main.py architecture.md

# Windows
python main.py architecture.md
```

**Output:**
```
📦 Step 1/4 — Extracting mermaid blocks …
   Found 3 mermaid block(s).

🖼 Step 2/4 — Converting .mmd files to .png …
   [Generated 3 diagrams]

✏️ Step 3/4 — Replacing mermaid blocks with image references …
   Written: output/markdown/architecture.md

📄 Step 4/4 — Generating PDF …
   PDF: output/pdf/architecture.pdf

✅ Pipeline complete!
   Markdown: output/markdown/architecture.md
   PDF: output/pdf/architecture.pdf
```

### Example 2: Folder with Multiple Files

```bash
# macOS/Linux
python3 main.py ../reports/

# Windows
python main.py ..\reports
```

**Output:**
```
🗂 Found 5 markdown file(s) in reports/

============================================================
Processing 1/5: report1.md
============================================================
[... processing report1 ...]

============================================================
Processing 2/5: report2.md
============================================================
[... processing report2 ...]

[... continues for all files ...]

✅ All 5 file(s) processed successfully!
```

### Example 3: File Without Mermaid Diagrams

```bash
# macOS/Linux
python3 main.py simple-doc.md

# Windows
python main.py simple-doc.md
```

**Output:**
```
📦 Step 1/4 — Extracting mermaid blocks …
⚠️  No mermaid blocks found. Proceeding with PDF generation.

   Written: output/markdown/simple-doc.md

📄 Step 4/4 — Generating PDF …
   PDF: output/pdf/simple-doc.pdf

✅ Pipeline complete!
   Markdown: output/markdown/simple-doc.md
   PDF: output/pdf/simple-doc.pdf
```

### Example 4: Process Files from Custom Directory (Docker)

```bash
# Process all reports from another project
make run-custom-all PATH=/Users/username/Documents/GitHub/MyProject/reports/markdown

# Process specific file from Desktop
make run-custom PATH=/Users/username/Desktop/docs FILE=meeting-notes.md

# Process files from external drive
make run-custom-all PATH=/Volumes/USB_Drive/documentation
```

**Output:**
```
📚 Processing all .md files from /Users/username/Documents/GitHub/MyProject/reports/markdown...

🗂  Found 9 markdown file(s) in input/

============================================================
Processing 1/9: BACKEND_ARCHITECTURE_ANALYSIS.md
============================================================
[... processing continues ...]

✅ All 9 file(s) processed successfully!
```

> **💡 Tip:** Output files are always saved to `./output` in the current directory, regardless of input location.

## Common Use Cases

### 1. Process Documentation from Multiple Projects

Convert markdown files from different projects without changing directories:

```bash
# Process reports from project A
make run-custom-all PATH=/Users/username/Projects/ProjectA/docs

# Process documentation from project B  
make run-custom-all PATH=/Users/username/Projects/ProjectB/documentation

# All PDFs are saved to ./output/pdf/ for easy organization
```

### 2. Batch Process Files on External Storage

Process markdown files from USB drives, network shares, or cloud storage:

```bash
# External USB drive (macOS/Linux)
make run-custom-all PATH=/Volumes/MyBackup/markdown_files

# Windows external drive
make run-custom-all PATH=E:\\Documents\\Reports

# Network share (macOS)
make run-custom-all PATH=/Volumes/CompanyShare/Documentation
```

### 3. Continuous Integration / Build Pipeline

Integrate into your project's build process:

```bash
# In your CI/CD script
cd /path/to/docs-pipeline
make run-custom-all PATH=/path/to/project/documentation
# PDFs are generated in ./output/pdf/
# Copy or upload PDFs as needed
```

### 4. Cross-Project Report Generation

Convert reports from active development projects:

```bash
# Generate PDFs from actively developed markdown files
make run-custom-all PATH=/Users/username/Documents/GitHub/SequelSpeak/temp/Reports/Markdown

# All PDFs available in one location for review or distribution
ls -lh output/pdf/
```

### 5. Desktop Quick Conversion

Keep the pipeline in one location and process files anywhere:

```bash
# Convert a file from Desktop without moving it
make run-custom PATH=/Users/username/Desktop FILE=notes.md

# Convert meeting notes from Downloads
make run-custom PATH=/Users/username/Downloads FILE=meeting-2026-02-11.md
```

## Best Practices

### File Organization
- Keep your docs pipeline in a dedicated folder
- Generated PDFs accumulate in `./output/pdf/` - organize or move them as needed
- Use `make clean-output` to clear old PDFs before new batch processing

### Custom Paths
- Use absolute paths for reliability: `/Users/username/path/to/files`
- Or relative paths from pipeline directory: `../sibling-project/docs`
- Ensure the path exists and contains `.md` files

### Batch Processing
- Process entire folders with `make run-custom-all PATH=/path/to/folder`
- Process single files with `make run-custom PATH=/path/to/folder FILE=file.md`
- Review output in `./output/pdf/` after completion

### Docker vs Native
- **Docker (Recommended)**: Zero dependency management, consistent results
- **Native Python**: Faster execution if all dependencies are properly installed
- Use Docker for reliability, native for speed (if set up correctly)

### Resource Management and Cleanup
- **Regular cleanup**: Run `make clean-output` periodically to remove old PDFs
- **Docker cleanup**: Use `docker system prune` monthly to free up disk space
- **Container management**: Containers auto-remove with `--rm` flag (already included)
- **Stop stuck processes**: Use `docker ps` to check running containers, then `docker stop <id>` if needed
- **Image rebuilds**: Use `make clean` before rebuilding if you encounter issues
- **Disk space**: Each PDF is 150-300KB; monitor `./output/pdf/` size for large batches
- **Docker storage**: Docker images take ~2-3GB; clean up unused images with `docker image prune`

### When to Use Stop Commands
- **Normal operation**: No need to stop - containers auto-stop when processing completes
- **Stuck container**: If a process hangs, use `docker ps` then `docker stop <id>`
- **System resources**: If your system is slow, check `docker ps` for accidentally running containers
- **Before rebuilding**: Run `make clean` to remove old image before `make build`
- **Disk cleanup**: Monthly cleanup with `docker system prune` to reclaim space

## Troubleshooting

### Pandoc Errors

**Error: `pandoc: command not found`**
- **macOS**: `brew install pandoc`
- **Linux**: `sudo apt-get install pandoc`
- **Windows**: `choco install pandoc` or download installer from [pandoc.org](https://pandoc.org/)
- After installation, restart your terminal/command prompt

**Error: `xelatex not found`**
- **macOS**: Install MacTeX via `brew install --cask mactex`
- **Linux**: Install TeX Live via `sudo apt-get install texlive-full`
- **Windows**: Install MiKTeX from [miktex.org](https://miktex.org/) or TeX Live
- Add the LaTeX bin directory to your PATH environment variable

### Font Errors

**Error: `Font 'Barlow' not found`**
- Download and install Barlow from Google Fonts
- Restart your terminal after installation

### Mermaid Errors

**Error: `mmdc: command not found`**
- Install Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`

**Error: Diagram rendering fails**
- Check your Mermaid syntax at [mermaid.live](https://mermaid.live/)
- Ensure Chrome/Chromium is installed (required by mermaid-cli)

### Path Errors

**Error: `path not found`**
- Use relative paths from the `docs/` directory
- Or use absolute paths
- **Windows users**: Use backslashes (`\`) or forward slashes (`/`) in paths
  - Example: `python main.py C:\Users\Name\Documents\file.md`
  - Or: `python main.py C:/Users/Name/Documents/file.md`

### Windows-Specific Issues

**Error: `python: command not found`**
- Make sure Python is installed and added to PATH
- Try using `py` instead of `python`: `py main.py file.md`
- Verify installation: `python --version` or `py --version`

**Error: `Permission denied` when installing fonts**
- Right-click the font file and select "Install for all users" (requires admin)

### Docker-Specific Issues

**Error: `docker: command not found` (macOS)**
- Docker is installed but not in Make's PATH
- **Solution**: The updated Makefile automatically detects Docker location
- Verify Docker is running: `docker --version`
- If issue persists, use Docker commands directly instead of `make`

**Error: `Cannot connect to the Docker daemon`**
- Docker Desktop is not running
- **Solution**: Start Docker Desktop and wait for it to fully initialize
- Verify: `docker info` should show Docker information

**Error: `Error response from daemon: user declined directory sharing`**
- Docker doesn't have permission to access the folder
- **macOS**: Docker Desktop → Preferences → Resources → File Sharing → Add path
- **Windows**: Docker Desktop → Settings → Resources → File Sharing → Add drive

**Error: `no such file or directory` with custom paths**
- Verify the path exists: `ls -la /path/to/folder` (macOS/Linux)
- Ensure path is absolute, not relative
- Check for typos in the path
- Windows: Use forward slashes or escape backslashes: `C:/Users/...` or `C:\\Users\\...`

**Error: Build fails with `Dockerfile not found`**
- Make sure you're running commands from the docs pipeline directory
- Current directory should contain `Dockerfile`, `Makefile`, etc.

**Error: `Image not found: docs-pipeline`**
- Build the Docker image first: `make build`
- Or: `docker build -t docs-pipeline .`

**Performance: Docker is slow**
- Increase Docker Desktop memory: Settings → Resources → Memory (4GB+ recommended)
- On macOS, consider using Docker virtualization framework (Settings → General)
- Initial build takes 10-20 minutes; subsequent runs are faster

### Process and Container Issues

**Container won't stop or is stuck:**
```bash
# 1. Find the container ID
docker ps

# 2. Try graceful stop (wait 10 seconds)
docker stop <container_id>

# 3. If still running, force kill
docker kill <container_id>

# 4. Emergency: Stop ALL running containers
docker stop $(docker ps -q)
```

**Long-running process needs to be cancelled:**
- Press `Ctrl+C` in the terminal to interrupt
- If container continues running, use `docker ps` and `docker stop <id>`
- For make commands, `Ctrl+C` should stop both make and the container

**Container auto-restarting unexpectedly:**
```bash
# Check if using docker-compose with restart policy
docker-compose down

# Remove any restart policies
docker update --restart=no <container_id>
```

**"Resource busy" or "file locked" errors:**
- A container might still be accessing files
- Stop all containers: `docker stop $(docker ps -q)`
- Wait a few seconds, then retry
- Check for zombie processes: `docker ps -a`

**Out of disk space:**
```bash
# Check Docker disk usage
docker system df

# Clean up everything safely
docker system prune -a

# More aggressive cleanup (removes volumes too)
docker system prune -a --volumes
```

### Custom Path Issues

**Error: Path not accessible from Docker**
- Ensure Docker has file sharing permissions for the directory
- Try using absolute paths instead of relative paths
- Verify the path exists and contains `.md` files

**Output files not appearing**
- Check `./output/pdf/` in the **docs pipeline directory**, not the source directory
- Output always goes to the pipeline's output folder
- If needed, copy PDFs to source location after generation
- Or copy font files to `C:\Windows\Fonts\`

**Error: LaTeX compilation fails with font errors**
- Ensure fonts are installed system-wide (not just for current user)
- Try using the Windows Font Viewer to install fonts
- Restart your terminal after font installation

**Error: Node/npm command not found**
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Or use Chocolatey: `choco install nodejs`
- Restart terminal after installation

**Path separator issues**
- The script handles both `/` and `\` path separators on Windows
- Use quotes around paths with spaces: `python main.py "path with spaces\file.md"`

## Configuration

### Customizing the Title Page

Edit the title page template in [scripts/main.py](scripts/main.py) (around line 159):

```python
titlepage_tex = rf"""
\begin{{titlepage}}
\centering

\vspace*{{3cm}}

{{\Huge\bfseries {doc_title_escaped}\par}}

\vspace{{1.5cm}}

{{\Large Your Name Here\par}}  # Change author name

\vspace{{1cm}}

{{\large \today\par}}

\vfill

\includegraphics[height=40pt]{{{logo_path}}}

\vspace{{1cm}}
\end{{titlepage}}
```

### Customizing Styling

Edit the LaTeX preamble in [styles/style-preamble.tex](styles/style-preamble.tex) to adjust:
- Colors
- Font sizes
- Spacing
- Headers/footers
- Code block styling

### Changing Output Directory

Modify the `PROJECT_ROOT` and `output_dir` variables in [scripts/main.py](scripts/main.py):

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
output_dir = PROJECT_ROOT / "output"  # Change this path
```

## Advanced Usage

### Custom Resource Paths

If you have images in your markdown, place them in:
- `docs/assets/` - For global assets
- Same directory as the source markdown - For local assets

They will be automatically copied to the temp directory during processing.

### Supported Image Formats

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- SVG (`.svg`)

### Table of Contents Depth

The TOC depth is set to 3 levels. To change it, edit [scripts/main.py](scripts/main.py):

```python
"--toc-depth=3",  # Change to your preferred depth (1-5)
```

## CI/CD Integration

### GitHub Actions

The repository includes automated workflows for building and testing:

**Workflow Features:**
- ✅ Automatic Docker image build on push
- ✅ Basic functionality testing with README.md
- ✅ Custom path functionality testing
- ✅ Dockerfile linting with Hadolint
- ✅ Artifact uploads (PDFs retained for 30 days)
- ✅ Build caching for faster runs

**Workflow Configuration:** [`.github/workflows/docker.yml`](.github/workflows/docker.yml)

**Key Fix for CI/CD:**
The workflow uses `load: true` in the Docker build action to ensure the image is available:
```yaml
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    load: true  # Critical for local image usage
    tags: docs-pipeline:latest
```

**View Workflow Results:**
- Go to repository → Actions tab
- Download generated PDFs from artifacts
- Review job summaries for build status

### Integration with Your Projects

Add this pipeline to your project's CI/CD:

```yaml
# .github/workflows/docs-pipeline.yml
name: Generate Documentation

on:
  push:
    paths:
      - 'docs/**/*.md'
  workflow_dispatch:

jobs:
  generate-pdfs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Checkout docs-pipeline
        uses: actions/checkout@v4
        with:
          repository: your-org/docs-pipeline
          path: pipeline
      
      - name: Build pipeline image
        run: |
          cd pipeline
          docker build -t docs-pipeline:latest .
      
      - name: Generate PDFs
        run: |
          cd pipeline
          docker run --rm \
            -v ${{ github.workspace }}/docs:/app/input:ro \
            -v ${{ github.workspace }}/output:/app/output \
            docs-pipeline:latest python3 main.py /app/input
      
      - name: Upload PDFs
        uses: actions/upload-artifact@v4
        with:
          name: documentation-pdfs
          path: output/pdf/*.pdf
```

**For detailed CI/CD setup and troubleshooting**, see [`.github/workflows/README.md`](.github/workflows/README.md)

### Local CI Testing

Test CI workflow locally before pushing:

```bash
# Build (simulates CI build)
make build

# Test basic functionality
make test

# Test custom paths
mkdir -p /tmp/ci-test
cp README.md /tmp/ci-test/
make run-custom-all PATH=/tmp/ci-test

# Verify outputs
ls -lh output/pdf/
```

## Contributing

When modifying the pipeline:

1. **Test with various inputs**: Files with/without mermaid, different sizes
2. **Check error handling**: Invalid paths, missing dependencies
3. **Verify cleanup**: Ensure temp files are removed
4. **Update this README**: Document any new features or changes

## License

This pipeline is part of the SequelSpeak project.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [DOCKER.md](DOCKER.md) for detailed Docker documentation
3. See [DOCKER_QUICK_REF.md](DOCKER_QUICK_REF.md) for command reference
4. Verify all dependencies are installed (if not using Docker)
5. Test with a simple markdown file first
6. Check the terminal output for specific error messages

## Quick Reference Card

### Processing Commands

| Task | Command |
|------|---------|
| **Setup** | `./setup.sh` (Mac/Linux) or `setup.bat` (Windows) |
| **Build** | `make build` |
| **Test** | `make test` |
| **Current dir file** | `make run FILE=file.md` |
| **Current dir all** | `make run-all` |
| **Custom dir file** | `make run-custom PATH=/path/to/folder FILE=file.md` |
| **Custom dir all** | `make run-custom-all PATH=/path/to/folder` |
| **Help** | `make help` |

### Stop & Cleanup Commands

| Task | Command |
|------|---------|
| **Stop container** | `docker stop <container_id>` |
| **Stop all containers** | `docker stop $(docker ps -q)` |
| **Kill stuck container** | `docker kill <container_id>` |
| **Docker Compose stop** | `docker-compose down` |
| **Clean output files** | `make clean-output` |
| **Clean everything** | `make clean` |
| **Remove Docker image** | `docker rmi docs-pipeline` |
| **Prune containers** | `docker container prune` |
| **Prune images** | `docker image prune` |
| **Full Docker cleanup** | `docker system prune -a` |
| **List running** | `docker ps` |
| **List all containers** | `docker ps -a` |

---

**Version**: 2.0.0 (Custom Path Support)  
**Last Updated**: February 11, 2026  
**Developed by**: [Cognic AI](https:/github.com/CognicAI)
