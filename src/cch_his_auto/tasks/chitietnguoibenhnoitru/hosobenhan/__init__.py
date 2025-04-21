import logging
from contextlib import contextmanager

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor import sign_staff_name, sign_patient_name
from cch_his_auto.helper import tracing
from .helper import (
    open_dialog,
    close_dialog,
    filter_check_expand_sign,
    do_nothing,
    sign_current,
    sign_current2,
    sign_current_both,
    sign_tab,
)

_logger = logging.getLogger().getChild("hosobenhan")
_trace = tracing(_logger)


@contextmanager
def session(driver):
    "use as contextmanager for open and close hosobenhan dialog"
    try:
        yield open_dialog(driver)
    finally:
        close_dialog(driver)


@_trace
def tobiabenhannhikhoa(driver: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    filter_check_expand_sign(
        driver,
        name="Tờ bìa bệnh án Nhi khoa",
        chuaky_fn=lambda driver, i: sign_tab(
            driver, i, sign_staff_name.tobiabenhannhikhoa
        ),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def mucAbenhannhikhoa(driver: Driver):
    "Filter and sign name: *Mục A bệnh án nhi khoa*"
    filter_check_expand_sign(
        driver,
        name="Mục A - Bệnh án Nhi khoa",
        chuaky_fn=lambda driver, i: sign_tab(
            driver, i, sign_staff_name.mucAbenhannhikhoa
        ),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def mucBtongketbenhan(driver: Driver):
    "Filter and sign name: *Mục B tổng kết bệnh án*"
    filter_check_expand_sign(
        driver,
        name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        chuaky_fn=lambda driver, i: sign_tab(
            driver, i, sign_staff_name.mucBtongketbenhan
        ),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieukhambenhvaovien(driver: Driver):
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    filter_check_expand_sign(
        driver,
        name="Phiếu khám bệnh vào viện",
        chuaky_fn=lambda driver, _: sign_current(driver),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieuchidinhxetnghiem(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định xét nghiệm",
        chuaky_fn=lambda driver, _: sign_current(driver),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def todieutri(driver: Driver):
    "Filter and sign name: *Tờ điều trị*"
    filter_check_expand_sign(
        driver,
        name="Tờ điều trị",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, sign_staff_name.todieutri),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieuchidinhPTTT(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định PTTT",
        chuaky_fn=lambda driver, _: sign_current(driver),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieuCT_bschidinh(driver: Driver):
    def chuaky_fn(driver):
        sign_staff_name.phieuCT_bschidinh(driver)

    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieuCT(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"

    def dangky_fn(driver):
        sign_staff_name.phieuCT_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuCT_bn(driver, signature)

    def chuaky_fn(driver):
        sign_staff_name.phieuCT_bschidinh(driver)
        dangky_fn(driver)

    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda driver, i: sign_tab(driver, i, dangky_fn),
    )


@_trace
def phieuMRI(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"

    def dangky_fn(driver):
        sign_staff_name.phieuMRI_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuMRI_bn(driver, signature)

    def chuaky_fn(driver):
        sign_staff_name.phieuMRI_bschidinh(driver)
        dangky_fn(driver)

    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda driver, i: sign_tab(driver, i, dangky_fn),
    )


@_trace
def giaiphaubenh(driver: Driver):
    "Filter and sign name: *Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    filter_check_expand_sign(
        driver,
        name="Phiếu xét nghiệm giải phẫu bệnh sinh thiết",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, sign_staff_name.giaiphaubenh),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieusanglocdinhduong(driver: Driver):
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    filter_check_expand_sign(
        driver,
        name="Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú",
        chuaky_fn=lambda driver, _: sign_current(driver),
        dangky_fn=lambda *_: do_nothing(),
    )


@_trace
def phieusoket15ngay(driver: Driver):
    "Filter and sign name: *Phiếu sơ kết 15 ngày điều trị*"
    filter_check_expand_sign(
        driver,
        name="Phiếu sơ kết 15 ngày điều trị",
        chuaky_fn=lambda driver, _: sign_current_both(driver),
        dangky_fn=lambda driver, _: sign_current2(driver),
    )


@_trace
def donthuoc(driver: Driver):
    "Filter and sign name: *Đơn thuốc*"
    filter_check_expand_sign(
        driver,
        name="Đơn thuốc",
        chuaky_fn=lambda driver, _: sign_current(driver),
        dangky_fn=lambda *_: do_nothing(),
    )

# his bug
# @_trace
# def phieudutrucungcapmau(driver: Driver):
#     "Filter and sign name: *Phiếu dự trù và cung cấp máu*"
#     filter_check_expand_sign(
#         driver,
#         name="Phiếu dự trù và cung cấp máu",
#         chuaky_fn=lambda driver, i: sign_tab(driver,i,),
#         dangky_fn=lambda *_: do_nothing(),
#     )
