import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os.path

TITLE = "Kiểm tra hồ sơ cũ"
APP_PATH = os.path.dirname(os.path.abspath(__file__))

from . import config
from . import db

from cch_his_auto.app import PROFILE_PATH
from cch_his_auto.app.common_ui.LogInfo import UsernamePasswordDeptFrame

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login
from cch_his_auto.tasks import danhsachnguoibenhnoitru
from cch_his_auto.tasks.chitietnguoibenhnoitru import danhsachnguoibenh, hosobenhan
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
        mainframe.columnconfigure(0, weight=1)
        tk.Label(
            mainframe,
            text="Đường dẫn đến file CSV chứa mã hồ sơ mỗi dòng, không có header",
            anchor="w",
        ).grid(row=0, column=0, sticky="NEW", padx=20, columnspan=2)
        csv_path_var = tk.StringVar()

        def ask_csv():
            filename = filedialog.askopenfilename(
                title="CSV file",
                filetypes=[("csv", ".csv")],
            )
            csv_path_var.set(filename)

        tk.Entry(mainframe, textvariable=csv_path_var).grid(
            row=1, column=0, sticky="NEW", padx=20
        )
        tk.Button(mainframe, text="...", command=ask_csv).grid(row=1, column=1)

        tk.Label(
            mainframe,
            text=process.__doc__ or "",
            justify="left",
            anchor="w",
        ).grid(row=2, column=0, sticky="NEW", padx=20, columnspan=2)

        def load():
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            bacsi.set_department(cf["department"])
            csv_path_var.set(cf["csv_path"])

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
                "department": bacsi.get_department(),
                "csv_path": csv_path_var.get().strip(),
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
        run_btn.bind("<Button-1>", lambda _: run(get_config()))
        btns.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

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
    """
    Chức năng hiện tại:
        + Tờ bìa, mục A, mục B
        + phiếu chỉ định, tờ điều trị
        + Phiếu CT, MRI
    """
    hosobenhan.open(driver)
    hosobenhan.tobiabenhannhikhoa(driver)
    hosobenhan.mucAbenhannhikhoa(driver)
    hosobenhan.mucBtongketbenhan(driver)
    hosobenhan.phieuchidinhxetnghiem(driver)
    hosobenhan.todieutri(driver)
    hosobenhan.phieuCT(driver)
    hosobenhan.phieuMRI(driver)
    hosobenhan.close(driver)
