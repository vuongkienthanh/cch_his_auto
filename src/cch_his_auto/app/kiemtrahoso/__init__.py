from tkinter import ttk

TITLE = "Kiểm tra hồ sơ"

from . import kiemtrahosocu, kiemtrahosodangnamvien

class App(ttk.Notebook):
    def __init__(self):
        super().__init__()
        self.add(kiemtrahosodangnamvien.App(), text=kiemtrahosodangnamvien.TITLE)
        self.add(kiemtrahosocu.App(), text=kiemtrahosocu.TITLE)
