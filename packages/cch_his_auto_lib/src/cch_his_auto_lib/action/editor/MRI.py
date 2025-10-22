from . import wait_loaded
from cch_his_auto_lib.driver import Driver


def bschidinh(d: Driver):
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ chỉ định",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
        name="phieu MRI bs chi dinh",
    )


def bsthuchien(d: Driver):
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ thực hiện",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image img",
        name="phieu MRI bs thuc hien",
    )


def bn(d: Driver, signature: str):
    wait_loaded(d)
    d.sign_patient_signature(
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
        name="phieu MRI benh nhan",
    )
