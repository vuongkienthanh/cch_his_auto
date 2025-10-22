from contextlib import contextmanager


from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr
from . import TOP_BTN_CSS

_lgr = _root_lgr.getChild("top_chitietthongtin")

DIALOG_CSS = ".ant-modal:has(.avatar__image)"


@contextmanager
def dialog(d: Driver):
    d.clicking(f"{TOP_BTN_CSS}>div:first-child")
    d.waiting(DIALOG_CSS)
    try:
        yield
    finally:
        d.clicking(f"{DIALOG_CSS} button.ant-modal-close")
        d.wait_closing(DIALOG_CSS)
