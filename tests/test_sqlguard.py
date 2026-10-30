import pytest
from ailab.sqlguard import validate_select


def test_accepts_select_and_strips_semicolon():
    assert validate_select("SELECT 1;") == "SELECT 1"


@pytest.mark.parametrize("sql", [
    "DROP TABLE runs", "SELECT 1; DROP TABLE runs", "DELETE FROM runs",
    "UPDATE runs SET ok=0", "PRAGMA table_info(runs)", "select * from runs; select 2",
])
def test_rejects_dangerous(sql):
    with pytest.raises(ValueError):
        validate_select(sql)
