from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.button_frame import RunConfig, setLogLevel
from cch_his_auto.common_tasks.navigation import first_patient, next_patient

from cch_his_auto_lib.driver import start_global_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    tab_thongtinchung,
    top_hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.top_hosobenhan import (
    tab_dvkt,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.tab_thongtinchung import (
    edit_thongtinvaovien,
)
from . import config

TITLE = "Nhóm máu"


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    def process():
        bloodtype = tab_thongtinchung.get_bloodtype()
        if bloodtype is None:
            with top_hosobenhan.session(tab_dvkt.TAB_NUMBER):
                found_bloodtype = tab_dvkt.get_bloodtype()
            if found_bloodtype is not None:
                with edit_thongtinvaovien.session():
                    edit_thongtinvaovien.set_bloodtype(found_bloodtype)

    setLogLevel(run_cfg)
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]

    with start_global_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH):
        with auth.session(cfg["username"], cfg["password"], cfg["department"]):
            with create_connection() as con:
                danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all()

                ma_hs = listing.pop()
                first_patient(con, ma_hs)
                process()

                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(con, ma_hs)
                    process()
    messagebox.showinfo(message="finish")
