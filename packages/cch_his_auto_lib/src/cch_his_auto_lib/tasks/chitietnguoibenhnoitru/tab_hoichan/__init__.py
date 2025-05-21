from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import ACTIVE_PANE
from cch_his_auto_lib.tasks.editor.sign_staff_name import (
    bienbanhoichan_thuky,
    bienbanhoichan_truongkhoa,
)

TAB_NUMBER = 7


def sign_BBHC_thuky(driver: Driver):
    main_tab = driver.current_url
    driver.clicking2(
        f"{ACTIVE_PANE} tbody .ant-table-row td:last-child svg:nth-child(2)",
        "BBHC print icon",
    )
    driver.clicking(".ant-dropdown li:first-child a", "open BBHC")
    driver.goto_newtab_do_smth_then_goback(main_tab, bienbanhoichan_thuky)


def sign_BBHC_truongkhoa(driver: Driver):
    main_tab = driver.current_url
    driver.clicking2(
        f"{ACTIVE_PANE} tbody .ant-table-row td:last-child svg:nth-child(2)",
        "BBHC print icon",
    )
    driver.clicking(".ant-dropdown li:first-child a", "open BBHC")
    driver.goto_newtab_do_smth_then_goback(main_tab, bienbanhoichan_truongkhoa)
