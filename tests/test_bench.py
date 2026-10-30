from ailab.bench import run_bench
from ailab.db import connect


def test_run_bench_scores_correctness(tmp_path):
    conn = connect(tmp_path / "t.db")
    cases = [{"text": "x", "category": "billing"}, {"text": "y", "category": "account"}]
    fake = lambda p, **k: '{"category":"billing","urgency":"low","reply":"ok"}'
    run_bench(conn, cases, ["m1"], variants=("zero_shot", "few_shot"), llm=fake)
    rows = conn.execute(
        "select variant, sum(correct), sum(valid), count(*) from bench group by variant order by variant"
    ).fetchall()
    assert rows == [("few_shot", 1, 2, 2), ("zero_shot", 1, 2, 2)]
