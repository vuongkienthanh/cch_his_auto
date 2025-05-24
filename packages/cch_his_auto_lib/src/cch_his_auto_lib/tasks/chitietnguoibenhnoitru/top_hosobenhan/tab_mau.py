from selenium.common import NoSuchElementException


from cch_his_auto_lib.driver import get_global_driver
from . import ACTIVE_PANE, _lgr

TAB_NUMBER = 7
_lgr = _lgr.getChild("tab_mau")


def get_bloodtype() -> str | None:
    _d = get_global_driver()
    for i in range(2, 10):
        try:
            ele = _d.waiting(
                f"{ACTIVE_PANE} tr:nth-child({i}) td:nth-child(12)", "nhóm máu phát"
            ).text.strip()
        except NoSuchElementException:
            _lgr.warning("-> can't find bloodtype")
            return None
        else:
            if ele == "Chưa xác định":
                continue
            else:
                _lgr.info(f"bloodtype = {ele}")
                return ele
    else:
        _lgr.warning("-> can't find bloodtype")
        return None
