import logging
import datetime as dt

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import _lgr, ACTIVE_PANE

TAB_NUMBER = 1

_lgr = logging.getLogger("tab_thongtinchung")

THONGTINVAOVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(1)"
THONGTINRAVIEN_CSS = f"{ACTIVE_PANE} .info:nth-child(3)"


def get_admission_date() -> dt.date:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(1) b",
            "admission date",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find discharge_date")
        raise NoSuchElementException("should exist admission_date")
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"admission_date={date}")
        return date


def get_discharge_date() -> dt.date | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(4) b",
            "discharge date",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find discharge_date")
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"discharge_date={date}")
        return date


def get_appointment_date() -> dt.date | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(2) .item-sub:nth-child(5) b",
            "appointment date",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find appointment_date")
        return None
    else:
        date = dt.datetime.strptime(
            ele,
            "%d/%m/%Y %H:%M:%S",
        ).date()
        _lgr.info(f"appointment_date={date}")
        return date


def get_discharge_diagnosis() -> str | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(1) b",
            "discharge diagnosis",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find discharge_diagnosis")
        return None
    else:
        _lgr.info(f"discharge_diagnosis={ele}")
        return ele


def get_discharge_comorbid() -> list[str]:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(2) b",
            "discharge comormid",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find discharge_comorbid")
        return []
    else:
        _lgr.info(f"discharge_comorbid={ele}")
        return ele.split("; ")


def get_discharge_diagnosis_detail() -> str | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(3) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find discharge_diagnosis_detail")
        return None
    else:
        _lgr.info(f"discharge_diagnosis_detail={ele}")
        return ele


def get_treatment() -> str | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINRAVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(4) b",
            "discharge diagnosis detail",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find treatment")
        return None
    else:
        _lgr.info(f"treatment={ele}")
        return ele


def get_bloodtype() -> str | None:
    _d = get_global_driver()
    try:
        ele = _d.waiting(
            f"{THONGTINVAOVIEN_CSS} .ant-col:nth-child(1) .item-sub:nth-child(6) b",
            "bloodtype",
        ).text
    except NoSuchElementException:
        _lgr.warning("=> can't find bloodtype")
        return None
    else:
        _lgr.info(f"bloodtype={ele}")
        if ele.strip() == "Chưa xác định":
            return None
        return ele
