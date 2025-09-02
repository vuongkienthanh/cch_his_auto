from cch_his_auto_lib.driver import Driver
from . import wait_loaded


def bs(d: Driver):
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ khám/ điều trị",
        img_css=".sign-image img",
        name="phieu cam ket thu thuat a5 (bac si)",
    )


def bn(d: Driver, signature: str | None):
    if signature is None:
        return
    wait_loaded(d)
    d.sign_patient_signature(
        btn_css=".sign-image button",
        btn_txt="Ký",
        img_css=".sign-image img",
        signature=signature,
        name="phieu cam ket thu thuat a5 (benh nhan)",
    )
