from ailab.schemas import TicketTriage
from ailab.structured import run_structured

GOOD = '{"category":"billing","urgency":"high","reply":"ok"}'


def test_valid_first_try():
    r = run_structured("p", TicketTriage, llm=lambda p, **k: GOOD)
    assert r.ok and r.attempts == 1 and r.obj.category == "billing"


def test_retry_then_success():
    calls = []
    def llm(p, **k):
        calls.append(p)
        return "não é json" if len(calls) == 1 else GOOD
    r = run_structured("p", TicketTriage, llm=llm)
    assert r.ok and r.attempts == 2 and "inválida" in calls[1]


def test_gives_up():
    r = run_structured("p", TicketTriage, retries=2, llm=lambda p, **k: "x")
    assert not r.ok and r.attempts == 3 and r.obj is None and r.error
