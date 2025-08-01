#!/usr/bin/env python3
"""
Main entry point for Agentic Mentor
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import app

if __name__ == "__main__":
    app.run() 