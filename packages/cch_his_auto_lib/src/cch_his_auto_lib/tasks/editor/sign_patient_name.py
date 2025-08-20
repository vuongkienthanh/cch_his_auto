import time

from selenium.common import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.tracing import EndOfLoop
from . import _lgr, fill_info


def sign_canvas(signature: str):
    "use when patient signature needed"
    _d = get_global_driver()
    _d.waiting("canvas")
    script = """
        let c = document.querySelector('canvas');
        let ctx = c.getContext('2d');
        let image = new Image();
        image.onload = function() {{
            ctx.drawImage(image, 0, 0, 400, 200);
        }};
        image.src = '{signature}'
        """.format(signature=signature)

    _d.execute_script(script)
    time.sleep(3)
    _d.clicking("canvas")
    _d.clicking(
        ".ant-modal .bottom-action-right button",
        "save after finish drawing signature",
    )


def _sign(name: str, btn_css: str, btn_txt: str, img_css: str, signature: str):
    _d = get_global_driver()
    for _ in range(120):
        time.sleep(1)
        try:
            _lgr.debug(f"finding {name} button")
            ele = _d.find(btn_css)
        except NoSuchElementException:
            _lgr.debug("-> can't find sign button, finding signature")
            try:
                _d.find(img_css)
            except NoSuchElementException:
                _lgr.debug("-> can't find signature -> continue")
                continue
            else:
                _lgr.info("-> found signature already signed")
                return
        else:
            try:
                if ele.text.strip().startswith(btn_txt.strip()):
                    _lgr.debug("-> found sign button with correct btn_txt")
                    ele.click()
                    sign_canvas(signature)
                    _d.waiting(img_css, "signature image")
                    return
                else:
                    _lgr.debug("-> found sign button but wrong btn_txt -> continue")
                    continue
            except StaleElementReferenceException as e:
                _lgr.warning(f"get {e}")
                continue
    else:
        raise EndOfLoop("can't sign")


def phieuthuchienylenh_bn(arr: tuple[bool, bool, bool, bool, bool], signature: str):
    "*Phiếu thực hiện y lệnh (bệnh nhân)*"
    _d = get_global_driver()
    _lgr.info("++++ doing phieuthuchienylenh_bn, may take a while")
    _d.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        try:
            _lgr.debug(f"cheking row 4 col {col - 2}")
            for i in range(120):
                try:
                    _lgr.debug(f"finding row 4 col {col - 2} button {i}...")
                    ele = _d.find(
                        f"table tbody tr:nth-last-child(1) td:nth-child({col}) button",
                    )
                except NoSuchElementException:
                    _lgr.debug(f"-> can't find row 4 col {col - 2} button")
                    try:
                        _lgr.debug(
                            f"finding row 4 col {col - 2} signature image {i}..."
                        )
                        _d.find(
                            f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                        )
                        _lgr.debug(f"-> found row 4 col {col - 2} signature image")
                        break
                    except NoSuchElementException:
                        _lgr.debug(f"-> can't find row 4 col {col - 2} signature image")
                        continue
                else:
                    _lgr.debug(
                        f"-> found row 4 col {col - 2} button -> proceed to click"
                    )
                    ActionChains(_d).scroll_to_element(ele).pause(1).click(
                        ele
                    ).perform()
                    sign_canvas(signature)
                    try:
                        _d.waiting(
                            f"table tbody tr:nth-last-child(1) td:nth-child({col}) img",
                            f"row 4 col {col - 2} signature",
                        )
                        _lgr.debug(f"-> finish row 4 col {col - 2}")
                    except TimeoutException:
                        _lgr.warning(
                            "get TimeoutException -> maybe clicked but didn't load"
                        )
                    finally:
                        break
            else:
                raise EndOfLoop(f"can't sign row 4 col {col - 2}")
        except Exception as e:
            _lgr.warning(f"get {e} -> proceed to next in queue")
    time.sleep(2)


def phieuCT_bn(signature: str):
    "*Phiếu chỉ định CT (bệnh nhân)*"
    _sign(
        name="phieu CT benh nhan",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(29) .sign-image img",
        signature=signature,
    )


def phieuMRI_bn(signature: str):
    "*Phiếu chỉ định MRI (bệnh nhân)*"
    _sign(
        name="phieu MRI benh nhan",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image button",
        btn_txt="Ký",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(2) .sign-image img",
        signature=signature,
    )


def phieucamkettruyenmau_bn(signature: str):
    "*Phiếu cam kết truyền máu (bệnh nhân)*"
    _sign(
        name="phieu cam ket truyen mau benh nhan",
        btn_css=".sign-image button",
        btn_txt="Ký",
        img_css=".sign-image img",
        signature=signature,
    )


def phieucamkettta5(signature: str):
    "*Phiếu cam kết thủ thuật a5 (bệnh nhân)*"
    _sign(
        name="phieu cam ket thu thuat a5",
        btn_css=".sign-image button",
        btn_txt="Ký",
        img_css=".sign-image img",
        signature=signature,
    )


###########
## COMBO ##
###########


def phieucamkettruyenmau_fill_info_then_sign_bn(signature: str):
    fill_info.phieucamkettruyenmau_fill_info()
    phieucamkettruyenmau_bn(signature)
