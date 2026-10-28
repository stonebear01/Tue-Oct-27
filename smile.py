#!/usr/bin/env python3
"""Print a smiley face icon in the terminal.

Usage:
    python3 smile.py              # default size
    python3 smile.py --size 24    # bigger face
    python3 smile.py --no-color   # plain text, no ANSI colors
"""

import argparse
import math
import sys

YELLOW = "\033[93m"
RESET = "\033[0m"


def draw_smile(size: int, char: str = "#") -> str:
    """Return a smiley face as a multi-line string, `size` rows tall."""
    rows = []
    for row in range(size):
        # Map the grid onto [-1, 1]; terminal cells are ~2x taller than wide,
        # so use twice as many columns to keep the face round.
        y = (row + 0.5) / size * 2 - 1
        line = []
        for col in range(size * 2):
            x = (col + 0.5) / (size * 2) * 2 - 1
            on_outline = abs(math.hypot(x, y) - (1 - 1 / size)) < 1.2 / size
            on_eye = math.hypot(abs(x) - 0.33, y + 0.3) < 0.13
            on_mouth = y > 0.15 and abs(math.hypot(x, y + 0.05) - 0.55) < 1.0 / size
            line.append(char if on_outline or on_eye or on_mouth else " ")
        rows.append("".join(line).rstrip())
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a smiley face icon.")
    parser.add_argument("--size", type=int, default=16, help="height in rows (min 10, default 16)")
    parser.add_argument("--char", default="#", help="character used to draw (default '#')")
    parser.add_argument("--no-color", action="store_true", help="disable yellow color")
    args = parser.parse_args()

    face = draw_smile(max(args.size, 10), args.char[:1] or "#")
    if sys.stdout.isatty() and not args.no_color:
        face = f"{YELLOW}{face}{RESET}"
    print(face)


if __name__ == "__main__":
    main()
