import logging
import time
from contextlib import contextmanager

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.errors import EndOfLoopException
from .. import TOP_BTN_CSS

_lgr = logging.getLogger("top_chitietthongtin")

DIALOG_CSS = ".ant-modal:has(.avatar__image)"


@contextmanager
def session(d: Driver):
    "use as contextmanager for open and close chitietthongtin dialog"
    try:
        yield open_dialog(d)
    finally:
        close_dialog(d)


def open_dialog(d: Driver):
    d.clicking(
        f"{TOP_BTN_CSS}>div:first-child",
        "click Chi tiết thông tin button",
    )
    d.waiting(DIALOG_CSS, "Chi tiết thông tin dialog")


def close_dialog(d: Driver):
    d.clicking(
        f"{DIALOG_CSS} .ant-modal-close",
        "close Chi tiết thông tin dialog",
    )
    d.wait_closing(DIALOG_CSS)


def get_chieucao(d: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = d.find(
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


def get_cannang(d: Driver) -> str | None:
    for _ in range(30):
        time.sleep(1)
        try:
            value = d.find(
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


def get_age_in_month(d: Driver) -> int:
    for _ in range(30):
        time.sleep(1)
        try:
            value = d.find(
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
        raise EndOfLoopException("-> can't find age")
