from tkinter import ttk

TITLE = "Kiểm tra hồ sơ"

from . import kiemtrahosocu, kiemtrahosodangnamvien
from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan

class App(ttk.Notebook):
    def __init__(self):
        super().__init__()
        self.add(kiemtrahosocu.App(), text=kiemtrahosocu.TITLE)
        self.add(kiemtrahosodangnamvien.App(), text=kiemtrahosodangnamvien.TITLE)
