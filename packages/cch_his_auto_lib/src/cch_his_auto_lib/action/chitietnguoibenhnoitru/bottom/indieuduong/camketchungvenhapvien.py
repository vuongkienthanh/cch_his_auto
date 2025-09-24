from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

from .. import _lgr


def get_signature(d: Driver) -> str | None:
    "Get patient signature data in *Cam kết chung khi nhập viện*"
    try:
        ele = d.waiting(".layout-line-item:nth-child(43) img", "patient signature")
        ans = ele.get_dom_attribute("src").strip()
        _lgr.info(">>> found patient signature")
        return ans
    except NoSuchElementException:
        _lgr.warning("??? can't find patient signature")
        return None
