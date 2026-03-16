from dataclasses import dataclass

from datetime import datetime

import tkinter as tk
from tkinter import ttk

from typing import List

DATE_FORMAT = "%Y.%m.%d"
DATA_FILE = "data.txt"


@dataclass
class CurrencyRates:
    """Represents a currency rate object."""
    color: str
    currency_name_1: str
    currency_name_2: str
    rate: float
    date: datetime.date


def parse_currency_rate(line: str) -> CurrencyRates:
    """Convert a line from file into a CurrencyRates object."""
    parts = line.strip().split()

    color = parts[0]
    currency1 = parts[1]
    currency2 = parts[2]
    rate = float(parts[3])
    date = datetime.strptime(parts[4], DATE_FORMAT).date()

    return CurrencyRates(color, currency1, currency2, rate, date)


def load_currency_rates(filename: str) -> List[CurrencyRates]:
    """Load objects from file."""
    rates = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            rates.append(parse_currency_rate(line))

    return rates


def save_currency_rates(filename: str, data: List[CurrencyRates]):
    """Save objects to file."""
    with open(filename, "w", encoding="utf-8") as file:
        for obj in data:
            line = (f"{obj.color} "
                    f"{obj.currency_name_1} "
                    f"{obj.currency_name_2} "
                    f"{obj.rate} "
                    f"{obj.date.strftime(DATE_FORMAT)}\n")
            file.write(line)


class CurrencyApp:
    """GUI application."""

    def __init__(self, root: tk.Tk, data: List[CurrencyRates]):
        self.root = root
        self.data = data

        self.root.title("Currency Rates")

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        """Create interface widgets."""
        self.tree = ttk.Treeview(
            self.root,
            columns=("Color", "Currency1", "Currency2", "Rate", "Date"),
            show="headings",
        )

        for col in ("Color", "Currency1", "Currency2", "Rate", "Date"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Add", command=self.add_item).pack(side=tk.LEFT,
                                                                 padx=5)
        tk.Button(frame, text="Delete",
                  command=self.delete_item).pack(side=tk.LEFT, padx=5)

    def populate_table(self):
        """Display objects in table."""
        for obj in self.data:
            self.tree.insert(
                "",
                tk.END,
                values=(obj.color, obj.currency_name_1, obj.currency_name_2,
                        obj.rate, obj.date),
            )

    def add_item(self):
        """Open window to add new object."""
        window = tk.Toplevel(self.root)
        window.title("Add")

        labels = ["Color", "Currency1", "Currency2", "Rate", "Date YYYY.MM.DD"]
        entries = []

        for i, text in enumerate(labels):
            tk.Label(window, text=text).grid(row=i, column=0)
            entry = tk.Entry(window)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def save():
            obj = CurrencyRates(
                entries[0].get(),
                entries[1].get(),
                entries[2].get(),
                float(entries[3].get()),
                datetime.strptime(entries[4].get(), DATE_FORMAT).date(),
            )

            self.data.append(obj)

            self.tree.insert(
                "",
                tk.END,
                values=(obj.color, obj.currency_name_1, obj.currency_name_2,
                        obj.rate, obj.date),
            )

            save_currency_rates(DATA_FILE, self.data)

            window.destroy()

        tk.Button(window, text="Save", command=save).grid(row=5, columnspan=2)

    def delete_item(self):
        """Delete selected object."""
        selected = self.tree.selection()

        for item in selected:
            index = self.tree.index(item)

            self.tree.delete(item)
            del self.data[index]

        save_currency_rates(DATA_FILE, self.data)


def main():
    """Program entry point."""
    data = load_currency_rates(DATA_FILE)

    root = tk.Tk()
    app = CurrencyApp(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()
