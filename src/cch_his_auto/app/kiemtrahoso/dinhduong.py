from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.button_frame import RunConfig
from cch_his_auto.common_tasks.navigation import first_patient, next_patient

from cch_his_auto_lib.driver import start_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_chitietthongtin,
    tab_thongtinchung,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_sanglocdinhduong import (
    add_all_phieusanglocdinhduong,
)
from . import config


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    chieucao_cannang_missing = []

    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:

        def check(ma_hs: int):
            with top_chitietthongtin.session(d):
                if (top_chitietthongtin.get_chieucao(d) is None) or (
                    top_chitietthongtin.get_cannang(d) is None
                ):
                    chieucao_cannang_missing.append(ma_hs)
                    return False
                return True

        def process():
            admission_date = tab_thongtinchung.get_admission_date(d)
            add_all_phieusanglocdinhduong(d, admission_date)

        with auth.session(d, cfg["username"], cfg["password"], cfg["department"]):
            with create_connection() as con:
                danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all(d)

                ma_hs = cfg["listing"].pop()
                first_patient(d, con, ma_hs)
                if check(ma_hs):
                    process()

                while len(cfg["listing"]) > 0:
                    ma_hs = cfg["listing"].pop()
                    next_patient(d, con, ma_hs)
                    if check(ma_hs):
                        process()
    if len(chieucao_cannang_missing) > 0:
        messagebox.showwarning(
            message="Thiếu chiều cao cân nặng ở chi tiết thông tin:\n"
            + "\n".join([str(x) for x in chieucao_cannang_missing])
        )
    messagebox.showinfo(message="finish")
