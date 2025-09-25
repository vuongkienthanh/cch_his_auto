from selenium.common import NoSuchElementException
from cch_his_auto_lib.driver import Driver


def wait_loaded(d: Driver):
    try:
        d.waiting(".app-main")
    except NoSuchElementException:
        d.refresh()
        d.waiting(".app-main")



def tobiabenhannhikhoa(d: Driver):
    "*Tờ bìa bệnh án nhi khoa*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".layout-line-item div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
        name="to bia benh an nhi khoa",
    )


def mucAbenhannhikhoa(d: Driver):
    "*Mục A bệnh án nhi khoa*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
        name="muc A",
    )


def mucBtongketbenhan(d: Driver):
    "*Mục B tổng kết bệnh án*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css="td:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
        name="muc B",
    )


def todieutri(d: Driver):
    "*Tờ điều trị*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
        name="to dieu tri",
    )


def giaiphaubenh(d: Driver):
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
        name="phieu giai phau benh",
    )


def phieudutrucungcapmau(d: Driver):
    "*Phiếu dự trù và cung cấp máu*"
    wait_loaded(d)
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
        name="phieu du tru cung cap mau",
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
