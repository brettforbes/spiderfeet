"""Scan orchestration shared with sf.py / sfwebui startscan."""

from __future__ import annotations

import multiprocessing as mp
from copy import deepcopy
from typing import List

from sflib import SpiderFeet

from sfscan import startSpiderFeetScanner
from spiderfeet import SpiderFeetDb, SpiderFeetHelpers
from spiderfeet.api.bootstrap import Runtime
from spiderfeet.api.schemas import ScanCreateRequest, UseCase


class ScanStartError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def resolve_module_list(
    config: dict, request: ScanCreateRequest
) -> List[str]:
    sf = SpiderFeet(deepcopy(config))
    modlist: List[str] = []

    if request.modules:
        modlist = [m.strip() for m in request.modules if m.strip()]

    if not modlist and request.event_types:
        typesx = list(request.event_types)
        modlist = sf.modulesProducing(typesx)
        newmods = deepcopy(modlist)
        newmodcpy = deepcopy(newmods)
        while len(newmodcpy) > 0:
            for etype in sf.eventsToModules(newmodcpy):
                xmods = sf.modulesProducing([etype])
                for mod in xmods:
                    if mod not in modlist:
                        modlist.append(mod)
                        newmods.append(mod)
            newmodcpy = deepcopy(newmods)
            newmods = []

    if not modlist and request.use_case:
        usecase = request.use_case.value
        for mod in config["__modules__"]:
            if usecase == "all" or usecase in config["__modules__"][mod]["group"]:
                modlist.append(mod)

    if not modlist:
        raise ScanStartError("No modules selected for scan")

    if "sfp__stor_db" not in modlist:
        modlist.append("sfp__stor_db")
    if "sfp__stor_stdout" in modlist:
        modlist.remove("sfp__stor_stdout")
    modlist.sort()
    return modlist


def normalize_target(target: str, target_type: str) -> str:
    if target_type in ["HUMAN_NAME", "USERNAME", "BITCOIN_ADDRESS"]:
        return target.replace('"', "")
    return target.lower()


def start_scan(runtime: Runtime, request: ScanCreateRequest) -> str:
    """Launch scan worker process and return scan_id immediately (non-blocking)."""
    target = request.target.strip()
    scan_name = (request.scan_name or target).strip()
    if not scan_name:
        raise ScanStartError("scan_name is required")

    target_type = SpiderFeetHelpers.targetTypeFromString(target)
    if target_type is None:
        raise ScanStartError("Unrecognised target type")

    modlist = resolve_module_list(runtime.config, request)
    scantarget = normalize_target(target, target_type)

    cfg = deepcopy(runtime.config)
    if request.debug:
        cfg["_debug"] = True

    scan_id = SpiderFeetHelpers.genScanInstanceId()

    try:
        proc = mp.Process(
            target=startSpiderFeetScanner,
            args=(
                runtime.logging_queue,
                scan_name,
                scan_id,
                scantarget,
                target_type,
                modlist,
                cfg,
            ),
        )
        proc.daemon = True
        proc.start()
    except Exception as exc:
        raise ScanStartError(f"Failed to start scan: {exc}", status_code=500) from exc

    return scan_id
