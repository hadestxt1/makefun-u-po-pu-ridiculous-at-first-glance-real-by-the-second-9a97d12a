#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second.

A one-sentence startup pitch — trained alpacas rented out as wedding
witnesses — written to /output/entry.txt and printed to stdout. The pitch
must stay exactly one line, non-empty, and at most 200 characters; the
program validates that on every run and refuses to write an invalid line.

Deterministic: no clock, no randomness, no network, stdlib only.
"""

import argparse
import os
import sys

LINE = (
    "We rent out trained alpacas as wedding witnesses for $400 a ceremony, "
    "because they never object, never forget, and look unforgettable in "
    "every photo."
)

OUTPUT_PATH = "/output/entry.txt"

MAX_LINE_CHARS = 200


def validate_line(line: str) -> None:
    """Fail loudly unless the line is exactly one non-empty line of at most 200 chars."""
    if not line:
        raise ValueError("pitch line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("pitch line must be exactly one line")
    if len(line) > MAX_LINE_CHARS:
        raise ValueError(
            f"pitch line is {len(line)} characters, over the {MAX_LINE_CHARS} limit"
        )


def write_entry(path: str = OUTPUT_PATH) -> str:
    """Write the line to path (no trailing newline) and return it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    return LINE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Write one startup pitch (trained alpacas as wedding "
        "witnesses) to /output/entry.txt and print it. The pitch is "
        "validated first: exactly one line, non-empty, at most 200 "
        "characters.",
    )
    parser.add_argument(
        "--line",
        action="store_true",
        help="write and print the line (the default behaviour)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="only validate the pitch line (one line, non-empty, at most "
        "200 characters) and exit 0 if it passes, 1 if it fails",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help="path of the entry file (default: /output/entry.txt)",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        validate_line(LINE)
    except ValueError as exc:
        print(f"invalid pitch line: {exc}", file=sys.stderr)
        return 1
    if args.verify:
        print(f"line valid: {len(LINE)} characters, 1 line")
        return 0
    line = write_entry(args.output)
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
