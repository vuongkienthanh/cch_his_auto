import logging


from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import editor
from cch_his_auto_lib.tracing import tracing

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/chi-tiet"

_lgr = logging.getLogger("bienbanhoichan")
_trace = tracing(_lgr)


@_trace
def open_editor(d: Driver):
    d.clicking(".action-bottom .button-right a:nth-child(2)")
    d.clicking(".ant-popover .item-file")
    editor.wait_loaded(d)
