from sqlite3 import Connection
import logging

from cch_his_auto.global_db import get_url_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_danhsachnguoibenh,
)
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru


_logger = logging.getLogger().getChild("app")


def first_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        driver.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(driver, ma_hs)
        _logger.info(f"patient url is {driver.current_url}")
    _logger.info(f"************ ma_hs= {ma_hs} ************")


def next_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        driver.goto(url)
    else:
        top_danhsachnguoibenh.open_dialog(driver)
        top_danhsachnguoibenh.goto_patient(driver, ma_hs)
        _logger.info(f"patient url is {driver.current_url}")
    _logger.info(f"************ ma_hs= {ma_hs} ************")
