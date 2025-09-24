import sqlite3
from rich import print

from cch_his_auto.global_db import save_db, get_signature_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.common_tasks import get_signature_from_HIS


def try_get_signature(d: Driver, con: sqlite3.Connection, ma_hs: int) -> str | None:
    if signature := get_signature_from_db(con, ma_hs):
        print("[green]patient signature found in db")
        return signature
    else:
        print("[green]patient signature not found in db")
        if signature := get_signature_from_HIS(d, ma_hs):
            print("[green]found patient signature from HIS")
            save_db(con, ma_hs, signature)
            print("[green]patient signature saved")
        else:
            print("[green]can't find patient signature from HIS")
        return signature
