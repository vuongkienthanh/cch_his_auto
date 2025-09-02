from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import Driver

from . import goto, _lgr, _trace


@_trace
def get_signature_data(d: Driver) -> str | None:
    "Get patient signature data in *Cam kết chung khi nhập viện*"
    current_tab = d.current_window_handle
    goto(d, "cam kết chung về nhập viện")
    d.goto_newtab(current_tab)
    try:
        ele = d.waiting(".layout-line-item:nth-child(43) img", "patient signature")
        ans = ele.get_dom_attribute("src").strip()
        _lgr.info(">>> found patient signature")
        return ans
    except NoSuchElementException:
        _lgr.warning("??? can't find patient signature")
        return None
    finally:
        d.close()
        d.switch_to.window(current_tab)
