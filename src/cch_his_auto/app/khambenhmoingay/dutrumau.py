import tkinter as tk
from typing import cast

from .config import DutruMau

from cch_his_auto.common_ui.item_listframe import ListItem
from .more_listframe import MoreListFrame

HEADER_STATS = [
    ("url", 200, 1),
    ("dppt", 80, 0),
    ("nhom1", 100, 0),
    ("date", 80, 0),
    ("đã TM", 80, 0),
    ("KT BT", 80, 0),
    ("PỨ TM", 80, 0),
    ("HCT", 80, 0),
    ("CX", 80, 0),
    ("cùng nhóm", 80, 0),
    ("Xóa", 80, 0),
]
type Item = DutruMau


class Frame(MoreListFrame):
    def __init__(self, parent):
        super().__init__(parent, Line, header_stats=HEADER_STATS)

    def get_title(self) -> str:
        return f"Dự trù máu ({self.count()})"


class Line(ListItem):
    def __init__(self, parent, column_stats):
        super().__init__(parent, column_stats)
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

        del_btn = tk.Button(self, text="Xóa", command=self.on_del)
        del_btn.grid(row=0, column=10)

    def on_del(self):
        tab_frame = self.master.master.master.master  # pyright: ignore
        self.destroy()
        cast(Frame, tab_frame).change_tab_text()

    def set_item(self, item: Item):
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

    def get_item(self) -> Item:
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
