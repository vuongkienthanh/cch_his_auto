import tkinter as tk
from tkinter import messagebox, ttk

from validators import url

from cch_his_auto.app import PROFILE_PATH, _lgr
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.staff_info import UsernamePasswordFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig
from cch_his_auto.common_tasks.signature import try_get_signature
from cch_his_auto.common_tasks.navigation import pprint_patient_info
from cch_his_auto.structs import is_user_valid

from . import config, todieutri_tab, bienbanhoichan_tab
from .tabbed_listframe import TabbedListFrame

from cch_his_auto_lib.driver import Driver, start_driver
from cch_his_auto_lib.action import auth, todieutri, editor, bienbanhoichan
from cch_his_auto_lib.action.editor import (
    phieuthuchienylenh as editor_phieuthuchienylenh,
    bienbanhoichan as editor_bienbanhoichan,
)
from cch_his_auto_lib.action.chitietnguoibenhnoitru import get_patient_info


TITLE = "Khám bệnh mỗi ngày"


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        info = tk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = UsernamePasswordFrame(info, text="Bác sĩ")
        dieuduong = UsernamePasswordFrame(info, text="Điều dưỡng")
        truongkhoa = UsernamePasswordFrame(info, text="Trưởng khoa")
        thanhvienkhac = UsernamePasswordFrame(info, text="Thành viên khác")

        bacsi.grid(row=0, column=0)
        dieuduong.grid(row=0, column=1)
        truongkhoa.grid(row=0, column=2)
        thanhvienkhac.grid(row=0, column=3)
        dept_var = tk.StringVar()
        tk.Label(info, text="Khoa lâm sàng:", justify="right").grid(
            row=1, column=0, sticky="E"
        )
        tk.Entry(info, textvariable=dept_var).grid(row=1, column=1, sticky="W")
        info.grid(row=0, column=0, sticky="N", pady=20)

        nb = ttk.Notebook(self)
        nb.grid(row=1, column=0, sticky="NSEW")

        todieutri_frame = TabbedListFrame(
            nb,
            title="Tờ điều trị",
            item_type=todieutri_tab.Line,
            stats=todieutri_tab.HEADERS_STATS,
        )
        bienbanhoichan_frame = TabbedListFrame(
            nb,
            title="Biên bản hội chẩn",
            item_type=bienbanhoichan_tab.Line,
            stats=bienbanhoichan_tab.HEADERS_STATS,
        )

        for i, t in enumerate([todieutri_frame, bienbanhoichan_frame]):
            nb.add(t, text=t.get_title_with_count(), sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = config.load()

            bacsi.set_username(cfg["bacsi"]["username"])
            bacsi.set_password(cfg["bacsi"]["password"])
            dieuduong.set_username(cfg["dieuduong"]["username"])
            dieuduong.set_username(cfg["dieuduong"]["username"])
            truongkhoa.set_password(cfg["truongkhoa"]["password"])
            truongkhoa.set_password(cfg["truongkhoa"]["password"])
            thanhvienkhac.set_password(cfg["thanhvienkhac"]["password"])
            thanhvienkhac.set_password(cfg["thanhvienkhac"]["password"])
            dept_var.set(cfg["department"])

            todieutri_frame.clear()
            for item in cfg["todieutri"]:
                todieutri_frame.add_item(item)

            button_frame.load_config()

        def get_config() -> config.Config | None:
            cfg = {
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
                "thanhvienkhac": {
                    "username": thanhvienkhac.get_username(),
                    "password": thanhvienkhac.get_password(),
                },
                "department": dept_var.get(),
                "todieutri": todieutri_frame.get_items(),
                "bienbanhoichan": bienbanhoichan_frame.get_items(),
            }
            if (
                len(cfg["todieutri"]) > 0
                and all(
                    url(tdt["url"])
                    and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in tdt["url"])
                    for tdt in cfg["todieutri"]
                )
                and all(
                    url(bbhc["url"])
                    and (
                        "chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/" in bbhc["url"]
                    )
                    for bbhc in cfg["bienbanhoichan"]
                )
            ):
                return cfg
            else:
                messagebox.showerror(message="Sai/Trống link bệnh nhân")
                return

        def save():
            if messagebox.askyesno(message="Save?"):
                config.save(get_config())
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: config.Config, run_cfg: RunConfig):
    with start_driver(headless=run_cfg["headless"], profile_path=PROFILE_PATH) as d:
        if is_user_valid(cfg["bacsi"]):
            with auth.session(
                d,
                cfg["bacsi"]["username"],
                cfg["bacsi"]["password"],
                cfg["department"],
            ):
                run_bs(d, cfg)

        if is_user_valid(cfg["dieuduong"]):
            with auth.session(
                d,
                cfg["dieuduong"]["username"],
                cfg["dieuduong"]["password"],
                cfg["department"],
            ):
                run_dd(d, cfg)
                if any(any(p["ky_3tra"]["benhnhan"]) for p in cfg["todieutri"]):
                    run_bn(d, cfg)
        if is_user_valid(cfg["truongkhoa"]):
            with auth.session(
                d,
                cfg["truongkhoa"]["username"],
                cfg["truongkhoa"]["password"],
                cfg["department"],
            ):
                run_tk(d, cfg)

    messagebox.showinfo(message="finish")


def run_bs(d: Driver, cfg: config.Config):
    _lgr.info("~~~~~ TỜ ĐIỀU TRỊ ~~~~~")

    def bbhc_bs(d: Driver, khac_note: str):
        editor_bienbanhoichan.fill(d, khac_note)
        editor_bienbanhoichan.thuky(d)

    for tdt in cfg["todieutri"]:
        if not (tdt["ky_xn"] or tdt["ky_todieutri"] or any(tdt["ky_3tra"]["bacsi"])):
            continue

        d.goto(tdt["url"])
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)

        if tdt["ky_xn"]:
            todieutri.phieuchidinh(d)
        if tdt["ky_todieutri"]:
            d.do_next_tab_do(
                f1=lambda d: todieutri.ingiayto(d, name="Tờ điều trị"),
                f2=editor.todieutri,
            )
        if any(tdt["ky_3tra"]["bacsi"]):
            d.do_next_tab_do(
                f1=lambda d: todieutri.ingiayto(d, name="Phiếu thực hiện y lệnh"),
                f2=lambda d: editor_phieuthuchienylenh.bs(d, tdt["ky_3tra"]["bacsi"]),
            )

    for bbhc in cfg["bienbanhoichan"]:
        if not bbhc["ky_thuky"]:
            continue

        d.goto(bbhc["url"])
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=bienbanhoichan.open_editor, f2=lambda d: bbhc_bs(d, bbhc["khac_note"])
        )


def run_dd(d: Driver, cfg: config.Config):
    for p in cfg["todieutri"]:
        if not any(p["ky_3tra"]["dieuduong"]):
            continue

        d.goto(p["url"])
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=lambda d: todieutri.ingiayto(d, name="Phiếu thực hiện y lệnh"),
            f2=lambda d: editor_phieuthuchienylenh.dd(d, p["ky_3tra"]["dieuduong"]),
        )


def run_bn(d: Driver, cfg: config.Config):
    with create_connection() as con:
        for p in cfg["todieutri"]:
            if not any(p["ky_3tra"]["benhnhan"]):
                continue

            d.goto(p["url"])
            pinfo = get_patient_info(d)
            pprint_patient_info(pinfo)

            ma_hs = int(pinfo["ma_hs"])
            signature = try_get_signature(d, con, ma_hs)
            d.do_next_tab_do(
                f1=lambda d: todieutri.ingiayto(d, name="Phiếu thực hiện y lệnh"),
                f2=lambda d: editor_phieuthuchienylenh.bn(
                    d, p["ky_3tra"]["benhnhan"], signature
                ),
            )


def run_tk(d: Driver, cfg: config.Config):
    for bbhc in cfg["bienbanhoichan"]:
        if not bbhc["ky_truongkhoa"]:
            continue

        d.goto(bbhc["url"])
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=bienbanhoichan.open_editor, f2=editor_bienbanhoichan.truongkhoa
        )


def run_tvk(d: Driver, cfg: config.Config):
    for bbhc in cfg["bienbanhoichan"]:
        if not bbhc["ky_thanhvienkhac"]:
            continue

        d.goto(bbhc["url"])
        pinfo = get_patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=bienbanhoichan.open_editor, f2=editor_bienbanhoichan.thanhvienkhac
        )
