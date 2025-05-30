import datetime as dt
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordDeptFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.common_tasks.signature import try_get_signature


from cch_his_auto_lib.driver import start_global_driver
from cch_his_auto_lib.tasks import auth, danhsachnguoibenhnoitru
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.tab_thongtinchung import (
    edit_thongtinvaovien,
    edit_thongtinravien,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    tab_thongtinchung,
    top_hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.top_hosobenhan import (
    tab_dvkt,
    tab_hosokhamchuabenh,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.bot_sanglocdinhduong import (
    add_all_phieusanglocdinhduong,
)

from . import config, check_cannang_chieucao, check_thongtinxv


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

        dinhduong_var = tk.BooleanVar()
        nhommau_var = tk.BooleanVar()
        normal_sign_var = tk.BooleanVar()
        final_sign_var = tk.BooleanVar()

        def normal_exclusive():
            if final_sign_var.get() == True:
                final_sign_var.set(False)

        def final_exclusive():
            if normal_sign_var.get() == True:
                normal_sign_var.set(False)

        optionframe = tk.Frame(self)
        optionframe.grid(row=1, column=0, sticky="EW")
        tk.Checkbutton(optionframe, text="Dinh dưỡng", variable=dinhduong_var).grid(
            row=0, column=0, padx=20, pady=20, sticky="W"
        )
        tk.Checkbutton(optionframe, text="Nhóm máu", variable=nhommau_var).grid(
            row=1, column=0, padx=20, pady=20, sticky="W"
        )
        tk.Checkbutton(
            optionframe,
            text="Ký thường ngày",
            variable=normal_sign_var,
            command=normal_exclusive,
        ).grid(row=0, column=1, padx=20, pady=20, sticky="W")
        tk.Checkbutton(
            optionframe,
            text="Ký dự XV",
            variable=final_sign_var,
            command=final_exclusive,
        ).grid(row=1, column=1, padx=20, pady=20, sticky="W")
        check_chieucao_cannang_btn = tk.Button(
            optionframe, text="Kiểm tra thông tin dinh dưỡng"
        )
        check_chieucao_cannang_btn.grid(row=0, column=2)
        check_thongtinxv_btn = tk.Button(
            optionframe, text="Kiểm tra thông tin xuất viện"
        )
        check_thongtinxv_btn.grid(row=1, column=2)

        tk.Label(self, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=3, column=0, padx=20, sticky="NEW"
        )
        listing = scrolledtext.ScrolledText(self)
        listing.grid(row=4, column=0, padx=20, pady=10, sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=5, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["username"])
            bacsi.set_password(cfg["password"])
            bacsi.set_department(cfg["department"])

            listing.delete("1.0", "end")
            listing.insert("1.0", cfg["listing"])
            dinhduong_var.set(cfg["dinhduong"])
            nhommau_var.set(cfg["nhommau"])
            normal_sign_var.set(cfg["normal_sign"])
            final_sign_var.set(cfg["final_sign"])

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "listing": listing.get("1.0", "end"),
                "dinhduong": dinhduong_var.get(),
                "nhommau": nhommau_var.get(),
                "normal_sign": normal_sign_var.get(),
                "final_sign": final_sign_var.get(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        check_chieucao_cannang_btn.configure(
            command=lambda: check_cannang_chieucao.run(
                get_config(), button_frame.get_config()
            )
        )
        check_thongtinxv_btn.configure(
            command=lambda: check_thongtinxv.run(
                get_config(), button_frame.get_config()
            )
        )
        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_valid(cfg):
        messagebox.showerror(message="chưa đủ thông tin")
        return

    setLogLevel(run_cfg)
    listing = [int(ma_hs) for ma_hs in cfg["listing"].strip().splitlines()]

    if cfg["dinhduong"]:
        dinhduong = process_dinhduong
    else:
        dinhduong = lambda: ...

    if cfg["nhommau"]:
        nhommau = process_nhommau
    else:
        nhommau = lambda: ...

    if cfg["normal_sign"]:
        normal_sign = process_normal_sign
    else:
        normal_sign = lambda _: ...

    if cfg["final_sign"]:
        final_sign = process_final_sign
    else:
        final_sign = lambda _: ...

    def process(signature: str | None):
        dinhduong()
        nhommau()
        normal_sign(signature)
        final_sign(signature)

    with start_global_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH):
        with auth.session(cfg["username"], cfg["password"], cfg["department"]):
            with create_connection() as con:
                danhsachnguoibenhnoitru.filter_trangthainguoibenh_check_all()

                ma_hs = listing.pop()
                first_patient(con, ma_hs)
                signature = try_get_signature(con, ma_hs)
                process(signature)

                while len(listing) > 0:
                    ma_hs = listing.pop()
                    next_patient(con, ma_hs)
                    signature = try_get_signature(con, ma_hs)
                    process(signature)

    messagebox.showinfo(message="finish")


def process_dinhduong():
    admission_date = tab_thongtinchung.get_admission_date()
    add_all_phieusanglocdinhduong(admission_date)


def process_nhommau():
    bloodtype = tab_thongtinchung.get_bloodtype()
    if bloodtype is None:
        with top_hosobenhan.session(tab_dvkt.TAB_NUMBER):
            found_bloodtype = tab_dvkt.get_bloodtype()
        if found_bloodtype is not None:
            with edit_thongtinvaovien.session():
                edit_thongtinvaovien.set_bloodtype(found_bloodtype)


def process_normal_sign(signature: str | None):
    with top_hosobenhan.session():
        tab_hosokhamchuabenh.phieuchidinhxetnghiem()
        tab_hosokhamchuabenh.todieutri(dt.date.today())
        tab_hosokhamchuabenh.phieuCT(signature)
        tab_hosokhamchuabenh.phieuMRI(signature)
        tab_hosokhamchuabenh.giaiphaubenh()
        tab_hosokhamchuabenh.phieusanglocdinhduong()
        tab_hosokhamchuabenh.phieuchidinhPTTT()
        tab_hosokhamchuabenh.phieusoket15ngay()
        tab_hosokhamchuabenh.phieucamkettruyenmau(signature)
        # tab_hosokhamchuabenh.phieucamkettta5( signature) # HIS BUG


def process_final_sign(signature: str | None):
    discharge_date = tab_thongtinchung.get_discharge_date()

    # mở rộng chữ viết tắt
    viettat_dict = {
        "hp": "hậu phẫu",
        "pt": "phẫu thuật",
        "nmc": "ngoài màng cứng",
        "dmc": "dưới màng cứng",
    }
    detail = tab_thongtinchung.get_discharge_diagnosis_detail()
    if detail is not None:
        detail = detail.lower()
        for k, v in viettat_dict.items():
            detail = detail.replace(k, v)
        with edit_thongtinravien.session():
            edit_thongtinravien.set_discharge_diagnosis_detail(detail)
    treatment = tab_thongtinchung.get_treatment()
    if treatment is not None:
        treatment = treatment.lower()
        for k, v in viettat_dict.items():
            treatment = treatment.replace(k, v)
        with edit_thongtinravien.session():
            edit_thongtinravien.set_treatment(treatment)

    with top_hosobenhan.session():
        # tab_hosokhamchuabenh.tobiabenhannhikhoa()
        tab_hosokhamchuabenh.mucAbenhannhikhoa()
        tab_hosokhamchuabenh.mucBtongketbenhan()
        tab_hosokhamchuabenh.phieukhambenhvaovien()
        tab_hosokhamchuabenh.phieuchidinhxetnghiem()
        tab_hosokhamchuabenh.todieutri(discharge_date)
        tab_hosokhamchuabenh.phieuCT(signature)
        tab_hosokhamchuabenh.phieuMRI(signature)
        tab_hosokhamchuabenh.giaiphaubenh()
        tab_hosokhamchuabenh.phieusanglocdinhduong()
        tab_hosokhamchuabenh.phieuchidinhPTTT()
        tab_hosokhamchuabenh.phieusoket15ngay()
        tab_hosokhamchuabenh.donthuoc()
        tab_hosokhamchuabenh.phieucamkettruyenmau(signature)
        # tab_hosokhamchuabenh.phieucamkettta5( signature) # HIS BUG
