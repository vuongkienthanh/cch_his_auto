import tkinter as tk
from typing import cast

from .config import DutruMau

from cch_his_auto.common_ui.item_listframe import ScrollList, ScrollItem


class DutruMauFrame(tk.LabelFrame):
    type Item = DutruMau

    def __init__(self, parent):
        super().__init__(parent, text="Dự trù máu")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        header = tk.Frame(self)
        columnconfigure(header)
        header.grid(row=0, column=0, sticky="WE", padx=(0, 15), pady=(15, 0))
        headers = [
            "url",
            "dppt",
            "nhom1",
            "date",
            "đã TM",
            "KT BT",
            "PỨ TM",
            "HCT",
            "CX",
            "cùng nhóm",
            "Xóa",
        ]
        for i, h in enumerate(headers):
            w = tk.Label(header, text=h, relief="raised", anchor="center")
            w.grid(row=0, column=i, sticky="NSEW")

        w = tk.Button(self, text="+", command=self.add_new, background="#d4a5ab")
        w.grid(row=0, column=1, sticky="NSEW")
        self.listframe = ScrollList(self)
        self.listframe.grid_propagate(False)
        self.listframe.configure(height=100)
        self.listframe.grid(row=1, column=0, sticky="NSEW")

    def add_new(self):
        self.listframe.add_new(Line)

    def add_item(self, item: Item):
        line = self.listframe.add_new(Line)
        line.set_item(item)

    def get_items(self) -> list[Item]:
        return self.listframe.get_items()

    def clear(self):
        self.listframe.clear()


class Line(ScrollItem):
    def __init__(self, parent):
        super().__init__(parent)
        columnconfigure(self)
        self.url_var = tk.StringVar()
        self.note_var = tk.StringVar()

        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, sticky="WE")
        info_frame.columnconfigure(1, weight=1)
        tk.Entry(info_frame, textvariable=self.url_var).grid(
            row=0, column=0, sticky="WE", columnspan=2
        )
        tk.Label(info_frame, text="note").grid(row=1, column=0)
        tk.Entry(info_frame, textvariable=self.note_var).grid(
            row=1, column=1, sticky="WE"
        )

        self.duphongphauthuat = tk.BooleanVar()
        self.nhom1 = tk.BooleanVar()
        self.date = tk.StringVar()
        self.datruyenmau = tk.BooleanVar()
        self.khangthebatthuong = tk.BooleanVar()
        self.phanungtruyenmau = tk.BooleanVar()
        self.hcthientai = tk.StringVar()
        self.truyenmaucochieuxa = tk.BooleanVar()
        self.cungnhom = tk.BooleanVar()

        for i, v in zip(
            [1, 2, 4, 5, 6, 8, 9],
            [
                self.duphongphauthuat,
                self.nhom1,
                self.datruyenmau,
                self.khangthebatthuong,
                self.phanungtruyenmau,
                self.truyenmaucochieuxa,
                self.cungnhom,
            ],
        ):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

        date = tk.Entry(self, textvariable=self.date, width=9)
        date.grid(row=0, column=3)
        hct = tk.Entry(self, textvariable=self.hcthientai, width=4)
        hct.grid(row=0, column=7)

        self.duphongphauthuat.set(True)
        self.nhom1.set(True)
        self.cungnhom.set(True)

        del_btn = tk.Button(self, text="Xóa", command=self.destroy)
        del_btn.grid(row=0, column=10)

    def set_item(self, item: DutruMau):
        self.url_var.set(item["url"])
        self.note_var.set(item["note"])
        self.duphongphauthuat.set(item["duphongphauthuat"])
        self.nhom1.set(item["nhom1"])
        self.date.set(item["date"])
        self.datruyenmau.set(item["datruyenmau"])
        self.khangthebatthuong.set(item["khangthebatthuong"])
        self.phanungtruyenmau.set(item["phanungtruyenmau"])
        self.hcthientai.set(item["hcthientai"])
        self.truyenmaucochieuxa.set(item["truyenmaucochieuxa"])
        self.cungnhom.set(item["cungnhom"])

    def get_item(self) -> DutruMau:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "duphongphauthuat": self.duphongphauthuat.get(),
            "nhom1": self.nhom1.get(),
            "date": self.date.get(),
            "datruyenmau": self.datruyenmau.get(),
            "khangthebatthuong": self.khangthebatthuong.get(),
            "phanungtruyenmau": self.phanungtruyenmau.get(),
            "hcthientai": self.hcthientai.get(),
            "truyenmaucochieuxa": self.truyenmaucochieuxa.get(),
            "cungnhom": self.cungnhom.get(),
        }


def columnconfigure(w: tk.Widget):
    w.columnconfigure(0, weight=1, minsize=200)
    for i in [1, 2, 4, 5, 6, 7, 8, 9, 10]:
        w.columnconfigure(i, minsize=80)
    w.columnconfigure(3, minsize=100)
