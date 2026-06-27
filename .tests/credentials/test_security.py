"""Unit security tests for credential layer (no API fixtures)."""

import pytest

from spiderfeet.credentials.vault import encrypt_value, is_encrypted
from spiderfeet.settings import cli_apps


def test_cli_app_path_traversal_rejected():
    with pytest.raises(ValueError, match="\\.\\."):
        cli_apps.validate_binary_path("../../etc/passwd")
    with pytest.raises(ValueError, match="\\.tools/"):
        cli_apps.validate_env_file_path("/etc/passwd")


def test_encrypt_does_not_contain_plaintext():
    plain = "secret-value-abc"
    enc = encrypt_value(plain)
    assert plain not in enc
    assert is_encrypted(enc)
