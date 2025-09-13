import logging
import time

from cch_his_auto_lib.driver import Driver


_lgr = logging.getLogger("top_patient_info")

TOP_BTN_CSS = "#root .thong-tin-benh-nhan .bunch-icon"


def wait_loaded(d: Driver):
    d.waiting("#root .patient-information")
    time.sleep(5)
    p = get_patient_info(d)
    _lgr.info(f"Patient loaded: {p['name']} ,{p['ma_hs']}")


def get_patient_info(d: Driver) -> dict[str, str]:
    ret = {}
    ret["name"] = d.waiting("#root .patient-content .text-fullname").text.strip()

    moreinfo = d.waiting("#root .patient-content .more-info").text.strip().split("-")
    ret["gender"] = moreinfo[0][1:].strip()
    ret["birthdate"] = moreinfo[2].strip()

    ret["ma_hs"] = d.waiting(
        "#root .patient-information span:nth-child(2) b"
    ).text.strip()
    ret["doituong"] = d.waiting(
        "#root .patient-information span:nth-child(4) b"
    ).text.strip()
    return ret
