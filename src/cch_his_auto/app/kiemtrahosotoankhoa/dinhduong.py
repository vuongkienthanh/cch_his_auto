from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs import (
    thongtinchung,
    change_tab,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom.sanglocdinhduong import (
    add_all_phieusanglocdinhduong,
)


def run(d: Driver):
    change_tab(d, thongtinchung.TAB_NUMBER)
    add_all_phieusanglocdinhduong(d)
