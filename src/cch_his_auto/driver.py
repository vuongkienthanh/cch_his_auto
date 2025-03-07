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
    "A function typing hint that accepts Driver as first argument"

    def __init__(self, *args, **kwargs) -> None:
        "@private"
        super().__init__(*args, **kwargs)

    def __call__(self, driver: "Driver", *args, **kwargs) -> None: ...

class Driver(webdriver.Chrome):
    """
    Preconfigured chrome driver with some convenient methods.
    """

    def __init__(
        self, headless: bool = False, profile_path: PurePath | str | None = None
    ):
        """
        - `headless`: run driver in headless mode
        - `profile_path`: provide a profile path for more efficient subsequent use
        """
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

    def find(self, css: str) -> WebElement:
        "Find element by `css`"
        return self.find_element(By.CSS_SELECTOR, css)

    def find_all(self, css: str) -> list[WebElement]:
        "Find all elements by `css`"
        return self.find_elements(By.CSS_SELECTOR, css)

    def waiting(self, css: str, /, name: str = "") -> WebElement:
        """
        Waiting element by `css`.
        You can also provide a `name` for logging
        """
        logger.info(f"---waiting {name or css}")
        WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        logger.info(f"---done waiting {name or css}")
        return self.find(css)

    def waiting_to_be(self, css: str, to_be: str, /, name: str = "") -> WebElement:
        """
        Waiting element by `css` with textContent equals `to_be`.
        You can also provide a `name` for logging
        """
        logger.info(f"---waiting {name or css} to be {to_be}")
        WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        if to_be:
            for _ in range(120):
                time.sleep(1)
                if self.find(css).text.strip().startswith(to_be.strip()):
                    logger.info(f"-->> found {to_be}")
                    break
            else:
                txt = self.find(css).text.strip()
                ctx = f"{name or css} with to_be {to_be} != textContent {txt}"
                logger.error(f"---no such element: {ctx}")
                raise NoSuchElementException(ctx)
        logger.info(f"---done waiting {name or css} to be {to_be}")
        return self.find(css)

    def clicking(self, css: str, /, name: str = "") -> None:
        """
        Clicking element by `css`.
        You can also provide a `name` for logging
        """
        logger.info(f"---clicking {name or css}")
        logger.setLevel(logging.CRITICAL)
        ele = self.waiting(css, name)
        ActionChains(self).scroll_to_element(ele).pause(1).click(ele).perform()
        logger.setLevel(logging.INFO)
        logger.info(f"---done clicking {name or css}")

    def goto(self, url: str) -> None:
        "Go to `url`"
        logger.info(f"---goto {url}")
        self.get(url)

    def goto_newtab_do_smth_then_goback(self, main_tab: str, fn: DriverFn) -> None:
        """
        Go to a tab different than `main_tab` and execute `fn`.
        - `main_tab`: you can can this using `driver.current_window_handle`
        """
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
        "Find element by `css` then clear it"
        logger.info("clearing input")
        logger.setLevel(logging.CRITICAL)
        ele = self.waiting(css)
        logger.setLevel(logging.INFO)
        v = ele.get_attribute("value")
        assert v is not None
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        return ele

__all__ = ["Driver", "DriverFn"]
