import tkinter as tk
from tkinter import messagebox
import os.path

TITLE = "Ký tờ điều trị hằng ngày"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config
from .patient_list import PatientFrame

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.app.common_ui.LogInfo import UsernamePasswordFrame
from cch_his_auto.app.patient_db import create_connection, exists, save_db

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login, logout
from cch_his_auto.tasks.todieutri import ingiayto as igt
from cch_his_auto.tasks.todieutri import dangkyPHCN as dkphcn
from cch_his_auto.tasks.chitietnguoibenhnoitru import get_signature

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(
            info,
            text="Headless Chrome",
            variable=headless,
            onvalue=True,
            offvalue=False,
        )
        headless_btn.grid(row=1, column=0, columnspan=2, pady=5)

        info.grid(row=0, column=0, sticky="N", pady=20)
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)

        mainframe = PatientFrame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")

        def load():
            mainframe.clear()
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["bacsi"]["username"])
            bacsi.set_password(cf["bacsi"]["password"])
            dieuduong.set_username(cf["dieuduong"]["username"])
            dieuduong.set_password(cf["dieuduong"]["password"])
            for p in cf["patients"]:
                mainframe.add_patient(p)

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "bacsi": {
                    "username": bacsi.get_username(),
                    "password": bacsi.get_password(),
                },
                "dieuduong": {
                    "username": dieuduong.get_username(),
                    "password": dieuduong.get_password(),
                },
                "patients": mainframe.get_patients(),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

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
    if config.is_patient_list_valid(cf):
        bs, dd = config.is_bs_valid(cf), config.is_dd_valid(cf)
        match (bs, dd):
            case (True, True):
                driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
                login(driver, cf["bacsi"]["username"], cf["bacsi"]["password"])
                run_bs(driver, cf)
                logout(driver)
                login(
                    driver,
                    cf["dieuduong"]["username"],
                    cf["dieuduong"]["password"],
                )
                run_dd(driver, cf)
                driver.close()
            case (True, False):
                driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
                login(driver, cf["bacsi"]["username"], cf["bacsi"]["password"])
                run_bs(driver, cf)
                driver.close()
                messagebox.showerror(message="chưa nhập điều dưỡng")
            case (False, True):
                driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
                login(
                    driver,
                    cf["dieuduong"]["username"],
                    cf["dieuduong"]["password"],
                )
                run_dd_w_check_signature(driver, cf)
                driver.close()
                messagebox.showerror(message="chưa nhập bác sĩ")
            case _:
                messagebox.showerror(message="chưa nhập bác sĩ, điều dưỡng")

        messagebox.showinfo(message="finish")
    else:
        messagebox.showerror(message="không có bệnh nhân")

def run_bs(driver: Driver, config: config.Config):
    con = create_connection()
    for p in config["patients"]:
        driver.goto(p["url"])
        ma_hs = int(
            driver.waiting(
                ".patient-information .additional-item:nth-child(2) .info"
            ).text
        )
        if not exists(con, ma_hs):
            driver.clicking(".home-breadcrumbs div:nth-child(4) a")
            driver.waiting(".patient-information .additional-item:nth-child(2) .info")
            url = driver.current_url.encode()
            signature = get_signature(driver)
            save_db(con, url, signature)
            driver.goto(p["url"])

        if p["ky_xetnghiem"]:
            igt.phieuchidinh(driver)
        if p["ky_todieutri"]:
            igt.todieutri(driver)
        if p["ky_3tra"]:
            igt.phieuthuchienylenh_bs(driver, p["ky_3tra"]["bacsi"])
        if any(p["phcn"]):
            dkphcn.open(driver)
            dkphcn.clear(driver)
            for ph, fn in zip(
                p["phcn"],
                [dkphcn.bunuot, dkphcn.giaotiep, dkphcn.hohap, dkphcn.vandong],
            ):
                if ph:
                    fn(driver)
            dkphcn.closemenu(driver)
            dkphcn.save(driver)

    con.close()

def run_dd(driver: Driver, config: config.Config):
    for p in config["patients"]:
        driver.goto(p["url"])
        if p["ky_3tra"]:
            igt.phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])

def run_dd_w_check_signature(driver: Driver, config: config.Config):
    con = create_connection()
    for p in config["patients"]:
        driver.goto(p["url"])
        ma_hs = int(
            driver.waiting(
                ".patient-information .additional-item:nth-child(2) .info"
            ).text
        )
        if not exists(con, ma_hs):
            driver.clicking(".home-breadcrumbs div:nth-child(4) a")
            driver.waiting(".patient-information .additional-item:nth-child(2) .info")
            url = driver.current_url.encode()
            signature = get_signature(driver)
            save_db(con, url, signature)
            driver.goto(p["url"])
        if p["ky_3tra"]:
            igt.phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])
    con.close()
