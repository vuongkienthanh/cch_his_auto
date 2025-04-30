import time

from selenium.common import NoSuchElementException, TimeoutException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import iframe
from cch_his_auto_lib.tasks.editor.sign_patient_name import sign_canvas
from . import goto, _trace


def _sign_bangkechiphiBHYT_staff(driver: Driver):
    "Click the sign staff button in *bảng kê chi phí BHYT*"
    try:
        driver.clicking(
            ".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button"
        )
    except (NoSuchElementException, TimeoutException):
        ...
    finally:
        driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")
        time.sleep(2)


def _sign_bangkechiphiBHYT_patient(driver: Driver, signature: str):
    "Click the sign patient button in *bảng kê chi phí BHYT* and put signature in the dialog then save"
    try:
        driver.clicking(
            ".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image button"
        )
    except (NoSuchElementException, TimeoutException):
        ...
    else:
        sign_canvas(driver, signature)
    finally:
        driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image img")


@_trace
def sign_bangkechiphiBHYT(
    driver: Driver, staff: bool = True, patient_signature: str | None = None
):
    "Sign both staff and patient in *Bảng kê chi phí BHYT*"
    goto(driver, "Bảng kê chi phí BHYT")
    with iframe(driver, ".ant-modal iframe"):
        if staff:
            _sign_bangkechiphiBHYT_staff(driver)
        if patient_signature:
            _sign_bangkechiphiBHYT_patient(driver, patient_signature)
    driver.find(".ant-modal-close:has(~.ant-modal-body iframe)").click()
    driver.wait_closing(".ant-modal-body iframe")
