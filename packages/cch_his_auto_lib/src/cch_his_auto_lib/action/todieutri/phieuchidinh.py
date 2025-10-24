import time
from enum import Enum

from selenium.common import StaleElementReferenceException

from cch_his_auto_lib.driver import Driver
from . import _lgr


def sign(d: Driver):
    PHIEUCHIDINH_DIALOG = ".ant-modal:has(.__list)"

    class State(Enum):
        Trinh = "Trình ký"
        Ky = "Ký Bác sĩ"
        Huy = "Hủy ký Bác sĩ"

    # d.waiting_to_startswith(
    #     f"{PHIEUCHIDINH_DIALOG} .__button > button:nth-child(2)", State.Trinh
    # )
    d.waiting_to_startswith(
        f"{PHIEUCHIDINH_DIALOG} .__button > button:first-child", State.Ky.value
    )
    d.clicking(f"{PHIEUCHIDINH_DIALOG} .__button > button:first-child")
    try:
        for i in range(30):
            time.sleep(1)
            _lgr.debug(f"checking button state {i}...")
            found = False
            for ele in d.find_all(f"{PHIEUCHIDINH_DIALOG} .__button > button"):
                try:
                    if ele.text == State.Huy.value:
                        _lgr.debug(f" found button state is {State.Huy.value}")
                        found = True
                        break
                except StaleElementReferenceException as e:
                    _lgr.warning(f"get {e}")
            if found:
                break
        else:
            _lgr.warning("can't assure phieuchidinh signed while in dialog, maybe MRI")
    finally:
        d.clicking(f"{PHIEUCHIDINH_DIALOG} button.ant-modal-close")
        d.wait_closing(PHIEUCHIDINH_DIALOG)
