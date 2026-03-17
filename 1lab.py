from dataclasses import dataclass
from datetime import datetime
from typing import List

import os

import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame

DATE_FORMAT = "%Y.%m.%d"
DATA_FILE = "data.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "html", "help.html")


@dataclass
class CurrencyRates:
    """Represents a currency rate object."""
    color: str
    currency_name_1: str
    currency_name_2: str
    rate: float
    date: datetime.date


def parse_currency_rate(line: str) -> CurrencyRates:
    parts = line.strip().split()

    return CurrencyRates(
        parts[0],
        parts[1],
        parts[2],
        float(parts[3]),
        datetime.strptime(parts[4], DATE_FORMAT).date(),
    )


def load_currency_rates(filename: str) -> List[CurrencyRates]:
    rates = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            rates.append(parse_currency_rate(line))
    return rates


def save_currency_rates(filename: str, data: List[CurrencyRates]):
    with open(filename, "w", encoding="utf-8") as file:
        for obj in data:
            file.write(f"{obj.color} {obj.currency_name_1} "
                       f"{obj.currency_name_2} {obj.rate} "
                       f"{obj.date.strftime(DATE_FORMAT)}\n")


class CurrencyApp:
    """Window for working with data."""

    def __init__(self, root: tk.Tk, data: List[CurrencyRates], back_callback):
        self.root = root
        self.data = data
        self.back_callback = back_callback
        self.root.minsize(600, 400)
        self.root.title("Работа с данными")

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
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
        tk.Button(frame, text="Назад", command=self.go_back).pack(side=tk.LEFT,
                                                                  padx=5)

    def populate_table(self):
        for obj in self.data:
            self.tree.insert(
                "",
                tk.END,
                values=(obj.color, obj.currency_name_1, obj.currency_name_2,
                        obj.rate, obj.date),
            )

    def add_item(self):
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
        selected = self.tree.selection()

        for item in selected:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.data[index]

        save_currency_rates(DATA_FILE, self.data)

    def go_back(self):
        self.root.destroy()
        self.back_callback()


class HelpWindow:
    """Help window with HTML support."""

    def __init__(self, root: tk.Tk, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.root.title("Справка")
        self.root.minsize(600, 500)

        self.create_widgets()

    def create_widgets(self):
        self.html_frame = HtmlFrame(self.root)
        self.html_frame.pack(fill=tk.BOTH, expand=True)
        self.html_frame.load_file(f"file//{FILE_PATH}")

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, pady=5)

        tk.Button(bottom_frame, text="Назад",
                  command=self.go_back).pack(pady=5)

    def go_back(self):
        self.root.destroy()
        self.back_callback()


class MainMenu:
    """Main menu window."""

    def __init__(self, root: tk.Tk, data: List[CurrencyRates]):
        self.root = root
        self.data = data

        self.root.title("Главное меню")
        self.root.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Работать", width=20,
                  command=self.open_work).pack(pady=10)

        tk.Button(self.root, text="Справка", width=20,
                  command=self.open_help).pack(pady=10)

        tk.Button(self.root, text="Выход", width=20,
                  command=self.root.quit).pack(pady=10)

    def open_work(self):
        self.root.destroy()
        new_root = tk.Tk()
        CurrencyApp(new_root, self.data, self.restart)
        new_root.mainloop()

    def open_help(self):
        self.root.destroy()
        new_root = tk.Tk()
        HelpWindow(new_root, self.restart)
        new_root.mainloop()

    def restart(self):
        new_root = tk.Tk()
        MainMenu(new_root, self.data)
        new_root.mainloop()


def main():
    data = load_currency_rates(DATA_FILE)

    root = tk.Tk()
    MainMenu(root, data)
    root.mainloop()


if __name__ == "__main__":
    #print(os.getcwd())
    main()
