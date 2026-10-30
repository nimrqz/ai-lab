import argparse
import json
from pathlib import Path
from ailab.automations import run_batch
from ailab.bench import run_bench
from ailab.db import connect
from ailab.llm import DEFAULT_MODEL

DATA = Path("data/synthetic")
SOURCES = {"triage": "tickets", "extract": "invoices", "summarize": "docs"}


def _load(source, n):
    return json.loads((DATA / f"{source}.json").read_text(encoding="utf-8"))[:n]


def main():
    p = argparse.ArgumentParser(prog="ailab")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("automate")
    a.add_argument("name", choices=SOURCES)
    a.add_argument("--n", type=int, default=10)
    a.add_argument("--model", default=DEFAULT_MODEL)
    b = sub.add_parser("bench")
    b.add_argument("--n", type=int, default=15)
    b.add_argument("--models", nargs="+", default=[DEFAULT_MODEL])
    args = p.parse_args()
    conn = connect()
    if args.cmd == "automate":
        items = _load(SOURCES[args.name], args.n)
        texts = [i["text"] if isinstance(i, dict) else i for i in items]
        res = run_batch(conn, args.name, texts, model=args.model)
        print(f"{sum(r.ok for r in res)}/{len(res)} ok")
    else:
        run_bench(conn, _load("tickets", args.n), args.models)
        print("benchmark gravado")


if __name__ == "__main__":
    main()
