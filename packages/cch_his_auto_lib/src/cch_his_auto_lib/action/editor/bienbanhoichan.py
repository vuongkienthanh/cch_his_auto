from selenium.webdriver import ActionChains, Keys

from cch_his_auto_lib.driver import Driver
from cch_his_auto_lib.tracing import console
from . import wait_loaded


def thuky(d: Driver):
    with console.status("signing biên bản hội chẩn..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image button",
            btn_txt="Xác nhận ký Thư ký",
            img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(3) .sign-image img",
            name="bien ban hoi chan (thu ky)",
        )


def truongkhoa(d: Driver):
    with console.status("signing biên bản hội chẩn..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image button",
            btn_txt="Xác nhận ký Trưởng khoa",
            img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(2) .sign-image img",
            name="bien ban hoi chan (truong khoa)",
        )


def thanhvienkhac(d: Driver):
    with console.status("signing biên bản hội chẩn..."):
        wait_loaded(d)
        d.sign_staff_signature(
            btn_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(4) .sign-image button",
            btn_txt="Xác nhận ký Thành Viên",
            img_css=".layout-line-item .layout-line-item:nth-child(39)>div:nth-child(4) .sign-image img",
            name="bien ban hoi chan (thanh vien khac)",
        )


def fill(d: Driver, khac_note: str):
    wait_loaded(d)
    d.waiting(".layout-line-item .layout-line-item:nth-child(37)")
    ActionChains(d).click(
        d.find(
            ".layout-line-item .layout-line-item:nth-child(37) span[contenteditable]"
        )
    ).send_keys(Keys.CONTROL, "a").send_keys(Keys.DELETE).send_keys(khac_note).perform()
