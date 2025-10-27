"""Decrypt file(s)."""
from __future__ import annotations

__all__: list[str] = []

import zlib
from argparse import ArgumentParser, Namespace
from base64 import b64decode
from glob import glob

import jsonyx as json
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Decrypt file(s).")
    parser.add_argument("files", nargs="+", help="The file(s) to decrypt")
    return parser.parse_args()


def _decrypt_file(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as fp:
        encrypted_data: dict[str, str] = json.load(fp)

    with open("auth/private.pem", "rb") as f:
        private_key: PrivateKeyTypes = load_pem_private_key(f.read(), None)
        assert isinstance(private_key, RSAPrivateKey)

    nonce: bytes = b64decode(encrypted_data["nonce"])
    encrypted_key: bytes = b64decode(encrypted_data["encrypted_key"])
    ciphertext: bytes = b64decode(encrypted_data["ciphertext"])
    aes_key: bytes = private_key.decrypt(
        encrypted_key, OAEP(MGF1(SHA256()), SHA256(), None)
    )
    compressed_data: bytes = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    data: bytes = zlib.decompress(compressed_data)
    with open(filename.removesuffix(".enc"), "wb") as fp:
        fp.write(data)


def _main() -> None:
    args: Namespace = _parse_args()
    for file in args.files:
        if not (matches := glob(file)):
            raise SystemExit(f"No matches found: {file}")

        for match in matches:
            _decrypt_file(match)


if __name__ == "__main__":
    _main()
