from rich import print

from cch_his_auto_lib.action import danhsachnguoibenhnoitru
from cch_his_auto_lib.action.top_patient_info import danhsachnguoibenh, get_patient_info
from cch_his_auto_lib.driver import Driver, DriverFn


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


def iterate_patient_list(d: Driver, listing: list[int], f: DriverFn):
    if len(listing) == 0:
        return
    danhsachnguoibenhnoitru.load(d)
    first_patient = listing.pop()
    danhsachnguoibenhnoitru.goto_patient(d, first_patient)
    while len(listing) > 0:
        next_patient = listing.pop()
        danhsachnguoibenh.goto_patient(d, next_patient)


def iterate_all_patient(d: Driver, f: DriverFn):
    l = len(d.find_all(f"{danhsachnguoibenhnoitru.MAIN_TABLE} tr.ant-table-row"))
    for i in range(2, l + 2):
        danhsachnguoibenhnoitru.load(d)
        danhsachnguoibenhnoitru.open_patient(d, i)
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)
        f(d)
