from cch_his_auto.common_ui.item_listframe import ListFrame, ListItem


type Size = int
type Weight = int


class MoreListFrame(ListFrame):
    def __init__(self, parent, item_type: type[ListItem], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tab_index: int | None = None
        self.item_type = item_type

    def get_title(self) -> str: ...
    def get_sizes(self) -> list[tuple[str, Size, Weight]]: ...

    def set_tab_index(self, i: int):
        self.tab_index = i

    def add_new(self):
        assert self.item_type is not None
        self.add(self.item_type)
        self.change_tab_text()

    def add_item(self, item):
        assert self.item_type is not None
        line = self.add(self.item_type)
        line.set_item(item)
        self.change_tab_text()

    def clear(self):
        super().clear()
        self.change_tab_text()

    def change_tab_text(self):
        self.master.nametowidget("kcb_nb").tab(self.tab_index, text=self.get_title())
