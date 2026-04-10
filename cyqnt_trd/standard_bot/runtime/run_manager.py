"""
Local background process manager for standard bot demo/runtime commands.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


def _now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class ManagedRunRecord:
    run_id: str
    profile: str
    command: List[str]
    pid: int
    pgid: Optional[int]
    status: str
    started_at: int
    updated_at: int
    workdir: str
    log_path: str
    metadata_path: str
    stop_requested_at: Optional[int] = None
    ended_at: Optional[int] = None
    tags: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ManagedRunRecord":
        return cls(
            run_id=str(payload["run_id"]),
            profile=str(payload["profile"]),
            command=list(payload.get("command", [])),
            pid=int(payload["pid"]),
            pgid=None if payload.get("pgid") is None else int(payload["pgid"]),
            status=str(payload["status"]),
            started_at=int(payload["started_at"]),
            updated_at=int(payload["updated_at"]),
            workdir=str(payload["workdir"]),
            log_path=str(payload["log_path"]),
            metadata_path=str(payload["metadata_path"]),
            stop_requested_at=None
            if payload.get("stop_requested_at") is None
            else int(payload["stop_requested_at"]),
            ended_at=None if payload.get("ended_at") is None else int(payload["ended_at"]),
            tags=dict(payload.get("tags", {})),
        )


class LocalRunManager:
    def __init__(self, root_dir: str = ".standard_bot_runs") -> None:
        self.root_dir = Path(root_dir)
        self.records_dir = self.root_dir / "records"
        self.logs_dir = self.root_dir / "logs"
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def start_command(
        self,
        *,
        profile: str,
        command: Sequence[str],
        workdir: str,
        run_id: Optional[str] = None,
        log_path: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        tags: Optional[Dict[str, Any]] = None,
    ) -> ManagedRunRecord:
        resolved_run_id = run_id or str(uuid.uuid4())
        metadata_path = self.records_dir / ("%s.json" % resolved_run_id)
        if metadata_path.exists():
            raise FileExistsError("run_id already exists: %s" % resolved_run_id)

        resolved_log_path = Path(log_path) if log_path else self.logs_dir / ("%s.log" % resolved_run_id)
        resolved_log_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_env = os.environ.copy()
        runtime_env.setdefault("STANDARD_BOT_MANAGED_RUN_ID", resolved_run_id)
        runtime_env.setdefault("STANDARD_BOT_MANAGED_PROFILE", profile)
        if env:
            runtime_env.update(env)

        with resolved_log_path.open("ab") as sink:
            process = subprocess.Popen(
                list(command),
                cwd=workdir,
                env=runtime_env,
                stdin=subprocess.DEVNULL,
                stdout=sink,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        try:
            pgid = os.getpgid(process.pid)
        except OSError:
            pgid = None

        record = ManagedRunRecord(
            run_id=resolved_run_id,
            profile=profile,
            command=list(command),
            pid=process.pid,
            pgid=pgid,
            status="running",
            started_at=_now_ms(),
            updated_at=_now_ms(),
            workdir=str(workdir),
            log_path=str(resolved_log_path),
            metadata_path=str(metadata_path),
            tags=dict(tags or {}),
        )
        self._write_record(record)
        return record

    def list_runs(self, *, refresh: bool = True) -> List[ManagedRunRecord]:
        records: List[ManagedRunRecord] = []
        for path in sorted(self.records_dir.glob("*.json")):
            record = self._read_record(path)
            if refresh:
                record = self.refresh(record.run_id)
            records.append(record)
        return sorted(records, key=lambda item: item.started_at, reverse=True)

    def get_run(self, run_id: str, *, refresh: bool = True) -> ManagedRunRecord:
        path = self.records_dir / ("%s.json" % run_id)
        if not path.exists():
            raise FileNotFoundError("unknown run_id: %s" % run_id)
        record = self._read_record(path)
        return self.refresh(run_id) if refresh else record

    def stop(self, run_id: str, *, timeout_seconds: float = 5.0) -> ManagedRunRecord:
        return self._terminate(run_id, sig=signal.SIGTERM, timeout_seconds=timeout_seconds)

    def kill(self, run_id: str, *, timeout_seconds: float = 2.0) -> ManagedRunRecord:
        return self._terminate(run_id, sig=signal.SIGKILL, timeout_seconds=timeout_seconds)

    def refresh(self, run_id: str) -> ManagedRunRecord:
        record = self.get_run(run_id, refresh=False)
        alive = self._is_alive(record.pid)
        updated = False
        if alive and record.status not in {"running", "stopping"}:
            record.status = "running"
            record.ended_at = None
            updated = True
        elif not alive and record.status not in {"exited", "stopped", "killed"}:
            record.status = "exited"
            record.ended_at = _now_ms()
            updated = True
        if updated:
            record.updated_at = _now_ms()
            self._write_record(record)
        return record

    def _terminate(self, run_id: str, *, sig: signal.Signals, timeout_seconds: float) -> ManagedRunRecord:
        record = self.get_run(run_id, refresh=False)
        if not self._is_alive(record.pid):
            if record.status not in {"exited", "stopped", "killed"}:
                record.status = "exited"
                record.ended_at = _now_ms()
                record.updated_at = _now_ms()
                self._write_record(record)
            return record

        record.stop_requested_at = _now_ms()
        record.status = "stopping" if sig == signal.SIGTERM else "killing"
        record.updated_at = _now_ms()
        self._write_record(record)

        target = -record.pgid if record.pgid else record.pid
        try:
            os.kill(target, sig)
        except ProcessLookupError:
            record.status = "exited"
            record.ended_at = _now_ms()
            record.updated_at = _now_ms()
            self._write_record(record)
            return record

        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if not self._is_alive(record.pid):
                break
            time.sleep(0.1)

        alive = self._is_alive(record.pid)
        if alive:
            record.status = "running"
        else:
            record.status = "stopped" if sig == signal.SIGTERM else "killed"
            record.ended_at = _now_ms()
        record.updated_at = _now_ms()
        self._write_record(record)
        return record

    def _read_record(self, path: Path) -> ManagedRunRecord:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return ManagedRunRecord.from_dict(payload)

    def _write_record(self, record: ManagedRunRecord) -> None:
        path = Path(record.metadata_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _is_alive(self, pid: int) -> bool:
        try:
            waited_pid, _status = os.waitpid(pid, os.WNOHANG)
            if waited_pid == pid:
                return False
        except ChildProcessError:
            pass
        except OSError:
            pass

        try:
            os.kill(pid, 0)
        except OSError:
            return False
        ps = subprocess.run(
            ["ps", "-o", "stat=", "-p", str(pid)],
            check=False,
            capture_output=True,
            text=True,
        )
        state = ps.stdout.strip()
        if not state:
            return False
        if "Z" in state:
            return False
        return True
