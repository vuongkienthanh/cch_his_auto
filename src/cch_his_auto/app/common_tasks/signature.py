import sqlite3
import logging

from cch_his_auto.driver import Driver
from cch_his_auto.app.global_db import save_db, get_signature_from_db
from cch_his_auto.tasks.chitietnguoibenhnoitru import scrape_signature
from cch_his_auto.tasks.danhsachnguoibenhnoitru import URL, goto_patient

_logger = logging.getLogger().getChild("app")


def get_signature_from_elsewhere(
    driver: Driver, con: sqlite3.Connection, ma_hs: int
) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        _logger.info("***** patient signature found in db")
        return signature
    else:
        _logger.info("***** patient signature not found in db")
        working_url = driver.current_url
        driver.goto(URL)
        goto_patient(driver, ma_hs)
        url = driver.current_url
        if signature := scrape_signature(driver):
            save_db(con, ma_hs, url, signature)
            _logger.info("patient signature saved")
            driver.goto(working_url)
            return signature
        else:
            return None


def get_signature_from_ctnbnt(
    driver: Driver, con: sqlite3.Connection, ma_hs: int
) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        _logger.info("***** patient signature found in db")
        return signature
    else:
        _logger.info("***** patient signature not found in db")
        url = driver.current_url
        if signature := scrape_signature(driver):
            save_db(con, ma_hs, url, signature)
            _logger.info("patient signature saved")
            return signature
        else:
            return None
