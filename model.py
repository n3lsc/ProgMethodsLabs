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

    # ---------- COMMANDS ----------
    def process_commands(self, filename):
        """Process a commands file containing lines:
        ADD <csv fields>
        REM <condition>
        SAVE <filename>

        - ADD: CSV fields (semicolon or comma separated) matching
          color, currency_name_1, currency_name_2, rate, date
        - REM: simple condition like "rate < 1.0" or "currency_name_1 == USD"
        - SAVE: path to save current data
        """

        def parse_add_args(arg_str: str):
            sep = ";" if ";" in arg_str else ","
            parts = [p.strip() for p in arg_str.split(sep)]
            if len(parts) != 5:
                raise ValidationError(f"ADD ожидает 5 полей: {arg_str}")
            return parts

        def eval_condition(obj, field: str, op: str, value: str) -> bool:
            # get attribute
            if not hasattr(obj, field):
                raise ValidationError(f"Неизвестное поле в REM: {field}")

            left = getattr(obj, field)

            # try to coerce numeric
            try:
                right = float(value)
                left_val = float(left)
            except Exception:
                right = value.strip("'\"")
                left_val = str(left)

            if op == "==":
                return left_val == right
            if op == "!=":
                return left_val != right
            if op == "<":
                return left_val < right
            if op == "<=":
                return left_val <= right
            if op == ">":
                return left_val > right
            if op == ">=":
                return left_val >= right

            raise ValidationError(f"Неизвестный оператор в REM: {op}")

        import pathlib

        path = pathlib.Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"Commands file not found: {filename}")

        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                # split command and argument
                if " " not in line:
                    continue
                cmd, arg = line.split(" ", 1)
                cmd = cmd.upper()

                if cmd == "ADD":
                    parts = parse_add_args(arg)
                    # add expects: color, c1, c2, rate_str, date_str
                    self.add(parts[0], parts[1], parts[2], parts[3], parts[4])

                elif cmd == "REM":
                    # simple parser: field op value
                    tokens = arg.split()
                    if len(tokens) < 3:
                        raise ValidationError(f"Неверный REM: {arg}")

                    field = tokens[0]
                    op = tokens[1]
                    value = " ".join(tokens[2:])

                    # filter out matching
                    new_data = []
                    for obj in self.data:
                        try:
                            match = eval_condition(obj, field, op, value)
                        except ValidationError:
                            match = False

                        if not match:
                            new_data.append(obj)

                    self.data = new_data

                elif cmd == "SAVE":
                    # arg is filename
                    out = arg.strip()
                    self.save(out)

                else:
                    logging.warning(f"Unknown command in commands file: {cmd}")
