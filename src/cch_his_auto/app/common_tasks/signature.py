import sqlite3
import logging

_logger = logging.getLogger()

from cch_his_auto.driver import Driver
from cch_his_auto.app.ma_hs_db import exists_in_db, save_db, get_signature_from_db
from cch_his_auto.tasks.chitietnguoibenhnoitru import get_signature_from_web
from cch_his_auto.tasks.danhsachnguoibenhnoitru import URL, goto_patient

def get_signature(driver: Driver, con: sqlite3.Connection, ma_hs: int) -> str:
    if not exists_in_db(con, ma_hs):
        _logger.info("***** patient signature not found in db")
        working_url = driver.current_url
        driver.goto(URL)
        goto_patient(driver, ma_hs)
        driver.waiting(
            ".patient-information .additional-item:nth-child(2) .info", "ma ho so"
        )
        url = driver.current_url
        signature = get_signature_from_web(driver)
        save_db(con, ma_hs, url, signature)
        _logger.info("patient signature saved")
        driver.goto(working_url)
        return signature
    else:
        _logger.info("***** patient signature found in db")
        return get_signature_from_db(con, ma_hs)
