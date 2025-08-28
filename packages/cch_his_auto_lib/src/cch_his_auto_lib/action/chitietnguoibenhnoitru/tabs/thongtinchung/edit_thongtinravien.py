from contextlib import contextmanager

from cch_his_auto_lib.driver import Driver
from . import _lgr, THONGTINRAVIEN_CSS

DIALOG_CSS = ".ant-modal:has(.ant-row:first-child+.more-info)"


@contextmanager
def session(d: Driver):
    d.clicking2(f"{THONGTINRAVIEN_CSS} .title svg", "edit thongtinravien button")
    d.waiting(DIALOG_CSS, "edit thongtinravien dialog")
    try:
        yield
    finally:
        d.clicking(
            f"{DIALOG_CSS} .bottom-action-right button:nth-child(2)",
            "save button",
        )
        d.clicking2(
            f"{DIALOG_CSS} .ant-modal-close",
            "close button",
        )
        d.wait_disappearing(DIALOG_CSS, "edit thongtinravien dialog")


def set_discharge_diagnosis_detail(d: Driver, value: str):
    d.clear_input(
        f"{DIALOG_CSS} .ant-row .ant-col:nth-child(1)>div:nth-child(3) textarea"
    ).send_keys(value)
    _lgr.info(f"set discharge_diagnosis_detail= {value}")


def set_treatment(d: Driver, value: str):
    d.clear_input(
        f"{DIALOG_CSS} .ant-row .ant-col:nth-child(1)>div:nth-child(4)>div>div"
    ).send_keys(value)
    _lgr.info(f"set treatment= {value}")
