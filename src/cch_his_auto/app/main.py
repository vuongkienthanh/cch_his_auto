import tkinter as tk
from tkinter import ttk
from typing import cast

from cch_his_auto.app import kytodieutrihangngay
from cch_his_auto.app import kiemtrahoso

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
        h = self.winfo_height()
        w = self.winfo_width()
        self.geometry(f"{w * 1200}x{h * 900}")
        nb = ttk.Notebook(self)
        nb.grid(row=0, column=0, sticky="NSEW")
        nb.add(kytodieutrihangngay.App(), text=kytodieutrihangngay.TITLE, sticky="NSEW")
        nb.add(kiemtrahoso.App(), text=kiemtrahoso.TITLE, sticky="NSEW")

if __name__ == "__main__":
    MainApp().mainloop()
