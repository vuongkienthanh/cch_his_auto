from sqlite3 import Connection

from rich import print

from cch_his_auto.global_db import get_url_from_db

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.top_patient_info import (
    danhsachnguoibenh,
)
from cch_his_auto_lib.action import danhsachnguoibenhnoitru


def pprint_patient_info(p: dict[str, str]):
    print(
        "\n".join(
            [
                "",
                "[red]" + "~" * 50 + "[/red]",
                "[red]~"
                + f"[white bold]patient: {p['name']}[/white bold]".center(73)
                + "~[/red]",
                "[red]~"
                + f"[white bold]ma_hs: {p['ma_hs']}[/white bold]".center(73)
                + "~[/red]",
                "[red]" + "~" * 50 + "[/red]",
                "",
            ]
        )
    )


def first_patient(d: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        print(f"found {ma_hs} in db")
        d.goto(url)
    else:
        danhsachnguoibenhnoitru.goto_patient(d, ma_hs)


def next_patient(d: Driver, con: Connection, ma_hs: int):
    if url := get_url_from_db(con, ma_hs):
        print(f"found {ma_hs} in db")
        d.goto(url)
    else:
        danhsachnguoibenh.goto_patient(d, ma_hs)
