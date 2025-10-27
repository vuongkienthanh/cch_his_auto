from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded

def bs(d: Driver):
    with console.status("signing phiếu giải phẫu bệnh..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".sign-image button",
            btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
            img_css=".sign-image img",
            name="phieu giai phau benh",
        )
