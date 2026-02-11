# Docker Guide for Documentation Pipeline

This guide provides detailed information about using Docker with the Documentation Pipeline.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Commands](#docker-commands)
- [Makefile Commands](#makefile-commands)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Prerequisites

- **Docker Desktop** installed and running
  - [Download for Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Download for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Download for Linux](https://docs.docker.com/desktop/install/linux-install/)

## Quick Start

### 1. Build the Docker Image

```bash
# Using Makefile (recommended)
make build

# Or using Docker directly
docker build -t docs-pipeline .
```

### 2. Process a Markdown File

```bash
# Using Makefile (current directory)
make run FILE=README.md

# Using Makefile (custom directory)
make run-custom PATH=/path/to/folder FILE=yourfile.md
make run-custom-all PATH=/path/to/folder

# Or using Docker Compose
docker-compose run docs-pipeline python3 main.py /app/input/README.md

# Or using Docker directly (current directory)
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input/README.md

# Or using Docker directly (custom directory)
docker run --rm \
  -v /path/to/your/folder:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input
```

### 3. Check the Output

Results will be in:
- `output/markdown/` - Processed markdown files
- `output/pdf/` - Generated PDF files

## Docker Commands

### Build Image

```bash
docker build -t docs-pipeline .
```

### Process Single File

```bash
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input/your-file.md
```

**Windows PowerShell:**
```powershell
docker run --rm `
  -v ${PWD}:/app/input:ro `
  -v ${PWD}/output:/app/output `
  docs-pipeline python3 main.py /app/input/your-file.md
```

### Process All Files in Directory

```bash
# Current directory
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input

# Custom directory
docker run --rm \
  -v /path/to/your/folder:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input
```

**Example with specific path:**
```bash
docker run --rm \
  -v /Users/username/Documents/GitHub/SequelSpeak/temp/Reports:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input
```

### Interactive Shell

```bash
docker run --rm -it \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline /bin/bash
```

## Makefile Commands

The included Makefile provides convenient shortcuts:

```bash
# Show help
make help

# Build the Docker image
make build

# Test with README.md
make test

# Process a specific file from current directory
make run FILE=README.md
make run FILE=output/markdown/Epic_Plan.md

# Process file from custom directory
make run-custom PATH=/path/to/folder FILE=yourfile.md

# Process all .md files from custom directory
make run-custom-all PATH=/path/to/folder

# Process all .md files in current directory
make run-all

# Open interactive shell
make bash

# Clean Docker image and outputs
make clean

# Clean only output files
make clean-output
```

**Custom Path Examples:**
```bash
# Process specific Reports folder
make run-custom-all PATH=/Users/harshavardhan/Documents/GitHub/SequelSpeak/temp/Reports

# Process single file from custom location
make run-custom PATH=/Users/username/Desktop/documents FILE=report.md
```

## Docker Compose

### Configuration

The `docker-compose.yml` file is configured for easy usage:

```yaml
version: '3.8'

services:
  docs-pipeline:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./:/app/input:ro
      - ./output:/app/output
```

### Commands

```bash
# Process a file
docker-compose run docs-pipeline python3 main.py /app/input/README.md

# Process all files
docker-compose run docs-pipeline python3 main.py /app/input

# Rebuild image
docker-compose build

# Remove containers
docker-compose down
```

## Troubleshooting

### Issue: Port Already in Use

**Solution:** This is not a server application, so no ports are needed. If you copied from another docker-compose, remove port mappings.

### Issue: Permission Denied on Output Files

**Solution:** The container runs as root. Fix permissions:

```bash
# Linux/Mac
sudo chown -R $USER:$USER output/

# Or run container with your user ID
docker run --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input/README.md
```

### Issue: Fonts Not Rendering

**Solution:** Rebuild the image to ensure fonts are installed:

```bash
docker build --no-cache -t docs-pipeline .
```

### Issue: Mermaid Diagrams Not Rendering

**Solution:** Ensure Chromium is properly configured:

```bash
# Check Puppeteer path
docker run --rm docs-pipeline which chromium-browser

# If missing, rebuild with --no-cache
docker build --no-cache -t docs-pipeline .
```

### Issue: Out of Memory

**Solution:** Increase Docker memory allocation:
- Docker Desktop → Settings → Resources → Memory
- Increase to at least 4GB for large documents

### Issue: Slow Build Times

**Solution:** 
1. Use Docker layer caching
2. Uncomment `.dockerignore` entries to exclude unnecessary files
3. Build once and reuse: `make build` only when Dockerfile changes

## Advanced Usage

### Custom Fonts

To add custom fonts, modify the Dockerfile:

```dockerfile
# Add to Dockerfile after existing font installation
RUN mkdir -p /usr/share/fonts/truetype/custom && \
    cd /tmp && \
    wget https://example.com/your-font.ttf && \
    mv your-font.ttf /usr/share/fonts/truetype/custom/ && \
    fc-cache -f -v
```

### Environment Variables

Create a `.env` file (use `.env.example` as template):

```bash
cp .env.example .env
```

Then modify docker-compose.yml to use it:

```yaml
services:
  docs-pipeline:
    env_file:
      - .env
```

### Volume Mounting

Mount specific directories:

```bash
# Input from specific directory
docker run --rm \
  -v /path/to/markdown/files:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input

# Output to specific directory
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v /path/to/output:/app/output \
  docs-pipeline python3 main.py /app/input/README.md
```

### Multi-Stage Build (Optimization)

For production, you can optimize the Dockerfile with multi-stage builds to reduce image size.

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build Documentation

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t docs-pipeline .
      
      - name: Generate PDFs
        run: |
          docker run --rm \
            -v $(pwd):/app/input:ro \
            -v $(pwd)/output:/app/output \
            docs-pipeline python3 main.py /app/input
      
      - name: Upload PDFs
        uses: actions/upload-artifact@v3
        with:
          name: documentation-pdfs
          path: output/pdf/*.pdf
```

## Architecture

### Docker Image Contents

- **Base:** Ubuntu 22.04
- **Python:** 3.x (system package)
- **Pandoc:** Latest from apt
- **LaTeX:** TeX Live with XeLaTeX
- **Mermaid CLI:** @mermaid-js/mermaid-cli (npm)
- **Chromium:** For Mermaid rendering
- **Fonts:** Barlow, Fira Code

### Image Size

Approximately 2-3 GB due to full LaTeX installation.

### Build Time

First build: 10-20 minutes (downloading packages)
Subsequent builds: <1 minute (using cache)

## Performance Tips

1. **Build Once:** Build the image once and reuse it
2. **Use Makefile:** Simplifies commands
3. **Process Bulk:** Process multiple files at once instead of one-by-one
4. **Mount Wisely:** Use read-only mounts for source files (`:ro`)
5. **Clean Regularly:** Run `make clean-output` to free disk space

## Security Considerations

- Source files are mounted read-only (`:ro`)
- Container runs isolated from host system
- No network access needed for processing
- Output directory is the only writable mount

## Support

For issues related to:
- **Docker:** Check Docker Desktop logs
- **Fonts:** Verify font installation in container: `make bash` then `fc-list`
- **Mermaid:** Check Chromium: `make bash` then `mmdc --version`
- **LaTeX:** Verify XeLaTeX: `make bash` then `xelatex --version`
