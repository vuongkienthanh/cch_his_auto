import tkinter as tk
from tkinter import ttk
from typing import cast

from cch_his_auto.app import kiemtrahoso, khambenhmoingay


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tự động hóa HIS")
        self.bind_class(
            "Entry",
            "<Control-a>",
            lambda e: cast(tk.Entry, e.widget).select_range(0, "end"),
        )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        nb = ttk.Notebook(self)
        nb.grid(row=0, column=0, sticky="NSEW")

        for m in [khambenhmoingay, kiemtrahoso]:
            nb.add(m.App(), text=m.TITLE, sticky="NSEW")


def run():
    MainApp().mainloop()


if __name__ == "__main__":
    run()
