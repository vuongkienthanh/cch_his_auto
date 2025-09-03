import logging


from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action.chitietnguoibenhnoitru import (
    get_patient_info,
)
from cch_his_auto_lib.action import editor
from cch_his_auto_lib.tracing import tracing

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/chi-tiet"

_lgr = logging.getLogger("bienbanhoichan")
_trace = tracing(_lgr)



def wait_loaded(d: Driver):
    d.waiting("#root .patient-information")
    p = get_patient_info(d)
    _lgr.info(f"Bien ban hoi chan page loaded: {p['name']} ,{p['ma_hs']}")


@_trace
def open_editor(d: Driver):
    d.clicking(".action-bottom .button-right a:nth-child(2)")
    d.clicking(".ant-popover .item-file")
    editor.wait_loaded(d)
