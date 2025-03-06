import logging
import sys
import time
from typing import Protocol
from pathlib import PurePath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout)

class DriverFn(Protocol):
    def __call__(self, driver: "Driver", *args, **kwargs) -> None: ...

class Driver(webdriver.Chrome):
    """Preconfigured chrome driver"""

    def __init__(self, headless: bool = False, profile_path: PurePath | None = None):
        logger.info("opening chrome ...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2}
        )

        if headless:
            options.add_argument("--headless")
        if profile_path:
            options.add_argument(f"--user-data-dir={profile_path}")

        super().__init__(options=options)

    def finding(self, css: str) -> WebElement:
        return self.find_element(By.CSS_SELECTOR, css)

    def findings(self, css: str) -> list[WebElement]:
        return self.find_elements(By.CSS_SELECTOR, css)

    def waiting(self, css: str, /, name: str = "") -> WebElement:
        logger.info(f"---waiting {name or css}")
        WebDriverWait(self, 120).until(lambda _: self.finding(css).is_displayed())
        logger.info(f"---done waiting {name or css}")
        return self.finding(css)

    def waiting_to_be(self, css: str, to_be: str, /) -> WebElement:
        logger.info(f"---waiting {css} to be {to_be}")
        WebDriverWait(self, 120).until(lambda _: self.finding(css).is_displayed())
        if to_be:
            for _ in range(120):
                time.sleep(1)
                if self.finding(css).text.strip().startswith(to_be.strip()):
                    logger.info(f"-->> found {to_be}")
                    break
            else:
                txt = self.finding(css).text.strip()
                ctx = f"{css} with to_be {to_be} != textContent {txt}"
                logger.error(f"---no such element: {ctx}")
                raise NoSuchElementException(ctx)
        logger.info(f"---done waiting {css} to be {to_be}")
        return self.finding(css)

    def clicking(self, css: str, /, name: str = "") -> None:
        logger.info(f"---clicking {name or css}")
        logger.setLevel(logging.CRITICAL)
        ele = self.waiting(css, name)
        ActionChains(self).scroll_to_element(ele).pause(1).click(ele).perform()
        logger.setLevel(logging.INFO)
        logger.info(f"---done clicking {name or css}")

    def goto(self, url: str) -> None:
        logger.info(f"---goto {url}")
        self.get(url)

    def goto_newtab_do_smth_then_goback(self, main_tab: str, fn: DriverFn) -> None:
        """main_tab: driver.current_window_handle"""
        logger.info("---go to new tab")
        for window_handle in self.window_handles:
            if window_handle != main_tab:
                self.switch_to.window(window_handle)
                break
        else:
            self.quit()
            raise Exception("cant go to new tab")
        fn(self)
        logger.info("---going back to main tab")
        self.close()
        self.switch_to.window(main_tab)

    def clear_input(self, css: str) -> WebElement:
        logger.info("clearing input")
        ele = self.waiting(css)
        v = ele.get_attribute("value")
        assert v is not None
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        return ele
