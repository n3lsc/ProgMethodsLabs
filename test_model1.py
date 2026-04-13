import pytest
from model import CurrencyModel, ParseError, ValidationError

# ---------- PARSE ----------


def test_parse_valid():
    model = CurrencyModel()
    line = "red USD EUR 0.92 2024.05.12"

    obj = model.parse(line)

    assert obj.color == "red"
    assert obj.currency_name_1 == "USD"
    assert obj.rate == 0.92


@pytest.mark.parametrize(
    "line",
    ["bad data", "red USD EUR abc 2024.05.12", "red USD EUR 0.92 wrongdate"])
def test_parse_invalid(line):
    model = CurrencyModel()

    with pytest.raises(ParseError):
        model.parse(line)


# ---------- ADD ----------


def test_add_valid():
    model = CurrencyModel()

    obj = model.add("red", "USD", "EUR", "0.92", "2024.05.12")

    assert len(model.data) == 1
    assert obj.rate == 0.92


def test_add_invalid():
    model = CurrencyModel()

    with pytest.raises(ValidationError):
        model.add("red", "USD", "EUR", "abc", "2024.05.12")


# ---------- DELETE ----------


def test_delete_valid():
    model = CurrencyModel()
    model.add("red", "USD", "EUR", "0.92", "2024.05.12")

    model.delete(0)

    assert len(model.data) == 0


def test_delete_invalid():
    model = CurrencyModel()

    with pytest.raises(ValidationError):
        model.delete(10)


# ---------- LOAD ----------


def test_load_with_invalid_lines(tmp_path):
    file = tmp_path / "data.txt"

    file.write_text("red USD EUR 0.92 2024.05.12\n"
                    "bad line\n"
                    "blue EUR USD abc 2024.05.12\n")

    model = CurrencyModel()
    model.load(file)

    # только одна валидная строка
    assert len(model.data) == 1


# ---------- SAVE ----------


def test_save(tmp_path):
    file = tmp_path / "data.txt"

    model = CurrencyModel()
    model.add("red", "USD", "EUR", "0.92", "2024.05.12")

    model.save(file)

    content = file.read_text()

    assert "red USD EUR 0.92 2024.05.12" in content
