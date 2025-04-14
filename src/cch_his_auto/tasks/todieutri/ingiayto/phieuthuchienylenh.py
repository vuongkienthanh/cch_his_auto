from functools import partial
import logging

from cch_his_auto.driver import Driver, DriverFn
from cch_his_auto.tasks.editor import sign_staff_name, sign_patient_name
from cch_his_auto.helper import tracing
from . import open_menu, goto

_logger = logging.getLogger().getChild("todieutri")
_trace = tracing(_logger)

def _sign(
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
    _sign(driver, arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_bs)

@_trace
def sign_phieuthuchienylenh_dd(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool]
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (dd) in sequence"
    _sign(driver, arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_dd)

@_trace
def sign_phieuthuchienylenh_bn(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bn) in sequence"
    _sign(
        driver,
        arr=arr,
        sign_fn=partial(sign_patient_name.phieuthuchienylenh_bn, signature=signature),
    )
