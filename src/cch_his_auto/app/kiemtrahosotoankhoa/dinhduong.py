from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru.tabs import (
    thongtinchung,
    change_tab,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru.bottom.sanglocdinhduong import (
    add_all_phieusanglocdinhduong,
)
from .config import Config


def run(d: Driver, cfg:Config):
    if not cfg.dinhduong:
        return
    print("Start dinhduong")
    change_tab(d, thongtinchung.TAB_NUMBER)
    add_all_phieusanglocdinhduong(d)
