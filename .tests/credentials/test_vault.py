"""Tests for credential vault encryption."""

from spiderfeet.credentials.vault import decrypt_value, encrypt_value, is_encrypted


def test_encrypt_decrypt_roundtrip():
    plain = "super-secret-api-key-12345"
    enc = encrypt_value(plain)
    assert is_encrypted(enc)
    assert decrypt_value(enc) == plain
    assert plain not in enc


def test_empty_encrypt():
    assert encrypt_value("") == ""
    assert decrypt_value("") == ""


def test_decrypt_plaintext_passthrough():
    assert decrypt_value("legacy-plaintext-key") == "legacy-plaintext-key"
