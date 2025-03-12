import tkinter as tk
from tkinter import messagebox
import os.path

TITLE = "Kiểm tra hồ sơ nội viện"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config

from ..common import process

from cch_his_auto.app.common.username_password import UsernamePasswordFrame
from cch_his_auto.app import PROFILE_PATH

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login
from cch_his_auto.tasks import danhsachnguoibenhnoitru
from cch_his_auto.tasks.common import choose_dept

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        bacsi = UsernamePasswordFrame(self, label="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0, sticky="N", columnspan=2)

        dept_row = tk.Frame(self)
        dept_row.grid(row=1, column=0, sticky="NEWS", padx=(50, 0))
        dept_row.columnconfigure(1, weight=1)
        tk.Label(dept_row, text="Khoa lâm sàng:", justify="right").grid(row=0, column=0)
        dept_var = tk.StringVar()
        dept_entry = tk.Entry(dept_row, textvariable=dept_var)
        dept_entry.grid(row=0, column=1, sticky="w")

        id_row = tk.Frame(self)
        id_row.grid(row=2, column=0, sticky="NEWS", padx=(50, 0))
        id_row.columnconfigure(1, weight=1)
        tk.Label(dept_row, text="Mã hồ sơ:", justify="right").grid(row=0, column=0)
        id_var = tk.StringVar()
        id_entry = tk.Entry(id_row, textvariable=id_var)
        id_entry.grid(row=0, column=1, sticky="w")

        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(self, variable=headless, text="headless")
        headless_btn.grid(row=1, column=1, sticky="N", pady=10, padx=10)

        def load():
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            dept_var.set(cf["department"])
            id_var.set(str(cf["id"]))

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": dept_var.get(),
                "id": int(id_var.get()),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

        load_btn = tk.Button(self, text="Load", command=load, width=10)
        load_btn.grid(row=2, column=1, pady=10, padx=10)
        save_btn = tk.Button(self, text="Save", command=save, width=10)
        save_btn.grid(row=3, column=1, pady=10, padx=10)
        run_btn = tk.Button(self, text="RUN", width=10, bg="#ff0073", fg="#ffffff")
        run_btn.grid(row=5, column=1, sticky="N")
        run_btn.bind("<Button-1>", lambda _: run(get_config()))

def run(cf: config.Config):
    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
    login(driver, cf["username"], cf["password"])
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, cf["department"])
    danhsachnguoibenhnoitru.goto_patient(driver, id)
    process(driver)
    driver.quit()
