import json
import random
from pathlib import Path

rng = random.Random(42)
OUT = Path("data/synthetic")
OUT.mkdir(parents=True, exist_ok=True)

TICKETS = {
    "billing": ["Fui cobrado duas vezes no cartão", "Quero o estorno da fatura de {m}",
                "O boleto veio com valor errado", "Minha assinatura foi renovada sem aviso"],
    "technical": ["O aplicativo fecha sozinho ao abrir", "Não consigo enviar arquivos, dá erro 500",
                  "A página de relatórios não carrega", "O sistema está lento desde ontem"],
    "account": ["Esqueci minha senha e o e-mail não chega", "Quero trocar o e-mail da conta",
                "Como excluo meu perfil?", "Preciso adicionar um novo usuário na minha equipe"],
    "other": ["Vocês têm parceria para revendedores?", "Qual o horário de atendimento?",
              "Gostaria de elogiar o atendimento de ontem", "Onde encontro a política de privacidade?"],
}
URGENT = [" Preciso resolver hoje, é urgente!", " Não é urgente.", ""]
MONTHS = ["janeiro", "fevereiro", "março", "abril"]

tickets = []
for i in range(30):
    cat = list(TICKETS)[i % 4]
    text = rng.choice(TICKETS[cat]).format(m=rng.choice(MONTHS)) + rng.choice(URGENT)
    urg = "high" if "urgente!" in text else ("low" if "Não é urgente" in text else "medium")
    tickets.append({"text": text, "category": cat, "urgency": urg})

VENDORS = ["Padaria Pão Quente", "Mercado Boa Compra", "Acme Cloud Inc.", "Oficina do Zé", "Papelaria Central"]
invoices = []
for _ in range(15):
    v, d, m = rng.choice(VENDORS), rng.randint(1, 28), rng.randint(1, 12)
    total = f"{rng.uniform(40, 3000):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    invoices.append(f"NF {rng.randint(1000, 9999)} - {v} - emitida em {d:02d}/{m:02d}/2026 - "
                    f"valor total R$ {total}")

TOPICS = ["migração do banco de dados", "campanha de lançamento", "reestruturação do suporte",
          "auditoria de segurança", "contratação de novos analistas"]
NAMES = ["Ana", "Beto", "Carla", "Diego"]
docs = []
for t in TOPICS * 2:
    a, b = rng.sample(NAMES, 2)
    docs.append(f"Na reunião de hoje discutimos a {t}. O prazo ficou para o fim do mês. "
                f"{a} vai preparar o levantamento inicial e {b} ficou de agendar a próxima rodada com o time. "
                f"Também foi lembrado que o orçamento ainda precisa de aprovação da diretoria.")

for name, data in [("tickets", tickets), ("invoices", invoices), ("docs", docs)]:
    (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok")
