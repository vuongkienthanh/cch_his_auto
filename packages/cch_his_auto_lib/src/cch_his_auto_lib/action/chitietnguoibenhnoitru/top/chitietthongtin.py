from contextlib import contextmanager
import logging


from cch_his_auto_lib.driver import Driver
from . import TOP_BTN_CSS

_lgr = logging.getLogger("top_chitietthongtin")

DIALOG_CSS = ".ant-modal:has(.avatar__image)"


@contextmanager
def session(d: Driver):
    "Open and close *Chi tiết thông tin* dialog"
    d.clicking(f"{TOP_BTN_CSS}>div:first-child")
    d.waiting(DIALOG_CSS)
    try:
        yield
    finally:
        d.clicking(f"{DIALOG_CSS} button.ant-modal-close")
        d.wait_disappearing(DIALOG_CSS)


CHIEUCAO_CSS = f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(5) input"
CANNANG_CSS = f"{DIALOG_CSS} .ant-col:nth-child(5) .ant-row:nth-child(1) .ant-col:nth-child(6) input"


def get_chieucao(d: Driver) -> str:
    return d.get_input_value(CHIEUCAO_CSS, "chiều cao")


def get_cannang(d: Driver) -> str:
    return d.get_input_value(CANNANG_CSS, "cân nặng")
