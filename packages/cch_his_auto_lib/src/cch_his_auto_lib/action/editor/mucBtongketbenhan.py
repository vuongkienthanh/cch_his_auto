from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded


def bs(d: Driver):
    with console.status("signing mục B tổng kết bệnh án..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css="td:nth-child(3) .sign-image button",
            btn_txt="Xác nhận ký Bác sĩ điều trị",
            img_css="td:nth-child(3) .sign-image img",
            name="muc B",
        )
