#!/usr/bin/env python3
"""Test that py-kabusapi can be imported successfully."""

import sys


def test_import():
    """Test importing the package."""
    try:
        from py_kabusapi import KabuStationAPI  # noqa: F401

        print(f"✓ Python {sys.version.split()[0]}: Import successful")
        assert True
        return True
    except ImportError as e:
        print(f"✗ Python {sys.version.split()[0]}: Import failed - {e}")
        assert False, f"Import failed: {e}"
        return False


if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)
