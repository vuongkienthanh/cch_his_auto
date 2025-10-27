from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded


def bschidinh(d: Driver):
    with console.status("signing phiếu chỉ định CT..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image button",
            btn_txt="Xác nhận ký Bác sĩ điều trị",
            img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image img",
            name="phieu CT bs chi dinh",
        )


def bsthuchien(d: Driver):
    with console.status("signing phiếu chỉ định CT..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button:nth-child(1)",
            btn_txt="Xác nhận ký Bác sĩ Chẩn đoán hình ảnh",
            img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
            name="phieu CT bs thuc hien",
        )


def bn(d: Driver, signature: str):
    with console.status("signing phiếu chỉ định CT..."):
        wait_loaded(d)
        d.sign_patient_signature(
            btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image button",
            btn_txt="Ký",
            img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image img",
            signature=signature,
            name="phieu CT benh nhan",
        )
