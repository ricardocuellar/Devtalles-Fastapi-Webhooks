"""Importar librerias"""
import hmac
import hashlib
import os


GITHUB_SECRET = os.getenv("GITHUB_SECRET", "secretosuper123")


def verify_signature(body: bytes, signature_header: str | None) -> bool:
    """Verificar que la firma sea valida"""
    if not signature_header:
        return False

    try:
        sha_name, signature = signature_header.split(
            "=")  # sha256=firmitahexadecimal
    except ValueError:
        return False

    if sha_name != "sha256":
        return False

    mac = hmac.new(
        GITHUB_SECRET.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256,
    )

    expected = mac.hexdigest()

    return hmac.compare_digest(expected, signature)
