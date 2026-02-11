.PHONY: help build run clean bash test run-custom run-custom-all

# Docker command (auto-detect full path for macOS compatibility)
DOCKER := $(shell which docker 2>/dev/null || echo /usr/local/bin/docker)

# Docker image name
IMAGE_NAME = docs-pipeline

# Default target
help:
	@echo "Documentation Pipeline - Docker Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make build                    - Build the Docker image"
	@echo "  make run FILE=...             - Process a single markdown file"
	@echo "  make run-all                  - Process all .md files in current directory"
	@echo "  make run-custom PATH=... FILE=... - Process file from custom directory"
	@echo "  make run-custom-all PATH=...  - Process all files from custom directory"
	@echo "  make bash                     - Open a bash shell in the container"
	@echo "  make clean                    - Remove Docker image and output files"
	@echo "  make test                     - Test the pipeline with README.md"
	@echo ""
	@echo "Examples:"
	@echo "  make test"
	@echo "  make run FILE=README.md"
	@echo "  make run-custom-all PATH=/Users/you/Documents/myfiles"
	@echo "  make run-custom PATH=/Users/you/Documents/myfiles FILE=report.md"

# Build Docker image
build:
	@echo "🐋 Building Docker image..."
	$(DOCKER) build -t $(IMAGE_NAME) .
	@echo "✅ Build complete!"

# Process a single file
run:
ifndef FILE
	@echo "❌ Error: FILE parameter is required"
	@echo "Usage: make run FILE=your-file.md"
	@exit 1
endif
	@echo "📄 Processing $(FILE)..."
	$(DOCKER) run --rm \
		-v $$(pwd):/app/input:ro \
		-v $$(pwd)/output:/app/output \
		$(IMAGE_NAME) python3 main.py /app/input/$(FILE)

# Process all markdown files in current directory
run-all:
	@echo "📚 Processing all .md files..."
	$(DOCKER) run --rm \
		-v $$(pwd):/app/input:ro \
		-v $$(pwd)/output:/app/output \
		$(IMAGE_NAME) python3 main.py /app/input

# Process a single file from custom directory
run-custom:
ifndef PATH
	@echo "❌ Error: PATH parameter is required"
	@echo "Usage: make run-custom PATH=/path/to/folder FILE=your-file.md"
	@exit 1
endif
ifndef FILE
	@echo "❌ Error: FILE parameter is required"
	@echo "Usage: make run-custom PATH=/path/to/folder FILE=your-file.md"
	@exit 1
endif
	@echo "📄 Processing $(FILE) from $(PATH)..."
	$(DOCKER) run --rm \
		-v $(PATH):/app/input:ro \
		-v $$(pwd)/output:/app/output \
		$(IMAGE_NAME) python3 main.py /app/input/$(FILE)

# Process all markdown files from custom directory
run-custom-all:
ifndef PATH
	@echo "❌ Error: PATH parameter is required"
	@echo "Usage: make run-custom-all PATH=/path/to/folder"
	@exit 1
endif
	@echo "📚 Processing all .md files from $(PATH)..."
	$(DOCKER) run --rm \
		-v $(PATH):/app/input:ro \
		-v $$(pwd)/output:/app/output \
		$(IMAGE_NAME) python3 main.py /app/input

# Run with docker-compose
compose-run:
ifndef FILE
	@echo "❌ Error: FILE parameter is required"
	@echo "Usage: make compose-run FILE=your-file.md"
	@exit 1
endif
	docker-compose run docs-pipeline python3 main.py /app/input/$(FILE)

# Process all with docker-compose
compose-run-all:
	docker-compose run docs-pipeline python3 main.py /app/input

# Open bash shell in container
bash:
	@echo "🐚 Opening shell in container..."
	$(DOCKER) run --rm -it \
		-v $$(pwd):/app/input:ro \
		-v $$(pwd)/output:/app/output \
		$(IMAGE_NAME) /bin/bash

# Test the pipeline with README.md
test: build
	@echo "🧪 Testing pipeline with README.md..."
	@$(MAKE) run FILE=README.md
	@echo "✅ Test complete! Check output/pdf/README.pdf"

# Clean up Docker image and output files
clean:
	@echo "🧹 Cleaning up..."
	-$(DOCKER) rmi $(IMAGE_NAME)
	-rm -rf output/pdf/* output/markdown/* output/temp/*
	@echo "✅ Cleanup complete!"

# Clean only output files
clean-output:
	@echo "🧹 Cleaning output files..."
	-rm -rf output/pdf/* output/markdown/* output/temp/*
	@echo "✅ Output cleaned!"
