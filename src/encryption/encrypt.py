"""Encrypt file."""
from __future__ import annotations

__all__: list[str] = []

import zlib
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from os import urandom

import jsonyx as json
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def _parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="Encrypt file.")
    parser.add_argument("file", help="The file to encrypt")
    return parser.parse_args()


def _main() -> None:
    args: Namespace = _parse_args()
    with open(args.file, "rb") as fp:
        data: bytes = fp.read()

    with open("auth/public.pem", "rb") as f:
        public_key: PublicKeyTypes = load_pem_public_key(f.read())
        assert isinstance(public_key, RSAPublicKey)

    aes_key: bytes = AESGCM.generate_key(256)
    nonce: bytes = urandom(12)
    compressed_data: bytes = zlib.compress(data)
    ciphertext: bytes = AESGCM(aes_key).encrypt(nonce, compressed_data, None)
    encrypted_key: bytes = public_key.encrypt(
        aes_key, OAEP(MGF1(SHA256()), SHA256(), None)
    )
    encrypted_data: dict[str, str] = {
        "nonce": b64encode(nonce).decode(),
        "encrypted_key": b64encode(encrypted_key).decode(),
        "ciphertext": b64encode(ciphertext).decode()
    }
    with open(args.file + ".enc", "w", encoding="utf-8") as fp:
        json.dump(encrypted_data, fp, indent=4)


if __name__ == "__main__":
    _main()
