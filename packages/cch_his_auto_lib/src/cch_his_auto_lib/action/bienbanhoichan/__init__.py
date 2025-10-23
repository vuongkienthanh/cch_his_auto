from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import editor

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/chi-tiet"


def click_ingiayto(d: Driver):
    d.clicking(".action-bottom .button-right a:nth-child(2)")


def open_editor(d: Driver):
    click_ingiayto(d)
    d.clicking(".ant-popover .item-file")
    editor.wait_loaded(d)
