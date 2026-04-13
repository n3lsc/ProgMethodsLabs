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
    pass


class ValidationError(Exception):
    pass


class CurrencyModel:

    def __init__(self):
        self.data: List[CurrencyRates] = []

    # ---------- PARSE ----------
    def parse(self, line: str) -> CurrencyRates:
        parts = line.strip().split()

        if len(parts) != 5:
            raise ParseError(f"Неверный формат строки: {line}")

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

    # ---------- LOAD ----------
    def load(self, filename: str):
        self.data.clear()

        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        obj = self.parse(line)
                        self.data.append(obj)
                    except ParseError as e:
                        logging.warning(str(e))
        except FileNotFoundError:
            logging.warning("Файл данных не найден")

    # ---------- SAVE ----------
    def save(self, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            for obj in self.data:
                file.write(f"{obj.color} {obj.currency_name_1} "
                           f"{obj.currency_name_2} {obj.rate} "
                           f"{obj.date.strftime(DATE_FORMAT)}\n")

    # ---------- ADD ----------
    def add(self, color, c1, c2, rate_str, date_str):
        try:
            rate = float(rate_str)
            date = datetime.strptime(date_str, DATE_FORMAT).date()

            obj = CurrencyRates(color, c1, c2, rate, date)
            self.data.append(obj)

            return obj

        except Exception as e:
            logging.error(
                f"Ошибка добавления: {color}, {c1}, {c2}, {rate_str}, {date_str}"
            )
            raise ValidationError("Некорректные данные") from e

    # ---------- DELETE ----------
    def delete(self, index: int):
        try:
            del self.data[index]
        except IndexError as e:
            logging.error(f"Ошибка удаления, индекс: {index}")
            raise ValidationError("Некорректный индекс") from e
