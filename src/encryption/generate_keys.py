"""Generate keys."""
from __future__ import annotations

__all__: list[str] = []

from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey, RSAPublicKey, generate_private_key
)
from cryptography.hazmat.primitives.serialization import (
    Encoding, NoEncryption, PrivateFormat, PublicFormat
)


def _main() -> None:
    private_key: RSAPrivateKey = generate_private_key(65537, 4096)
    public_key: RSAPublicKey = private_key.public_key()
    with open("auth/private.pem", "wb") as fp:
        fp.write(private_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
        ))

    with open("auth/public.pem", "wb") as fp:
        fp.write(public_key.public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
        ))


if __name__ == "__main__":
    _main()
