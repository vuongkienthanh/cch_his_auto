import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os.path

TITLE = "Kiểm tra hồ sơ cũ"
APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(APP_PATH, "Profile")

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login
from cch_his_auto.tasks import danhsachnguoibenhnoitru
from cch_his_auto.tasks.chitietnguoibenhnoitru import hosobenhan, danhsachnguoibenh
from cch_his_auto.tasks.common import choose_dept
from ..common.username_password import UsernamePasswordFrame
from . import config
from . import db

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
        dept = tk.StringVar()
        dept_entry = tk.Entry(dept_row, textvariable=dept)
        dept_entry.grid(row=0, column=1, sticky="w")

        csv_help_label = tk.Label(
            self, text="Đường dẫn đến file CSV chứa mã hồ sơ mỗi dòng, không có header"
        )
        csv_help_label.grid(row=2, column=0, sticky="W", padx=(50, 0))
        csv_path_var = tk.StringVar()
        csv_path_entry = tk.Entry(self, textvariable=csv_path_var)
        csv_path_entry.grid(row=3, column=0, sticky="NEW", padx=30)
        app_help_label = tk.Label(
            self,
            text="""Chức năng hiện tại:
            + Tờ bìa, mục A, mục B
            + phiếu chỉ định, tờ điều trị""",
            justify="left",
        )
        app_help_label.grid(row=4, column=0, sticky="W", padx=(50, 0))

        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(self, variable=headless, text="headless")
        headless_btn.grid(row=1, column=1, sticky="N", pady=10, padx=10)

        def load():
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            dept.set(cf["department"])
            csv_path_var.set(cf["csv_path"])

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": dept.get(),
                "csv_path": csv_path_var.get().strip(),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

        def ask_csv():
            filename = filedialog.askopenfilename(
                title="CSV file",
                filetypes=[("csv", ".csv")],
            )
            csv_path_var.set(filename)

        load_btn = tk.Button(self, text="Load", command=load, width=10)
        load_btn.grid(row=2, column=1, pady=10, padx=10)
        save_btn = tk.Button(self, text="Save", command=save, width=10)
        save_btn.grid(row=3, column=1, pady=10, padx=10)
        new_btn = tk.Button(self, text="CSV file", command=lambda: ask_csv(), width=10)
        new_btn.grid(row=4, column=1, pady=10, padx=10)
        run_btn = tk.Button(self, text="RUN", width=10, bg="#ff0073", fg="#ffffff")
        run_btn.grid(row=5, column=1, sticky="N")
        run_btn.bind("<Button-1>", lambda _: run(get_config()))

def run(cf: config.Config):
    if not os.path.exists(cf["csv_path"]):
        return

    con = db.create_connection()
    listing = db.filter_listing(con, cf["csv_path"])

    if len(listing) == 0:
        return

    driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)

    # set up HIS
    login(driver, cf["username"], cf["password"])
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, cf["department"])
    danhsachnguoibenhnoitru.filter_trangthainguoibenh(driver, [10])

    id = listing.pop()
    first_patient(driver, id)
    process(driver)
    db.save_db(con, id)

    while len(listing) > 0:
        id = listing.pop()
        next_patient(driver, id)
        process(driver)
        db.save_db(con, id)

    driver.quit()
    con.close()

def first_patient(driver: Driver, id: int):
    danhsachnguoibenhnoitru.goto_patient(driver, id)

def next_patient(driver: Driver, id: int):
    danhsachnguoibenh.open(driver)
    danhsachnguoibenh.goto_patient(driver, id)

def process(driver: Driver):
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.close(driver)
