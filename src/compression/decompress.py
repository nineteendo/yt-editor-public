"""Decompress file(s)."""
from __future__ import annotations

__all__: list[str] = []

from os import remove
import gzip
from argparse import ArgumentParser, Namespace
from glob import glob


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Decompress file(s).")
    parser.add_argument("files", nargs="+", help="The file(s) to decompress")
    return parser.parse_args()


def _decompress_file(filename: str) -> None:
    with open(filename, "rb") as fp:
        compressed_data: bytes = fp.read()

    data: bytes = gzip.decompress(compressed_data)
    with open(filename.removesuffix(".gz"), "w", encoding="utf-8") as fp:
        fp.write(data.decode())

    remove(filename)


def _main() -> None:
    args: Namespace = _parse_args()
    for file in args.files:
        if not (matches := glob(file)):
            raise SystemExit(f"No matches found: {file}")

        for match in matches:
            _decompress_file(match)


if __name__ == "__main__":
    _main()
