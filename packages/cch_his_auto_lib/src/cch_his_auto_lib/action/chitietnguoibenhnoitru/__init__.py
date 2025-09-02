import logging

from cch_his_auto_lib.driver import Driver

URL = "http://emr.ndtp.org/quan-ly-noi-tru/chi-tiet-nguoi-benh-noi-tru/"

_lgr = logging.getLogger("chitietnguoibenhnoitru")


def wait_loaded(d: Driver):
    d.waiting("#root .patient-information")
    p = get_patient_info(d)
    _lgr.info(f"Patient page loaded: {p['name']} ,{p['ma_hs']}")


def get_patient_info(d: Driver) -> dict[str, str]:
    ret = {}
    ret["name"] = d.waiting("#root .patient-content .text-fullname").text.strip()

    moreinfo = d.waiting("#root .patient-content .more-info").text.strip().split("-")
    ret["gender"] = moreinfo[0][1:]
    ret["birthdate"] = moreinfo[2]

    ret["ma_hs"] = d.waiting(
        "#root .patient-information span:nth-child(2) b"
    ).text.strip()
    ret["doituong"] = d.waiting("#root .patient-information span:nth-child(4) b")
    return ret
