import time
import logging
from enum import StrEnum
from typing import Callable

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto.driver import Driver, DriverFn
from cch_his_auto.tasks.editor import sign_staff_name, sign_patient_name
from cch_his_auto.helper import tracing

_logger = logging.getLogger().getChild("hosobenhan")
_trace = tracing(_logger)


class _Status(StrEnum):
    CHUAKY = "Chưa ký"
    DANGKY = "Đang ký"
    HOANTHANH = "Hoàn thành"


@_trace
def open_dialog(driver: Driver):
    driver.clicking(
        ".thong-tin-benh-nhan .bunch-icon div:nth-child(3)", "xem ho so benh an"
    )
    driver.waiting(
        ".ant-modal:has(.img-avatar) .right-content tr:nth-child(2)",
        "Danh sách phiếu first item",
    )


@_trace
def close_dialog(driver: Driver):
    driver.clicking(".ant-modal:has(.img-avatar) .ant-modal-close", "close button")
    driver.wait_closing(".ant-modal .img-avatar", "Hồ sơ bệnh án dialog")


def filter(driver: Driver, name: str) -> bool:
    "Filter document based on `name`"
    _logger.debug(f"name={name}")
    ele = driver.clear_input(".right-content .header input")
    _logger.debug("+++++ typing name")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(60):  # 120 is too long
        time.sleep(1)
        try:
            ele = driver.find(
                ".right-content tbody tr:nth-child(2) td:nth-child(2) div"
            )
            if ele.text.strip().startswith(name):
                _logger.info(f"-> found {name}")
                return True
        except NoSuchElementException:
            ...
    else:
        _logger.warning(f"-> filtered {name} with no result")
        return False


def is_row(driver: Driver, idx: int, status: _Status) -> bool:
    "Check if row at `idx` is _status_, first row is id=2"
    try:
        _logger.debug(f"checking status = {status}")
        return (
            driver.waiting(
                f".ant-table-tbody tr:nth-child({idx}) td:nth-child(3)",
                f"row {idx} status",
            ).text.strip()
            == status
        )
    except StaleElementReferenceException:
        return is_row(driver, idx, status)


def is_row_expandable(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is expandable, first row is id=2"
    name = driver.waiting(
        f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.debug(f"checking {name}: expandable")
    for _ in range(5):
        time.sleep(1)
        try:
            ele = driver.find(
                f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button"
            )
            class_list = ele.get_attribute("class")
            assert class_list is not None
            return "ant-table-row-expand-icon-collapsed" in class_list
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    else:
        return False


def expand_row(driver: Driver, idx: int):
    "Expand row at `idx`"
    name = driver.waiting(
        f".ant-table-tbody tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.info(f"expanding {name}")
    driver.clicking(f".right-content tbody tr:nth-child({idx}) td:nth-child(1) button")


type CheckSign_fn = Callable[[Driver, int], None]


def _filter_check_expand_sign(
    driver: Driver, name: str, chuaky_fn: CheckSign_fn, dangky_fn: CheckSign_fn
):
    def check_and_sign(driver: Driver, i: int):
        name = driver.waiting(
            f".ant-table-tbody tr:nth-child({i}) td:nth-child(2)"
        ).text
        _logger.debug(f"checking {name}")
        if is_row(driver, i, _Status.CHUAKY):
            _logger.info(f"row condition: not met: {name}")
            driver.clicking(f"tbody tr:nth-child({i})")
            chuaky_fn(driver, i)
            time.sleep(5)
        elif is_row(driver, i, _Status.DANGKY):
            dangky_fn(driver, i)
            time.sleep(5)
        else:
            _logger.info("row condition: OK")

    if filter(driver, name) and (
        driver.waiting(
            ".right-content tbody tr:nth-child(2) td:nth-child(3)"
        ).text.strip()
        != _Status.HOANTHANH
    ):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(3, len(driver.find_all("tbody .ant-table-row-level-1")) + 3):
                check_and_sign(driver, i)
        else:
            check_and_sign(driver, 2)


def _unimplemented(_: Driver):
    _logger.warning("not implemented")


def _sign_current(driver: Driver):
    driver.clicking(
        ".right-content .__action button:nth-child(2)", "clicking Ký tên BS dieu tri"
    )


def _sign_current2(driver: Driver):
    driver.clicking(
        ".right-content .__action button:nth-child(3)", "clicking Ký tên BS truong khoa"
    )


def _sign_current_both(driver: Driver):
    _sign_current(driver)
    _sign_current2(driver)


def _sign_tab(driver: Driver, idx: int, sign_fn: DriverFn):
    tab0 = driver.current_window_handle
    datakey = driver.find(f".ant-table-tbody tr:nth-child({idx})").get_attribute(
        "data-row-key"
    )
    _logger.debug(f"data row key = {datakey}")
    driver.clicking(f".ant-table-tbody tr:nth-child({idx})", f"row {idx - 1}")
    time.sleep(2)
    driver.clicking(f"a[data-key='{datakey}'] button", f"edit button {idx - 1}")
    driver.goto_newtab_do_smth_then_goback(tab0, sign_fn)


@_trace
def tobiabenhannhikhoa(driver: Driver):
    "Filter and sign name: *Tờ bìa bệnh án nhi khoa*"
    _filter_check_expand_sign(
        driver,
        name="Tờ bìa bệnh án Nhi khoa",
        chuaky_fn=lambda driver, i: _sign_tab(
            driver, i, sign_staff_name.tobiabenhannhikhoa
        ),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def mucAbenhannhikhoa(driver: Driver):
    "Filter and sign name: *Mục A bệnh án nhi khoa*"
    _filter_check_expand_sign(
        driver,
        name="Mục A - Bệnh án Nhi khoa",
        chuaky_fn=lambda driver, i: _sign_tab(
            driver, i, sign_staff_name.mucAbenhannhikhoa
        ),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def mucBtongketbenhan(driver: Driver):
    "Filter and sign name: *Mục B tổng kết bệnh án*"
    _filter_check_expand_sign(
        driver,
        name="Mục B - Tổng kết Bệnh án (Nội khoa, Nhi Khoa, Truyền nhiễm, Sơ sinh, Da liễu, DD-PHCN, HHTM)",
        chuaky_fn=lambda driver, i: _sign_tab(
            driver, i, sign_staff_name.mucBtongketbenhan
        ),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieukhambenhvaovien(driver: Driver):
    "Filter and sign name: *Phiếu khám bệnh vào viện*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu khám bệnh vào viện",
        chuaky_fn=lambda driver, _: _sign_current(driver),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieuchidinhxetnghiem(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định xét nghiệm*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định xét nghiệm",
        chuaky_fn=lambda driver, _: _sign_current(driver),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def todieutri(driver: Driver):
    "Filter and sign name: *Tờ điều trị*"
    _filter_check_expand_sign(
        driver,
        name="Tờ điều trị",
        chuaky_fn=lambda driver, i: _sign_tab(driver, i, sign_staff_name.todieutri),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieuchidinhPTTT(driver: Driver):
    "Filter and sign name: *Phiếu chỉ định PTTT*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định PTTT",
        chuaky_fn=lambda driver, _: _sign_current(driver),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieuCT(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp CT*"

    def chuaky_fn(driver):
        sign_staff_name.phieuCT_bschidinh(driver)
        sign_staff_name.phieuCT_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuCT_bn(driver, signature)

    def dangky_fn(driver):
        sign_staff_name.phieuCT_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuCT_bn(driver, signature)

    _filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
        chuaky_fn=lambda driver, i: _sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda driver, i: _sign_tab(driver, i, dangky_fn),
    )


@_trace
def phieuMRI(driver: Driver, signature: str | None):
    "Filter and sign name: *Phiếu chỉ định chụp MRI*"

    def chuaky_fn(driver):
        sign_staff_name.phieuMRI_bschidinh(driver)
        sign_staff_name.phieuMRI_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuMRI_bn(driver, signature)

    def dangky_fn(driver):
        sign_staff_name.phieuMRI_bsthuchien(driver)
        if signature:
            sign_patient_name.phieuMRI_bn(driver, signature)

    _filter_check_expand_sign(
        driver,
        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
        chuaky_fn=lambda driver, i: _sign_tab(driver, i, chuaky_fn),
        dangky_fn=lambda driver, i: _sign_tab(driver, i, dangky_fn),
    )


@_trace
def giaiphaubenh(driver: Driver):
    "Filter and sign name: *Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu xét nghiệm giải phẫu bệnh sinh thiết",
        chuaky_fn=lambda driver, i: _sign_tab(driver, i, sign_staff_name.giaiphaubenh),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieusanglocdinhduong(driver: Driver):
    "Filter and sign name: *Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu sàng lọc dinh dưỡng - Bệnh nhi nội trú",
        chuaky_fn=lambda driver, _: _sign_current(driver),
        dangky_fn=lambda driver, _: _unimplemented(driver),
    )


@_trace
def phieusoket15ngay(driver: Driver):
    "Filter and sign name: *Phiếu sơ kết 15 ngày điều trị*"
    _filter_check_expand_sign(
        driver,
        name="Phiếu sơ kết 15 ngày điều trị",
        chuaky_fn=lambda driver, _: _sign_current_both(driver),
        dangky_fn=lambda driver, _: _sign_current2(driver),
    )
