from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded


def bs(d: Driver):
    with console.status("signing tờ điều trị..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".sign-image button",
            btn_txt="Xác nhận ký Bác sĩ điều trị",
            img_css=".sign-image img",
            name="to dieu tri",
        )
