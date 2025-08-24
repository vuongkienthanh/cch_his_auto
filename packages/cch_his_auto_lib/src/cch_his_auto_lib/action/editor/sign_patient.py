import time

from cch_his_auto_lib.driver import Driver

from . import _lgr


def phieuthuchienylenh_bn(
    d: Driver, arr: tuple[bool, bool, bool, bool, bool], signature: str
):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    _lgr.info("++++ doing phieuthuchienylenh_bn, may take a while")
    d.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_patient_signature(
            btn_css=f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
            signature=signature,
            name=f"row 4 col {col - 2}",
        )


def phieuCT_bn(d: Driver, signature: str):
    "*Phiếu chỉ định CT (bệnh nhân)*"
    d.sign_patient_signature(
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image img",
        signature=signature,
        name="phieu CT benh nhan",
    )


def phieuMRI_bn(d: Driver, signature: str):
    "*Phiếu chỉ định MRI (bệnh nhân)*"
    d.sign_patient_signature(
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
        name="phieu MRI benh nhan",
    )


def phieucamkettruyenmau_bn(d: Driver, signature: str):
    "*Phiếu cam kết truyền máu (bệnh nhân)*"
    d.sign_patient_signature(
        btn_css=".sign-image button",
        btn_txt="Ký",
        img_css=".sign-image img",
        signature=signature,
        name="phieu cam ket truyen mau benh nhan",
    )


def phieucamkettta5(d: Driver, signature: str):
    "*Phiếu cam kết thủ thuật a5 (bệnh nhân)*"
    d.sign_patient_signature(
        btn_css=".sign-image button",
        btn_txt="Ký",
        img_css=".sign-image img",
        signature=signature,
        name="phieu cam ket thu thuat a5",
    )
