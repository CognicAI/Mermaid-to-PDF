#!/usr/bin/env python3
"""
remove_backticks.py – Remove inline code backticks from markdown text.

This script removes single backticks (`) used for inline code formatting,
converting `code` to code. This is useful when generating PDFs where
backticks might not render correctly or are not desired.

Usage:
    from remove_backticks import remove_inline_backticks
    
    text = "This is `inline code` and more `text`."
    cleaned = remove_inline_backticks(text)
    # Result: "This is inline code and more text."
"""

import re
from pathlib import Path


# Pattern to match inline code (single backticks)
# Matches: `text` but not ``` (code blocks)
INLINE_CODE_PATTERN = re.compile(r'`([^`\n]+?)`')


def remove_inline_backticks(text: str) -> str:
    """
    Remove inline code backticks from markdown text.
    
    Replaces `code` with code while preserving the content.
    Does not affect code blocks (```) since they should already
    be processed by earlier pipeline stages.
    
    Args:
        text: The markdown text to process
        
    Returns:
        The text with inline backticks removed
    """
    return INLINE_CODE_PATTERN.sub(r'\1', text)


def process_file(input_path: Path, output_path: Path) -> None:
    """
    Process a markdown file to remove inline backticks.
    
    Args:
        input_path: Path to the input markdown file
        output_path: Path to write the processed output
    """
    content = input_path.read_text(encoding="utf-8")
    cleaned = remove_inline_backticks(content)
    output_path.write_text(cleaned, encoding="utf-8")
    print(f"✔ Removed backticks: {output_path}")


def main():
    """Command-line interface for standalone usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python remove_backticks.py <input.md> [output.md]")
        print("If output.md is not specified, will overwrite input.md")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path
    process_file(input_path, output_path)


if __name__ == "__main__":
    main()
