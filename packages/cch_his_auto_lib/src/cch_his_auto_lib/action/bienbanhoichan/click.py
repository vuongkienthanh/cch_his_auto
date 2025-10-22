from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import editor

def open_editor(d: Driver):
    d.clicking(".action-bottom .button-right a:nth-child(2)")
    d.clicking(".ant-popover .item-file")
    editor.wait_loaded(d)
