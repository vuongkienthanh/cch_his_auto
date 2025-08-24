import datetime as dt
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig
from cch_his_auto.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.common_tasks.signature import try_get_signature


from cch_his_auto_lib.driver import Driver, start_driver
from cch_his_auto_lib.action import danhsachnguoibenhnoitru
from cch_his_auto_lib.task import auth
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    tab_thongtinchung,
    top_hosobenhan,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru.top_hosobenhan import (
    tab_hosokhamchuabenh,
)

from . import config, dinhduong, thongtinxv, nhommau


TITLE = "Kiểm tra hồ sơ"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        info.grid(row=0, column=0, sticky="N", pady=20)

        final_var = tk.BooleanVar()

        optionframe = tk.Frame(self)
        optionframe.grid(row=1, column=0, sticky="EW", padx=10)

        add_all_phieuDD_btn = tk.Button(optionframe, text="Add all phiếu dinh dưỡng")
        add_nhommau_btn = tk.Button(optionframe, text="Add Nhóm máu")
        check_thongtinxv_btn = tk.Button(optionframe, text="Check thông tin XV")

        add_all_phieuDD_btn.grid(row=0, column=0, padx=5)
        add_nhommau_btn.grid(row=0, column=1, padx=5)
        check_thongtinxv_btn.grid(row=0, column=2, padx=5)

        tk.Checkbutton(optionframe, text="Dự XV", variable=final_var).grid(
            row=0, column=3
        )

        tk.Label(self, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=3, column=0, padx=20, sticky="NEW"
        )
        listing = scrolledtext.ScrolledText(self)
        listing.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["username"])
            bacsi.set_password(cfg["password"])
            bacsi.set_department(cfg["department"])

            listing.delete("1.0", "end")
            listing.insert("1.0", "\n".join([str(ma_hs) for ma_hs in cfg["listing"]]))
            final_var.set(cfg["final"])

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "listing": [
                    int(ma_hs)
                    for ma_hs in listing.get("1.0", "end").strip().splitlines()
                ],
                "final": final_var.get(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        add_all_phieuDD_btn.configure(
            command=lambda: dinhduong.run(get_config(), button_frame.get_config())
        )
        check_thongtinxv_btn.configure(
            command=lambda: thongtinxv.run(get_config(), button_frame.get_config())
        )
        add_nhommau_btn.configure(
            command=lambda: nhommau.run(get_config(), button_frame.get_config())
        )
        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    if cfg["final"]:
        process = process_final_sign
    else:
        process = process_normal_sign

    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:
        with auth.session(d, cfg["username"], cfg["password"], cfg["department"]):
            with create_connection() as con:
                danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all(d)

                ma_hs = cfg["listing"].pop()
                first_patient(d, con, ma_hs)
                signature = try_get_signature(d, con, ma_hs)
                process(d, signature)

                while len(cfg["listing"]) > 0:
                    ma_hs = cfg["listing"].pop()
                    next_patient(d, con, ma_hs)
                    signature = try_get_signature(d, con, ma_hs)
                    process(d, signature)

    messagebox.showinfo(message="finish")


def process_normal_sign(d: Driver, signature: str | None):
    with top_hosobenhan.session(d):
        tab_hosokhamchuabenh.phieuchidinhxetnghiem(
            d,
        )
        tab_hosokhamchuabenh.todieutri(d, dt.date.today())
        tab_hosokhamchuabenh.phieuCT(d, signature)
        tab_hosokhamchuabenh.phieuMRI(d, signature)
        tab_hosokhamchuabenh.giaiphaubenh(d)
        tab_hosokhamchuabenh.phieusanglocdinhduong(d)
        tab_hosokhamchuabenh.phieuchidinhPTTT(d)
        tab_hosokhamchuabenh.phieusoket15ngay(d)
        tab_hosokhamchuabenh.phieucamkettruyenmau(d, signature)
        # tab_hosokhamchuabenh.phieucamkettta5( signature) # HIS BUG


def process_final_sign(d: Driver, signature: str | None):
    discharge_date = tab_thongtinchung.get_discharge_date(d)

    with top_hosobenhan.session(d):
        # tab_hosokhamchuabenh.tobiabenhannhikhoa()
        tab_hosokhamchuabenh.mucAbenhannhikhoa(d)
        tab_hosokhamchuabenh.mucBtongketbenhan(d)
        tab_hosokhamchuabenh.phieukhambenhvaovien(d)
        tab_hosokhamchuabenh.todieutri(d, discharge_date)
        tab_hosokhamchuabenh.donthuoc(d)
