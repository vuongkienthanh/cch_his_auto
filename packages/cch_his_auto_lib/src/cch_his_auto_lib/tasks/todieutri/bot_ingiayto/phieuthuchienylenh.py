from functools import partial
from typing import Callable

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.editor import sign_staff, sign_patient
from . import _trace, goto


def _sign_phieuthuchienylenh(
    d: Driver,
    arr: tuple[bool, bool, bool, bool, bool],
    sign_fn: Callable,
):
    main_tab = d.current_window_handle
    goto(d, "Phiếu thực hiện y lệnh")
    d.goto_newtab_do_smth_then_goback(main_tab, partial(sign_fn, arr=arr))


@_trace
def sign_phieuthuchienylenh_bs(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bs) in sequence"
    _sign_phieuthuchienylenh(d, arr=arr, sign_fn=sign_staff.phieuthuchienylenh_bs)


@_trace
def sign_phieuthuchienylenh_dd(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (dd) in sequence"
    _sign_phieuthuchienylenh(d, arr=arr, sign_fn=sign_staff.phieuthuchienylenh_dd)


@_trace
def sign_phieuthuchienylenh_bn(
    d: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "Inside *tờ điều trị*, try to sign *phiếu thực hiện y lệnh* (bn) in sequence"
    _sign_phieuthuchienylenh(
        d,
        arr=arr,
        sign_fn=partial(sign_patient.phieuthuchienylenh_bn, signature=signature),
    )
