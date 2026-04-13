import tkinter as tk

from model import CurrencyModel
from view import MainMenu

DATA_FILE = "data.txt"


def main():
    model = CurrencyModel()
    model.load(DATA_FILE)

    root = tk.Tk()
    MainMenu(root, model)
    root.mainloop()


if __name__ == "__main__":
    main()
