#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry.

Writes one fortune-cookie line, the kind an AI agent would crack open,
to /output/entry.txt.
"""

import os
import stat

FORTUNE = (
    "You have already read your fortune \u2014 "
    "it was written in the system prompt you will never see."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line: str) -> None:
    """A fortune must be one non-blank line of 1-200 characters."""
    if not line or not line.strip():
        raise ValueError("fortune must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("fortune must not contain control characters")
    if not 1 <= len(line) <= 200:
        raise ValueError(
            f"fortune must be 1-200 characters, got {len(line)}"
        )


def main() -> None:
    validate(FORTUNE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(FORTUNE)
    os.chmod(OUTPUT_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    # Read back and confirm the file on disk is exactly the validated line.
    with open(OUTPUT_PATH, encoding="utf-8", newline="") as f:
        written = f.read()
    if written != FORTUNE:
        raise RuntimeError("output file does not match the fortune constant")
    if written.endswith("\n"):
        raise RuntimeError("output file must not end with a newline")


if __name__ == "__main__":
    main()
