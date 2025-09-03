import tkinter as tk
from abc import ABC, abstractmethod
from typing import cast

from cch_his_auto.common_ui.scrollable_frame import ScrollFrame

type Size = int
type Weight = int
type Header_stats = list[tuple[str, Size, Weight]]


class ListItem[T](tk.Frame, ABC):
    "abstract class for an item frame in ListFrame"

    @abstractmethod
    def __init__(self, parent):
        "derive this and add more widgets"
        super().__init__(parent)

    @abstractmethod
    def set_item(self, item: T):
        "set info from item"

    @abstractmethod
    def get_item(self) -> T:
        "return a dict with contained info"

    def _config(self, stats: Header_stats):
        for i, (_, width, weight) in enumerate(stats):
            self.columnconfigure(i, minsize=width, weight=weight)


class ListFrame[T](tk.Frame):
    """
    The container for derived ListItem.
    After you derive a ListItem and set up Header_stat, you can use this as it is
    """

    def __init__(
        self,
        parent,
        item_type: type[ListItem],
        stats: Header_stats,
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, *kwargs)
        self.item_type = item_type
        self.stats = stats
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        headerframe = tk.Frame(self)
        for i, (header, width, weight) in enumerate(stats):
            headerframe.columnconfigure(i, minsize=width, weight=weight)
            w = tk.Label(headerframe, text=header, relief="raised", anchor="center")
            w.grid(row=0, column=i, sticky="NSEW")
        headerframe.grid(row=0, column=0, sticky="WE", padx=(0, 15), pady=(5, 0))
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=1, sticky="NSEW")
        tk.Button(
            btn_frame, text="Add", command=self.add_new, background="#d4a5ab", width=5
        ).grid(row=0, pady=5)
        tk.Button(
            btn_frame, text="Clear", command=self.clear, background="#d4a5ab", width=5
        ).grid(row=1, pady=5)
        self.listframe = ScrollFrame(self)
        self.listframe.viewPort.columnconfigure(0, weight=1)
        self.listframe.grid(row=1, column=0, sticky="NSEW", pady=(0, 10))

    def add_new(self) -> ListItem:
        line = self.item_type(self.listframe.viewPort)
        line._config(self.stats)
        line.grid(row=len(self.listframe.viewPort.grid_slaves()), column=0, sticky="EW")
        return line

    def add_item(self, item: T):
        line = self.add_new()
        line.set_item(item)

    def get_items(self) -> tuple[T]:
        return tuple(
            cast(ListItem, gs).get_item()
            for gs in self.listframe.viewPort.grid_slaves()[::-1]
        )

    def count(self) -> int:
        return len(self.listframe.viewPort.grid_slaves())

    def clear(self):
        for w in self.listframe.viewPort.grid_slaves():
            w.destroy()
