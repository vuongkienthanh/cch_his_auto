import os.path
import logging

TITLE = "Ký tờ điều trị hằng ngày"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

import tkinter as tk
from tkinter import messagebox

from . import config

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.todieutri import ingiayto as igt

_logger = logging.getLogger()

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        from cch_his_auto.app.common_ui.staff_info import UsernamePasswordFrame
        from .patient_list import PatientFrame

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)
        dept_var = tk.StringVar()
        headless_var = tk.BooleanVar()
        tk.Label(info, text="Khoa lâm sàng:", justify="right").grid(
            row=1, column=0, sticky="E"
        )
        tk.Entry(info, textvariable=dept_var).grid(row=1, column=1, sticky="W")
        tk.Checkbutton(
            info,
            text="Headless Chrome",
            variable=headless_var,
        ).grid(row=2, column=0, columnspan=2, pady=5)

        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = PatientFrame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")

        def load():
            mainframe.clear()
            cf = config.load()
            headless_var.set(cf["headless"])
            dept_var.set(cf["department"])
            bacsi.set_username(cf["bacsi"]["username"])
            bacsi.set_password(cf["bacsi"]["password"])
            dieuduong.set_username(cf["dieuduong"]["username"])
            dieuduong.set_password(cf["dieuduong"]["password"])
            for p in cf["patients"]:
                mainframe.add_patient(p)

        def get_config() -> config.Config:
            return {
                "headless": headless_var.get(),
                "bacsi": {
                    "username": bacsi.get_username(),
                    "password": bacsi.get_password(),
                },
                "dieuduong": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "patients": mainframe.get_patients(),
                "department": dept_var.get(),
            }

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                messagebox.showinfo(message="Đã lưu")

        btns = tk.Frame(self)
        load_btn = tk.Button(btns, text="Load", command=load, width=10)
        load_btn.grid(row=0, column=0, pady=5)
        save_btn = tk.Button(btns, text="Save", command=save, width=10)
        save_btn.grid(row=1, column=0, pady=5)
        new_btn = tk.Button(
            btns, text="Add", command=lambda: mainframe.add_new(), width=10
        )
        new_btn.grid(row=2, column=0, pady=5)
        run_btn = tk.Button(
            btns,
            text="RUN",
            command=lambda: run(get_config()),
            width=10,
            bg="#ff0073",
            fg="#ffffff",
        )
        run_btn.grid(row=3, column=0, pady=5)
        btns.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

def run(cf: config.Config):
    from cch_his_auto.app import PROFILE_PATH
    from cch_his_auto.tasks.auth import session

    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)

    try:
        if config.is_patient_list_valid(cf):
            bs, dd = config.is_bs_valid(cf), config.is_dd_valid(cf)
            driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
            match (bs, dd):
                case (True, True):
                    with session(
                        driver,
                        cf["bacsi"]["username"],
                        cf["bacsi"]["password"],
                        cf["department"],
                    ):
                        run_bs(driver, cf)

                    with session(
                        driver,
                        cf["dieuduong"]["username"],
                        cf["dieuduong"]["password"],
                        cf["department"],
                    ):
                        run_dd(driver, cf)
                        run_bn(driver, cf)
                case (True, False):
                    with session(
                        driver,
                        cf["bacsi"]["username"],
                        cf["bacsi"]["password"],
                        cf["department"],
                    ):
                        run_bs(driver, cf)
                        run_bn(driver, cf)
                    messagebox.showerror(message="chưa nhập điều dưỡng")
                case (False, True):
                    with session(
                        driver,
                        cf["dieuduong"]["username"],
                        cf["dieuduong"]["password"],
                        cf["department"],
                    ):
                        run_dd(driver, cf)
                        run_bn(driver, cf)
                    messagebox.showerror(message="chưa nhập bác sĩ")
                case _:
                    messagebox.showerror(message="chưa nhập bác sĩ, điều dưỡng")

        else:
            messagebox.showerror(message="không có bệnh nhân")
    finally:
        driver.quit()
        messagebox.showinfo(message="finish")

def run_bs(driver: Driver, cf: config.Config):
    for p in cf["patients"]:
        driver.goto(p["url"])
        _logger.info(f"patient: {driver.waiting('.name span').text}")

        if p["ky_xetnghiem"]:
            igt.phieuchidinh(driver)
        if p["ky_todieutri"]:
            igt.todieutri(driver)
        if any(p["ky_3tra"]["bacsi"]):
            igt.phieuthuchienylenh_bs(driver, p["ky_3tra"]["bacsi"])

def run_dd(driver: Driver, cf: config.Config):
    for p in cf["patients"]:
        driver.goto(p["url"])
        _logger.info(f"patient: {driver.waiting('.name span').text}")
        if any(p["ky_3tra"]["dieuduong"]):
            igt.phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])

def run_bn(driver: Driver, cf: config.Config):
    from cch_his_auto.app.global_db import create_connection
    from cch_his_auto.app.common_tasks.signature import get_signature_from_elsewhere

    with create_connection() as con:
        for p in cf["patients"]:
            driver.goto(p["url"])
            _logger.info(f"patient: {driver.waiting('.name span').text}")
            ma_hs = int(
                driver.waiting(
                    ".patient-information .additional-item:nth-child(2) .info",
                    "ma ho so",
                ).text
            )
            if signature := get_signature_from_elsewhere(driver, con, ma_hs):
                if any(p["ky_3tra"]["benhnhan"]):
                    igt.phieuthuchienylenh_bn(
                        driver, p["ky_3tra"]["benhnhan"], signature
                    )
