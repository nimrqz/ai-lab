import time
from dataclasses import dataclass
from pydantic import BaseModel, ValidationError
from ailab.llm import generate, DEFAULT_MODEL


@dataclass
class StructuredResult:
    obj: BaseModel | None
    ok: bool
    attempts: int
    seconds: float
    error: str | None = None


def run_structured(prompt, schema, model=DEFAULT_MODEL, retries=2, llm=generate):
    start, current, error = time.perf_counter(), prompt, None
    for attempt in range(1, retries + 2):
        raw = llm(current, model=model, json_mode=True)
        try:
            obj = schema.model_validate_json(raw)
            return StructuredResult(obj, True, attempt, time.perf_counter() - start)
        except ValidationError as e:
            error = str(e)
            current = (f"{prompt}\n\nSua resposta anterior foi inválida:\n{raw}\n"
                       f"Erro: {error}\nCorrija e responda apenas com JSON válido.")
    return StructuredResult(None, False, retries + 1, time.perf_counter() - start, error)
