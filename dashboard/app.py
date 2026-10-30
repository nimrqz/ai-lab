import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3

import pandas as pd
import streamlit as st

from ailab.askdata import ask
from ailab.db import connect

DB = "data/results.db"
connect(DB).close()
st.set_page_config(page_title="ai-lab", page_icon="🤖", layout="wide")
st.title("🤖 ai-lab — IA aplicada, 100% local")
st.caption("Automações com LLM rodando em CPU via Ollama. Sem API key, sem dados reais.")

conn = sqlite3.connect(DB)
runs = pd.read_sql_query("select * from runs", conn)
bench = pd.read_sql_query("select * from bench", conn)
conn.close()

tab1, tab2, tab3 = st.tabs(["⏱️ Horas economizadas", "🧪 Benchmark de prompts", "💬 Pergunte aos dados"])

with tab1:
    if runs.empty:
        st.info("Rode `python -m ailab.cli automate triage --n 10` para gerar dados.")
    else:
        saved_h = (runs.manual_seconds.sum() - runs.actual_seconds.sum()) / 3600
        c1, c2, c3 = st.columns(3)
        c1.metric("Itens processados", len(runs))
        c2.metric("Horas economizadas", f"{saved_h:.2f} h")
        c3.metric("Taxa de sucesso", f"{runs.ok.mean():.0%}")
        by_auto = (runs.groupby("automation")[["manual_seconds", "actual_seconds"]].sum()
                   .assign(horas=lambda d: (d.manual_seconds - d.actual_seconds) / 3600)["horas"])
        st.bar_chart(by_auto.rename("horas economizadas"))
        st.caption("Premissa: tempo manual estimado por item (triagem 90 s, extração 120 s, resumo 300 s).")
        st.dataframe(runs.tail(20), width="stretch")

with tab2:
    if bench.empty:
        st.info("Rode `python -m ailab.cli bench --n 15 --models qwen2.5:3b llama3.2:3b`.")
    else:
        agg = bench.groupby(["model", "variant"]).agg(
            acerto=("correct", "mean"), formato_valido=("valid", "mean"),
            latencia_s=("seconds", "mean")).reset_index()
        st.dataframe(agg.style.format({"acerto": "{:.0%}", "formato_valido": "{:.0%}",
                                       "latencia_s": "{:.1f}"}), width="stretch")
        st.bar_chart(agg.pivot(index="variant", columns="model", values="acerto"), stack=False)
        st.caption("Amostra pequena (12 casos por célula): use como indício, não como conclusão estatística.")

with tab3:
    q = st.text_input("Pergunte algo sobre os dados", "Qual automação economizou mais tempo?")
    if st.button("Perguntar"):
        try:
            sql, df = ask(DB, q)
            st.code(sql, language="sql")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Não consegui responder: {e}")
