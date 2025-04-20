import logging
import time

from selenium.common import NoSuchElementException, TimeoutException

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor.sign_patient_name import sign_canvas
from .helper import open_menu, goto
from cch_his_auto.helper import tracing, iframe

_logger = logging.getLogger().getChild("indieuduong")
_trace = tracing(_logger)


@_trace
def sign_staff(driver: Driver):
    "Click the sign staff button"
    try:
        driver.clicking(
            ".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button"
        )
    except (NoSuchElementException, TimeoutException):
        ...
    finally:
        driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")
        time.sleep(2)


@_trace
def sign_patient(driver: Driver, signature: str):
    "Click the sign patient button and put signature in the dialog then save"
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
def sign_bangkechiphiBHYT(driver: Driver, signature: str):
    "Sign both staff and patient in *Bảng kê chi phí BHYT*"
    open_menu(driver)
    goto(driver, "Bảng kê chi phí BHYT")
    with iframe(driver, ".ant-modal iframe"):
        sign_staff(driver)
        sign_patient(driver, signature)
    driver.find(".ant-modal-close:has(~.ant-modal-body iframe)").click()
