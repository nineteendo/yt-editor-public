"""Compress file(s)."""
from __future__ import annotations

__all__: list[str] = []

from os import remove
import gzip
from argparse import ArgumentParser, Namespace
from glob import glob


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Compress file(s).")
    parser.add_argument("--glob", action="store_true", help="Expand pattern")
    parser.add_argument("file", help="The file(s) to compress")
    return parser.parse_args()


def _compress_file(filename: str) -> None:
    with open(filename, "rb") as fp:
        data: bytes = fp.read()

    compressed_data: bytes = gzip.compress(data)
    with open(filename + ".gz", "wb") as fp:
        fp.write(compressed_data)

    remove(filename)


def _main() -> None:
    args: Namespace = _parse_args()
    if args.glob:
        for filename in glob(args.file):
            _compress_file(filename)
    else:
        _compress_file(args.file)


if __name__ == "__main__":
    _main()
