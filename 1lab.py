from dataclasses import dataclass
from datetime import datetime
import sys

@dataclass
class CurrencyRates:
    color: str
    currency_name_1: str
    currency_name_2: str
    rate: float
    date: datetime.date



    def __str__(self):
        return (f"Цвет связки {self.color} и курс валюты {self.currency_name_1} к {self.currency_name_2} на дату {self.date} составляет {self.rate}")

def main():
    if len(sys.argv) != 6:
        print("python 1lab.py цвет валюта1 валюта2 курс гггг.мм.дд")
        return
    color = sys.argv[1]
    currency1 = sys.argv[2]
    currency2 = sys.argv[3]
    rate = float(sys.argv[4])
    date = datetime.strptime(sys.argv[5], "%Y.%m.%d").date()

    obj = CurrencyRates(color, currency1, currency2, rate, date)
    print("Создан объект:")
    print(obj)

if __name__ == "__main__":
    main()