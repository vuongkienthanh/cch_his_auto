import logging
import datetime as dt

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs import _lgr, ACTIVE_PANE

TAB_NUMBER = 0

_lgr = logging.getLogger("tab_thongtinchung")

THONGTINVAOVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(1)"
THONGTINRAVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(3)"


def get_admission_date(d: Driver) -> dt.date:
    try:
        ele = d.waiting(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(1) b",
            "admission date",
        ).text
    except NoSuchElementException:
        raise NoSuchElementException("should exist admission_date")
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"admission_date={date}")
        return date


def get_discharge_date(d: Driver) -> dt.date | None:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(4) b",
            "discharge date",
        ).text
    except NoSuchElementException:
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"discharge_date={date}")
        return date


def get_appointment_date(d: Driver) -> dt.date | None:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(5) b",
            "appointment date",
        ).text
    except NoSuchElementException:
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"appointment_date={date}")
        return date


def get_discharge_diagnosis(d: Driver) -> str | None:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(1) b",
            "discharge diagnosis",
        ).text
    except NoSuchElementException:
        return None
    else:
        _lgr.info(f"discharge_diagnosis={ele}")
        return ele


def get_discharge_comorbid(d: Driver) -> list[str]:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(2) b",
            "discharge comormid",
        ).text
    except NoSuchElementException:
        return []
    else:
        _lgr.info(f"discharge_comorbid={ele}")
        return ele.split("; ")


def get_discharge_diagnosis_detail(d: Driver) -> str | None:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(3) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        return None
    else:
        _lgr.info(f"discharge_diagnosis_detail={ele}")
        return ele


def get_treatment(d: Driver) -> str | None:
    try:
        ele = d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(4) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        return None
    else:
        _lgr.info(f"treatment={ele}")
        return ele


def get_bloodtype(d: Driver) -> str | None:
    try:
        ele = d.find(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(6) b",
        ).text.strip()
    except NoSuchElementException:
        return None
    else:
        _lgr.info(f"bloodtype={ele}")
        if ele == "Chưa xác định" or ele == "":
            return None
        return ele
