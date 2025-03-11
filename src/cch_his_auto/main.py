import tkinter as tk
from tkinter import ttk
from typing import cast
from cch_his_auto.app import kytodieutrihangngay
from cch_his_auto.app import kiemtrahosocu

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tự động hóa HIS")
        self.bind_class(
            "Entry",
            "<Control-a>",
            lambda e: cast(tk.Entry, e.widget).select_range(0, "end"),
        )

        nb = ttk.Notebook(self)
        nb.pack(fill="both")
        nb.add(kytodieutrihangngay.App(), text=kytodieutrihangngay.TITLE)
        nb.add(kiemtrahosocu.App(), text=kiemtrahosocu.TITLE, sticky="NSEW")

MainApp().mainloop()
