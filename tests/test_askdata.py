import pytest
from ailab.askdata import ask
from ailab.db import connect, log_run


def make_db(tmp_path):
    p = tmp_path / "t.db"
    log_run(connect(p), "triage", "m", "few_shot", True, 90, 5)
    return p


def test_ask_runs_generated_select(tmp_path):
    llm = lambda p, **k: "```sql\nSELECT count(*) AS n FROM runs;\n```"
    sql, df = ask(make_db(tmp_path), "quantas execuções?", llm=llm)
    assert sql == "SELECT count(*) AS n FROM runs" and df["n"][0] == 1


def test_ask_rejects_write(tmp_path):
    with pytest.raises(ValueError):
        ask(make_db(tmp_path), "apague tudo", llm=lambda p, **k: "DROP TABLE runs")
