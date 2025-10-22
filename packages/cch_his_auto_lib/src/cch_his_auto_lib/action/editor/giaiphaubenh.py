from . import wait_loaded
from cch_his_auto_lib.driver import Driver

def bs(d: Driver):
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
        name="phieu giai phau benh",
    )
