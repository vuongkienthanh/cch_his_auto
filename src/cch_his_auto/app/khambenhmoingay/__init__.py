from functools import partial
import tkinter as tk
from tkinter import messagebox, ttk


from cch_his_auto.app import PROFILE_PATH, _lgr
from cch_his_auto.global_db import create_connection
from cch_his_auto.common_ui.user_frame import UsernamePasswordFrame
from cch_his_auto.common_ui.button_frame import ButtonFrame, RunConfig
from cch_his_auto.common_tasks.signature import try_get_signature
from cch_his_auto_lib.common_tasks import pprint_patient_info

from . import todieutri_tab, bienbanhoichan_tab
from .tabbed_listframe import TabbedListFrame
from .config import Config

from cch_his_auto_lib.driver import Driver, start_driver
from cch_his_auto_lib.action import auth
from cch_his_auto_lib.action.todieutri import (
    click as tdt_click,
    phieuchidinh as tdt_phieuchidinh,
)
from cch_his_auto_lib.action.bienbanhoichan import click as bbhc_click
from cch_his_auto_lib.action.editor import (
    phieuthuchienylenh as editor_phieuthuchienylenh,
    bienbanhoichan as editor_bienbanhoichan,
    todieutri as editor_todieutri,
)
from cch_his_auto_lib.action.top_info import (
    get as top_info_get,
    wait_loaded,
)


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
            title=todieutri_tab.TITLE,
            tab_index=0,
            item_type=todieutri_tab.Line,
            stats=todieutri_tab.HEADERS_STATS,
        )
        bienbanhoichan_frame = TabbedListFrame(
            nb,
            title=bienbanhoichan_tab.TITLE,
            tab_index=1,
            item_type=bienbanhoichan_tab.Line,
            stats=bienbanhoichan_tab.HEADERS_STATS,
        )

        for t in [todieutri_frame, bienbanhoichan_frame]:
            nb.add(t, text=t.get_title_with_count(), sticky="NSEW")

        button_frame = ButtonFrame(self)
        button_frame.grid(row=0, column=1, rowspan=2, padx=20, sticky="S", pady=(0, 20))

        def load():
            cfg = Config.load()

            bacsi.set_user(cfg.bacsi)
            dieuduong.set_user(cfg.dieuduong)
            truongkhoa.set_user(cfg.truongkhoa)
            thanhvienkhac.set_user(cfg.thanhvienkhac)
            dept_var.set(cfg.department)

            todieutri_frame.clear()
            for item in cfg.todieutri:
                todieutri_frame.add_item(item)

            bienbanhoichan_frame.clear()
            for item in cfg.bienbanhoichan:
                bienbanhoichan_frame.add_item(item)

            button_frame.load_config()

        def get_config() -> Config:
            return Config(
                bacsi.get_user(),
                dieuduong.get_user(),
                truongkhoa.get_user(),
                thanhvienkhac.get_user(),
                dept_var.get(),
                todieutri_frame.get_items(),
                bienbanhoichan_frame.get_items(),
            )

        def save():
            if messagebox.askyesno(message="Save?"):
                get_config().save()
                button_frame.save_config()
                messagebox.showinfo(message="Đã lưu")

        button_frame.bind_load(load)
        button_frame.bind_save(save)
        button_frame.bind_run(lambda: run(get_config(), button_frame.get_config()))


def run(cfg: Config, run_cfg: RunConfig):
    if not cfg.is_valid():
        return

    with start_driver(headless=run_cfg.headless, profile_path=PROFILE_PATH) as d:
        if cfg.bacsi.is_valid():
            with auth.session(
                d,
                cfg.bacsi.name,
                cfg.bacsi.password,
                cfg.department,
            ):
                run_bs(d, cfg)

        if cfg.dieuduong.is_valid():
            with auth.session(
                d,
                cfg.dieuduong.name,
                cfg.dieuduong.password,
                cfg.department,
            ):
                run_dd(d, cfg)
                if any(any(p.ky_3tra.benhnhan) for p in cfg.todieutri):
                    run_bn(d, cfg)
        if cfg.truongkhoa.is_valid():
            with auth.session(
                d,
                cfg.truongkhoa.name,
                cfg.truongkhoa.password,
                cfg.department,
            ):
                run_tk(d, cfg)

    messagebox.showinfo(message="finish")


def run_bs(d: Driver, cfg: Config):
    _lgr.info("~~~~~ TỜ ĐIỀU TRỊ ~~~~~")

    def bbhc_bs(d: Driver, khac_note: str):
        editor_bienbanhoichan.fill(d, khac_note)
        editor_bienbanhoichan.thuky(d)

    for tdt in cfg.todieutri:
        if not (tdt.ky_xn or tdt.ky_todieutri or any(tdt.ky_3tra.bacsi)):
            continue

        d.goto(tdt.url)
        wait_loaded(d)
        pinfo = top_info_get.patient_info(d)
        pprint_patient_info(pinfo)

        if tdt.ky_xn:
            tdt_click.ingiayto(d, name="Phiếu chỉ định")
            tdt_phieuchidinh.sign(d)
        if tdt.ky_todieutri:
            d.do_next_tab_do(
                f1=lambda d: tdt_click.ingiayto(d, name="Tờ điều trị"),
                f2=editor_todieutri.bs,
            )
        if any(tdt.ky_3tra.bacsi):
            d.do_next_tab_do(
                f1=lambda d: tdt_click.ingiayto(d, name="Phiếu thực hiện y lệnh"),
                f2=partial(editor_phieuthuchienylenh.bs, arr=tdt.ky_3tra.bacsi),
            )

    for bbhc in cfg.bienbanhoichan:
        if not bbhc.ky_thuky:
            continue

        d.goto(bbhc.url)
        wait_loaded(d)
        pinfo = top_info_get.patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=bbhc_click.open_editor, f2=partial(bbhc_bs, khac_note=bbhc.khac_note)
        )


def run_dd(d: Driver, cfg: Config):
    for p in cfg.todieutri:
        if not any(p.ky_3tra.dieuduong):
            continue

        d.goto(p.url)
        wait_loaded(d)
        pinfo = top_info_get.patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=lambda d: tdt_click.ingiayto(d, name="Phiếu thực hiện y lệnh"),
            f2=partial(editor_phieuthuchienylenh.dd, arr=p.ky_3tra.dieuduong),
        )


def run_bn(d: Driver, cfg: Config):
    with create_connection() as con:
        for p in cfg.todieutri:
            if not any(p.ky_3tra.benhnhan):
                continue

            d.goto(p.url)
            wait_loaded(d)
            pinfo = top_info_get.patient_info(d)
            pprint_patient_info(pinfo)

            ma_hs = int(pinfo["ma_hs"])
            if signature := try_get_signature(d, con, ma_hs):
                d.do_next_tab_do(
                    f1=lambda d: tdt_click.ingiayto(d, name="Phiếu thực hiện y lệnh"),
                    f2=partial(
                        editor_phieuthuchienylenh.bn,
                        arr=p.ky_3tra.benhnhan,
                        signature=signature,
                    ),
                )


def run_tk(d: Driver, cfg: Config):
    for bbhc in cfg.bienbanhoichan:
        if not bbhc.ky_truongkhoa:
            continue

        d.goto(bbhc.url)
        wait_loaded(d)
        pinfo = top_info_get.patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(f1=bbhc_click.open_editor, f2=editor_bienbanhoichan.truongkhoa)


def run_tvk(d: Driver, cfg: Config):
    for bbhc in cfg.bienbanhoichan:
        if not bbhc.ky_thanhvienkhac:
            continue

        d.goto(bbhc.url)
        pinfo = top_info_get.patient_info(d)
        pprint_patient_info(pinfo)

        d.do_next_tab_do(
            f1=bbhc_click.open_editor, f2=editor_bienbanhoichan.thanhvienkhac
        )
