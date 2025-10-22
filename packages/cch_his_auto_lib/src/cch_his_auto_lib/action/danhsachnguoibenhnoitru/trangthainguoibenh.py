from contextlib import contextmanager

from . import _lgr
from cch_his_auto_lib.driver import Driver

TRANGTHAINGUOIBENH_POPOVER = ".ant-popover:has(.check-all)"


@contextmanager
def open_menu(d: Driver):
    d.clicking(
        "#base-search_component .ant-col:nth-child(7) button",
        "open menu trạng thái người bệnh",
    )
    d.waiting(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all")
    try:
        yield
    finally:
        d.clicking(
            "#base-search_component .ant-col:nth-child(7) button",
            "close menu trạng thái người bệnh",
        )
        d.wait_closing(TRANGTHAINGUOIBENH_POPOVER)


def check(d: Driver, indexes: list[int]):
    """
    Uncheck all checkboxes, then check those in `indexes`.
    `indexes` is 1-indexed.
    """
    _lgr.debug(f"filter_trangthainguoibenh indexes={indexes}")
    _lgr.debug("first uncheck all boxes in trạng thái người bệnh")
    ele = d.find(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox input")
    if ele.is_selected():
        ele.click()
    else:
        ele.click()
        ele.click()

    for i in indexes:
        d.clicking(
            f"{TRANGTHAINGUOIBENH_POPOVER} .ant-checkbox-group label:nth-child({i}) .ant-checkbox input",
            d.find(f".ant-popover label:nth-child({i})").text,
        )


def check_all(d: Driver):
    """
    Check all checkboxes
    """
    _lgr.debug("check all boxes in trạng thái người bệnh")
    ele = d.find(f"{TRANGTHAINGUOIBENH_POPOVER} .check-all .ant-checkbox input")
    if not ele.is_selected():
        ele.click()
