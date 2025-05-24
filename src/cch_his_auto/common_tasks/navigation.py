from sqlite3 import Connection
import logging

from cch_his_auto.global_db import get_url_from_db

from cch_his_auto_lib.driver import get_global_driver
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


def first_patient(con: Connection, ma_hs: int):
    _d = get_global_driver()
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        _d.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(ma_hs)
    log_patient(
        _d.waiting(".name span").text,
        _d.current_url,
        str(ma_hs),
    )


def next_patient(con: Connection, ma_hs: int):
    _d = get_global_driver()
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        _d.goto(url)
    else:
        top_danhsachnguoibenh.open_dialog()
        top_danhsachnguoibenh.goto_patient(ma_hs)
    log_patient(
        _d.waiting(".name span").text,
        _d.current_url,
        str(ma_hs),
    )
