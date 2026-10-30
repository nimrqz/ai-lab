import re

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum)\b", re.I)


def validate_select(sql):
    cleaned = sql.strip().rstrip(";").strip()
    if ";" in cleaned:
        raise ValueError("apenas uma instrução é permitida")
    if not re.match(r"^(select|with)\b", cleaned, re.I):
        raise ValueError("apenas SELECT é permitido")
    if FORBIDDEN.search(cleaned):
        raise ValueError("comando proibido na consulta")
    return cleaned
