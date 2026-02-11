# Use Ubuntu as base image for better LaTeX support
FROM ubuntu:22.04

# Set shell options for better error handling
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # Core utilities
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    # Python
    python3 \
    python3-pip \
    # Pandoc
    pandoc \
    # LaTeX distribution (TeX Live)
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-latex-recommended \
    lmodern \
    # Chromium for Mermaid rendering
    chromium-browser \
    # Font utilities
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x (LTS) from NodeSource
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && apt-get install --no-install-recommends -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Verify Node.js installation
RUN node --version && npm --version

# Install Mermaid CLI with pinned version
RUN npm install -g @mermaid-js/mermaid-cli@10.6.1

# Install required fonts
# Download and install Barlow font
RUN mkdir -p /usr/share/fonts/truetype/barlow
WORKDIR /tmp
RUN wget --progress=dot:giga https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Regular.ttf && \
    wget --progress=dot:giga https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Bold.ttf && \
    wget --progress=dot:giga https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Italic.ttf && \
    wget --progress=dot:giga https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-BoldItalic.ttf && \
    mv ./*.ttf /usr/share/fonts/truetype/barlow/

# Download and install Fira Code font
RUN mkdir -p /usr/share/fonts/truetype/firacode
WORKDIR /tmp
RUN wget --progress=dot:giga https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip && \
    apt-get update && apt-get install --no-install-recommends -y unzip && \
    unzip Fira_Code_v6.2.zip -d firacode && \
    mv firacode/ttf/*.ttf /usr/share/fonts/truetype/firacode/ && \
    rm -rf firacode Fira_Code_v6.2.zip && \
    apt-get remove -y unzip && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -f -v

# Set Puppeteer environment for Mermaid CLI
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Switch back to app directory
WORKDIR /app

# Copy application files
COPY . /app/

# Create output directories
RUN mkdir -p /app/output/markdown /app/output/pdf /app/output/temp

# Set up volumes for input/output
VOLUME ["/app/input", "/app/output"]

# Make the main script executable
RUN chmod +x /app/main.py

# Default command - show usage
CMD ["python3", "main.py"]
