#!/usr/bin/env python3
"""Chunked nuclei trial: katana URLs -> critical/high findings with progress tracking.

Each chunk is a short-lived nuclei run. Findings accumulate in critical_high_findings.json.
Job progress lives in job_overview.json.

Network: defaults to WiFi 2 (USB) when connected via -i; use --launch-dual for parallel
WiFi 2 + main WiFi workers (alternating chunks).

Examples:
  python .seed/scripts/cli_corpus/run_nuclei_katana_trial.py --prepare-chunks
  python .seed/scripts/cli_corpus/run_nuclei_katana_trial.py --launch-chunked --resume
  python .seed/scripts/cli_corpus/run_nuclei_katana_trial.py --launch-dual --resume
  python .seed/scripts/cli_corpus/run_nuclei_katana_trial.py --status
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from network_bind import default_scan_interface, dual_scan_plan, resolve_wifi_adapters

REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DIR = REPO_ROOT / ".docs/docs-for-cli-tools/exploration_scratch/nuclei/trials/katana_exam6_upside_com"
CHUNKS_DIR = TRIAL_DIR / "chunks"
DEFAULT_KATANA_TEXT = (
    REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/katana/6_output_text.txt"
)
URL_LIST = TRIAL_DIR / "targets_urls.txt"
REVIEW_JSON = TRIAL_DIR / "critical_high_findings.json"
JOB_OVERVIEW = TRIAL_DIR / "job_overview.json"
STATUS_JSON = TRIAL_DIR / "run_status.json"  # legacy alias; mirrors job overview phase
PAUSE_AFTER_NEXT_FLAG = TRIAL_DIR / "pause_after_next.flag"
RUN_LOG = TRIAL_DIR / "run.log"
NUCLEI_BIN = REPO_ROOT / ".tools/bin/nuclei.exe"
TEMPLATES = REPO_ROOT / ".tools/nuclei-templates"
SEVERITIES = frozenset({"critical", "high"})
DEFAULT_CHUNK_SIZE = 5
DEFAULT_CHUNK_TIMEOUT_S = 2400
CHUNK_COOLDOWN_S = 3.0
MAX_CHUNK_ATTEMPTS = 3
CIRCUIT_BREAKER_INSTANT_FAILS = 3
INSTANT_FAIL_DURATION_S = 3.0
NUCLEI_OK_EXIT_CODES = frozenset({0, 1})
JOB_LOCK = TRIAL_DIR / ".job.lock"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def append_log(message: str) -> None:
    TRIAL_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{utc_now()}] {message}\n"
    with RUN_LOG.open("a", encoding="utf-8") as fh:
        fh.write(line)
    print(message, flush=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def extract_urls_from_katana_text(text_path: Path, out_path: Path) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    with text_path.open(encoding="utf-8", errors="replace") as src:
        for raw in src:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            url = line.split()[0].strip()
            if not url.startswith(("http://", "https://")):
                continue
            if url in seen:
                continue
            seen.add(url)
            urls.append(url)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8")
    return urls


def finding_to_review_dict(rec: dict[str, Any], *, chunk_id: str | None = None) -> dict[str, Any]:
    info = rec.get("info") or {}
    refs = info.get("reference")
    if isinstance(refs, list):
        refs_out: str | list[str] | None = refs
    elif refs:
        refs_out = str(refs)
    else:
        refs_out = None
    out: dict[str, Any] = {
        "severity": str(info.get("severity", "")).lower(),
        "template_id": rec.get("template-id"),
        "name": info.get("name"),
        "matched_at": rec.get("matched-at"),
        "host": rec.get("host"),
        "type": rec.get("type"),
        "matcher_name": rec.get("matcher-name"),
        "description": info.get("description"),
        "reference": refs_out,
        "tags": info.get("tags") or [],
    }
    if chunk_id is not None:
        out["chunk_id"] = chunk_id
    return out


def consolidate_findings_from_jsonl(
    raw_jsonl: Path,
    *,
    severities: frozenset[str] = SEVERITIES,
    chunk_id: str | None = None,
) -> list[dict[str, Any]]:
    if not raw_jsonl.is_file() or raw_jsonl.stat().st_size == 0:
        return []
    findings: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    with raw_jsonl.open(encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line.startswith("{"):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            sev = str((rec.get("info") or {}).get("severity", "")).lower()
            if sev not in severities:
                continue
            review = finding_to_review_dict(rec, chunk_id=chunk_id)
            dedupe_key = (
                str(review.get("template_id") or ""),
                str(review.get("matched_at") or ""),
                str(review.get("matcher_name") or ""),
            )
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
            findings.append(review)
    findings.sort(
        key=lambda item: (
            0 if item.get("severity") == "critical" else 1,
            str(item.get("matched_at") or ""),
            str(item.get("template_id") or ""),
        )
    )
    return findings


def merge_findings(existing: list[dict[str, Any]], new_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = list(existing)
    seen = {
        (
            str(item.get("template_id") or ""),
            str(item.get("matched_at") or ""),
            str(item.get("matcher_name") or ""),
        )
        for item in existing
    }
    for item in new_items:
        key = (
            str(item.get("template_id") or ""),
            str(item.get("matched_at") or ""),
            str(item.get("matcher_name") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    merged.sort(
        key=lambda item: (
            0 if item.get("severity") == "critical" else 1,
            str(item.get("matched_at") or ""),
            str(item.get("template_id") or ""),
        )
    )
    return merged


def build_nuclei_argv(
    url_list: Path,
    raw_jsonl: Path,
    *,
    interface: str | None = None,
    source_ip: str | None = None,
) -> list[str]:
    argv = [
        str(NUCLEI_BIN),
        "-l",
        str(url_list),
        "-severity",
        "critical,high",
        "-silent",
        "-jsonl",
        "-omit-raw",
        "-omit-template",
        "-t",
        str(TEMPLATES),
        "-no-interactsh",
        "-etags",
        "dos,fuzz,misc",
        "-duc",
        "-retries",
        "1",
        "-c",
        "10",
        "-bs",
        "10",
        "-timeout",
        "10",
        "-mhe",
        "50",
    ]
    if interface:
        argv.extend(["-i", interface])
    elif source_ip:
        argv.extend(["-sip", source_ip])
    argv.extend(["-jle", str(raw_jsonl)])
    return argv


def review_json_for_worker(worker_id: int | None) -> Path:
    if worker_id is None:
        return REVIEW_JSON
    return TRIAL_DIR / f"critical_high_findings_worker{worker_id}.json"


@contextmanager
def job_lock() -> Iterator[None]:
    TRIAL_DIR.mkdir(parents=True, exist_ok=True)
    JOB_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with JOB_LOCK.open("a+", encoding="utf-8") as fh:
        if sys.platform == "win32":
            import msvcrt

            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            if sys.platform == "win32":
                import msvcrt

                fh.seek(0)
                msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)


def reload_job() -> dict[str, Any]:
    job = load_json(JOB_OVERVIEW, None)
    if not job:
        raise SystemExit("job_overview.json missing")
    return job


def chunk_assigned_to_worker(chunk_index: int, worker_id: int | None, worker_count: int) -> bool:
    if worker_count <= 1 or worker_id is None:
        return True
    return (chunk_index - 1) % worker_count == worker_id


def merge_all_findings() -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    paths = [REVIEW_JSON] + sorted(TRIAL_DIR.glob("critical_high_findings_worker*.json"))
    for path in paths:
        if path.is_file():
            merged = merge_findings(merged, load_json(path, []))
    write_json(REVIEW_JSON, merged)
    return merged


def chunk_paths(chunk_index: int) -> dict[str, Path]:
    cid = f"chunk_{chunk_index:04d}"
    base = CHUNKS_DIR / cid
    return {
        "id": cid,
        "urls": base.with_suffix(".txt"),
        "raw": base.with_suffix(".jsonl"),
        "status": base.with_name(f"{cid}_status.json"),
        "stderr": base.with_name(f"{cid}_stderr.txt"),
        "termination": base.with_name(f"{cid}_termination.txt"),
    }


def build_termination_record(
    *,
    phase: str,
    exit_code: int,
    finding_count: int,
    duration_s: float,
    timed_out: bool,
    attempt: int,
    interface: str | None,
    stderr_tail: str | None,
) -> dict[str, str]:
    iface = interface or "default"
    if phase == "complete" and finding_count > 0:
        kind = "hit"
        message = (
            f"HIT: {finding_count} critical/high finding(s) after {duration_s}s "
            f"(exit={exit_code}, attempt={attempt}, interface={iface})"
        )
    elif phase == "complete":
        kind = "clean_miss"
        message = (
            f"CLEAN_MISS: no critical/high findings after {duration_s}s "
            f"(exit={exit_code}, attempt={attempt}, interface={iface})"
        )
    elif timed_out:
        kind = "timeout"
        message = (
            f"TIMEOUT: chunk exceeded limit after {duration_s}s "
            f"(exit={exit_code}, attempt={attempt}, interface={iface})"
        )
    elif is_windows_crash_exit(exit_code) or duration_s < INSTANT_FAIL_DURATION_S:
        kind = "crash"
        detail = (stderr_tail or "no stderr captured").strip().splitlines()[-1] if stderr_tail else "no stderr"
        message = (
            f"CRASH: nuclei died early after {duration_s}s "
            f"(exit={exit_code}, attempt={attempt}, interface={iface}) — {detail}"
        )
    else:
        kind = "error"
        detail = (stderr_tail or "no stderr captured").strip().splitlines()[-1] if stderr_tail else "no stderr"
        message = (
            f"ERROR: scan failed after {duration_s}s "
            f"(exit={exit_code}, attempt={attempt}, interface={iface}) — {detail}"
        )
    return {"termination_kind": kind, "termination_message": message}


def is_windows_crash_exit(exit_code: int) -> bool:
    """NTSTATUS-style exits (e.g. 0xC000013A killed, 0xC0000142 DLL init failed)."""
    return exit_code not in NUCLEI_OK_EXIT_CODES and exit_code not in (2, 124) and exit_code >= 0xC0000000


def classify_chunk_phase(
    *,
    exit_code: int,
    timed_out: bool,
    duration_s: float,
) -> str:
    if timed_out:
        return "timed_out"
    if exit_code in NUCLEI_OK_EXIT_CODES:
        return "complete"
    if exit_code == 2:
        return "failed"
    if is_windows_crash_exit(exit_code):
        return "failed"
    # Unknown non-zero: treat short runs as crash, longer as completed-with-errors.
    if duration_s < INSTANT_FAIL_DURATION_S:
        return "failed"
    return "complete"


def chunk_is_retryable(status: str, *, duration_s: float | None = None, attempts: int = 0) -> bool:
    if attempts >= MAX_CHUNK_ATTEMPTS:
        return False
    if status == "timed_out":
        return True
    if status != "failed":
        return False
    if duration_s is not None and duration_s < INSTANT_FAIL_DURATION_S:
        return True
    return True


def split_into_chunks(urls: list[str], chunk_size: int) -> list[list[str]]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    return [urls[i : i + chunk_size] for i in range(0, len(urls), chunk_size)]


def prepare_chunks(urls: list[str], chunk_size: int) -> dict[str, Any]:
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    groups = split_into_chunks(urls, chunk_size)
    manifest_chunks: list[dict[str, Any]] = []
    for idx, group in enumerate(groups, start=1):
        paths = chunk_paths(idx)
        paths["urls"].write_text("\n".join(group) + "\n", encoding="utf-8")
        manifest_chunks.append(
            {
                "chunk_index": idx,
                "chunk_id": paths["id"],
                "url_count": len(group),
                "url_list": rel(paths["urls"]),
                "status": "pending",
            }
        )
    job = {
        "schema": "nuclei_chunked_trial_v1",
        "job_id": "katana_exam6_upside_com",
        "source": rel(DEFAULT_KATANA_TEXT),
        "severity_filter": sorted(SEVERITIES),
        "chunk_size": chunk_size,
        "chunk_timeout_s": DEFAULT_CHUNK_TIMEOUT_S,
        "total_urls": len(urls),
        "total_chunks": len(groups),
        "completed_chunks": 0,
        "failed_chunks": 0,
        "timed_out_chunks": 0,
        "current_chunk_index": 0,
        "finding_count": 0,
        "progress_pct": 0.0,
        "phase": "ready",
        "started_at": None,
        "finished_at": None,
        "last_updated_at": utc_now(),
        "chunks": manifest_chunks,
        "review_json": rel(REVIEW_JSON),
    }
    write_json(JOB_OVERVIEW, job)
    write_json(STATUS_JSON, {"phase": "ready", "job_overview": rel(JOB_OVERVIEW)})
    write_json(REVIEW_JSON, [])
    append_log(f"prepared {len(groups)} chunks ({chunk_size} urls each) from {len(urls)} targets")
    return job


def save_job(job: dict[str, Any]) -> None:
    completed = sum(1 for c in job["chunks"] if c.get("status") == "complete")
    failed = sum(1 for c in job["chunks"] if c.get("status") == "failed")
    timed_out = sum(1 for c in job["chunks"] if c.get("status") == "timed_out")
    pending = sum(1 for c in job["chunks"] if c.get("status") in ("pending", "running"))
    total = job.get("total_chunks") or 0
    job["completed_chunks"] = completed
    job["failed_chunks"] = failed
    job["timed_out_chunks"] = timed_out
    job["pending_chunks"] = pending
    job["progress_pct"] = round((completed / total) * 100, 2) if total else 0.0
    job["last_updated_at"] = utc_now()
    write_json(JOB_OVERVIEW, job)
    write_json(
        STATUS_JSON,
        {
            "phase": job.get("phase"),
            "progress_pct": job["progress_pct"],
            "completed_chunks": completed,
            "total_chunks": total,
            "finding_count": job.get("finding_count", 0),
            "job_overview": rel(JOB_OVERVIEW),
        },
    )


def run_single_chunk(
    chunk_index: int,
    *,
    timeout_s: int = DEFAULT_CHUNK_TIMEOUT_S,
    interface: str | None = None,
    source_ip: str | None = None,
    attempt: int = 1,
) -> dict[str, Any]:
    paths = chunk_paths(chunk_index)
    if not paths["urls"].is_file():
        raise FileNotFoundError(f"chunk url list missing: {paths['urls']}")
    if paths["raw"].is_file():
        paths["raw"].unlink()
    paths["stderr"].unlink(missing_ok=True)

    argv = build_nuclei_argv(
        paths["urls"],
        paths["raw"],
        interface=interface,
        source_ip=source_ip,
    )
    started = time.monotonic()
    iface_label = interface or source_ip or "default"
    append_log(
        f"{paths['id']}: starting on {iface_label} attempt={attempt} ({paths['urls'].name})"
    )
    child_pid: int | None = None
    stdout_text = ""
    stderr_text = ""
    try:
        popen = subprocess.Popen(
            argv,
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        child_pid = popen.pid
        stdout_text, stderr_text = popen.communicate(timeout=timeout_s)
        exit_code = popen.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        exit_code = 124
        timed_out = True
        if child_pid is not None and sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/PID", str(child_pid), "/T"],
                capture_output=True,
                timeout=15,
            )
        time.sleep(1.0)
    duration_s = round(time.monotonic() - started, 3)
    stderr_tail = (stderr_text or stdout_text or "").strip()[-2000:]
    if stderr_tail:
        paths["stderr"].write_text(stderr_tail + "\n", encoding="utf-8")

    findings = consolidate_findings_from_jsonl(paths["raw"], chunk_id=paths["id"])
    phase = classify_chunk_phase(exit_code=exit_code, timed_out=timed_out, duration_s=duration_s)
    # Timed-out chunks may still have partial hits — count as complete if jsonl was written.
    if phase == "timed_out" and paths["raw"].is_file() and paths["raw"].stat().st_size > 0:
        phase = "complete"
        append_log(f"{paths['id']}: timed out but kept partial jsonl ({paths['raw'].stat().st_size} bytes)")

    if not findings and paths["raw"].is_file() and phase == "complete":
        paths["raw"].unlink(missing_ok=True)

    termination = build_termination_record(
        phase=phase,
        exit_code=exit_code,
        finding_count=len(findings),
        duration_s=duration_s,
        timed_out=timed_out,
        attempt=attempt,
        interface=interface,
        stderr_tail=stderr_tail or None,
    )
    paths["termination"].write_text(termination["termination_message"] + "\n", encoding="utf-8")

    status = {
        "chunk_index": chunk_index,
        "chunk_id": paths["id"],
        "phase": phase,
        "exit_code": exit_code,
        "duration_s": duration_s,
        "finding_count": len(findings),
        "finished_at": utc_now(),
        "attempt": attempt,
        "interface": interface,
        "stderr_tail": stderr_tail or None,
        "stderr_log": rel(paths["stderr"]) if paths["stderr"].is_file() else None,
        "termination_log": rel(paths["termination"]),
        **termination,
    }
    write_json(paths["status"], status)
    append_log(f"{paths['id']}: {termination['termination_message']}")
    return {"status": status, "findings": findings}


def run_single_chunk_with_retries(
    chunk_index: int,
    *,
    timeout_s: int,
    interface: str | None,
    source_ip: str | None,
    prior_attempts: int = 0,
) -> dict[str, Any]:
    attempt = prior_attempts + 1
    while attempt <= MAX_CHUNK_ATTEMPTS:
        result = run_single_chunk(
            chunk_index,
            timeout_s=timeout_s,
            interface=interface,
            source_ip=source_ip,
            attempt=attempt,
        )
        phase = result["status"]["phase"]
        duration_s = float(result["status"]["duration_s"])
        if phase == "complete":
            return result
        if not chunk_is_retryable(phase, duration_s=duration_s, attempts=attempt):
            return result
        append_log(
            f"{chunk_paths(chunk_index)['id']}: retrying ({attempt}/{MAX_CHUNK_ATTEMPTS}) "
            f"after {phase} exit={result['status']['exit_code']}"
        )
        time.sleep(CHUNK_COOLDOWN_S * attempt)
        attempt += 1
    return result


def preflight_smoke_test(
    *,
    interface: str | None,
    source_ip: str | None,
    timeout_s: int = 120,
) -> None:
    """Verify nuclei can start and reach the network before a long job."""
    if not URL_LIST.is_file():
        raise SystemExit(f"URL list missing: {URL_LIST}")
    first_url = URL_LIST.read_text(encoding="utf-8").splitlines()[0].strip()
    if not first_url:
        raise SystemExit("URL list is empty")
    smoke_urls = TRIAL_DIR / "preflight_smoke_urls.txt"
    smoke_raw = TRIAL_DIR / "preflight_smoke.jsonl"
    smoke_urls.write_text(first_url + "\n", encoding="utf-8")
    smoke_raw.unlink(missing_ok=True)
    argv = build_nuclei_argv(smoke_urls, smoke_raw, interface=interface, source_ip=source_ip)
    append_log(f"preflight smoke test: {first_url} on {interface or source_ip or 'default'}")
    try:
        proc = subprocess.run(
            argv,
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
        )
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        # Nuclei still running after preflight window means it started successfully (templates are slow).
        append_log(
            f"preflight smoke test: nuclei still running after {timeout_s}s — "
            "treating as ok (slow template load)"
        )
        return
    if is_windows_crash_exit(exit_code) or (
        exit_code not in NUCLEI_OK_EXIT_CODES and exit_code != 2
    ):
        tail = (proc.stderr or proc.stdout or "").strip()[-1000:]
        raise SystemExit(f"preflight smoke test failed exit={exit_code}: {tail}")
    append_log(f"preflight smoke test ok exit={exit_code}")


def request_pause_after_next() -> None:
    TRIAL_DIR.mkdir(parents=True, exist_ok=True)
    PAUSE_AFTER_NEXT_FLAG.write_text(utc_now() + "\n", encoding="utf-8")
    append_log("pause requested — will stop after current chunk finishes")


def pause_requested() -> bool:
    return PAUSE_AFTER_NEXT_FLAG.is_file()


def pause_job_now(*, reset_running: bool = True) -> dict[str, Any]:
    job = load_json(JOB_OVERVIEW, None)
    if not job:
        raise SystemExit("No job_overview.json to pause")
    if reset_running:
        for chunk in job["chunks"]:
            if chunk.get("status") == "running":
                chunk["status"] = "pending"
    job["phase"] = "paused"
    job["paused_at"] = utc_now()
    PAUSE_AFTER_NEXT_FLAG.unlink(missing_ok=True)
    save_job(job)
    append_log(
        f"job paused at chunk {job.get('current_chunk_index')} "
        f"({job.get('completed_chunks')}/{job.get('total_chunks')} complete)"
    )
    return job


def reset_retryable_chunks(job: dict[str, Any], *, include_timed_out: bool = True) -> int:
    """Re-queue failed/timed-out chunks so resume can retry with fixed runner settings."""
    reset = 0
    for chunk in job["chunks"]:
        status = chunk.get("status")
        if status == "complete":
            continue
        if status == "timed_out" and not include_timed_out:
            continue
        if status in ("failed", "timed_out", "running"):
            chunk["status"] = "pending"
            for key in ("finished_at", "duration_s", "exit_code", "finding_count", "attempt"):
                chunk.pop(key, None)
            reset += 1
    return reset


def job_fully_processed(job: dict[str, Any]) -> bool:
    return all(c.get("status") in ("complete", "failed", "timed_out") for c in job["chunks"])


def maybe_finalize_job(job: dict[str, Any], *, errors: int) -> None:
    if not job_fully_processed(job):
        return
    has_errors = any(c.get("status") != "complete" for c in job["chunks"]) or errors > 0
    job["phase"] = "complete" if not has_errors else "complete_with_errors"
    job["finished_at"] = utc_now()


def run_chunked_job(
    *,
    chunk_size: int,
    chunk_timeout_s: int,
    resume: bool,
    interface: str | None = None,
    source_ip: str | None = None,
    worker_id: int | None = None,
    worker_count: int = 1,
    worker_label: str | None = None,
    skip_preflight: bool = False,
) -> int:
    if not NUCLEI_BIN.is_file():
        raise SystemExit(f"nuclei binary not found: {NUCLEI_BIN}")
    if not TEMPLATES.is_dir():
        raise SystemExit(f"nuclei templates not found: {TEMPLATES}")

    if not URL_LIST.is_file():
        raise SystemExit(f"URL list missing: {URL_LIST} (run --prepare-chunks first)")

    bind_iface, bind_ip = default_scan_interface(interface)
    if source_ip:
        bind_ip = source_ip
    if bind_iface is None and bind_ip is None:
        append_log("warning: no WiFi adapter resolved; nuclei will use system default route")

    with job_lock():
        job = load_json(JOB_OVERVIEW, None)
        if job is None or not resume:
            urls = extract_urls_from_katana_text(DEFAULT_KATANA_TEXT, URL_LIST)
            job = prepare_chunks(urls, chunk_size)
        elif job.get("chunk_size") != chunk_size:
            append_log(
                f"warning: job chunk_size={job.get('chunk_size')} differs from --chunk-size={chunk_size}; using job value"
            )
            chunk_size = int(job.get("chunk_size") or chunk_size)
        elif resume:
            reset_n = reset_retryable_chunks(job, include_timed_out=True)
            if reset_n:
                append_log(f"resume: reset {reset_n} incomplete chunk(s) to pending")

        if job.get("phase") not in ("ready", "running", "paused"):
            append_log(f"job phase is {job.get('phase')}; nothing to do")
            return 0

        job["phase"] = "running"
        if not job.get("started_at"):
            job["started_at"] = utc_now()
        job["chunk_timeout_s"] = chunk_timeout_s
        if worker_id is not None:
            job.setdefault("workers", {})
            job["workers"][str(worker_id)] = {
                "label": worker_label or f"worker{worker_id}",
                "interface": bind_iface,
                "source_ip": bind_ip,
                "started_at": utc_now(),
            }
        save_job(job)

    review_path = review_json_for_worker(worker_id)
    accumulated: list[dict[str, Any]] = load_json(review_path, [])
    errors = 0
    worker_tag = f"w{worker_id}" if worker_id is not None else "solo"
    append_log(
        f"worker {worker_tag} binding interface={bind_iface or 'default'} "
        f"ip={bind_ip or 'auto'} chunks={worker_id}/{worker_count if worker_count > 1 else 1}"
    )

    if not skip_preflight:
        try:
            preflight_smoke_test(interface=bind_iface, source_ip=bind_ip)
        except SystemExit as exc:
            append_log(f"preflight failed: {exc}")
            raise

    job = reload_job()
    consecutive_instant_fails = 0
    for chunk in job["chunks"]:
        idx = int(chunk["chunk_index"])
        if not chunk_assigned_to_worker(idx, worker_id, worker_count):
            continue
        if chunk.get("status") == "complete":
            continue
        if pause_requested():
            with job_lock():
                job = reload_job()
                job["phase"] = "paused"
                job["paused_at"] = utc_now()
                save_job(job)
            PAUSE_AFTER_NEXT_FLAG.unlink(missing_ok=True)
            append_log("paused after chunk boundary (pause_after_next flag)")
            return 0

        with job_lock():
            job = reload_job()
            chunk_ref = job["chunks"][idx - 1]
            chunk_ref["status"] = "running"
            chunk_ref["worker_id"] = worker_id
            chunk_ref["interface"] = bind_iface
            job["current_chunk_index"] = idx
            save_job(job)

        result = run_single_chunk_with_retries(
            idx,
            timeout_s=chunk_timeout_s,
            interface=bind_iface,
            source_ip=bind_ip,
            prior_attempts=0,
        )
        chunk_status = result["status"]["phase"]
        duration_s = float(result["status"]["duration_s"])

        if chunk_status != "complete" and duration_s < INSTANT_FAIL_DURATION_S:
            consecutive_instant_fails += 1
        else:
            consecutive_instant_fails = 0

        if consecutive_instant_fails >= CIRCUIT_BREAKER_INSTANT_FAILS:
            append_log(
                f"circuit breaker: {consecutive_instant_fails} instant failures in a row — pausing job"
            )
            with job_lock():
                job = reload_job()
                job["phase"] = "paused"
                job["paused_at"] = utc_now()
                job["circuit_breaker"] = {
                    "reason": "consecutive_instant_nuclei_failures",
                    "at_chunk": idx,
                    "at": utc_now(),
                }
                save_job(job)
            return 1

        time.sleep(CHUNK_COOLDOWN_S)

        with job_lock():
            job = reload_job()
            chunk_ref = job["chunks"][idx - 1]
            chunk_ref["status"] = chunk_status
            chunk_ref["finding_count"] = result["status"]["finding_count"]
            chunk_ref["duration_s"] = result["status"]["duration_s"]
            chunk_ref["finished_at"] = result["status"]["finished_at"]
            chunk_ref["worker_id"] = worker_id
            chunk_ref["interface"] = bind_iface
            chunk_ref["attempt"] = result["status"].get("attempt")
            chunk_ref["exit_code"] = result["status"].get("exit_code")
            save_job(job)

        if result["findings"]:
            accumulated = merge_findings(accumulated, result["findings"])
            write_json(review_path, accumulated)
            with job_lock():
                merge_all_findings()
            append_log(
                f"{worker_tag} accumulated findings now {len(accumulated)} "
                f"(merged total {len(load_json(REVIEW_JSON, []))})"
            )

        if chunk_status != "complete":
            errors += 1

        if pause_requested():
            with job_lock():
                job = reload_job()
                job["phase"] = "paused"
                job["paused_at"] = utc_now()
                save_job(job)
            PAUSE_AFTER_NEXT_FLAG.unlink(missing_ok=True)
            append_log("paused after chunk finished (pause_after_next flag)")
            return 0

    with job_lock():
        job = reload_job()
        pending_for_worker = [
            c
            for c in job["chunks"]
            if chunk_assigned_to_worker(int(c["chunk_index"]), worker_id, worker_count)
            and c.get("status") != "complete"
        ]
        if not pending_for_worker:
            maybe_finalize_job(job, errors=errors)
        job["finding_count"] = len(merge_all_findings())
        save_job(job)

    append_log(
        f"worker {worker_tag} finished errors={errors} findings={len(accumulated)}"
    )
    return 0 if errors == 0 else 1


def print_status() -> None:
    job = load_json(JOB_OVERVIEW, None)
    if not job:
        print("No job_overview.json — run --prepare-chunks first")
        return
    findings = load_json(REVIEW_JSON, [])
    adapters = resolve_wifi_adapters()
    print(json.dumps(
        {
            "phase": job.get("phase"),
            "progress_pct": job.get("progress_pct"),
            "completed_chunks": job.get("completed_chunks"),
            "total_chunks": job.get("total_chunks"),
            "failed_chunks": job.get("failed_chunks"),
            "timed_out_chunks": job.get("timed_out_chunks"),
            "finding_count": len(findings),
            "current_chunk_index": job.get("current_chunk_index"),
            "workers": job.get("workers"),
            "adapters": adapters,
            "review_json": rel(REVIEW_JSON),
        },
        indent=2,
    ))


def launch_detached_worker(
    *,
    chunk_size: int,
    chunk_timeout_s: int,
    resume: bool,
    worker_id: int | None = None,
    worker_count: int = 1,
    interface: str | None = None,
    source_ip: str | None = None,
) -> None:
    script = Path(__file__).resolve()
    TRIAL_DIR.mkdir(parents=True, exist_ok=True)
    log_handle = RUN_LOG.open("a", encoding="utf-8")
    args = [
        sys.executable,
        str(script),
        "--run-chunked",
        "--chunk-size",
        str(chunk_size),
        "--chunk-timeout",
        str(chunk_timeout_s),
    ]
    if resume:
        args.extend(["--resume", "--reset-incomplete"])
    if worker_id is not None:
        args.extend(["--worker-id", str(worker_id), "--worker-count", str(worker_count)])
    if interface:
        args.extend(["--interface", interface])
    if source_ip:
        args.extend(["--source-ip", source_ip])
    args.append("--skip-preflight")
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS  # type: ignore[attr-defined]
    subprocess.Popen(
        args,
        cwd=str(REPO_ROOT),
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
        close_fds=False,
    )


def launch_detached_chunked(
    chunk_size: int,
    chunk_timeout_s: int,
    resume: bool,
    *,
    interface: str | None = None,
) -> None:
    bind_iface, bind_ip = default_scan_interface(interface)
    launch_detached_worker(
        chunk_size=chunk_size,
        chunk_timeout_s=chunk_timeout_s,
        resume=resume,
        interface=bind_iface,
        source_ip=bind_ip,
    )
    append_log(
        f"launched detached chunked nuclei job on {bind_iface or bind_ip or 'default route'}"
    )
    print(f"Job overview: {JOB_OVERVIEW}")
    print(f"Findings:     {REVIEW_JSON}")
    print(f"Log:          {RUN_LOG}")


def launch_detached_dual(chunk_size: int, chunk_timeout_s: int, resume: bool) -> None:
    plan = dual_scan_plan()
    if len(plan) < 2:
        append_log("dual WiFi unavailable — only one adapter up; launching single worker on WiFi 2/default")
        launch_detached_chunked(chunk_size, chunk_timeout_s, resume)
        return
    worker_count = len(plan)
    for entry in plan:
        wid = int(entry["worker_id"])  # type: ignore[arg-type]
        launch_detached_worker(
            chunk_size=chunk_size,
            chunk_timeout_s=chunk_timeout_s,
            resume=resume,
            worker_id=wid,
            worker_count=worker_count,
            interface=entry.get("interface"),
            source_ip=entry.get("source_ip"),
        )
        append_log(
            f"launched worker {wid} ({entry.get('label')}) on {entry.get('interface')} "
            f"ip={entry.get('source_ip')}"
        )
    print(f"Launched {worker_count} parallel workers (WiFi 2 + WiFi)")
    print(f"Job overview: {JOB_OVERVIEW}")
    print(f"Findings:     {REVIEW_JSON}")
    print(f"Log:          {RUN_LOG}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Chunked nuclei critical/high trial over katana URLs")
    parser.add_argument("--katana-text", type=Path, default=DEFAULT_KATANA_TEXT)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--chunk-timeout", type=int, default=DEFAULT_CHUNK_TIMEOUT_S)
    parser.add_argument("--prepare-chunks", action="store_true", help="Extract URLs and split into chunk lists")
    parser.add_argument("--launch-chunked", action="store_true", help="Prepare (if needed) and start detached chunked run (defaults to WiFi 2)")
    parser.add_argument("--launch-dual", action="store_true", help="Start two detached workers on WiFi 2 + WiFi in parallel")
    parser.add_argument("--run-chunked", action="store_true", help="Run pending chunks in this process")
    parser.add_argument("--resume", action="store_true", help="Resume existing chunk job (skip finished chunks)")
    parser.add_argument("--interface", metavar="NAME", help="Nuclei -i adapter name (default: WiFi 2 when connected)")
    parser.add_argument("--source-ip", metavar="IP", help="Nuclei -sip source IP (overrides auto-detect)")
    parser.add_argument("--worker-id", type=int, help="Worker index for parallel dual-WiFi runs (0-based)")
    parser.add_argument("--worker-count", type=int, default=1, help="Total parallel workers (use 2 with --launch-dual)")
    parser.add_argument("--merge-findings", action="store_true", help="Merge per-worker findings into critical_high_findings.json")
    parser.add_argument("--status", action="store_true", help="Print job progress summary")
    parser.add_argument("--request-pause", action="store_true", help="Stop after the current chunk finishes")
    parser.add_argument("--pause-now", action="store_true", help="Pause immediately (reset in-flight chunk to pending)")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip nuclei smoke test before chunked run")
    parser.add_argument("--reset-incomplete", action="store_true", help="On resume, reset all failed/timed_out chunks to pending")
    parser.add_argument("--extract-only", action="store_true", help="Only rebuild targets_urls.txt")
    args = parser.parse_args()

    katana_text = args.katana_text if args.katana_text.is_absolute() else REPO_ROOT / args.katana_text
    if not katana_text.is_file():
        raise SystemExit(f"katana text not found: {katana_text}")

    if args.status:
        print_status()
        return 0

    if args.merge_findings:
        merged = merge_all_findings()
        print(f"Merged {len(merged)} findings -> {REVIEW_JSON}")
        return 0

    if args.pause_now:
        pause_job_now(reset_running=True)
        print_status()
        return 0

    if args.request_pause:
        request_pause_after_next()
        print("Pause scheduled after the current chunk completes.")
        print_status()
        return 0

    urls = extract_urls_from_katana_text(katana_text, URL_LIST)
    append_log(f"extracted {len(urls)} unique URLs -> {rel(URL_LIST)}")
    if args.extract_only:
        return 0

    if args.prepare_chunks:
        prepare_chunks(urls, args.chunk_size)
        print_status()
        return 0

    if args.launch_chunked:
        if not JOB_OVERVIEW.is_file() or not args.resume:
            prepare_chunks(urls, args.chunk_size)
        launch_detached_chunked(
            args.chunk_size,
            args.chunk_timeout,
            resume=args.resume,
            interface=args.interface,
        )
        print_status()
        return 0

    if args.launch_dual:
        if not JOB_OVERVIEW.is_file() or not args.resume:
            prepare_chunks(urls, args.chunk_size)
        launch_detached_dual(args.chunk_size, args.chunk_timeout, resume=args.resume)
        print_status()
        return 0

    if args.run_chunked:
        worker_id = args.worker_id
        if args.worker_count > 1 and worker_id is None:
            raise SystemExit("--worker-count > 1 requires --worker-id")
        return run_chunked_job(
            chunk_size=args.chunk_size,
            chunk_timeout_s=args.chunk_timeout,
            resume=args.resume or JOB_OVERVIEW.is_file(),
            interface=args.interface,
            source_ip=args.source_ip,
            worker_id=worker_id,
            worker_count=args.worker_count,
            skip_preflight=args.skip_preflight,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
