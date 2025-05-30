from tkinter import messagebox

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.button_frame import RunConfig, setLogLevel
from cch_his_auto.common_tasks.navigation import first_patient, next_patient

from cch_his_auto_lib.driver import start_global_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import tab_thongtinchung

from . import config


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    setLogLevel(run_cfg)
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]

    machanthuong_kemtheo_missing = []
    discharge_date_is_none = []
    appointment_date_is_sat_sun = []

    def check_machanthuong_kemtheo(ma_hs: int):
        diagnosis = tab_thongtinchung.get_discharge_diagnosis()
        if diagnosis is not None:
            if diagnosis.startswith("S") and not any(
                [d[0] in "WYV" for d in tab_thongtinchung.get_discharge_comorbid()]
            ):
                machanthuong_kemtheo_missing.append(ma_hs)

    def check_discharge_date(ma_hs: int):
        date = tab_thongtinchung.get_discharge_date()
        if date is None:
            discharge_date_is_none.append(ma_hs)

    def check_appointment_date(ma_hs: int):
        date = tab_thongtinchung.get_appointment_date()
        # is saturday / sunday
        if date is not None:
            if date.weekday() in [5, 6]:
                appointment_date_is_sat_sun.append(ma_hs)

    def check(ma_hs: int):
        check_machanthuong_kemtheo(ma_hs)
        check_discharge_date(ma_hs)
        check_appointment_date(ma_hs)

    try:
        with start_global_driver(
            headless=run_cfg["headless"], profile_path=PROFILE_PATH
        ):
            with auth.session(cfg["username"], cfg["password"], cfg["department"]):
                with create_connection() as con:
                    danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all()

                    ma_hs = listing.pop()
                    first_patient(con, ma_hs)
                    check(ma_hs)

                    while len(listing) > 0:
                        ma_hs = listing.pop()
                        next_patient(con, ma_hs)
                        check(ma_hs)

    finally:
        is_ok = True
        if len(machanthuong_kemtheo_missing) > 0:
            messagebox.showwarning(
                message="Thiếu mã chấn thương kèm theo:\n"
                + "\n".join([str(x) for x in machanthuong_kemtheo_missing])
            )
            is_ok = False
        if len(discharge_date_is_none) > 0:
            messagebox.showwarning(
                message="Thiếu ngày ra viện:\n"
                + "\n".join([str(x) for x in discharge_date_is_none])
            )
            is_ok = False
        if len(appointment_date_is_sat_sun) > 0:
            messagebox.showwarning(
                message="Ngày tái khám T7 CN:\n"
                + "\n".join([str(x) for x in appointment_date_is_sat_sun])
            )
            is_ok = False
        return is_ok
