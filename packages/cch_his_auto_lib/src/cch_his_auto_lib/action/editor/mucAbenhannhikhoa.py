from . import wait_loaded
from cch_his_auto_lib.driver import Driver


def bs(d: Driver):
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
        name="muc A",
    )
