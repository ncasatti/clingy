#!/usr/bin/env python3
"""
Thin wrapper to execute the new modular CLI

Allows running: python manager.py build
Instead of:     python -m manager.cli build
"""

import os
import sys

# Add parent directory to path BEFORE importing manager modules
# This allows 'manager' package to be importable from parent directory
_current_file = os.path.abspath(__file__)
_current_dir = os.path.dirname(_current_file)
_parent_dir = os.path.dirname(_current_dir)
sys.path.insert(0, _parent_dir)

if __name__ == "__main__":
    from manager.cli import main

    main()
