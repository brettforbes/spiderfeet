"""UI-oriented scan: one consumed nugget + module -> scan-record + produced nuggets."""

from __future__ import annotations

import hashlib
from collections import Counter
from datetime import datetime, timezone
from typing import List, Optional

from spiderfeet.api.bootstrap import Runtime
from spiderfeet.api.nugget_catalog import (
    archetype_for_event_type,
    entity_type_for_nugget_id,
    validate_catalogue_nugget_id,
)
from spiderfeet.api.schemas import (
    ConsumedNuggetInput,
    NuggetInstance,
    OsintServiceRef,
    RouteRef,
    ScanCreateRequest,
    ScanRecordUi,
    ScanResultItem,
    ScanUiRequest,
    ScanUiResponse,
)
from spiderfeet.api.services.module_execution import (
    count_module_produced,
    infer_module_execution,
)
from spiderfeet.api.services.scan_results import (
    _STORAGE_MODULES,
    fetch_scan_logs,
    fetch_scan_results,
    wait_for_scan,
)
from spiderfeet.api.services.scan_targets import resolve_scan_ui_seed
from spiderfeet.api.services.scans import ScanStartError, start_scan
from spiderfeet.map.test_targets import expected_absent_types_for_entry, seed_entry


class ScanUiError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def _nugget_instance_id(event_type: str, data: str, generated: int) -> str:
    digest = hashlib.sha1(f"{event_type}:{data}:{generated}".encode()).hexdigest()[:12]
    return f"{event_type}--{digest}"


def result_to_nugget(item: ScanResultItem) -> NuggetInstance:
    archetype = archetype_for_event_type(item.type)
    description = item.event_description or archetype.get("nugget_description")
    return NuggetInstance(
        nugget_id=item.type,
        nugget_instance_id=_nugget_instance_id(item.type, item.data, item.generated),
        entity_type=entity_type_for_nugget_id(item.type),
        nugget_description=description,
        nugget_type=archetype.get("nugget_type"),
        nugget_event_type=item.type,
        nugget_icon=archetype.get("nugget_icon"),
        nugget_colour=archetype.get("nugget_colour"),
        nugget_data=item.data,
        nugget_source_data=item.source_data,
        nugget_module=item.module,
        nugget_generated=item.generated,
        nugget_confidence=item.confidence,
        nugget_visibility=item.visibility,
        nugget_risk=item.risk,
        nugget_false_positive=item.false_positive,
    )


def _consumed_from_input(consumed: ConsumedNuggetInput) -> NuggetInstance:
    archetype = validate_catalogue_nugget_id(consumed.nugget_id)
    if not archetype:
        raise ScanUiError(f"Unknown catalogue nugget_id: {consumed.nugget_id}")
    return NuggetInstance(
        nugget_id=consumed.nugget_id,
        nugget_instance_id=_nugget_instance_id(
            consumed.nugget_id, consumed.nugget_data, 0
        ),
        entity_type=entity_type_for_nugget_id(consumed.nugget_id),
        nugget_description=archetype.get("nugget_description"),
        nugget_type=archetype.get("nugget_type"),
        nugget_event_type=consumed.nugget_id,
        nugget_icon=archetype.get("nugget_icon"),
        nugget_colour=archetype.get("nugget_colour"),
        nugget_data=consumed.nugget_data,
        nugget_source_data=consumed.nugget_data,
        nugget_module="SpiderFeet UI",
        nugget_generated=0,
        nugget_confidence=100,
        nugget_visibility=100,
        nugget_risk=0,
        nugget_false_positive=False,
    )


def _is_consumed_event(
    item: ScanResultItem, consumed: ConsumedNuggetInput
) -> bool:
    if item.module == "SpiderFeet UI":
        return True
    return (
        item.type == consumed.nugget_id
        and item.data == consumed.nugget_data
    )


def _is_produced_event(item: ScanResultItem, module_id: str) -> bool:
    if item.module in _STORAGE_MODULES or item.module == "SpiderFeet UI":
        return False
    return item.module == module_id


def _module_display_name(config: dict, module_id: str) -> str:
    mod = config.get("__modules__", {}).get(module_id, {})
    return mod.get("name") or mod.get("descr") or module_id


def run_scan_ui(runtime: Runtime, request: ScanUiRequest) -> ScanUiResponse:
    consumed_input = request.consumed
    module_id = request.module_id.strip()

    if module_id not in runtime.config.get("__modules__", {}):
        raise ScanUiError(f"Unknown module_id: {module_id}")

    if not validate_catalogue_nugget_id(consumed_input.nugget_id):
        raise ScanUiError(f"Unknown catalogue nugget_id: {consumed_input.nugget_id}")

    try:
        target_value, target_type, seed_payload = resolve_scan_ui_seed(
            consumed_input.nugget_id,
            consumed_input.nugget_data,
        )
    except ValueError:
        raise ScanUiError("nugget_data is not a valid SpiderFeet target") from None

    scan_request = ScanCreateRequest(
        target=target_value,
        scan_name=request.scan_name or consumed_input.nugget_data,
        modules=[module_id],
        debug=request.debug,
    )

    try:
        scan_id = start_scan(
            runtime,
            scan_request,
            target_type=target_type,
            seed_payload_event=seed_payload,
        )
    except ScanStartError as exc:
        raise ScanUiError(exc.message, exc.status_code) from exc

    status = "STARTING"
    started: Optional[int] = None
    ended: Optional[int] = None

    if request.wait:
        try:
            status, started, ended = wait_for_scan(
                runtime.config,
                scan_id,
                timeout_seconds=request.timeout_seconds,
            )
        except TimeoutError as exc:
            raise ScanUiError(str(exc), status_code=504) from exc

    consumed_nugget = _consumed_from_input(consumed_input)
    produced: List[NuggetInstance] = []
    by_type_dict: dict[str, int] = {}
    event_count = 0
    scan_results_summary = {"status": status, "event_count": 0, "by_type": {}}
    raw: List[ScanResultItem] = []

    if status == "FINISHED":
        raw = fetch_scan_results(runtime.config, scan_id)
        by_type: Counter[str] = Counter()
        seen_consumed = False
        for item in raw:
            by_type[item.type] += 1
            if _is_consumed_event(item, consumed_input):
                consumed_nugget = result_to_nugget(item)
                seen_consumed = True
            elif _is_produced_event(item, module_id):
                produced.append(result_to_nugget(item))
        if not seen_consumed and raw:
            for item in raw:
                if _is_consumed_event(item, consumed_input):
                    consumed_nugget = result_to_nugget(item)
                    break
        by_type_dict = dict(by_type)
        event_count = len(raw)
        scan_results_summary = {
            "status": status,
            "event_count": event_count,
            "by_type": by_type_dict,
        }

    duration: Optional[float] = None
    if started is not None and ended is not None and ended >= started:
        duration = float(ended - started)

    ts: Optional[str] = None
    if started is not None:
        ts = datetime.fromtimestamp(started, tz=timezone.utc).isoformat()

    produced_types = sorted({n.nugget_id for n in produced})
    route_name: Optional[str] = None
    if produced_types:
        route_name = (
            f"{consumed_input.nugget_id}-to-{produced_types[0]}-via-{module_id}"
        )

    module_execution = None
    if status in ("FINISHED", "ERROR-FAILED"):
        module_events = (
            count_module_produced(
                raw,
                module_id,
                storage_modules=_STORAGE_MODULES,
            )
            if status == "FINISHED"
            else 0
        )
        log_rows: List = []
        try:
            log_rows = fetch_scan_logs(runtime.config, scan_id, limit=500)
        except Exception:
            log_rows = []

        entry = seed_entry(module_id, consumed_input.nugget_id)
        module_execution = infer_module_execution(
            module_id=module_id,
            status=status,
            events_emitted=module_events,
            log_rows=[
                (e.generated_ms, e.component, e.type, e.message, e.row_id)
                for e in log_rows
            ],
            expected_absent_types=expected_absent_types_for_entry(entry),
            scan_results_by_type=by_type_dict,
        )

    scan_record = ScanRecordUi(
        scan_instance_id=scan_id,
        status=status,
        scan_event_count=event_count,
        scan_results_by_type=by_type_dict,
        scan_results=scan_results_summary,
        scan_duration=duration,
        scan_timestamp=ts,
        scan_notes=request.scan_notes or "",
        service=OsintServiceRef(
            module_id=module_id,
            name=_module_display_name(runtime.config, module_id),
        ),
        route=RouteRef(route_name=route_name, route_state="in-test")
        if route_name
        else None,
    )

    return ScanUiResponse(
        scan_record=scan_record,
        consumed=[consumed_nugget],
        produced=produced,
        module_execution=module_execution,
    )
