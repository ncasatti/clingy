#!/usr/bin/env python3
"""
CLI Manager entry point

Allows running: python manager.py <command>
Instead of:     python -m manager.cli <command>
"""

import sys

if __name__ == "__main__":
    from manager.cli import main

    sys.exit(main())
