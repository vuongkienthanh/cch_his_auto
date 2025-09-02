import tkinter as tk
from typing import cast
from cch_his_auto.common_ui.item_listframe import ListItem
from .tabbed_listframe import TabbedListFrame
from .config import Bienbanhoichan


HEADERS_STATS = [
    ("url", 200, 1),
    ("thư ký", 80, 0),
    ("trưởng khoa", 80, 0),
    ("thành viên khác", 120, 0),
    ("Khác note", 200, 0),
    ("Xóa", 80, 0),
]
type Item = Bienbanhoichan


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

        self.ky_thuky_var = tk.BooleanVar()
        self.ky_truongkhoa_var = tk.BooleanVar()
        self.kt_thanhvienkhac_var = tk.BooleanVar()
        self.khac_note_var = tk.StringVar()

        for i, v in enumerate(
            [
                self.ky_thuky_var,
                self.ky_truongkhoa_var,
                self.kt_thanhvienkhac_var,
            ],
            1,
        ):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

        tk.Entry(self, textvariable=self.khac_note_var).grid(row=0, column=4)

        del_btn = tk.Button(self, text="Xóa", command=self.on_del)
        del_btn.grid(row=0, column=5)

    def on_del(self):
        tab_frame = self.master.master.master.master  # pyright: ignore
        self.destroy()
        cast(TabbedListFrame, tab_frame).change_tab_text()

    def set_item(self, item: Item):
        self.url_var.set(item["url"])
        self.note_var.set(item["note"])
        self.ky_thuky_var.set(item["ky_thuky"])
        self.ky_truongkhoa_var.set(item["ky_truongkhoa"])
        self.kt_thanhvienkhac_var.set(item["ky_thanhvienkhac"])
        self.khac_note_var.set(item["khac_note"])

    def get_item(self) -> Item:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "ky_thuky": self.ky_thuky_var.get(),
            "ky_truongkhoa": self.ky_truongkhoa_var.get(),
            "ky_thanhvienkhac": self.kt_thanhvienkhac_var.get(),
            "khac_note": self.khac_note_var.get(),
        }
