import tkinter as tk
from typing import cast

from .config import BBHC

from cch_his_auto.common_ui.item_listframe import ListItem
from .more_listframe import MoreListFrame

HEADER_STATS = [("url", 200, 1), ("khac", 200, 2), ("Xóa", 80, 0)]
type Item = BBHC


class Frame(MoreListFrame):
    def __init__(self, parent):
        super().__init__(parent, Line, header_stats=HEADER_STATS)

    def get_title(self) -> str:
        return f"Biên bản hội chẩn ({self.count()})"


class Line(ListItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        self.khac_var = tk.StringVar()
        tk.Entry(self, textvariable=self.khac_var).grid(row=0, column=1, sticky="WE")

        del_btn = tk.Button(self, text="Xóa", command=self.on_del)
        del_btn.grid(row=0, column=2)

    def on_del(self):
        tab_frame = self.master.master.master.master  # pyright: ignore
        self.destroy()
        cast(Frame, tab_frame).change_tab_text()

    def set_item(self, item: Item):
        self.url_var.set(item["url"])
        self.note_var.set(item["note"])
        self.khac_var.set(item["khac"])

    def get_item(self) -> Item:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "khac": self.khac_var.get(),
        }
