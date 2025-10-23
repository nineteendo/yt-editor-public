"""Decompress file(s)."""
from __future__ import annotations

__all__: list[str] = []

from os import remove
import gzip
from argparse import ArgumentParser, Namespace
from glob import glob


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Decompress file(s).")
    parser.add_argument("--glob", action="store_true", help="Expand pattern")
    parser.add_argument("file", help="The file(s) to decompress")
    return parser.parse_args()


def _decompress_file(filename: str) -> None:
    with open(filename, "rb") as fp:
        compressed_data: bytes = fp.read()

    data: bytes = gzip.decompress(compressed_data)
    with open(filename.removesuffix(".gz"), "wb") as fp:
        fp.write(data)

    remove(filename)


def _main() -> None:
    args: Namespace = _parse_args()
    if args.glob:
        for filename in glob(args.file):
            _decompress_file(filename)
    else:
        _decompress_file(args.file)


if __name__ == "__main__":
    _main()
