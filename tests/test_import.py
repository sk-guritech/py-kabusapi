#!/usr/bin/env python3
"""Test that py-kabusapi can be imported successfully."""

import sys


def test_import():
    """Test importing the package."""
    try:
        from py_kabusapi import KabuStationAPI

        # インポートをテストするため、クラスが存在することを確認
        assert KabuStationAPI is not None

        print(f"✓ Python {sys.version.split()[0]}: Import successful")
        # pytest用はassertのみ、スタンドアロン用はreturnも必要
        if __name__ != "__main__":
            assert True
        else:
            return True
    except ImportError as e:
        print(f"✗ Python {sys.version.split()[0]}: Import failed - {e}")
        if __name__ != "__main__":
            assert False, f"Import failed: {e}"
        else:
            return False


if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)
