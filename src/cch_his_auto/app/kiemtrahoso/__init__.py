import tkinter as tk
from tkinter import messagebox, scrolledtext
import os.path

TITLE = "Kiểm tra hồ sơ"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config
from cch_his_auto.app.common_tasks.navigation import first_patient, next_patient
from cch_his_auto.driver import Driver
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan
from cch_his_auto.tasks import danhsachnguoibenhnoitru

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        from cch_his_auto.app.common_ui.staff_info import UsernamePasswordDeptFrame

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordDeptFrame(info, text="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0)
        headless_var = tk.BooleanVar()
        headless_btn = tk.Checkbutton(
            info, variable=headless_var, text="Headless Chrome"
        )
        headless_btn.grid(row=1, column=0, pady=5)
        info.grid(row=0, column=0, sticky="N", pady=20)

        mainframe = tk.Frame(self)
        mainframe.grid(row=1, column=0, sticky="NSEW")
        discharged_var = tk.BooleanVar()
        tk.Checkbutton(mainframe, text="đã xuất viện", variable=discharged_var).grid(
            row=0, column=0, padx=20, pady=20, sticky="W"
        )
        tk.Label(mainframe, text="Danh sách mã hồ sơ:", anchor="w").grid(
            row=1, column=0, padx=20, sticky="NEW"
        )
        listing_entry = scrolledtext.ScrolledText(mainframe)
        listing_entry.grid(row=2, column=0, padx=20, sticky="NSEW")
        tk.Label(
            mainframe,
            text=process.__doc__ or "",
            justify="left",
            anchor="w",
        ).grid(row=2, column=0, sticky="SEW", padx=20)

        def load():
            cf = config.load()
            headless_var.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            bacsi.set_department(cf["department"])
            listing_entry.delete("1.0", "end")
            listing_entry.insert("1.0", cf["listing"])
            discharged_var.set(cf["discharged"])

        def get_config() -> config.Config:
            return {
                "headless": headless_var.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "listing": listing_entry.get("1.0", "end"),
                "discharged": discharged_var.get(),
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
    from cch_his_auto.tasks.auth import login_then_choose_dept
    from cch_his_auto.app import PROFILE_PATH
    from cch_his_auto.app.common_tasks.signature import get_signature_in_ctnbnt
    from cch_his_auto.app.global_db import create_connection

    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)
    con = create_connection()

    # set up HIS
    login_then_choose_dept(driver, cf["username"], cf["password"], cf["department"])
    if cf["discharged"]:
        danhsachnguoibenhnoitru.filter_trangthainguoibenh(driver, [10])

    listing = [int(ma_hs) for ma_hs in cf["listing"].strip().splitlines()]

    ma_hs = listing.pop()
    first_patient(driver, ma_hs)
    signature = get_signature_in_ctnbnt(driver, con, ma_hs)
    process(driver, signature)

    while len(listing) > 0:
        ma_hs = listing.pop()
        next_patient(driver, ma_hs)
        signature = get_signature_in_ctnbnt(driver, con, ma_hs)
        process(driver, signature)

    con.close()
    driver.quit()
    messagebox.showinfo(message="finish")

def process(driver: Driver, signature: str):
    """
    Chức năng hiện tại:
        + Tờ bìa, mục A, mục B
        + phiếu chỉ định, tờ điều trị
        + Phiếu CT, MRI
        + Phiếu giải phẫu bệnh
    """
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver, signature)
    hosobenhan.giaiphaubenh(driver)
    hosobenhan.close(driver)
