import time
from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr, console
from cch_his_auto_lib.action import top_info

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/to-dieu-tri"

_lgr = _root_lgr.getChild("todieutri")


def get_dienbien(d: Driver) -> str | None:
    try:
        ele = d.waiting("textarea.dien-bien").text.strip()
        if ele == "":
            return None
        else:
            _lgr.info(f"dien bien= {ele}")
            return ele
    except NoSuchElementException:
        _lgr.warning("-> can't find dien bien")
        return None


def click_back(d: Driver):
    d.clicking(".footer-btn .right button:nth-child(2)", "Quay lại")
    top_info.wait_loaded(d)


def click_ingiayto(d: Driver, name: str):
    d.clicking(".footer-btn .right button:nth-child(1)", "In giấy tờ")
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
