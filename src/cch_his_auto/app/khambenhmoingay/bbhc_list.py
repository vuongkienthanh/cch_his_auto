import tkinter as tk

from .config import BBHC

from cch_his_auto.common_ui.item_listframe import ScrollItem, ScrollList


class BBHCFrame(tk.LabelFrame):
    type Item = BBHC

    def __init__(self, parent):
        super().__init__(parent, text="Biên bản hội chẩn")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        header = tk.Frame(self)
        columnconfigure(header)
        header.grid(row=0, column=0, sticky="WE", padx=(0, 15), pady=(15, 0))
        headers = ["url", "khac", "Xóa"]
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

        self.khac_var = tk.StringVar()
        tk.Entry(self, textvariable=self.khac_var).grid(row=0, column=1)

        del_btn = tk.Button(self, text="Xóa", command=self.destroy)
        del_btn.grid(row=0, column=6)

    def set_item(self, item: BBHC):
        self.url_var.set(item["url"])
        self.note_var.set(item["note"])
        self.khac_var.set(item["khac"])

    def get_item(self) -> BBHC:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "khac": self.khac_var.get(),
        }


def columnconfigure(w: tk.Widget):
    w.columnconfigure(0, weight=1, minsize=200)
    w.columnconfigure(1, weight=2)
