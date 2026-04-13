from dataclasses import dataclass
from datetime import datetime
from typing import List
import logging

DATE_FORMAT = "%Y.%m.%d"

logging.basicConfig(filename="app.log",
                    level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(message)s")


@dataclass
class CurrencyRates:
    color: str
    currency_name_1: str
    currency_name_2: str
    rate: float
    date: datetime.date


class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass


def parse_currency_rate(line: str) -> CurrencyRates:
    parts = line.strip().split()

    if len(parts) != 5:
        raise ParseError(f"Неверное количество полей: {line}")

    try:
        return CurrencyRates(
            parts[0],
            parts[1],
            parts[2],
            float(parts[3]),
            datetime.strptime(parts[4], DATE_FORMAT).date(),
        )
    except Exception as e:
        raise ParseError(f"Ошибка парсинга строки: {line}") from e


def load_currency_rates(filename: str) -> List[CurrencyRates]:
    rates = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            try:
                obj = parse_currency_rate(line)
                rates.append(obj)
            except ParseError as e:
                logging.warning(str(e))  # логируем
                continue  # пропускаем строку

    return rates
