from ailab.automations import AUTOMATIONS, run_batch
from ailab.db import connect


def test_run_batch_logs_each_item(tmp_path):
    conn = connect(tmp_path / "t.db")
    fake = lambda p, **k: '{"category":"billing","urgency":"low","reply":"ok"}'
    results = run_batch(conn, "triage", ["a", "b"], llm=fake)
    assert [r.ok for r in results] == [True, True]
    rows = conn.execute("select automation, manual_seconds, ok from runs").fetchall()
    assert rows == [("triage", 90, 1), ("triage", 90, 1)]


def test_registry_keys():
    assert set(AUTOMATIONS) == {"triage", "extract", "summarize"}
