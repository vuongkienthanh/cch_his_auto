import time

from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import _root_lgr


_lgr = _root_lgr.getChild("top_info")

TOP_BTN_CSS = "#root .thong-tin-benh-nhan .bunch-icon"


def wait_loaded(d: Driver):
    try:
        d.waiting("#root .patient-information")
    except NoSuchElementException:
        d.refresh()
        d.waiting("#root .patient-information")
    finally:
        time.sleep(5)

def get_patient_info(d: Driver) -> dict[str, str]:
    ret = {}
    ret["name"] = d.waiting("#root .patient-content .text-fullname").text.strip()

    moreinfo = d.waiting("#root .patient-content .more-info").text.strip().split("-")
    ret["gender"] = moreinfo[0].strip(" (")
    ret["birthdate"] = moreinfo[2].strip(" )")

    ret["ma_hs"] = d.waiting(
        "#root .patient-information span:nth-child(2) b"
    ).text.strip()
    ret["doituong"] = d.waiting(
        "#root .patient-information span:nth-child(4) b"
    ).text.strip()
    return ret
