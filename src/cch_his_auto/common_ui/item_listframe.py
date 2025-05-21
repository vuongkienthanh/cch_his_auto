import tkinter as tk
from abc import ABC, abstractmethod
from typing import cast
from cch_his_auto.common_ui.scrollable_frame import ScrollFrame


class ScrollItem[T](tk.Frame, ABC):
    def __init__(self, parent):
        super().__init__(parent)

    @abstractmethod
    def set_item(self, item: T): ...
    @abstractmethod
    def get_item(self) -> T: ...


class ScrollList[T](ScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.viewPort.columnconfigure(0, weight=1)

    def add_new(self, _class: type[ScrollItem]) -> ScrollItem:
        line = _class(self.viewPort)
        line.grid(row=len(self.viewPort.grid_slaves()), column=0, sticky="EW")
        return line

    def get_items(self) -> list[T]:
        return [
            cast(ScrollItem, gs).get_item() for gs in self.viewPort.grid_slaves()[::-1]
        ]

    def clear(self):
        for w in self.viewPort.grid_slaves():
            w.destroy()
