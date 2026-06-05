"""Open a TypeDB driver from connection config."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional

from typedb.driver import (
    Credentials,
    Driver,
    DriverOptions,
    DriverTlsConfig,
    TypeDB,
    driver_tls_config_new_disabled,
    driver_tls_config_new_enabled_with_root_ca_path,
)

from spiderfeet.map.config import TypeDBConnectionConfig


def _tls_config(cfg: TypeDBConnectionConfig) -> DriverTlsConfig:
    if cfg.tls_enabled:
        if not cfg.root_ca_path:
            raise ValueError("tls.enabled requires root_ca_path")
        native = driver_tls_config_new_enabled_with_root_ca_path(cfg.root_ca_path)
    else:
        native = driver_tls_config_new_disabled()
    return DriverTlsConfig(native)


def open_driver(cfg: TypeDBConnectionConfig) -> Driver:
    """Create a connected TypeDB driver (caller must close)."""
    options = DriverOptions(_tls_config(cfg))
    return TypeDB.driver(cfg.addresses, Credentials(cfg.username, cfg.password), options)


@contextmanager
def driver_session(
    cfg: TypeDBConnectionConfig,
) -> Generator[Driver, None, None]:
    driver = open_driver(cfg)
    try:
        yield driver
    finally:
        driver.close()


def ping(cfg: TypeDBConnectionConfig, timeout_note: Optional[str] = None) -> bool:
    """Return True if the server accepts a connection."""
    try:
        with driver_session(cfg) as driver:
            _ = driver.databases.all()
        return True
    except Exception:
        return False
