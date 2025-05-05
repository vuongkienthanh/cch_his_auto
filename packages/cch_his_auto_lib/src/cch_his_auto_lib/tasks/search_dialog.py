import logging
from cch_his_auto_lib.driver import Driver


_logger = logging.getLogger("search dialog")

DIALOG_CSS = ".ant-modal:has(.ant-modal-body>div>div>div>.ant-select)"
DIALOG_SEARCH_CSS = f"{DIALOG_CSS} input[type=search]"
DIALOG_OK_CSS = f"{DIALOG_CSS} .bottom-action-right button"
DIALOG_BACK_CSS = f"{DIALOG_CSS} .bottom-action-left button"
DIALOG_CLOSE_CSS = f"{DIALOG_CSS} .ant-modal-close"

DROPDOWN_CSS = ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"


def close_dialog(driver: Driver):
    driver.clicking(DIALOG_CLOSE_CSS, "close dialog button")


def filter(driver: Driver, value: str):
    _logger.debug("filter with value = {value}")
    driver.clear_input(DIALOG_SEARCH_CSS).send_keys(value)


def count_item_dropdown(driver: Driver) -> int:
    driver.waiting(f"{DROPDOWN_CSS} .ant-select-item", "dropdown")
    return len(driver.find_all(f"{DROPDOWN_CSS} .ant-select-item"))


def select_item_dropdown(driver: Driver, i: int):
    driver.find_all(f"{DROPDOWN_CSS} .ant-select-item")[i].click()


def save(driver: Driver):
    driver.clicking(DIALOG_OK_CSS, "save dialog button")
    driver.wait_closing(DIALOG_CSS, "search dialog")
