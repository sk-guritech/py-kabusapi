#!/usr/bin/env python3
"""Simple import test that doesn't require dependencies."""

import sys


def test_syntax_only():
    """Test that all Python files have valid syntax."""
    import ast
    import os

    errors = []
    for root, dirs, files in os.walk("py_kabusapi"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        ast.parse(f.read())
                    print(f"✓ {filepath}: Syntax OK")
                except SyntaxError as e:
                    errors.append(f"✗ {filepath}: {e}")
                    print(errors[-1])

    if errors:
        print(f"\nFound {len(errors)} syntax errors")
        return False
    else:
        print(f"\n✓ All files have valid syntax for Python {sys.version.split()[0]}")
        return True


if __name__ == "__main__":
    success = test_syntax_only()
    sys.exit(0 if success else 1)
