from sqlite3 import Connection
import logging

from cch_his_auto.global_db import get_url_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_danhsachnguoibenh,
)
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru


_logger = logging.getLogger("app")


def log_patient(name: str, url: str, ma_hs: str):
    _logger.info(
        "\n".join(
            [
                "",
                "",
                "~" * 50,
                f"patient: {name}",
                f"url: {url}",
                f"ma_hs: {ma_hs}",
                "~" * 50,
            ]
        )
    )


def first_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        driver.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(driver, ma_hs)
    log_patient(
        driver.waiting(".name span").text,
        driver.current_url,
        str(ma_hs),
    )


def next_patient(driver: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        driver.goto(url)
    else:
        top_danhsachnguoibenh.open_dialog(driver)
        top_danhsachnguoibenh.goto_patient(driver, ma_hs)
    log_patient(
        driver.waiting(".name span").text,
        driver.current_url,
        str(ma_hs),
    )
