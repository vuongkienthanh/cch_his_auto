import datetime as dt

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import _logger, ACTIVE_PANE

TAB_NUMBER = 1
THONGTINVAOVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(1)"
THONGTINRAVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(3)"

_logger = _logger.getChild("tab_thongtinchung")


def get_admission_date(driver: Driver) -> dt.date:
    try:
        ele = driver.waiting(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(1) b",
            "admission date",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find discharge_date")
        raise NoSuchElementException("should exist admission_date")
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _logger.info(f"admission_date={date}")
        return date


def get_discharge_date(driver: Driver) -> dt.date | None:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(4) b",
            "discharge date",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find discharge_date")
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _logger.info(f"discharge_date={date}")
        return date


def get_appointment_date(driver: Driver) -> dt.date | None:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(5) b",
            "appointment date",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find appointment_date")
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _logger.info(f"appointment_date={date}")
        return date


def get_discharge_diagnosis(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(1) b",
            "discharge diagnosis",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find discharge_diagnosis")
        return None
    else:
        _logger.info(f"discharge_diagnosis={ele}")
        return ele


def get_discharge_comorbid(driver: Driver) -> list[str]:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(2) b",
            "discharge comormid",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find discharge_comorbid")
        return []
    else:
        _logger.info(f"discharge_comorbid={ele}")
        return ele.split("; ")


def get_discharge_diagnosis_detail(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(3) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find discharge_diagnosis_detail")
        return None
    else:
        _logger.info(f"discharge_diagnosis_detail={ele}")
        return ele

def get_treatment(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(4) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find treatment")
        return None
    else:
        _logger.info(f"treatment={ele}")
        return ele


def get_bloodtype(driver: Driver) -> str | None:
    try:
        ele = driver.waiting(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(6) b",
            "bloodtype",
        ).text
    except NoSuchElementException:
        _logger.warning("=> can't find bloodtype")
        return None
    else:
        _logger.info(f"bloodtype={ele}")
        if ele.strip() == "Chưa xác định":
            return None
        return ele
