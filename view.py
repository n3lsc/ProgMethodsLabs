import tkinter as tk
import os

from tkinter import ttk, messagebox, filedialog
from tkinterweb import HtmlFrame

from model import CurrencyModel

DATA_FILE = "data.txt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "html", "help.html")


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

    def __init__(self, root: tk.Tk, model):
        self.root = root
        self.model = model

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
        CurrencyApp(new_root, self.model)
        new_root.mainloop()

    def open_help(self):
        self.root.destroy()
        new_root = tk.Tk()
        HelpWindow(new_root, self.restart)
        new_root.mainloop()

    def restart(self):
        new_root = tk.Tk()
        MainMenu(new_root, self.model)
        new_root.mainloop()


class CurrencyApp:

    def __init__(self, root: tk.Tk, model: CurrencyModel):
        self.root = root
        self.model = model

        self.root.title("Currency Rates")
        self.root.minsize(600, 400)

        self.create_widgets()
        self.populate_table()

    # ---------- UI ----------
    def create_widgets(self):
        self.tree = ttk.Treeview(
            self.root,
            columns=("Color", "Currency1", "Currency2", "Rate", "Date",
                     "Comment"),
            show="headings",
        )

        for col in ("Color", "Currency1", "Currency2", "Rate", "Date",
                    "Comment"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Add", command=self.add_item).pack(side=tk.LEFT,
                                                                 padx=5)
        tk.Button(frame, text="Delete",
                  command=self.delete_item).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Run Commands",
                  command=self.run_commands_file).pack(side=tk.LEFT, padx=5)

    # ---------- TABLE ----------
    def populate_table(self):
        # clear existing
        for child in self.tree.get_children():
            self.tree.delete(child)

        for obj in self.model.data:
            self.tree.insert(
                "",
                tk.END,
                values=(obj.color, obj.currency_name_1, obj.currency_name_2,
                        obj.rate, obj.date, getattr(obj, "comment", "")),
            )

    def run_commands_file(self):
        path = filedialog.askopenfilename(
            title="Open commands file",
            filetypes=[("Text files", "*.txt"), ("All files", "*")],
        )

        if not path:
            return

        try:
            self.model.process_commands(path)
            self.populate_table()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------- ADD ----------
    def add_item(self):
        window = tk.Toplevel(self.root)
        window.title("Add")

        labels = ["Color", "Currency1", "Currency2", "Rate", "Date YYYY.MM.DD"]
        labels = [
            "Color", "Currency1", "Currency2", "Rate", "Date YYYY.MM.DD",
            "Comment"
        ]
        entries = []

        for i, text in enumerate(labels):
            tk.Label(window, text=text).grid(row=i, column=0)
            entry = tk.Entry(window)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def save():
            try:
                obj = self.model.add(
                    entries[0].get(),
                    entries[1].get(),
                    entries[2].get(),
                    entries[3].get(),
                    entries[4].get(),
                    entries[5].get() if len(entries) > 5 else "",
                )

                self.tree.insert(
                    "",
                    tk.END,
                    values=(obj.color, obj.currency_name_1,
                            obj.currency_name_2, obj.rate, obj.date,
                            getattr(obj, "comment", "")),
                )

                self.model.save(DATA_FILE)
                window.destroy()

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        tk.Button(window, text="Save", command=save).grid(row=5, columnspan=2)

    # ---------- DELETE ----------
    def delete_item(self):
        selected = self.tree.selection()

        for item in selected:
            try:
                index = self.tree.index(item)

                self.model.delete(index)
                self.tree.delete(item)

                self.model.save(DATA_FILE)

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
