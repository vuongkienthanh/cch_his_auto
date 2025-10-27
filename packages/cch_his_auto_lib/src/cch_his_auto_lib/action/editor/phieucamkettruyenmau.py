from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded, check_than_click


def check_agree(d: Driver):
    wait_loaded(d)
    check_than_click(
        d,
        ".component-page .layout-line-item:nth-child(10) .check-item:first-child",
    )


def bn(d: Driver, signature: str):
    with console.status("signing phiếu truyền máu bệnh nhân..."):
        wait_loaded(d)
        d.sign_patient_signature(
            btn_css=".sign-image button",
            btn_txt="Ký",
            img_css=".sign-image img",
            signature=signature,
            name="phieu cam ket truyen mau benh nhan",
        )
