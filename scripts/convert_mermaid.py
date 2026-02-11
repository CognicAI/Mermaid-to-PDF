"""Convert .mmd (Mermaid) files to .png using the Mermaid CLI (mmdc)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def _check_mmdc():
    """Ensure mmdc is available on PATH."""
    if shutil.which("mmdc") is None:
        print(
            "Error: 'mmdc' not found on PATH.\n"
            "Install it with:  npm install -g @mermaid-js/mermaid-cli"
        )
        sys.exit(1)


def convert_mmd_to_png(mmd_path: Path, output_path: Path | None = None) -> Path:
    """
    Convert a single .mmd file to .png.

    Parameters
    ----------
    mmd_path : Path
        Path to the source .mmd file.
    output_path : Path | None
        Destination .png path.  Defaults to the same name/location with a
        .png suffix.

    Returns
    -------
    Path
        The path of the generated .png file.
    """
    if output_path is None:
        output_path = mmd_path.with_suffix(".png")

    result = subprocess.run(
        [
            "mmdc",
            "-i", str(mmd_path),
            "-o", str(output_path),
            "-b", "transparent",
            "-s", "4",          # 4× scale for high-resolution output
            "-w", "2048",       # wider canvas to avoid cramped diagrams
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"✖ Failed to convert {mmd_path}:\n{result.stderr.strip()}")
        raise RuntimeError(f"mmdc failed for {mmd_path}")

    print(f"✔ Converted: {mmd_path} → {output_path}")
    return output_path


def convert_all(mmd_files: list[Path]) -> list[Path]:
    """
    Convert a batch of .mmd files to .png.

    Returns the list of generated .png paths (in the same order as the input).
    """
    _check_mmdc()
    png_paths: list[Path] = []
    for mmd in mmd_files:
        png_paths.append(convert_mmd_to_png(mmd))
    return png_paths


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_mermaid.py <file1.mmd> [file2.mmd ...]")
        sys.exit(1)

    mmd_files = [Path(p) for p in sys.argv[1:]]
    convert_all(mmd_files)
    print("\n✅ All conversions complete.")


if __name__ == "__main__":
    main()
