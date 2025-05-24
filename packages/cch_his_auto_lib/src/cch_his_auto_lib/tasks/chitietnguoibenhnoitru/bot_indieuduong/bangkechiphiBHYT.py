import time

from selenium.common import NoSuchElementException, TimeoutException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.editor.sign_patient_name import sign_canvas
from . import goto, _trace


def _sign_bangkechiphiBHYT_staff():
    "Click the sign staff button in *bảng kê chi phí BHYT*"
    _d = get_global_driver()
    try:
        _d.clicking(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button")
    except (NoSuchElementException, TimeoutException):
        ...
    finally:
        _d.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")
        time.sleep(2)


def _sign_bangkechiphiBHYT_patient(signature: str):
    "Click the sign patient button in *bảng kê chi phí BHYT* and put signature in the dialog then save"
    _d = get_global_driver()
    try:
        _d.clicking(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image button")
    except (NoSuchElementException, TimeoutException):
        ...
    else:
        sign_canvas(signature)
    finally:
        _d.waiting(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image img")


@_trace
def sign_bangkechiphiBHYT(staff: bool = True, patient_signature: str | None = None):
    "Sign both staff and patient in *Bảng kê chi phí BHYT*"
    _d = get_global_driver()
    goto("Bảng kê chi phí BHYT")
    with _d.iframe(".ant-modal iframe"):
        if staff:
            _sign_bangkechiphiBHYT_staff()
        if patient_signature:
            _sign_bangkechiphiBHYT_patient(patient_signature)
    _d.find(".ant-modal-close:has(~.ant-modal-body iframe)").click()
    _d.wait_closing(".ant-modal-body iframe")
