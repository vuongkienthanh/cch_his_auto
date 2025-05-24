from functools import partial
from typing import Callable

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.editor import sign_staff_name, sign_patient_name
from . import _trace, goto


def _sign_phieuthuchienylenh(
    arr: tuple[bool, bool, bool, bool, bool],
    sign_fn: Callable,
):
    _d = get_global_driver()
    main_tab = _d.current_window_handle
    goto("Phiếu thực hiện y lệnh")
    _d.goto_newtab_do_smth_then_goback(main_tab, partial(sign_fn, arr=arr))


@_trace
def sign_phieuthuchienylenh_bs(arr: tuple[bool, bool, bool, bool, bool]):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bs) in sequence"
    _sign_phieuthuchienylenh(arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_bs)


@_trace
def sign_phieuthuchienylenh_dd(arr: tuple[bool, bool, bool, bool, bool]):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (dd) in sequence"
    _sign_phieuthuchienylenh(arr=arr, sign_fn=sign_staff_name.phieuthuchienylenh_dd)


@_trace
def sign_phieuthuchienylenh_bn(
    arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bn) in sequence"
    _sign_phieuthuchienylenh(
        arr=arr,
        sign_fn=partial(sign_patient_name.phieuthuchienylenh_bn, signature=signature),
    )
