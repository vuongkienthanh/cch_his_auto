from functools import partial

from cch_his_auto.driver import Driver, DriverFn
from cch_his_auto.tasks.editor import sign_staff_name, sign_patient_name
from . import open_menu, goto

def _sign_phieuthuchienylenh(
    driver: Driver,
    arr: tuple[bool, bool, bool, bool, bool],
    sign_fn: DriverFn,
):
    main_tab = driver.current_window_handle
    try:
        open_menu(driver)
        goto(driver, "Phiếu thực hiện y lệnh")
    except:
        return
    else:
        driver.goto_newtab_do_smth_then_goback(main_tab, partial(sign_fn, arr=arr))

sign_phieuthuchienylenh_bs = partial(
    _sign_phieuthuchienylenh, sign_fn=sign_staff_name.phieuthuchienylenh_bs
)
sign_phieuthuchienylenh_dd = partial(
    _sign_phieuthuchienylenh, sign_fn=sign_staff_name.phieuthuchienylenh_dd
)

def sign_phieuthuchienylenh_bn(
    driver: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    _sign_phieuthuchienylenh(
        driver,
        arr=arr,
        sign_fn=partial(sign_patient_name.phieuthuchienylenh_bn, signature=signature),
    )
