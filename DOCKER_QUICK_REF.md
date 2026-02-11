# Docker Quick Reference

## Essential Commands

### Setup
```bash
# Run setup script (Mac/Linux)
./setup.sh

# Run setup script (Windows)
setup.bat

# Or manually build
make build
# OR
docker build -t docs-pipeline .
```

### Basic Usage
```bash
# Process single file (current directory)
make run FILE=README.md

# Process all files (current directory)
make run-all

# Process from custom directory
make run-custom PATH=/path/to/folder FILE=file.md
make run-custom-all PATH=/path/to/folder

# Test
make test
```

### Docker Direct Commands

**Process a file (current directory):**
```bash
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline python3 main.py /app/input/README.md
```

**Process from custom directory:**
```bash
docker run --rm \
  -v /path/to/your/folder:/app/input:ro \
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
  -v C:\\path\\to\\folder:/app/input:ro `
  -v ${PWD}/output:/app/output `
  docs-pipeline python3 main.py /app/input
```

### Docker Compose

```bash
# Process a file
docker-compose run docs-pipeline python3 main.py /app/input/README.md

# Process all files
docker-compose run docs-pipeline python3 main.py /app/input

# Rebuild
docker-compose build

# Clean up
docker-compose down
```

### Makefile Commands

```bash
make help                        # Show all commands
make build                       # Build Docker image
make test                        # Test with README.md
make run FILE=...                # Process specific file
make run-all                     # Process all .md files
make run-custom PATH=... FILE=...  # Process file from custom path
make run-custom-all PATH=...     # Process all from custom path
make bash                        # Open shell in container
make clean                       # Remove image and outputs
make clean-output                # Remove only outputs
```

**Custom Path Examples:**
```bash
# Process all files from Reports folder
make run-custom-all PATH=/Users/username/Documents/GitHub/SequelSpeak/temp/Reports

# Process specific file from custom location
make run-custom PATH=/Users/username/Desktop/docs FILE=report.md
```

### Debugging

```bash
# Open interactive shell
make bash
# OR
docker run --rm -it \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline /bin/bash

# Check fonts
docker run --rm docs-pipeline fc-list | grep -i barlow

# Check Mermaid CLI
docker run --rm docs-pipeline mmdc --version

# Check XeLaTeX
docker run --rm docs-pipeline xelatex --version
```

### Cleanup

```bash
# Clean outputs only
make clean-output

# Remove Docker image
docker rmi docs-pipeline

# Remove all unused Docker resources
docker system prune -a
```

## File Locations

- **Input:** Current directory (mounted read-only)
- **Output:** `output/` directory
  - `output/pdf/` - Generated PDFs
  - `output/markdown/` - Processed markdown
  - `output/temp/` - Temporary files (auto-cleaned)

## Environment Variables

Create `.env` file:
```bash
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Run `sudo chown -R $USER:$USER output/` |
| Fonts not rendering | Rebuild: `docker build --no-cache -t docs-pipeline .` |
| Mermaid fails | Check Chromium: `docker run --rm docs-pipeline which chromium-browser` |
| Out of memory | Increase Docker Desktop memory (Settings → Resources) |
| Slow build | Normal on first run (10-20 min); cached after |

## Links

- [Full Documentation](README.md)
- [Detailed Docker Guide](DOCKER.md)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Makefile Reference](Makefile)
