import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(
  id INTEGER PRIMARY KEY, ts TEXT DEFAULT CURRENT_TIMESTAMP, automation TEXT, model TEXT,
  variant TEXT, ok INTEGER, manual_seconds REAL, actual_seconds REAL);
CREATE TABLE IF NOT EXISTS bench(
  id INTEGER PRIMARY KEY, ts TEXT DEFAULT CURRENT_TIMESTAMP, task TEXT, model TEXT,
  variant TEXT, case_id INTEGER, correct INTEGER, valid INTEGER, seconds REAL);
"""


def connect(path="data/results.db"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn


def log_run(conn, automation, model, variant, ok, manual_seconds, actual_seconds):
    conn.execute(
        "INSERT INTO runs(automation,model,variant,ok,manual_seconds,actual_seconds) VALUES(?,?,?,?,?,?)",
        (automation, model, variant, int(ok), manual_seconds, actual_seconds))
    conn.commit()


def log_bench(conn, task, model, variant, case_id, correct, valid, seconds):
    conn.execute(
        "INSERT INTO bench(task,model,variant,case_id,correct,valid,seconds) VALUES(?,?,?,?,?,?,?)",
        (task, model, variant, case_id, int(correct), int(valid), seconds))
    conn.commit()
