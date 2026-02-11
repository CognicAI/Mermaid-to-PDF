import re
import sys
from pathlib import Path


MERMAID_BLOCK_REGEX = re.compile(
    r"```mermaid\s*(.*?)```",
    re.DOTALL | re.IGNORECASE
)


def extract_mermaid_blocks(markdown_text: str) -> list[str]:
    """Extract all mermaid code blocks from markdown text."""
    return [block.strip() for block in MERMAID_BLOCK_REGEX.findall(markdown_text)]


def process_markdown_file(md_path: Path, output_dir: Path):
    """Extract mermaid blocks from a markdown file and write .mmd files."""
    content = md_path.read_text(encoding="utf-8")
    blocks = extract_mermaid_blocks(content)

    if not blocks:
        return

    base_name = md_path.stem

    for idx, block in enumerate(blocks, start=1):
        output_file = output_dir / f"{base_name}_diagram_{idx}.mmd"
        output_file.write_text(block + "\n", encoding="utf-8")
        print(f"✔ Created: {output_file}")


def process_path(input_path: Path, output_dir: Path):
    """Process a single file or recursively process a directory."""
    if input_path.is_file() and input_path.suffix == ".md":
        process_markdown_file(input_path, output_dir)

    elif input_path.is_dir():
        for md_file in input_path.rglob("*.md"):
            process_markdown_file(md_file, output_dir)

    else:
        raise ValueError(f"Unsupported path: {input_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_mermaid.py <markdown-file-or-directory> [output-dir]")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("mermaid_output")

    output_dir.mkdir(parents=True, exist_ok=True)

    process_path(input_path, output_dir)

    print("\n✅ Mermaid extraction complete.")


if __name__ == "__main__":
    main()
