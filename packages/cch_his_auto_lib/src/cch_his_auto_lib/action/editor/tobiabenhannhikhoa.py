from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded


def bs(d: Driver):
    with console.status("signing tờ bìa bệnh án nhi khoa..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item div:nth-child(2) .sign-image button",
            btn_txt="Xác nhận ký Trưởng khoa",
            img_css=".layout-line-item div:nth-child(2) .sign-image img",
            name="to bia benh an nhi khoa",
        )
