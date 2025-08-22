import sqlite3
import logging

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_indieuduong import (
    get_signature_data,
)
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru

_logger = logging.getLogger("app")


def try_get_signature(d: Driver, con: sqlite3.Connection, ma_hs: int) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        _logger.info("***** patient signature found in db")
        return signature
    else:
        _logger.info("***** patient signature not found in db")
        working_url = d.current_url
        d.goto(danhsachnguoibenhnoitru.URL)
        danhsachnguoibenhnoitru.goto_patient(d, ma_hs)
        try:
            if signature := get_signature_data(d):
                save_db(con, ma_hs, d.current_url, signature)
                _logger.info("patient signature saved")
                return signature
            else:
                return None
        finally:
            d.goto(working_url)
