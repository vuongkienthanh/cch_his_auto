import time

from rich import print
from rich.panel import Panel

from cch_his_auto_lib.driver import Driver, DriverFn
from cch_his_auto_lib.tracing import console
from cch_his_auto_lib.action import danhsachnguoibenhnoitru as dsnbnt
from cch_his_auto_lib.action.danhsachnguoibenhnoitru import (
    main_table as dsnbnt_main_table,
)
from cch_his_auto_lib.action import top_info
from cch_his_auto_lib.action.top_info import danhsachnguoibenh
from cch_his_auto_lib.action import chitietnguoibenhnoitru
from cch_his_auto_lib.action.chitietnguoibenhnoitru.indieuduong import (
    camketchungvenhapvien,
)


def pprint_patient_info(p: dict[str, str]):
    print(
        Panel(
            "\n".join(
                [
                    f"patient: {p['name']}",
                    f"ma_hs: {p['ma_hs']}",
                ]
            ),
            expand=False,
            style="white bold",
        )
    )


def iterate_patient_list(d: Driver, listing: list[int], f: DriverFn):
    if len(listing) == 0:
        return
    dsnbnt.load(d)
    first_patient = listing.pop()
    dsnbnt_main_table.goto_patient(d, first_patient)
    while len(listing) > 0:
        next_patient = listing.pop()
        danhsachnguoibenh.goto_patient(d, next_patient)
        f(d)


def iterate_all_patient(d: Driver, f: DriverFn):
    l = len(d.find_all(f"{dsnbnt_main_table.MAIN_TABLE} tr.ant-table-row"))
    for i in range(2, l + 2):
        dsnbnt.load(d)
        dsnbnt_main_table.open_patient(d, i)
        pinfo = top_info.get_patient_info(d)
        pprint_patient_info(pinfo)
        f(d)
    if dsnbnt.has_next_page(d):
        console.print("[bold]Danh sách người bệnh nội trú[/bold]: go to next page")
        dsnbnt.click_next_page(d)
        iterate_all_patient(d, f)
    else:
        console.print("[bold]Danh sách người bệnh nội trú[/bold]: reach the end of patient list")


def get_signature_from_HIS(d: Driver, ma_hs: int) -> str | None:
    working_url = d.current_url
    dsnbnt.load_and_clear(d)
    dsnbnt_main_table.goto_patient(d, ma_hs)
    signature = d.do_next_tab_do(
        f1=lambda d: chitietnguoibenhnoitru.click_indieuduong(d, "cam kết"),
        f2=lambda d: camketchungvenhapvien.get_signature(d),
    )
    d.goto(working_url)
    time.sleep(5)
    return signature
