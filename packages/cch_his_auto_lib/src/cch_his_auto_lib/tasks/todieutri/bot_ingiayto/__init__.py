import time

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import tracing, EndOfLoop
from .. import _lgr

_lgr = _lgr.getChild("ingiayto")
_trace = tracing(_lgr)


def goto(name: str):
    "Open menu *In giấy tờ*, click `name`"
    _d = get_global_driver()
    _d.clicking(".footer-btn .right button:nth-child(1)", "open menu In giấy tờ")
    _lgr.info(f"goto name={name}")
    for i in range(120):
        time.sleep(1)
        _lgr.debug(f"finding link {name} {i}...")
        for ele in _d.find_all(".ant-dropdown li div div , .ant-dropdown li a"):
            if ele.text == name:
                _lgr.debug(f"-> found link {name} -> proceed to click link")
                ele.click()
                time.sleep(2)
                return
    else:
        _d.clicking(".footer-btn .right button:nth-child(1)", "close menu In giấy tờ")
        raise EndOfLoop(f"can't goto {name}")


from .todieutri import sign_todieutri
from .phieuchidinh import sign_phieuchidinh
from .phieuthuchienylenh import (
    sign_phieuthuchienylenh_bs,
    sign_phieuthuchienylenh_dd,
    sign_phieuthuchienylenh_bn,
)

__all__ = [
    "goto",
    "sign_todieutri",
    "sign_phieuchidinh",
    "sign_phieuthuchienylenh_bs",
    "sign_phieuthuchienylenh_dd",
    "sign_phieuthuchienylenh_bn",
]
