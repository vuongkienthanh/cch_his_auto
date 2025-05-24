from contextlib import contextmanager

from cch_his_auto_lib.driver import get_global_driver
from . import _lgr, THONGTINRAVIEN_CSS

DIALOG_CSS = ".ant-modal:has(.ant-row:first-child+.more-info)"


@contextmanager
def session():
    open_dialog()
    try:
        yield
    finally:
        save()


def open_dialog():
    _d = get_global_driver()
    _d.clicking2(f"{THONGTINRAVIEN_CSS} .title svg", "edit thongtinravien button")
    _d.waiting(DIALOG_CSS, "edit thongtinravien dialog")


def save():
    _d = get_global_driver()
    _d.clicking(
        f"{DIALOG_CSS} .bottom-action-right button:nth-child(2)",
        "save button",
    )
    _d.clicking2(
        f"{DIALOG_CSS} .ant-modal-close",
        "close button",
    )
    _d.wait_closing(DIALOG_CSS, "edit thongtinravien dialog")


def set_discharge_diagnosis_detail(value: str):
    _d = get_global_driver()
    _d.clear_input(
        f"{DIALOG_CSS} .ant-row .ant-col:nth-child(1)>div:nth-child(3) textarea"
    ).send_keys(value)
    _lgr.info(f"set discharge_diagnosis_detail= {value}")


def set_treatment(value: str):
    _d = get_global_driver()
    _d.clear_input(
        f"{DIALOG_CSS} .ant-row .ant-col:nth-child(1)>div:nth-child(4)>div>div"
    ).send_keys(value)
    _lgr.info(f"set treatment= {value}")
