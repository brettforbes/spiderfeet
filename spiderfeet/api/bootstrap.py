"""Load SpiderFeet runtime (modules, DB, logging) for the API process."""

from __future__ import annotations

import logging
import multiprocessing as mp
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from sflib import SpiderFeet

from spiderfeet import SpiderFeetCorrelator, SpiderFeetDb, SpiderFeetHelpers
from spiderfeet.credentials.vault import decrypt_config_map
from spiderfeet.logger import logListenerSetup, logWorkerSetup

# Repo root: spiderfeet/api/bootstrap.py -> parents[2]
REPO_ROOT = Path(__file__).resolve().parents[2]


def default_config() -> dict:
    return {
        "_debug": False,
        "_maxthreads": 3,
        "__logging": True,
        "__outputfilter": None,
        "_useragent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) "
            "Gecko/20100101 Firefox/62.0"
        ),
        "_dnsserver": "",
        "_fetchtimeout": 5,
        "_internettlds": "https://publicsuffix.org/list/effective_tld_names.dat",
        "_internettlds_cache": 72,
        "_genericusers": ",".join(
            SpiderFeetHelpers.usernamesFromWordlists(["generic-usernames"])
        ),
        "__database": f"{SpiderFeetHelpers.dataPath()}/spiderFeet.db",
        "__modules__": None,
        "__correlationrules__": None,
        "_socks1type": "",
        "_socks2addr": "",
        "_socks3port": "",
        "_socks4user": "",
        "_socks5pwd": "",
    }


@dataclass
class Runtime:
    """Shared API process state."""

    config: dict
    logging_queue: mp.Queue
    dbh: SpiderFeetDb


_runtime: Optional[Runtime] = None


def init_runtime() -> Runtime:
    """Bootstrap modules, DB, and logging (once per API process)."""
    global _runtime
    if _runtime is not None:
        return _runtime

    log = logging.getLogger("spiderFeet.api.bootstrap")
    sf_config = default_config()

    logging_queue = mp.Queue()
    logListenerSetup(logging_queue, sf_config)
    logWorkerSetup(logging_queue)

    mod_dir = str(REPO_ROOT / "modules") + os.sep
    sf_modules = SpiderFeetHelpers.loadModulesAsDict(mod_dir, ["sfp_template.py"])
    if not sf_modules:
        raise RuntimeError(f"No modules found in {mod_dir}")

    correlations_dir = str(REPO_ROOT / "correlations") + os.sep
    correlation_rules_raw = SpiderFeetHelpers.loadCorrelationRulesRaw(
        correlations_dir, ["template.yaml"]
    )

    sf_config["__modules__"] = sf_modules

    dbh = SpiderFeetDb(sf_config, init=True)
    sf = SpiderFeet(sf_config)
    sf_config = sf.configUnserialize(decrypt_config_map(dbh.configGet()), sf_config)
    sf_config["__modules__"] = sf_modules
    correlation_rules = []
    if correlation_rules_raw:
        correlator = SpiderFeetCorrelator(dbh, correlation_rules_raw)
        correlation_rules = correlator.get_ruleset()
    sf_config["__correlationrules__"] = correlation_rules

    _runtime = Runtime(config=sf_config, logging_queue=logging_queue, dbh=dbh)
    log.info("SpiderFeet API runtime ready (%s modules)", len(sf_modules))
    return _runtime


def get_runtime() -> Runtime:
    if _runtime is None:
        return init_runtime()
    return _runtime
