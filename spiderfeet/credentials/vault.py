"""Encrypt/decrypt credential values at rest (Fernet)."""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet, InvalidToken

from spiderfeet import SpiderFeetHelpers

ENC_PREFIX = "enc:v1:"
_CREDENTIAL_SCOPE = "credential"
_KEY_FILENAME = ".spiderfeet_credential.key"


def _key_path() -> Path:
    return Path(SpiderFeetHelpers.dataPath()) / _KEY_FILENAME


def _load_or_create_key() -> bytes:
    path = _key_path()
    if path.is_file():
        raw = path.read_bytes().strip()
        if raw:
            return raw
    key = Fernet.generate_key()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(key)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return key


def _fernet() -> Fernet:
    env_key = os.environ.get("SPIDERFEET_CREDENTIAL_KEY", "").strip()
    if env_key:
        return Fernet(env_key.encode("utf-8") if not env_key.startswith("gAAAA") else env_key)
    return Fernet(_load_or_create_key())


def is_encrypted(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(ENC_PREFIX)


def encrypt_value(plaintext: str) -> str:
    if not plaintext:
        return ""
    token = _fernet().encrypt(plaintext.encode("utf-8"))
    return ENC_PREFIX + base64.urlsafe_b64encode(token).decode("ascii")


def decrypt_value(stored: str) -> str:
    if not stored:
        return ""
    if not is_encrypted(stored):
        return stored
    blob = stored[len(ENC_PREFIX) :]
    try:
        token = base64.urlsafe_b64decode(blob.encode("ascii"))
        return _fernet().decrypt(token).decode("utf-8")
    except (InvalidToken, ValueError):
        return ""


def decrypt_config_map(config: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt encrypted values in a flat config map from configGet()."""
    out: Dict[str, Any] = {}
    for key, value in config.items():
        if isinstance(value, str) and is_encrypted(value):
            out[key] = decrypt_value(value)
        else:
            out[key] = value
    return out


def encrypt_module_secrets(module_id: str, secrets: Dict[str, str]) -> Dict[str, str]:
    store: Dict[str, str] = {}
    for opt_name, value in secrets.items():
        key = f"{module_id}:{opt_name}"
        store[key] = encrypt_value(value) if value else ""
    return store


def credential_db_key(provider_id: str, opt_name: str = "api_key") -> str:
    return f"{_CREDENTIAL_SCOPE}:{provider_id}:{opt_name}"


def encrypt_credential_store(provider_id: str, secrets: Dict[str, str]) -> Dict[str, str]:
    store: Dict[str, str] = {}
    for opt_name, value in secrets.items():
        store[credential_db_key(provider_id, opt_name)] = encrypt_value(value) if value else ""
    return store
