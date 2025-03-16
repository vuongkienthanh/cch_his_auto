import tkinter as tk
from tkinter import messagebox
import os.path

TITLE = "Kiểm tra hồ sơ đang nằm viện"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.app.common_ui.LogInfo import UsernamePasswordDeptFrame

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login
from cch_his_auto.tasks import danhsachnguoibenhnoitru
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan
from cch_his_auto.tasks.common import choose_dept

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(info, variable=headless, text="Headless Chrome")
        headless_btn.grid(row=1, column=0, pady=5)
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = tk.Frame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")
        tk.Label(mainframe, text="Mã hồ sơ:", justify="right").grid(
            row=0, column=0, padx=(20, 0)
        )
        id_var = tk.StringVar()
        tk.Entry(mainframe, textvariable=id_var).grid(row=0, column=1, sticky="w")

        def load():
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            bacsi.set_department(cf["department"])
            id_var.set(str(cf["id"]))

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "id": int(id_var.get()),
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
        run_btn = tk.Button(
            btns,
            text="RUN",
            command=lambda: run(get_config()),
            width=10,
            bg="#ff0073",
            fg="#ffffff",
        )
        run_btn.grid(row=2, column=0, pady=5)
        btns.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

def run(cf: config.Config):
    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
    login(driver, cf["username"], cf["password"])
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, cf["department"])
    danhsachnguoibenhnoitru.goto_patient(driver, cf["id"])
    process(driver)
    driver.quit()

def process(driver: Driver):
    hosobenhan.open(driver)
    # hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    # hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver)
    hosobenhan.close(driver)
