from ailab.db import log_bench
from ailab.llm import generate
from ailab.prompts import VARIANTS, load_template, render
from ailab.schemas import TicketTriage
from ailab.structured import run_structured


def run_bench(conn, cases, models, variants=VARIANTS, llm=generate):
    tpl = load_template("triage")
    for model in models:
        for variant in variants:
            for i, case in enumerate(cases):
                res = run_structured(render(tpl, case["text"], variant), TicketTriage,
                                     model=model, llm=llm)
                correct = res.ok and res.obj.category == case["category"]
                log_bench(conn, "triage", model, variant, i, correct, res.ok, res.seconds)
