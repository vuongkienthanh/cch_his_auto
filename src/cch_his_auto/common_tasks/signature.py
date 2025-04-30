import sqlite3
import logging

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_indieuduong import (
    get_signature,
)
from cch_his_auto_lib.tasks.danhsachnguoibenhnoitru import (
    URL as DSNBNT_URL,
    goto_patient,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import URL as CTNBNT_URL


_logger = logging.getLogger().getChild("app")


def try_get_signature(
    driver: Driver, con: sqlite3.Connection, ma_hs: int
) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        _logger.info("***** patient signature found in db")
        return signature
    else:
        _logger.info("***** patient signature not found in db")
        working_url = driver.current_url
        if not working_url.startswith(CTNBNT_URL):
            driver.goto(DSNBNT_URL)
            goto_patient(driver, ma_hs)
        if signature := get_signature(driver):
            url = driver.current_url
            save_db(con, ma_hs, url, signature)
            _logger.info("patient signature saved")
            if not working_url.startswith(CTNBNT_URL):
                driver.goto(working_url)
            return signature
        else:
            return None
