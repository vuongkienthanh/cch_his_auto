import tkinter as tk
from tkinter import messagebox
import os.path

from . import config
from .patient_list import PatientFrame
from ..common.username_password import UsernamePasswordFrame

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login, logout
from cch_his_auto.tasks.todieutri import ingiayto as igt
from cch_his_auto.tasks.todieutri import dangkyPHCN as dk

TITLE = "Ký tờ điều trị hằng ngày"
PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Profile")

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)

        staff_info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(staff_info, label="Bác sĩ")
        dieuduong = UsernamePasswordFrame(staff_info, label="Điều dưỡng")
        staff_info.grid(row=0, column=0, sticky="N", columnspan=2)
        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)

        patientframe = PatientFrame(self)
        patientframe.grid(row=1, column=0, sticky="NSEW", rowspan=7)

        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(
            self, text="headless", variable=headless, onvalue=True, offvalue=False
        )
        headless_btn.grid(row=1, column=1)

        def load():
            patientframe.clear()
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["bacsi"]["username"])
            bacsi.set_password(cf["bacsi"]["password"])
            dieuduong.set_username(cf["dieuduong"]["username"])
            dieuduong.set_password(cf["dieuduong"]["password"])
            for p in cf["patients"]:
                patientframe.add_patient(p)

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
                "patients": patientframe.get_patients(),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

        load_btn = tk.Button(self, text="Load", command=load, width=10)
        load_btn.grid(row=2, column=1)
        save_btn = tk.Button(self, text="Save", command=save, width=10)
        save_btn.grid(row=3, column=1)

        new_btn = tk.Button(
            self, text="Add", command=lambda: patientframe.add_new(), width=10
        )
        new_btn.grid(row=5, column=1)
        run_btn = tk.Button(
            self,
            text="RUN",
            command=lambda: run(get_config()),
            width=10,
            bg="#ff0073",
            fg="#ffffff",
        )
        run_btn.grid(row=6, column=1, padx=20)

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
                run_dd(driver, cf)
                driver.close()
                messagebox.showerror(message="chưa nhập bác sĩ")
            case _:
                messagebox.showerror(message="chưa nhập bác sĩ, điều dưỡng")

        messagebox.showinfo(message="finish")
    else:
        messagebox.showerror(message="không có bệnh nhân")

def run_bs(driver: Driver, config: config.Config):
    for p in config["patients"]:
        driver.goto(p["url"])
        if p["ky_xetnghiem"]:
            igt.phieuchidinh(driver)
        if p["ky_todieutri"]:
            igt.todieutri(driver)
        if p["ky_3tra"]:
            igt.phieuthuchienylenh_bs(driver, p["ky_3tra"]["bacsi"])
        if any(p["phcn"]):
            dk.open(driver)
            dk.clear(driver)
            for ph, fn in zip(
                p["phcn"], [dk.bunuot, dk.giaotiep, dk.hohap, dk.vandong]
            ):
                if ph:
                    fn(driver)
            dk.closemenu(driver)
            dk.save(driver)

def run_dd(driver: Driver, config: config.Config):
    for p in config["patients"]:
        driver.goto(p["url"])
        if p["ky_3tra"]:
            igt.phieuthuchienylenh_dd(driver, p["ky_3tra"]["dieuduong"])
