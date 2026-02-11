#!/usr/bin/env python3
"""
Wrapper script to run the main pipeline from the docs directory.
Redirects to scripts/main.py with the correct path handling.
"""
import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import and run the actual main function
from main import main

if __name__ == "__main__":
    main()
