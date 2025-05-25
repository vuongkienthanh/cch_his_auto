import tkinter as tk
from abc import ABC, abstractmethod
from typing import cast
from functools import cached_property

from cch_his_auto.common_ui.scrollable_frame import ScrollFrame

type Size = int
type Weight = int


class ListItem[T](tk.Frame, ABC):
    @abstractmethod
    def __init__(self, parent, column_stats: list[tuple[Size, Weight]]):
        "derive this and add more widgets"
        super().__init__(parent)
        for i, (width, weight) in enumerate(column_stats):
            self.columnconfigure(i, minsize=width, weight=weight)

    @abstractmethod
    def set_item(self, item: T):
        "set info from item"

    @abstractmethod
    def get_item(self) -> T:
        "return a dict with contained info"


class ListFrame[T](tk.Frame, ABC):
    def __init__(
        self,
        parent,
        item_type: type[ListItem],
        header_stats: list[tuple[str, Size, Weight]],
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, *kwargs)
        self.item_type = item_type
        self.header_stats = header_stats
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        headerframe = tk.Frame(self)
        for i, (header, width, weight) in enumerate(header_stats):
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

    @cached_property
    def column_stats(self) -> list[tuple[Size, Weight]]:
        return list(map(lambda x: (x[1], x[2]), self.header_stats))

    def add_new(self) -> ListItem:
        line = self.item_type(self.listframe.viewPort, self.column_stats)
        line.grid(row=len(self.listframe.viewPort.grid_slaves()), column=0, sticky="EW")
        return line

    def add_item(self, item: T):
        line = self.add_new()
        line.set_item(item)

    def get_items(self) -> list[T]:
        return [
            cast(ListItem, gs).get_item()
            for gs in self.listframe.viewPort.grid_slaves()[::-1]
        ]

    def count(self) -> int:
        return len(self.listframe.viewPort.grid_slaves())

    def clear(self):
        for w in self.listframe.viewPort.grid_slaves():
            w.destroy()
