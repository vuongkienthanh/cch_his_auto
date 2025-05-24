from selenium.common import NoSuchElementException

from cch_his_auto_lib.driver import get_global_driver
from . import goto, _lgr, _trace


@_trace
def get_signature() -> str | None:
    _d = get_global_driver()
    main_tab = _d.current_window_handle
    goto("cam kết chung về nhập viện")
    _d.goto_newtab(main_tab)
    try:
        ele = _d.waiting(".layout-line-item:nth-child(43) img", "patient signature")
        ans = ele.get_dom_attribute("src").strip()
        _lgr.info(">>> found patient signature")
        return ans
    except NoSuchElementException:
        _lgr.warning("??? can't find patient signature")
        return None
    finally:
        _d.close()
        _d.switch_to.window(main_tab)
