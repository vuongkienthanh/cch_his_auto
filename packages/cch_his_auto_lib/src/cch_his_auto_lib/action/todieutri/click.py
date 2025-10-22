import time

from selenium.common import NoSuchElementException

from . import _lgr
from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.action import top_patient_info
from cch_his_auto_lib.tracing import console


def back(d: Driver):
    d.clicking(".footer-btn .right button:nth-child(2)", "Quay lại")
    top_patient_info.wait_loaded(d)


def ingiayto(d: Driver, name: str):
    d.clicking(".footer-btn .right button:nth-child(1)", "In giấy tờ")
    with console.status("Open menu In giấy tờ..."):
        for i in range(120):
            time.sleep(1)
            _lgr.debug(f"finding link {name} {i}...")
            for ele in d.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
                if ele.text == name:
                    _lgr.info(f"-> found In giấy tờ: {name} -> proceed to click link")
                    ele.click()
                    time.sleep(2)
                    return
        else:
            d.clicking(
                ".footer-btn .right button:nth-child(1)", "close menu In giấy tờ"
            )
            raise NoSuchElementException(f"can't find ingiayto -> {name}")
