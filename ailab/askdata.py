import re
import sqlite3
import pandas as pd
from ailab.llm import generate
from ailab.sqlguard import validate_select

SCHEMA_HELP = """Tabelas SQLite:
runs(id, ts, automation, model, variant, ok, manual_seconds, actual_seconds)
bench(id, ts, task, model, variant, case_id, correct, valid, seconds)
ok/correct/valid são 0 ou 1. automation: triage, extract, summarize.
Tempo economizado = manual_seconds - actual_seconds (some com SUM). Acerto = AVG(correct).

Exemplos:
P: Quantas horas foram economizadas por automação?
SQL: SELECT automation, SUM(manual_seconds - actual_seconds) / 3600.0 AS horas FROM runs GROUP BY automation ORDER BY horas DESC
P: Qual variante de prompt acerta mais?
SQL: SELECT variant, AVG(correct) AS acerto FROM bench GROUP BY variant ORDER BY acerto DESC"""


def _extract_sql(text):
    m = re.search(r"```(?:sql)?\s*(.*?)```", text, re.S | re.I)
    return (m.group(1) if m else text).strip()


def ask(db_path, question, llm=generate):
    prompt = (f"{SCHEMA_HELP}\n\nEscreva UMA consulta SQLite SELECT que responda: {question}\n"
              "Responda apenas com o SQL.")
    sql = validate_select(_extract_sql(llm(prompt)))
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return sql, pd.read_sql_query(sql, conn)
    finally:
        conn.close()
