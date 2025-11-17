"""Compress file(s)."""
from __future__ import annotations

__all__: list[str] = []

from os import remove
import gzip
from argparse import ArgumentParser, Namespace
from glob import glob


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Compress file(s).")
    parser.add_argument("files", nargs="+", help="The file(s) to compress")
    return parser.parse_args()


def _compress_file(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as fp:
        data: bytes = fp.read().encode()

    compressed_data: bytes = gzip.compress(data)
    with open(filename + ".gz", "wb") as fp:
        fp.write(compressed_data)

    remove(filename)


def _main() -> None:
    args: Namespace = _parse_args()
    for file in args.files:
        if not (matches := glob(file)):
            raise SystemExit(f"No matches found: {file}")

        for match in matches:
            _compress_file(match)


if __name__ == "__main__":
    _main()
