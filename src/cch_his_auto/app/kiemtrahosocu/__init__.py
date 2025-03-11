import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os.path
import sqlite3

from cch_his_auto.driver import Driver
from cch_his_auto.tasks.auth import login
from ..common.username_password import UsernamePasswordFrame
from . import config

TITLE = "Kiểm tra hồ sơ cũ"
APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(APP_PATH, "Profile")
DB_PATH = os.path.join(APP_PATH, ".db")

def create_connection():
    con = sqlite3.Connection(DB_PATH)

    con.executescript("""
    CREATE TABLE IF NOT EXISTS kiemtrahosocu (
        id INTERGER PRIMARY KEY
    );
    """)
    return con

def save_db(con: sqlite3.Connection, db_name: str, id: int):
    con.execute(f"INSERT INTO {db_name} VALUES (?)", (id,))
    con.commit()

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        bacsi = UsernamePasswordFrame(self, label="Bác sĩ ký tên")
        bacsi.grid(row=0, column=0, sticky="N", columnspan=2)
        csv_help_label = tk.Label(
            self, text="Đường dẫn đến file CSV chứa mã hồ sơ mỗi dòng, không có header"
        )
        csv_help_label.grid(row=1, column=0, sticky="W", padx=(50, 0))
        csv_path_var = tk.StringVar()
        csv_path_entry = tk.Entry(self, textvariable=csv_path_var)
        csv_path_entry.grid(row=2, column=0, sticky="NEW", padx=30)
        app_help_label = tk.Label(
            self,
            text="""Chức năng hiện tại:
            + Tờ bìa, mục A, mục B
            + phiếu chỉ định, tờ điều trị""",
            justify="left",
        )
        app_help_label.grid(row=3, column=0, sticky="W", padx=(50, 0))

        headless = tk.BooleanVar()
        headless_btn = tk.Checkbutton(self, variable=headless, text="headless")
        headless_btn.grid(row=1, column=1, sticky="N", pady=10, padx=10)

        def load():
            cf = config.load()
            headless.set(cf["headless"])
            bacsi.set_username(cf["username"])
            bacsi.set_password(cf["password"])
            csv_path_var.set(cf["csv_path"])

        def get_config() -> config.Config:
            return {
                "headless": headless.get(),
                "username": bacsi.get_username(),
                "password": bacsi.get_password(),
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
    if len(cf["csv_path"]) is None:
        return
    listing = []
    con = create_connection()
    with open(cf["csv_path"], mode="r", encoding="utf-8-sig") as f:
        for id in f.readlines():
            if con.execute(
                "SELECT EXISTS( SELECT * FROM kiemtrahosocu WHERE id =?)", (id,)
            ).fetchone() == (0,):
                listing.append(id)

    if len(listing) > 0:
        driver = Driver(headless=cf["headless"], profile_path=PROFILE_PATH)

        driver.close()
    con.close()
