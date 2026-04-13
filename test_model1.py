import pytest
from model import parse_currency_rate, ParseError


def test_valid_line():
    line = "red USD EUR 0.92 2024.05.12"
    obj = parse_currency_rate(line)

    assert obj.color == "red"
    assert obj.currency_name_1 == "USD"
    assert obj.rate == 0.92


def test_invalid_rate():
    line = "red USD EUR abc 2024.05.12"

    with pytest.raises(ParseError):
        parse_currency_rate(line)


def test_invalid_date():
    line = "red USD EUR 0.92 wrong"

    with pytest.raises(ParseError):
        parse_currency_rate(line)


def test_invalid_format():
    line = "bad data"

    with pytest.raises(ParseError):
        parse_currency_rate(line)
