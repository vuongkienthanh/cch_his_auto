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


def first_patient(d:Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        d.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(d,ma_hs)
    log_patient(
        d.waiting(".name span").text,
        d.current_url,
        str(ma_hs),
    )


def next_patient(d: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        _logger.info(f"found {ma_hs} in db")
        d.goto(url)
    else:
        top_danhsachnguoibenh.open_dialog(d)
        top_danhsachnguoibenh.goto_patient(d,ma_hs)
    log_patient(
        d.waiting(".name span").text,
        d.current_url,
        str(ma_hs),
    )
