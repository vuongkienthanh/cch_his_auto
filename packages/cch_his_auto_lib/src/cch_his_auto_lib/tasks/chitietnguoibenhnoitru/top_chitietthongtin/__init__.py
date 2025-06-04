import logging
import time
from contextlib import contextmanager

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import EndOfLoop
from .. import TOP_BTN_CSS

_lgr = logging.getLogger("top_chitietthongtin")

DIALOG_CSS = ".ant-modal:has(.avatar__image)"


@contextmanager
def session():
    "use as contextmanager for open and close chitietthongtin dialog"
    try:
        yield open_dialog()
    finally:
        close_dialog()


def open_dialog():
    _d = get_global_driver()
    _d.clicking(
        f"{TOP_BTN_CSS}>div:first-child",
        "click Chi tiết thông tin button",
    )
    _d.waiting(DIALOG_CSS, "Chi tiết thông tin dialog")


def close_dialog():
    _d = get_global_driver()
    _d.clicking(
        f"{DIALOG_CSS} .ant-modal-close",
        "close Chi tiết thông tin dialog",
    )
    _d.wait_closing(DIALOG_CSS)


def get_chieucao() -> str | None:
    _d = get_global_driver()
    for _ in range(30):
        time.sleep(1)
        try:
            value = _d.find(
                f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(5) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _lgr.info(f"-> found chieucao={value}")
                return value
        except NoSuchElementException:
            ...
    else:
        _lgr.warning("-> can't find chieucao")
        return None


def get_cannang() -> str | None:
    _d = get_global_driver()
    for _ in range(30):
        time.sleep(1)
        try:
            value = _d.find(
                f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(6) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _lgr.info(f"-> found cannang={value}")
                return value
        except NoSuchElementException:
            ...
    else:
        _lgr.warning("-> can't find cannang")
        return None


def get_age_in_month() -> int:
    _d = get_global_driver()
    for _ in range(30):
        time.sleep(1)
        try:
            value = _d.find(
                f"{DIALOG_CSS} .ant-col:nth-child(2) .ant-row .ant-col:nth-child(4) input"
            ).get_attribute("value")
            if value == "":
                continue
            else:
                assert value is not None
                _lgr.info(f"-> found age={value} tuổi")
                a = value.strip().split(" ")
                if len(a) == 1:
                    return int(a[0]) * 12
                if len(a) == 2:
                    if a[1] == "tháng":
                        return int(a[0])
                    else:
                        return 0
                if len(a) == 4:
                    return int(a[0]) * 12 + int(a[2])

        except NoSuchElementException:
            ...
    else:
        _lgr.error("-> can't find age")
        raise EndOfLoop("-> can't find age")
