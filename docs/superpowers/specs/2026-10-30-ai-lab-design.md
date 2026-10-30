# ai-lab — Design

Portfólio de IA aplicada, 100% local (sem API key), construído em um dia.

## Objetivo
Demonstrar: (1) engenharia de prompts estruturados, (2) experimentação comparativa com LLMs, (3) automações com ganho de tempo mensurável, (4) dashboard com IA.

## Motor
Ollama local (CPU) com modelo pequeno (`qwen2.5:3b`; comparação com `llama3.2:3b`). Toda chamada passa por `ailab/llm.py` (`generate(prompt, model, schema=None) -> str|obj`), isolando o provedor.

## Módulos
- `ailab/llm.py` — cliente Ollama (HTTP `localhost:11434`), timeout, retry.
- `ailab/prompts/` — templates YAML (papel, contexto, formato, few-shot) + loader; saída JSON validada por Pydantic com retry em caso de formato inválido.
- `ailab/bench/` — roda um conjunto de casos rotulados contra variações de prompt (zero-shot, few-shot, CoT) e modelos; mede acerto, validade do formato e latência; salva em `data/results.db` (SQLite).
- `ailab/automations/` — 3 automações: triagem de tickets/e-mails, extração de dados de texto bagunçado para CSV, resumo de documentos em tópicos/ações. Cada execução registra tempo manual estimado vs. tempo real em SQLite.
- `dashboard/app.py` — Streamlit: itens processados, horas economizadas, acurácia por prompt/modelo; aba "pergunte aos dados" (LLM gera SQL somente-leitura sobre o SQLite, validado antes de executar).
- `data/synthetic/` — dados sintéticos gerados por script; nenhum dado pessoal real.

## Fluxo de dados
entrada (texto) → prompt template → llm.py → JSON validado → resultado + métricas → SQLite → dashboard.

## Erros
Saída inválida: até 2 retries com mensagem de erro de validação reaproveitada no prompt; depois registra falha (conta como erro no benchmark). SQL gerado: só `SELECT`, única instrução, rejeitado caso contrário.

## Testes
pytest com `llm.py` mockado para loader, validação, retry, cálculo de horas e guarda de SQL. Smoke test real contra Ollama separado.

## Entrega
README com prints/GIF, números reais do benchmark e seção de decisões técnicas.

## Fora de escopo (YAGNI)
Autenticação, deploy em nuvem, fine-tuning, RAG.
