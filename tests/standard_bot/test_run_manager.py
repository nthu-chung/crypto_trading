import sys

from cyqnt_trd.standard_bot.runtime.run_manager import LocalRunManager


def _sleep_command(seconds: float = 30.0) -> list[str]:
    return [sys.executable, "-c", "import time; time.sleep(%s)" % seconds]


def test_local_run_manager_start_list_and_stop(tmp_path):
    manager = LocalRunManager(root_dir=str(tmp_path / "runs"))

    record = manager.start_command(
        profile="test_sleep",
        command=_sleep_command(),
        workdir=str(tmp_path),
        tags={"kind": "unit_test"},
    )

    assert record.run_id
    assert record.status == "running"
    assert record.tags["kind"] == "unit_test"

    listed = manager.list_runs(refresh=True)
    assert any(item.run_id == record.run_id for item in listed)

    stopped = manager.stop(record.run_id, timeout_seconds=2.0)
    assert stopped.status in {"stopped", "exited"}

    refreshed = manager.get_run(record.run_id, refresh=True)
    assert refreshed.status in {"stopped", "exited"}


def test_local_run_manager_kill_updates_status(tmp_path):
    manager = LocalRunManager(root_dir=str(tmp_path / "runs"))

    record = manager.start_command(
        profile="test_sleep",
        command=_sleep_command(),
        workdir=str(tmp_path),
    )

    killed = manager.kill(record.run_id, timeout_seconds=1.0)
    assert killed.status in {"killed", "exited"}

    refreshed = manager.get_run(record.run_id, refresh=True)
    assert refreshed.status in {"killed", "exited"}
