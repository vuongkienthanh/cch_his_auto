from contextlib import contextmanager

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor.sign_patient_name import sign_canvas
from . import open_menu, goto

def open_dialog(driver: Driver):
    goto(driver, "Bảng kê chi phí BHYT")

def close_dialog(driver: Driver):
    driver.find(".ant-modal-close:has(~.ant-modal-body iframe)").click()

@contextmanager
def iframe(driver: Driver):
    try:
        _iframe = driver.waiting(".ant-modal iframe")
        driver.switch_to.frame(_iframe)
        yield _iframe
    finally:
        driver.switch_to.parent_frame()

def sign_staff(driver: Driver):
    try:
        driver.clicking(
            ".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button"
        )
    except:
        ...
    finally:
        driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")

def sign_patient(driver: Driver, signature: str):
    try:
        driver.clicking(
            ".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image button"
        )
    except:
        ...
    else:
        sign_canvas(driver, signature)
    finally:
        driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image img")

def sign_bangkechiphiBHYT(driver: Driver, signature: str):
    open_menu(driver)
    open_dialog(driver)
    with iframe(driver):
        sign_staff(driver)
        sign_patient(driver, signature)
    close_dialog(driver)
