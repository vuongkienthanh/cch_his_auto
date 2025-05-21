import logging
import tkinter as tk
from tkinter import messagebox
import datetime as dt
from typing import Literal, get_args

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig, setLogLevel
from cch_his_auto.common_tasks.signature import try_get_signature

from . import config
from .patient_list import PatientFrame
from .dutrumau_list import DutruMauFrame
from .bbhc_list import BBHCFrame

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tasks import auth
from cch_his_auto_lib.tasks.todieutri.bot_ingiayto import (
    sign_todieutri,
    sign_phieuchidinh,
    sign_phieuthuchienylenh_bn,
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru import (
    top_hosobenhan,
)
from cch_his_auto_lib.tasks.chitietnguoibenhnoitru.top_hosobenhan.tab_hosokhamchuabenh.helper import (
    filter_check_expand_sign,
    sign_tab,
)
from cch_his_auto_lib.tasks.editor import sign_staff_name


TITLE = "Khám bệnh mỗi ngày"
_logger = logging.getLogger("app")


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        truongkhoa = UsernamePasswordFrame(info, text="Trưởng khoa")
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)
        truongkhoa.grid(row=0, column=2)
        dept_var = tk.StringVar()
        tk.Label(info, text="Khoa lâm sàng:", justify="right").grid(
            row=1, column=0, sticky="E"
        )
        tk.Entry(info, textvariable=dept_var).grid(row=1, column=1, sticky="W")
        info.grid(row=0, column=0, sticky="N", pady=20)

        patient_frame = PatientFrame(self)
        patient_frame.grid(row=1, column=0, sticky="NSEW")
        dutrumau_frame = DutruMauFrame(self)
        dutrumau_frame.grid(row=2, column=0, sticky="NSEW")
        bbhc_frame = BBHCFrame(self)
        bbhc_frame.grid(row=3, column=0, sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=4, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            for w, name in zip(
                [bacsi, dieuduong, truongkhoa],  # widgets
                ["bacsi", "dieuduong", "truongkhoa"],  # dict names
            ):
                w.set_username(cfg[name]["username"])
                w.set_password(cfg[name]["password"])

            dept_var.set(cfg["department"])

            for w, name in zip(
                [patient_frame, dutrumau_frame, bbhc_frame],
                ["patients", "dutrumau", "bbhc"],
            ):
                w.clear()
                for p in cfg[name]:
                    w.add_item(p)

            button_frame.load_config()

        def get_config() -> config.Config:
            return {
                "bacsi": {
                    "username": bacsi.get_username(),
                    "password": bacsi.get_password(),
                },
                "dieuduong": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "truongkhoa": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "department": dept_var.get(),
                "patients": patient_frame.get_items(),
                "dutrumau": dutrumau_frame.get_items(),
                "bbhc": bbhc_frame.get_items(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    if not config.is_patient_list_valid(cfg):
        messagebox.showerror(message="Sai data đầu vào")
        return

    setLogLevel(run_cfg)
    driver = Driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH)

    try:
        if config.is_valid(cfg, "bacsi"):
            with auth.session(
                driver,
                cfg["bacsi"]["username"],
                cfg["bacsi"]["password"],
                cfg["department"],
            ):
                run_bs(driver, cfg)

        if config.is_valid(cfg, "dieuduong"):
            with auth.session(
                driver,
                cfg["dieuduong"]["username"],
                cfg["dieuduong"]["password"],
                cfg["department"],
            ):
                run_dd(driver, cfg)

        if any(p["ky_3tra"]["benhnhan"] for p in cfg["patients"]):
            for user in get_args(Literal["bacsi", "dieuduong"]):
                if config.is_valid(cfg, user):
                    with auth.session(
                        driver,
                        cfg[user]["username"],
                        cfg[user]["password"],
                        cfg["department"],
                    ):
                        run_bn(driver, cfg)
                    break
    finally:
        driver.quit()
        messagebox.showinfo(message="finish")


def run_bs(driver: Driver, cfg: config.Config):
    d = dt.date.today()
    for p in cfg["patients"]:
        driver.goto(p["url"])
        log_patient_name(driver.waiting(".name span").text)

        if p["ky_xn"]:
            sign_phieuchidinh(driver)
        if p["ky_todieutri"]:
            sign_todieutri(driver)
        if any(p["ky_3tra"]["bacsi"]):
            sign_phieuthuchienylenh_bs(driver, p["ky_3tra"]["bacsi"])
        if any([p["ky_ct"], p["ky_mri"]]):
            with top_hosobenhan.session(driver):
                if p["ky_ct"]:
                    filter_check_expand_sign(
                        driver,
                        name="Phiếu chỉ định chụp cắt lớp vi tính (CT)",
                        chuaky_fn=lambda driver, i: sign_tab(
                            driver, i, sign_staff_name.phieuCT_bschidinh
                        ),
                        date=d,
                    )
                if p["ky_mri"]:
                    filter_check_expand_sign(
                        driver,
                        name="Phiếu chỉ định chụp cộng hưởng từ (MRI)",
                        chuaky_fn=lambda driver, i: sign_tab(
                            driver, i, sign_staff_name.phieuMRI_bschidinh
                        ),
                        date=d,
                    )


def run_dd(driver: Driver, cfg: config.Config):
    for p in cfg["patients"]:
        if any(p["ky_3tra"]["dieuduong"]):
            driver.goto(p["url"])
            log_patient_name(driver.waiting(".name span").text)
            sign_phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])


def run_bn(driver: Driver, cfg: config.Config):
    with create_connection() as con:
        for p in cfg["patients"]:
            driver.goto(p["url"])
            log_patient_name(driver.waiting(".name span").text)
            ma_hs = int(
                driver.waiting(
                    ".patient-information .additional-item:nth-child(2) .info",
                    "ma ho so",
                ).text
            )
            if signature := try_get_signature(driver, con, ma_hs):
                if any(p["ky_3tra"]["benhnhan"]):
                    sign_phieuthuchienylenh_bn(
                        driver, p["ky_3tra"]["benhnhan"], signature
                    )


def log_patient_name(name: str):
    _logger.info(
        "\n".join(
            [
                "",
                "~" * 50,
                f"patient: {name}",
                "~" * 50,
            ]
        )
    )
