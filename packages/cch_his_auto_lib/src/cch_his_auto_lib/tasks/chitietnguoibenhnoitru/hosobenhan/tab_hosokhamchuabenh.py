import logging
from enum import StrEnum
import datetime as dt
import time
from typing import Callable

from selenium.webdriver import Keys
from selenium.common import NoSuchElementException, StaleElementReferenceException

from cch_his_auto_lib.driver import Driver, DriverFn
from cch_his_auto_lib.helper import tracing
from cch_his_auto_lib.tasks.editor import sign_staff_name, sign_patient_name
from . import ACTIVE_PANE


_logger = logging.getLogger().getChild("hosobenhan")
_trace = tracing(_logger)

TAB_NUMBER = 1
RIGHT_PANEL = f"{ACTIVE_PANE} .right-content"


class Status(StrEnum):
    "Possible status for each document"

    CHUAKY = "Chưa ký"
    DANGKY = "Đang ký"
    HOANTHANH = "Hoàn thành"


def filter(driver: Driver, name: str) -> bool:
    "Filter document based on `name`"
    _logger.debug(f"name={name}")
    ele = driver.clear_input(f"{RIGHT_PANEL} input")
    _logger.debug("+++++ typing name")
    ele.send_keys(name)
    ele.send_keys(Keys.ENTER)
    for _ in range(60):  # 120 is too long
        time.sleep(1)
        try:
            ele = driver.find(f"{RIGHT_PANEL} tr:nth-child(2) td:nth-child(2) div")
            if ele.text.strip().startswith(name):
                _logger.info(f"-> found {name}")
                return True
        except NoSuchElementException:
            ...
    else:
        _logger.warning(f"-> filtered {name} with no result")
        return False


def is_row(driver: Driver, idx: int, status: Status) -> bool:
    "Check if row at `idx` is `status`, first row is idx=2"
    try:
        _logger.debug(f"checking status = {status}")
        return (
            driver.waiting(
                f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(3)",
                f"row {idx} status",
            ).text.strip()
            == status
        )
    except StaleElementReferenceException:
        return is_row(driver, idx, status)


def is_row_expandable(driver: Driver, idx: int) -> bool:
    "Check if row at `idx` is expandable, first row is idx=2"
    name = driver.waiting(
        f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.debug(f"checking {name}: expandable")
    for _ in range(5):
        time.sleep(1)
        try:
            ele = driver.find(
                f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button"
            )
            class_list = ele.get_attribute("class")
            assert class_list is not None
            return "ant-table-row-expand-icon-collapsed" in class_list
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    else:
        return False


def expand_row(driver: Driver, idx: int):
    "Expand row at `idx`, first row is idx=2"
    name = driver.waiting(
        f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(2)", f"row {idx}"
    ).text
    _logger.info(f"expanding {name}")
    driver.clicking(f"{RIGHT_PANEL} tr:nth-child({idx}) td:nth-child(1) button")


def filter_check_expand_sign(
    driver: Driver,
    name: str,
    chuaky_fn: Callable[[Driver, int], None],
    dangky_fn: Callable[[Driver, int], None],
):
    "filter `name`, expand it if possible, then call `fn` respectively bases on status"

    def check_and_sign(driver: Driver, i: int):
        name = driver.waiting(f"{RIGHT_PANEL} tr:nth-child({i}) td:nth-child(2)").text
        _logger.debug(f"checking {name}")
        if is_row(driver, i, Status.CHUAKY):
            _logger.info(f"row condition: not met: {name} -> {Status.CHUAKY}")
            driver.clicking(f"{RIGHT_PANEL} tr:nth-child({i})")
            chuaky_fn(driver, i)
            time.sleep(5)
        elif is_row(driver, i, Status.DANGKY):
            _logger.info(f"row condition: not met: {name} -> {Status.DANGKY}")
            dangky_fn(driver, i)
            time.sleep(5)
        else:
            _logger.info("row condition: OK")

    if filter(driver, name) and (
        driver.waiting(f"{RIGHT_PANEL} tr:nth-child(2) td:nth-child(3)").text.strip()
        != Status.HOANTHANH
    ):
        if is_row_expandable(driver, 2):
            expand_row(driver, 2)
            for i in range(
                3, len(driver.find_all(f"{RIGHT_PANEL} .ant-table-row-level-1")) + 3
            ):
                check_and_sign(driver, i)
        else:
            check_and_sign(driver, 2)


def do_nothing():
    "@private"
    _logger.warning("should not be called")


def sign_current(driver: Driver):
    "@private"
    driver.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(2)", "clicking Ký tên BS dieu tri"
    )


def sign_current2(driver: Driver):
    "@private"
    driver.clicking(
        f"{RIGHT_PANEL} .__action button:nth-child(3)", "clicking Ký tên BS truong khoa"
    )


def sign_current_both(driver: Driver):
    "@private"
    sign_current(driver)
    sign_current2(driver)


def sign_tab(driver: Driver, idx: int, sign_fn: DriverFn):
    "@private"
    tab0 = driver.current_window_handle
    datakey = driver.find(f"{RIGHT_PANEL} tr:nth-child({idx})").get_attribute(
        "data-row-key"
    )
    _logger.debug(f"data row key = {datakey}")
    driver.clicking(f"{RIGHT_PANEL} tr:nth-child({idx})", f"row {idx - 1}")
    time.sleep(2)
    driver.clicking(f"a[data-key='{datakey}'] button", f"edit button {idx - 1}")
    driver.goto_newtab_do_smth_then_goback(tab0, sign_fn)


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
            sign_tab(driver, i, sign_staff_name.todieutri)

    filter_check_expand_sign(
        driver,
        name="Tờ điều trị",
        chuaky_fn=lambda driver, i: chuaky_fn(driver, i),
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
