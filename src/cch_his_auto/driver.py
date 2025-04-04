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
_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
_logger.addHandler(logging.StreamHandler(sys.stdout))

class DriverFn(Protocol):
    "A function typing hint that accepts Driver as first argument"

    def __call__(self, driver: "Driver", /, *args, **kwargs) -> None: ...

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
        _logger.info("opening chrome ...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")

        # intent to reduce page load
        # but not working in sign_canvas
        # options.add_experimental_option(
        #     "prefs", {"profile.managed_default_content_settings.images": 2}
        # )

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
        try:
            _logger.info(f"---waiting {name or css}")
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
            _logger.info(f"-->>done waiting {name or css}")
            time.sleep(2)
            return self.find(css)
        except Exception as e:
            _logger.error(f"-->>cant find {name or css}")
            raise e

    def waiting_to_be(self, css: str, to_be: str, /, name: str = "") -> WebElement:
        """
        Waiting element by `css` with textContent equals `to_be`.
        You can also provide a `name` for logging
        """
        _logger.info(f"---waiting {name or css} to be {to_be}")

        try:
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except Exception as e:
            _logger.error(f"-->>cant find {name or css}")
            raise e

        for _ in range(120):
            time.sleep(1)
            if self.find(css).text.strip().startswith(to_be.strip()):
                _logger.info(f"-->>done waiting {name or css} to be {to_be}")
                time.sleep(2)
                return self.find(css)
        else:
            txt = self.find(css).text.strip()
            ctx = f'{name or css} with to_be="{to_be}" is not equal to {txt}'
            _logger.error(f"-->>no such element: {ctx}")
            raise NoSuchElementException(ctx)

    def clicking(self, css: str, /, name: str = "") -> None:
        """
        Clicking element by `css`.
        You can also provide a `name` for logging
        """
        _logger.info(f"---clicking {name or css}")
        try:
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except Exception as e:
            _logger.error(f"-->>cant find {name or css}")
            raise e

        try:
            ele = self.find(css)
            ActionChains(self).scroll_to_element(ele).pause(1).click(ele).perform()
            _logger.info(f"-->>done clicking {name or css}")
            time.sleep(2)
        except Exception as e:
            _logger.error(f"-->>can't click {name or css}")
            raise e

    def goto(self, url: str) -> None:
        "Go to `url`"
        _logger.info(f"---goto {url}")
        self.get(url)
        time.sleep(2)

    def goto_newtab(self, main_tab: str) -> None:
        """
        Go to a tab different than `main_tab`
        - `main_tab`: you can can this using `driver.current_window_handle`
        """
        _logger.info("---go to new tab")
        for window_handle in self.window_handles:
            if window_handle != main_tab:
                self.switch_to.window(window_handle)
                time.sleep(2)
                break
        else:
            raise Exception("-->>cant go to new tab")

    def goto_newtab_do_smth_then_goback(self, main_tab: str, fn: DriverFn) -> None:
        """
        Go to a tab different than `main_tab` and execute `fn`.
        - `main_tab`: you can can this using `driver.current_window_handle`
        """
        self.goto_newtab(main_tab)
        fn(self)
        _logger.info("---going back to main tab")
        self.close()
        self.switch_to.window(main_tab)
        time.sleep(2)

    def clear_input(self, css: str) -> WebElement:
        "Find element by `css` then clear it"
        _logger.info("---clearing input")
        ele = self.waiting(css)
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        time.sleep(2)
        return ele

__all__ = ["Driver", "DriverFn"]
