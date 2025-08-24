import time

from cch_his_auto_lib.driver import Driver
from . import _lgr


def tobiabenhannhikhoa(d: Driver):
    "*Tờ bìa bệnh án nhi khoa*"
    d.sign_staff_signature(
        btn_css=".layout-line-item div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
        name="to bia benh an nhi khoa",
    )


def mucAbenhannhikhoa(d: Driver):
    "*Mục A bệnh án nhi khoa*"
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
        name="muc A",
    )


def mucBtongketbenhan(d: Driver):
    "*Mục B tổng kết bệnh án*"
    d.sign_staff_signature(
        btn_css="td:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
        name="muc B",
    )


def todieutri(d: Driver):
    "*Tờ điều trị*"
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
        name="to dieu tri",
    )


def phieuthuchienylenh_bs(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    _lgr.info("++++ doing phieuthuchienylenh_bs, may take a while")
    d.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(4) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(4) td:nth-child({col}) img",
            name="phieu thuc hien y lenh bac si row 1",
        )
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(3) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(3) td:nth-child({col}) img",
            name="phieu thuc hien y lenh bac si row 2",
        )


def phieuthuchienylenh_dd(d: Driver, arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    _lgr.info("++++ doing phieuthuchienylenh_dd, may take a while")
    d.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        d.sign_staff_signature(
            btn_css=f"table tbody tr:nth-last-child(2) td:nth-child({col}) button",
            btn_txt="Ký",
            img_css=f"table tbody tr:nth-last-child(2) td:nth-child({col}) img",
            name="phieu thuc hien y lenh dieu duong",
        )


def phieuCT_bschidinh(d: Driver):
    "*Phiếu chỉ định CT, bs chỉ định*"
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image img",
        name="phieu CT bs chi dinh",
    )


def phieuCT_bsthuchien(d: Driver):
    "*Phiếu chỉ định CT, bs thực hiện*"
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(20) .sign-image button:nth-child(1)",
        btn_txt="Xác nhận ký Bác sĩ Chẩn đoán hình ảnh",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(20) .sign-image img",
        name="phieu CT bs thuc hien",
    )


def phieuMRI_bschidinh(d: Driver):
    "*Phiếu chỉ định MRI, bs chỉ định*"
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ chỉ định",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
        name="phieu MRI bs chi dinh",
    )


def phieuMRI_bsthuchien(d: Driver):
    "*Phiếu chỉ định MRI, bs thực hiện*"
    d.sign_staff_signature(
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ thực hiện",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image img",
        name="phieu MRI bs thuc hien",
    )


def giaiphaubenh(d: Driver):
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
        name="phieu giai phau benh",
    )


def phieucamkettta5(d: Driver):
    "*Phiếu cam kết thủ thuật a5*"
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ khám/ điều trị",
        img_css=".sign-image img",
        name="phieu cam ket thu thuat a5",
    )


def bienbanhoichan_thuky(d: Driver):
    "*Biên bản hội chẩn (thư ký)*"
    d.sign_staff_signature(
        btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Thư ký",
        img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image img",
        name="bien ban hoi chan (thu ky)",
    )


def bienbanhoichan_truongkhoa(d: Driver):
    "*Biên bản hội chẩn (trưởng khoa)*"
    d.sign_staff_signature(
        btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image img",
        name="bien ban hoi chan (truong khoa)",
    )


def phieudutrucungcapmau(d: Driver):
    "*Phiếu dự trù và cung cấp máu*"
    d.sign_staff_signature(
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
        name="phieu du tru cung cap mau",
    )
