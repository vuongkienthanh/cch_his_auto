import datetime as dt

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.helper import tracing
from .. import (
    _logger,
)

TAB_NUMBER = 1
_logger = _logger.getChild("tab_hosokhamchuabenh")
_trace = tracing(_logger)

from .helper import (
    filter_check_expand_sign,
    sign_tab,
    sign_current,
    sign_current2,
    sign_current_both,
)
from cch_his_auto_lib.tasks.editor import (
    sign_staff_name,
    sign_patient_name,
    check_agreement,
)


@_trace
def tobiabenhannhikhoa(driver: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    filter_check_expand_sign(
        driver,
        name="Tờ bìa bệnh án Nhi khoa",
        chuaky_fn=lambda driver, i: sign_tab(
            driver, i, sign_staff_name.tobiabenhannhikhoa
        ),
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
    )


@_trace
def phieukhambenhvaovien(driver: Driver):
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    filter_check_expand_sign(
        driver,
        name="Phiếu khám bệnh vào viện",
        chuaky_fn=lambda driver, _: sign_current(driver),
    )


@_trace
def phieuchidinhxetnghiem(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định xét nghiệm",
        chuaky_fn=lambda driver, _: sign_current(driver),
    )


@_trace
def todieutri(driver: Driver, discharge_date: dt.date | None):
    "Filter and sign name: *Tờ điều trị*"

    def chuaky_fn(driver: Driver, i: int):
        if discharge_date:
            date = dt.datetime.strptime(
                driver.find(f".ant-table-tbody tr:nth-child({i}) td:nth-child(2)").text[
                    :10
                ],
                "%d/%m/%Y",
            ).date()
            if date < discharge_date:
                sign_tab(driver, i, sign_staff_name.todieutri)
            else:
                _logger.info("date >= discharge_date => skip")
        else:
            sign_tab(driver, i, sign_staff_name.todieutri)

    filter_check_expand_sign(
        driver,
        name="Tờ điều trị",
        chuaky_fn=lambda driver, i: chuaky_fn(driver, i),
    )


@_trace
def phieuchidinhPTTT(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định PTTT",
        chuaky_fn=lambda driver, _: sign_current(driver),
    )


@_trace
def phieuCT_bschidinh(driver: Driver):
    def chuaky_fn(driver):
        sign_staff_name.phieuCT_bschidinh(driver)

    filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
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
    )


@_trace
def phieusanglocdinhduong(driver: Driver):
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    filter_check_expand_sign(
        driver,
        name="Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú",
        chuaky_fn=lambda driver, _: sign_current(driver),
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
    )


@_trace
def phieucamkettruyenmau(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu cam kết truyền máu*"

    def chuaky_fn(driver):
        if signature:
            check_agreement.check_phieucamkettruyenmau(driver)
            sign_patient_name.phieucamkettruyenmau_bn(driver, signature)

    filter_check_expand_sign(
        driver,
        name="Giấy cam đoan chấp nhận truyền máu và các chế phẩm của máu",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
    )


@_trace
def phieucamkettta5(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu cam kết thủ thuật a5*"

    def chuaky_fn(driver):
        check_agreement.check_phieucamkettta5(driver)
        sign_staff_name.phieucamkettta5(driver)
        dangky_fn(driver)

    def dangky_fn(driver):
        if signature:
            sign_patient_name.phieucamkettta5(driver, signature)

    filter_check_expand_sign(
        driver,
        name="Giấy cam đoan chấp nhận phẫu thuật, thủ thuật và gây mê hồi sức(của BN) (A5)",
        chuaky_fn=lambda driver, i: sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda driver, i: sign_tab(driver, i, dangky_fn),
    )
