import logging
from cch_his_auto_lib.driver import get_global_driver


_lgr = logging.getLogger("search dialog")

DIALOG_CSS = ".ant-modal:has(.ant-modal-body>div>div>div>.ant-select)"
DIALOG_SEARCH_CSS = f"{DIALOG_CSS} input[type=search]"
DIALOG_OK_CSS = f"{DIALOG_CSS} .bottom-action-right button"
DIALOG_BACK_CSS = f"{DIALOG_CSS} .bottom-action-left button"
DIALOG_CLOSE_CSS = f"{DIALOG_CSS} .ant-modal-close"
DROPDOWN_CSS = ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"


def close_dialog():
    _d = get_global_driver()
    _d.clicking(DIALOG_CLOSE_CSS, "close dialog button")


def filter(value: str):
    _d = get_global_driver()
    _lgr.debug("filter with value = {value}")
    _d.clear_input(DIALOG_SEARCH_CSS).send_keys(value)


def count_item_dropdown() -> int:
    _d = get_global_driver()
    _d.waiting(f"{DROPDOWN_CSS} .ant-select-item", "dropdown")
    return len(_d.find_all(f"{DROPDOWN_CSS} .ant-select-item"))


def select_item_dropdown(i: int):
    _d = get_global_driver()
    _d.find_all(f"{DROPDOWN_CSS} .ant-select-item")[i].click()


def save():
    _d = get_global_driver()
    _d.clicking(DIALOG_OK_CSS, "save dialog button")
    _d.wait_closing(DIALOG_CSS, "search dialog")
