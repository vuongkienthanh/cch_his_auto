from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded, check_than_click


def check_agree(d: Driver):
    wait_loaded(d)
    check_than_click(
        d,
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child",
    )


def bs(d: Driver):
    with console.status("signing phiếu cam kết A5..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".sign-image button",
            btn_txt="Xác nhận ký Bác sĩ khám/ điều trị",
            img_css=".sign-image img",
            name="phieu cam ket thu thuat a5 (bac si)",
        )


def bn(d: Driver, signature: str):
    with console.status("signing phiếu cam kết A5..."):
        wait_loaded(d)
        d.sign_patient_signature(
            btn_css=".sign-image button",
            btn_txt="Ký",
            img_css=".sign-image img",
            signature=signature,
            name="phieu cam ket thu thuat a5 (benh nhan)",
        )
