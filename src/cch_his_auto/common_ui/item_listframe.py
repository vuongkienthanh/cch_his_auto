"""
Example:

```
from typing import TypedDict

class Patient(TypedDict):
    url: str
    sign_this: bool

type Item = Patient
type Size = int
type Weight = int

HEADERS_STATS = [
    ("url", 200, 1),
    ("sign this", 80, 0),
    ("Xóa", 80, 0),
]

class Frame(ListFrame):
    def get_sizes(self) -> list[tuple[str, Size, Weight]]:
        return HEADERS_STATS

    def add_new(self):
        self.add(Line)

    def add_item(self, item: Item):
        line = self.add(Line)
        line.set_item(item)

class Line(ListItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.url_var = tk.StringVar()
        self.this_var = tk.BooleanVar()

        tk.Entry(self, textvariable=self.url_var).grid(row=0, column=0, sticky="WE")
        tk.Checkbutton(self, variable=self.this_var).grid(row=0, column=1)

        del_btn = tk.Button(self, text="Xóa", command=self.destroy)
        del_btn.grid(row=0, column=3)

    def get_sizes(self) -> list[tuple[Size, Weight]]:
        return list(map(lambda x: (x[1], x[2]), HEADERS_STATS))

    def set_item(self, item: Item):
        self.url_var.set(item["url"])
        self.this_var.set(item["sign_this"])

    def get_item(self) -> Item:
        return {
            "url": self.url_var.get(),
            "sign_this": self.this_var.get(),
        }
```
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import cast
from cch_his_auto.common_ui.scrollable_frame import ScrollFrame

type Size = int
type Weight = int


class ListItem[T](tk.Frame, ABC):
    @abstractmethod
    def __init__(self, parent):
        "derive this and add more widgets"
        super().__init__(parent)
        for i, (width, weight) in enumerate(self.get_sizes()):
            self.columnconfigure(i, minsize=width, weight=weight)

    @abstractmethod
    def get_sizes(self) -> list[tuple[Size, Weight]]:
        "return minsize and weight for initialization"

    @abstractmethod
    def set_item(self, item: T):
        "set info from item"

    @abstractmethod
    def get_item(self) -> T:
        "return a dict with contained info"


class ListFrame[T](tk.Frame, ABC):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, *kwargs)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        headerframe = tk.Frame(self)
        for i, (header, width, weight) in enumerate(self.get_sizes()):
            headerframe.columnconfigure(i, minsize=width, weight=weight)
            w = tk.Label(headerframe, text=header, relief="raised", anchor="center")
            w.grid(row=0, column=i, sticky="NSEW")
        headerframe.grid(row=0, column=0, sticky="WE", padx=(0, 15), pady=(15, 0))
        w = tk.Button(self, text="+", command=self.add_new, background="#d4a5ab")
        w.grid(row=0, column=1, sticky="NSEW")
        w = tk.Button(self, text="x", command=self.clear, background="#d4a5ab")
        w.grid(row=1, column=1, sticky="N")
        self.listframe = ScrollFrame(self)
        self.listframe.viewPort.columnconfigure(0, weight=1)
        self.listframe.grid(row=1, column=0, sticky="NSEW")

    @abstractmethod
    def get_sizes(self) -> list[tuple[str, Size, Weight]]:
        "return header name, minsize and weight for initialization"

    @abstractmethod
    def add_new(self):
        "derive this and call add() inside"

    @abstractmethod
    def add_item(self, item: T):
        "derive this, call add() and setup widget inside"

    def add(self, _class: type[ListItem]) -> ListItem:
        "add a children with provided ListItem subclass"
        line = _class(self.listframe.viewPort)
        line.grid(row=len(self.listframe.viewPort.grid_slaves()), column=0, sticky="EW")
        return line

    def get_items(self) -> list[T]:
        "return all children as dicts"
        return [
            cast(ListItem, gs).get_item()
            for gs in self.listframe.viewPort.grid_slaves()[::-1]
        ]

    def count(self) -> int:
        "return children counts"
        return len(self.listframe.viewPort.grid_slaves())

    def clear(self):
        "destroy all children widgets"
        for w in self.listframe.viewPort.grid_slaves():
            w.destroy()
