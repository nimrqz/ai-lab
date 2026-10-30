import pytest
from ailab.prompts import load_template, render, VARIANTS


def test_variants_differ():
    tpl = load_template("triage")
    zero, few, cot = (render(tpl, "meu pix falhou", v) for v in VARIANTS)
    assert "meu pix falhou" in zero
    assert "Exemplo" not in zero and "Exemplo 1" in few
    assert "reasoning" in cot and "reasoning" not in zero


def test_unknown_variant():
    with pytest.raises(ValueError):
        render(load_template("triage"), "x", "nope")


@pytest.mark.parametrize("name", ["triage", "extract", "summarize"])
def test_templates_have_required_keys(name):
    tpl = load_template(name)
    assert {"role", "instructions", "output_format", "examples"} <= tpl.keys()
