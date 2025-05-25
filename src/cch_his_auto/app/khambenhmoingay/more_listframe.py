from cch_his_auto.common_ui.item_listframe import ListFrame, ListItem


class MoreListFrame(ListFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab_index: int | None = None

    def get_title(self) -> str: ...

    def set_tab_index(self, i: int):
        self.tab_index = i

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
        self.master.nametowidget("kcb_notebook").tab(self.tab_index, text=self.get_title())
