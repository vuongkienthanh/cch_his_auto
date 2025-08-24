from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from . import goto, _trace


# TODO: use driver.sign_staff_signature
def _sign_bangkechiphiBHYT_staff(d: Driver):
    "Click the sign staff button in *bảng kê chi phí BHYT*"
    try:
        d.clicking(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button")
    except NoSuchElementException:
        ...
    finally:
        d.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")


# TODO: use driver.sign_patient_signature
def _sign_bangkechiphiBHYT_patient(d: Driver, signature: str):
    "Click the sign patient button in *bảng kê chi phí BHYT* and put signature in the dialog then save"
    try:
        d.clicking(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image button")
    except NoSuchElementException:
        ...
    else:
        d.sign_canvas(signature)
    finally:
        d.waiting(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image img")


@_trace
def sign_bangkechiphiBHYT(
    d: Driver, staff: bool = True, patient_signature: str | None = None
):
    "Sign staff and patient signature in *Bảng kê chi phí BHYT*"
    goto(d, "Bảng kê chi phí BHYT")
    with d.iframe(".ant-modal iframe", ".ant-modal-close:has(~.ant-modal-body iframe)"):
        if staff:
            _sign_bangkechiphiBHYT_staff(d)
        if patient_signature:
            _sign_bangkechiphiBHYT_patient(d, patient_signature)
