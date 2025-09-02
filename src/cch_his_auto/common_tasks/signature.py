import sqlite3
from rich import print

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom.indieuduong import (
    get_signature_data,
)
from cch_his_auto_lib.action import danhsachnguoibenhnoitru


def try_get_signature(d: Driver, con: sqlite3.Connection, ma_hs: int) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        print("[green]patient signature found in db")
        return signature
    else:
        print("[green]patient signature not found in db")
        working_url = d.current_url
        d.goto(danhsachnguoibenhnoitru.URL)
        danhsachnguoibenhnoitru.goto_patient(d, ma_hs)
        try:
            if signature := get_signature_data(d):
                save_db(con, ma_hs, d.current_url, signature)
                print("[green]patient signature saved")
                return signature
            else:
                return None
        finally:
            d.goto(working_url)
