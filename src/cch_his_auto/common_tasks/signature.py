import sqlite3
from rich import print

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom.dieuduong.camketchungvenhapvien import (
    get_signature_from_HIS,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom import indieuduong
from cch_his_auto_lib.action import danhsachnguoibenhnoitru


def try_get_signature(d: Driver, con: sqlite3.Connection, ma_hs: int) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        print("[green]patient signature found in db")
        return signature
    else:
        print("[green]patient signature not found in db")
        working_url = d.current_url
        danhsachnguoibenhnoitru.load(d)
        danhsachnguoibenhnoitru.goto_patient(d, ma_hs)
        signature = d.do_next_tab_do(
            f1=lambda d: indieuduong(d, "cam kết"),
            f2=lambda d: get_signature_from_HIS(d),
        )

        if signature:
            save_db(con, ma_hs, d.current_url, signature)
            print("[green]patient signature saved")

        d.goto(working_url)
        return signature
