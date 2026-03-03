from dataclasses import dataclass
from datetime import datetime
import sys

@dataclass
class CurrencyRates:
    currency_name_1: str
    currency_name_2: str
    rate: float
    date: datetime.date

    def __str__(self):
        return (f"Курс валюты {self.currency_name_1} к {self.currency_name_2} на дату {self.date} составляет {self.rate}")
    
def menu():
    print("===================================" \
          " Меню для управления курсами валют " \
          " 1. Добавить новый объект          " \
          " 2. Удалить существующий объект    " \
          "===================================")

def main():
    if len(sys.argv) != 5:
        print("python 1lab.py валюта1 валюта2 курс гггг.мм.дд")
        return
    currency1 = sys.argv[1]
    currency2 = sys.argv[2]
    rate = float(sys.argv[3])
    date = datetime.strptime(sys.argv[4], "%Y.%m.%d").date()

    obj = CurrencyRates(currency1, currency2, rate, date)
    print("Создан объект:")
    print(obj)

if __name__ == "__main__":
    main()