import sqlite3
import logging

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_indieuduong import (
    get_signature,
)
from cch_his_auto_lib.tasks import danhsachnguoibenhnoitru

_logger = logging.getLogger("app")


def try_get_signature(con: sqlite3.Connection, ma_hs: int) -> str | None:
    _d = get_global_driver()
    if signature := get_signature_from_db(con, ma_hs):
        _logger.info("***** patient signature found in db")
        return signature
    else:
        _logger.info("***** patient signature not found in db")
        working_url = _d.current_url
        _d.goto(danhsachnguoibenhnoitru.URL)
        danhsachnguoibenhnoitru.goto_patient(ma_hs)
        try:
            if signature := get_signature():
                save_db(con, ma_hs, _d.current_url, signature)
                _logger.info("patient signature saved")
                return signature
            else:
                return None
        finally:
            _d.goto(working_url)
