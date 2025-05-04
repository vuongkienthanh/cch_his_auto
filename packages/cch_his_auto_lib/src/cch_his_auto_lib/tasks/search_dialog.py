import logging
from cch_his_auto_lib.driver import Driver


_logger = logging.getLogger("search dialog")
DIALOG_CSS = ".ant-modal:has(.ant-modal-body>div>div>div>.ant-select)"
DIALOG_SEARCH_CSS = f"{DIALOG_CSS} input[type=search]"
DIALOG_OK_CSS = f"{DIALOG_CSS} .bottom-action-right button"
DIALOG_BACK_CSS = f"{DIALOG_CSS} .bottom-action-left button"


def filter(driver: Driver, value: str):
    _logger.debug("filter with value = {value}")
    driver.clear_input(DIALOG_SEARCH_CSS).send_keys(value)


def save(driver: Driver):
    driver.clicking(DIALOG_OK_CSS, "save dialog button")
    driver.wait_closing(DIALOG_CSS, "search dialog")
