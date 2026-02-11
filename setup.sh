#!/bin/bash

# Documentation Pipeline - Quick Setup Script
# This script sets up the Docker environment for the documentation pipeline

set -e

echo "🚀 Documentation Pipeline Setup"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
check_docker() {
    echo -n "Checking for Docker... "
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        echo -e "${RED}Docker is not installed. Please install Docker Desktop:${NC}"
        echo "  macOS: https://docs.docker.com/desktop/install/mac-install/"
        echo "  Windows: https://docs.docker.com/desktop/install/windows-install/"
        echo "  Linux: https://docs.docker.com/desktop/install/linux-install/"
        exit 1
    fi
}

# Check if Docker is running
check_docker_running() {
    echo -n "Checking if Docker is running... "
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        echo -e "${RED}Docker is not running. Please start Docker Desktop.${NC}"
        exit 1
    fi
}

# Check if Docker Compose is available
check_docker_compose() {
    echo -n "Checking for Docker Compose... "
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Docker Compose not found (optional)"
    fi
}

# Create output directories
create_directories() {
    echo -n "Creating output directories... "
    mkdir -p output/markdown output/pdf output/temp
    echo -e "${GREEN}✓${NC}"
}

# Build Docker image
build_image() {
    echo ""
    echo "🐋 Building Docker image..."
    echo "This may take 10-20 minutes on first run (downloading packages)"
    echo ""
    
    if docker build -t docs-pipeline .; then
        echo ""
        echo -e "${GREEN}✅ Docker image built successfully!${NC}"
        return 0
    else
        echo ""
        echo -e "${RED}❌ Docker build failed${NC}"
        exit 1
    fi
}

# Run test
run_test() {
    echo ""
    echo "🧪 Testing with README.md..."
    echo ""
    
    if docker run --rm \
        -v "$(pwd):/app/input:ro" \
        -v "$(pwd)/output:/app/output" \
        docs-pipeline python3 main.py /app/input/README.md; then
        echo ""
        echo -e "${GREEN}✅ Test successful!${NC}"
        echo "Check output/pdf/README.pdf"
        return 0
    else
        echo ""
        echo -e "${RED}❌ Test failed${NC}"
        exit 1
    fi
}

# Show usage instructions
show_usage() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}✨ Setup Complete!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Quick Start Commands:"
    echo ""
    echo -e "${BLUE}Using Makefile (recommended):${NC}"
    echo "  make run FILE=README.md          # Process a file from current directory"
    echo "  make run-all                     # Process all .md files in current directory"
    echo "  make run-custom PATH=/path/to/folder FILE=file.md  # Process file from custom path"
    echo "  make run-custom-all PATH=/path/to/folder           # Process all files from custom path"
    echo "  make bash                        # Open shell in container"
    echo "  make clean                       # Clean up"
    echo ""
    echo -e "${BLUE}Using Docker directly:${NC}"
    echo "  # Current directory:"
    echo "  docker run --rm \\"
    echo "    -v \$(pwd):/app/input:ro \\"
    echo "    -v \$(pwd)/output:/app/output \\"
    echo "    docs-pipeline python3 main.py /app/input/your-file.md"
    echo ""
    echo "  # Custom directory:"
    echo "  docker run --rm \\"
    echo "    -v /path/to/your/folder:/app/input:ro \\"
    echo "    -v \$(pwd)/output:/app/output \\"
    echo "    docs-pipeline python3 main.py /app/input"
    echo ""
    echo -e "${BLUE}Using Docker Compose:${NC}"
    echo "  docker-compose run docs-pipeline python3 main.py /app/input/README.md"
    echo "  # For custom paths, create docker-compose.override.yml (see example file)"
    echo ""
    echo "📚 Documentation:"
    echo "  README.md     - Main documentation"
    echo "  DOCKER.md     - Detailed Docker guide"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main setup flow
main() {
    check_docker
    check_docker_running
    check_docker_compose
    create_directories
    
    echo ""
    read -p "Build Docker image now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_image
        
        echo ""
        read -p "Run test with README.md? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_test
        fi
    else
        echo ""
        echo -e "${YELLOW}Skipped build. Run 'make build' or 'docker build -t docs-pipeline .' when ready.${NC}"
    fi
    
    show_usage
}

# Run main setup
main
