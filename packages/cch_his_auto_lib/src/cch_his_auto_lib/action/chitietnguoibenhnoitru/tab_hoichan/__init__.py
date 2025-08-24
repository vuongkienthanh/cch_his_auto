from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru import ACTIVE_PANE
from cch_his_auto_lib.action.editor.sign_staff import (
    bienbanhoichan_thuky,
    bienbanhoichan_truongkhoa,
)

TAB_NUMBER = 7


def sign_BBHC_thuky(d: Driver):
    main_tab = d.current_url
    d.clicking2(
        f"{ACTIVE_PANE} tbody .ant-table-row td:last-child svg:nth-child(2)",
        "BBHC print icon",
    )
    d.clicking(".ant-dropdown li:first-child a", "open BBHC")
    d.goto_newtab_do_smth_then_goback(main_tab, bienbanhoichan_thuky)


def sign_BBHC_truongkhoa(d: Driver):
    main_tab = d.current_url
    d.clicking2(
        f"{ACTIVE_PANE} tbody .ant-table-row td:last-child svg:nth-child(2)",
        "BBHC print icon",
    )
    d.clicking(".ant-dropdown li:first-child a", "open BBHC")
    d.goto_newtab_do_smth_then_goback(main_tab, bienbanhoichan_truongkhoa)
