import time
from dataclasses import dataclass
from ailab.db import log_run
from ailab.llm import generate, DEFAULT_MODEL
from ailab.prompts import load_template, render
from ailab.schemas import TicketTriage, Invoice, Summary
from ailab.structured import run_structured


@dataclass
class Automation:
    template: str
    schema: type
    manual_seconds: int


AUTOMATIONS = {
    "triage": Automation("triage", TicketTriage, 90),
    "extract": Automation("extract", Invoice, 120),
    "summarize": Automation("summarize", Summary, 300),
}


def run_batch(conn, name, texts, variant="few_shot", model=DEFAULT_MODEL, llm=generate):
    auto = AUTOMATIONS[name]
    tpl = load_template(auto.template)
    results = []
    for text in texts:
        start = time.perf_counter()
        res = run_structured(render(tpl, text, variant), auto.schema, model=model, llm=llm)
        log_run(conn, name, model, variant, res.ok, auto.manual_seconds,
                time.perf_counter() - start)
        results.append(res)
    return results
