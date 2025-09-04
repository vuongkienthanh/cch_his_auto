from cch_his_auto.common_ui.item_listframe import ListFrame, ListItem


class TabbedListFrame(ListFrame):
    "ListFrame with title and tab index"

    def __init__(self, parent, title: str, tab_index: int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title = title
        self.tab_index = tab_index

    def get_title_with_count(self) -> str:
        return f"{self.title} ({self.count()})"

    def add_new(self) -> ListItem:
        line = super().add_new()
        self.change_tab_text()
        return line

    def add_item(self, item):
        super().add_item(item)
        self.change_tab_text()

    def clear(self):
        super().clear()
        self.change_tab_text()

    def change_tab_text(self):
        self.master.tab(self.tab_index, text=self.get_title_with_count())  # type:ignore
