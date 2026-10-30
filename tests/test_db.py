from ailab.db import connect, log_run, log_bench


def test_log_and_read(tmp_path):
    conn = connect(tmp_path / "t.db")
    log_run(conn, "triage", "m", "few_shot", True, 90, 4.2)
    log_bench(conn, "triage", "m", "cot", 1, True, True, 3.0)
    assert conn.execute("select count(*) from runs").fetchone()[0] == 1
    assert conn.execute("select correct from bench").fetchone()[0] == 1
