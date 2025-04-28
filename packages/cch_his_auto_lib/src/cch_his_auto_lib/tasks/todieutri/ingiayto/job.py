import time
from enum import StrEnum
from functools import partial

from selenium.common import StaleElementReferenceException

from cch_his_auto_lib.driver import Driver, DriverFn
from cch_his_auto_lib.helper import tracing, EndOfLoop
from cch_his_auto_lib.tasks.editor import sign_staff_name, sign_patient_name
from .helper import open_menu, goto
from . import _logger

_trace = tracing(_logger)


class _State(StrEnum):
    Sign = "Ký Bác sĩ"
    Cancel = "Hủy ký Bác sĩ"


@_trace
def sign_phieuchidinh(driver: Driver):
    "Inside *tờ điều trị*, try to sign *phiếu chỉ định* in sequence"

    def close_dialog():
        driver.clicking(
            ".ant-modal-close:has(~.ant-modal-body .__list)",
            "close dialog button",
        )
        driver.wait_closing(".ant-modal-body .__list", "phieu chi dinh dialog")

    open_menu(driver)
    goto(driver, name="Phiếu chỉ định")
    for i in range(120):
        time.sleep(1)
        _logger.debug(f"checking button state {i}...")
        for ele in driver.find_all(".__button button"):
            try:
                if ele.text == _State.Cancel:
                    _logger.debug(f"button state is {_State.Cancel}")
                    close_dialog()
                    return
                elif ele.text == "Ký Bác sĩ":
                    _logger.debug(f"button state is {_State.Sign} -> click")
                    ele.click()
                    time.sleep(5)
                    close_dialog()
                    return
            except StaleElementReferenceException as e:
                _logger.warning(f"get {e}")
    else:
        close_dialog()
        raise EndOfLoop("can't sign phieuchidinh while in dialog")


def _sign_phieuthuchienylenh(
    driver: Driver,
    arr: tuple[bool, bool, bool, bool, bool],
    sign_fn: DriverFn,
):
    main_tab = driver.current_window_handle
    open_menu(driver)
    goto(driver, "Phiếu thực hiện y lệnh")
    driver.goto_newtab_do_smth_then_goback(main_tab, partial(sign_fn, arr=arr))


@_trace
def sign_phieuthuchienylenh_bs(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool]
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bs) in sequence"
    _sign_phieuthuchienylenh(
        driver, arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_bs
    )


@_trace
def sign_phieuthuchienylenh_dd(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool]
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (dd) in sequence"
    _sign_phieuthuchienylenh(
        driver, arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_dd
    )


@_trace
def sign_phieuthuchienylenh_bn(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bn) in sequence"
    _sign_phieuthuchienylenh(
        driver,
        arr=arr,
        sign_fn=partial(sign_patient_name.phieuthuchienylenh_bn, signature=signature),
    )


@_trace
def sign_todieutri(driver: Driver):
    "Inside *tờ điều trị*, try to sign *tờ điều trị* in sequence"
    main_tab = driver.current_window_handle
    open_menu(driver)
    goto(driver, name="Tờ điều trị")
    driver.goto_newtab_do_smth_then_goback(main_tab, sign_staff_name.todieutri)
