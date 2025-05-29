import time

from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains

from cch_his_auto_lib.driver import get_global_driver
from cch_his_auto_lib.helper import EndOfLoop
from . import _lgr, fill_info


def _sign(name: str, btn_css: str, btn_txt: str, img_css: str):
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


def _sign_phieuthuchienylenh(row: int, col: int):
    _d = get_global_driver()
    try:
        _lgr.debug(f"checking row {5 - row} col {col - 2}")
        for i in range(120):
            try:
                _lgr.debug(f"finding row {5 - row} col {col - 2} button {i}...")
                ele = _d.find(
                    f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button",
                )
            except NoSuchElementException:
                _lgr.debug(f"-> can't find row {5 - row} col {col - 2} button")
                try:
                    _lgr.debug(
                        f"finding row {5 - row} col {col - 2} signature image {i}..."
                    )
                    _d.find(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                    )
                    _lgr.debug(f"found row {5 - row} col {col - 2} signature image")
                    break
                except NoSuchElementException:
                    _lgr.debug(f"can't row {5 - row} col {col - 2} signature image")
                    continue
            else:
                _lgr.debug(
                    f"-> found row {5 - row} col {col - 2} button -> proceed to click"
                )
                ActionChains(_d).scroll_to_element(ele).pause(1).click(ele).perform()
                try:
                    _d.waiting(
                        f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img",
                        f"row {5 - row} col {col - 2} signature",
                    )
                    _lgr.debug(f"-> finish row {5 - row} col {col - 2}")
                except TimeoutException:
                    _lgr.warning(
                        "get TimeoutException -> maybe clicked but didn't load"
                    )
                finally:
                    break
        else:
            raise EndOfLoop(f"can't sign row {row - 5} col {col - 2}")
    except Exception as e:
        _lgr.warning(f"get {e} -> proceed to next in queue")


def tobiabenhannhikhoa():
    "*Tờ bìa bệnh án nhi khoa*"
    _sign(
        name="to bia benh an nhi khoa",
        btn_css=".layout-line-item div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item div:nth-child(2) .sign-image img",
    )


def mucAbenhannhikhoa():
    "*Mục A bệnh án nhi khoa*"
    _sign(
        name="muc A",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ làm bệnh án",
        img_css=".sign-image img",
    )


def mucBtongketbenhan():
    "*Mục B tổng kết bệnh án*"
    _sign(
        name="muc B",
        btn_css="td:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css="td:nth-child(3) .sign-image img",
    )


def todieutri():
    "*Tờ điều trị*"
    _sign(
        name="to dieu tri",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".sign-image img",
    )


def phieuthuchienylenh_bs(arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (bác sĩ)*"
    _d = get_global_driver()
    _lgr.info("++++ doing phieuthuchienylenh_bs, may take a while")
    _d.waiting(".table-tbody")
    time.sleep(3)
    for row, col in (
        (row, col)
        for col in map(
            lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))
        )
        for row in [4, 3]
    ):
        _sign_phieuthuchienylenh(row, col)
    time.sleep(2)


def phieuthuchienylenh_dd(arr: tuple[bool, bool, bool, bool, bool]):
    "*Phiếu thực hiện y lệnh (điều dưỡng)*"
    _d = get_global_driver()
    _lgr.info("++++ doing phieuthuchienylenh_dd, may take a while")
    _d.waiting(".table-tbody")
    time.sleep(3)
    for col in map(lambda x: x[0], filter(lambda x: x[1], zip([3, 4, 5, 6, 7], arr))):
        _sign_phieuthuchienylenh(2, col)
    time.sleep(2)


def phieuCT_bschidinh():
    "*Phiếu chỉ định CT, bs chỉ định*"
    _sign(
        name="phieu CT bs chi dinh",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ điều trị",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(13) .sign-image img",
    )


def phieuCT_bsthuchien():
    "*Phiếu chỉ định CT, bs thực hiện*"
    _sign(
        name="phieu CT bs thuc hien",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(20) .sign-image button:nth-child(1)",
        btn_txt="Xác nhận ký Bác sĩ Chẩn đoán hình ảnh",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(20) .sign-image img",
    )


def phieuMRI_bschidinh():
    "*Phiếu chỉ định MRI, bs chỉ định*"
    _sign(
        name="phieu MRI bs chi dinh",
        btn_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ chỉ định",
        img_css=".layout-line-item:nth-child(1) .layout-line-item:nth-child(22) .sign-image img",
    )


def phieuMRI_bsthuchien():
    "*Phiếu chỉ định MRI, bs thực hiện*"
    _sign(
        name="phieu MRI bs thuc hien",
        btn_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image button",
        btn_txt="Xác nhận ký Bác sĩ thực hiện",
        img_css=".layout-line-item:nth-child(2) .layout-line-item:nth-child(25)>div[data-type=block]:nth-child(1) .sign-image img",
    )


def giaiphaubenh():
    "*Phiếu xét nghiệm giải phẫu bệnh sinh thiết*"
    _sign(
        name="phieu giai phau benh",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
    )


def phieucamkettta5():
    "*Phiếu cam kết thủ thuật a5*"
    _sign(
        name="phieu cam ket thu thuat a5",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký Bác sĩ khám/ điều trị",
        img_css=".sign-image img",
    )


def bienbanhoichan_thuky():
    "*Biên bản hội chẩn (thư ký)*"
    _sign(
        name="bien ban hoi chan (thu ky)",
        btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image button",
        btn_txt="Xác nhận ký Thư ký",
        img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image img",
    )


def bienbanhoichan_truongkhoa():
    "*Biên bản hội chẩn (trưởng khoa)*"
    _sign(
        name="bien ban hoi chan (truong khoa)",
        btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image button",
        btn_txt="Xác nhận ký Trưởng khoa",
        img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image img",
    )


def phieudutrucungcapmau():
    "*Phiếu dự trù và cung cấp máu*"
    _sign(
        name="phieu du tru cung cap mau",
        btn_css=".sign-image button",
        btn_txt="Xác nhận ký BÁC SĨ ĐIỀU TRỊ",
        img_css=".sign-image img",
    )


############
## UNSIGN ##
############


def _unsign(name: str, cancel_btn_css: str, img_css: str):
    _d = get_global_driver()
    _lgr.debug(f"unsigning {name}")
    try:
        _d.clicking2(img_css)
    except NoSuchElementException:
        return
    else:
        _d.clicking2(cancel_btn_css)
        _d.clicking(".ant-modal .ant-btn.warning")


def unsign_phieudutrucungcapmau():
    "*Phiếu dự trù và cung cấp máu*"
    _unsign(
        name="phieu du tru cung cap mau",
        cancel_btn_css=".layout-line-item .layout-line-item:nth-child(20) .info-sign svg",
        img_css=".sign-image img",
    )


###########
## COMBO ##
###########


def bienbanhoichan_fill_info_then_thuky(khac: str):
    fill_info.bienbanhoichan_fill_info(khac)
    bienbanhoichan_thuky()


def phieudutrucungcapmau_fill_info_then_sign(
    duphongphauthuat: bool,
    nhom1: bool,
    date: str,
    datruyenmau: bool,
    khangthebatthuong: bool,
    phanungtruyenmau: bool,
    hcthientai: str,
    truyenmaucochieuxa: bool,
    cungnhom: bool,
):
    fill_info.phieudutrucungcapmau_fill_info(
        duphongphauthuat,
        nhom1,
        date,
        datruyenmau,
        khangthebatthuong,
        phanungtruyenmau,
        hcthientai,
        truyenmaucochieuxa,
        cungnhom,
    )
    phieudutrucungcapmau()


def phieucamkettta5_fill_info_then_sign():
    fill_info.phieucamkettta5_fill_info()
    phieucamkettta5()
