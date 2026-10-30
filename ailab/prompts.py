from pathlib import Path
import yaml

TEMPLATES_DIR = Path(__file__).parent / "templates"
VARIANTS = ("zero_shot", "few_shot", "cot")


def load_template(name):
    return yaml.safe_load((TEMPLATES_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def render(tpl, text, variant="few_shot"):
    if variant not in VARIANTS:
        raise ValueError(f"variante desconhecida: {variant}")
    parts = [tpl["role"], tpl["instructions"],
             "Formato de saída (JSON): " + tpl["output_format"]]
    if variant == "few_shot":
        for i, ex in enumerate(tpl["examples"], 1):
            parts.append(f"Exemplo {i}\nEntrada: {ex['input']}\nSaída: {ex['output']}")
    if variant == "cot":
        parts.append('Inclua no JSON um campo "reasoning" com um raciocínio curto antes de decidir.')
    parts.append(f"Entrada: {text}\nSaída:")
    return "\n\n".join(parts)
