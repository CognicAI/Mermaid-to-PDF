from __future__ import annotations

import re
import sys
from pathlib import Path

# Regex to match fenced mermaid blocks
MERMAID_BLOCK_PATTERN = re.compile(
    r"```mermaid\s*[\s\S]*?\s*```",
    re.MULTILINE
)


def replace_mermaid_blocks_with_images(
    markdown_text: str, image_paths: list[str]
) -> str:
    """
    Replace each mermaid fenced code block with its corresponding image
    reference from *image_paths* (matched in order of appearance).
    """
    counter = iter(range(len(image_paths)))

    def _replacer(match: re.Match) -> str:
        idx = next(counter, None)
        if idx is None:
            return match.group(0)  # no more images – leave block as-is
        img = image_paths[idx]
        label = Path(img).stem.replace("_", " ").title()
        return f"![{label}]({img})"

    return MERMAID_BLOCK_PATTERN.sub(_replacer, markdown_text)


def replace_mermaid_blocks(markdown_text: str, replacement: str | None = None) -> str:
    """
    Replace all mermaid fenced code blocks with a static image reference.
    Kept for backward-compatibility with standalone usage.
    """
    if replacement is None:
        replacement = "![Diagram](diagram.png){ width=90% }"
    return MERMAID_BLOCK_PATTERN.sub(replacement, markdown_text)


def process_file(
    md_path: Path,
    image_paths: list[str],
    output_path: Path | None = None,
) -> Path:
    """
    Read *md_path*, replace mermaid blocks with image references, and write
    the result to *output_path* (defaults to overwriting *md_path*).
    Returns the path that was written.
    """
    if output_path is None:
        output_path = md_path

    original_text = md_path.read_text(encoding="utf-8")
    updated_text = replace_mermaid_blocks_with_images(original_text, image_paths)
    output_path.write_text(updated_text, encoding="utf-8")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python replace_mermaid.py <markdown_file> [image1.png image2.png ...]")
        sys.exit(1)

    md_path = Path(sys.argv[1])

    if not md_path.exists():
        print(f"Error: file not found: {md_path}")
        sys.exit(1)

    image_paths = sys.argv[2:] if len(sys.argv) > 2 else []

    if image_paths:
        out = process_file(md_path, image_paths)
    else:
        original_text = md_path.read_text(encoding="utf-8")
        updated_text = replace_mermaid_blocks(original_text)
        md_path.write_text(updated_text, encoding="utf-8")
        out = md_path

    print(f"✅ Replaced Mermaid diagrams in: {out}")


if __name__ == "__main__":
    main()