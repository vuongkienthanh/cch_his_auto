"""
CT, MRI, du tru mau nên ký tay
"""

import tkinter as tk
from typing import cast


from cch_his_auto.common_ui.item_listframe import ListItem

from .tabbed_listframe import TabbedListFrame
from .config import Todieutri

HEADERS_STATS = [
    ("url", 200, 1),
    ("XN", 80, 0),
    ("tờ ĐT", 80, 0),
    ("Vị trí ký 3tra", 180, 0),
    ("Xóa", 80, 0),
]
type Item = Todieutri


class Line(ListItem):
    def __init__(self, parent):
        super().__init__(parent)
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

        self.xn_var = tk.BooleanVar()
        self.ct_var = tk.BooleanVar()
        self.mri_var = tk.BooleanVar()
        self.tdt_var = tk.BooleanVar()

        for i, v in enumerate(
            [self.xn_var, self.ct_var, self.mri_var, self.tdt_var], 1
        ):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

        self.tdt_var.set(True)

        k3t = tk.Frame(self, borderwidth=10)
        k3t.grid(row=0, column=5)
        self.k3t_bs = Ky3Tra(k3t, text="Bác sĩ")
        self.k3t_dd = Ky3Tra(k3t, text="Điều dưỡng")
        self.k3t_bn = Ky3Tra(k3t, text="Bệnh nhân")
        self.k3t_bs.grid(row=0, column=0)
        self.k3t_dd.grid(row=1, column=0)
        self.k3t_bn.grid(row=2, column=0)

        del_btn = tk.Button(self, text="Xóa", command=self.on_del)
        del_btn.grid(row=0, column=6)

    def on_del(self):
        tab_frame = self.master.master.master.master  # pyright: ignore
        self.destroy()
        cast(TabbedListFrame, tab_frame).change_tab_text()

    def set_item(self, item: Item):
        self.url_var.set(item["url"])
        self.note_var.set(item["note"])
        self.xn_var.set(item["ky_xn"])
        self.tdt_var.set(item["ky_todieutri"])
        self.k3t_bs.set_vitri(item["ky_3tra"]["bacsi"])
        self.k3t_dd.set_vitri(item["ky_3tra"]["dieuduong"])
        self.k3t_bn.set_vitri(item["ky_3tra"]["benhnhan"])

    def get_item(self) -> Item:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "ky_xn": self.xn_var.get(),
            "ky_todieutri": self.tdt_var.get(),
            "ky_3tra": {
                "bacsi": self.k3t_bs.get_vitri(),
                "dieuduong": self.k3t_dd.get_vitri(),
                "benhnhan": self.k3t_bn.get_vitri(),
            },
        }


class Ky3Tra(tk.LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
        self.v0 = tk.BooleanVar()
        self.v1 = tk.BooleanVar()
        self.v2 = tk.BooleanVar()
        self.v3 = tk.BooleanVar()
        self.v4 = tk.BooleanVar()
        for i, v in enumerate([self.v0, self.v1, self.v2, self.v3, self.v4]):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

    def get_vitri(self) -> tuple[bool, bool, bool, bool, bool]:
        return (
            self.v0.get(),
            self.v1.get(),
            self.v2.get(),
            self.v3.get(),
            self.v4.get(),
        )

    def set_vitri(self, v: tuple[bool, bool, bool, bool, bool]):
        self.v0.set(v[0])
        self.v1.set(v[1])
        self.v2.set(v[2])
        self.v3.set(v[3])
        self.v4.set(v[4])
