import time
import logging
from pathlib import PurePath
from contextlib import contextmanager
from typing import Protocol

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import Keys

from . import tracing
from .errors import WaitClosingException


_lgr = logging.getLogger("driver")


class Driver(webdriver.Chrome):
    "Preconfigured chrome driver with some convenient methods."

    def __init__(
        self, headless: bool = False, profile_path: PurePath | str | None = None
    ):
        """
        - `headless`: run driver in headless mode
        - `profile_path`: provide a profile path for more efficient subsequent uses
        """
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
        Can raise NoSuchElementException
        """
        try:
            _lgr.debug(f"waiting {name or css}")
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except TimeoutException:
            _lgr.error(f"-> can't find {name or css}")
            raise NoSuchElementException(f"can't find {name or css}")
        except StaleElementReferenceException:
            return self.waiting(css, name)
        else:
            _lgr.debug(f"-> done waiting {name or css}")
            return self.find(css)

    def wait_closing(self, css: str, /, name: str = "") -> None:
        """
        Wait element by `css` to be closed.
        You can also provide a `name` for logging
        Can raise WaitClosingException
        """
        try:
            _lgr.debug(f"closing {name or css}")
            WebDriverWait(self, 120).until_not(lambda _: self.find(css).is_displayed())
        except TimeoutException:
            _lgr.error(f"-> can't close {name or css}")
            raise WaitClosingException(f"can't close {name or css}")
        except StaleElementReferenceException:
            return self.wait_closing(css, name)
        else:
            _lgr.debug(f"-> done closing {name or css}")

    def waiting_to_startswith(self, css: str, w: str, /, name: str = "") -> WebElement:
        """
        Waiting element by `css` with textContent startswith `w`.
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        try:
            _lgr.debug(f"waiting {name or css} to be {w}")
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except TimeoutException:
            _lgr.error(f"-> can't find {name or css}")
            raise NoSuchElementException(f"can't find {name or css}")
        except StaleElementReferenceException:
            return self.waiting_to_startswith(css, w, name)
        else:
            for _ in range(120):
                time.sleep(1)
                try:
                    if (ele := self.find(css)).text.strip().startswith(w.strip()):
                        _lgr.debug(f"-> done waiting {name or css} startswith {w}")
                        return ele
                except StaleElementReferenceException:
                    continue
            else:
                txt = self.find(css).text.strip()
                ctx = f"-> found {name or css} but not startswith {w}. Found {txt} instead."
                _lgr.error(ctx)
                raise NoSuchElementException(ctx)

    def clicking(self, css: str, /, name: str = "") -> None:
        """
        Clicking element by `css`.
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        try:
            _lgr.debug(f"clicking {name or css}")
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except TimeoutException:
            _lgr.error(f"-> can't find {name or css}")
            raise NoSuchElementException(f"can't find {name or css}")
        except StaleElementReferenceException:
            return self.clicking(css, name)
        else:
            ele = self.find(css)
            ActionChains(self).scroll_to_element(ele).pause(1).click(ele).perform()
            _lgr.debug(f"-> done clicking {name or css}")

    def clicking2(self, css: str, /, name: str = "") -> None:
        """
        Clicking non-clickable element by `css`.
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        try:
            _lgr.debug(f"clicking non-clickable {name or css}")
            WebDriverWait(self, 120).until(lambda _: self.find(css).is_displayed())
        except TimeoutException:
            _lgr.error(f"-> can't find {name or css}")
            raise NoSuchElementException(f"can't find {name or css}")
        except StaleElementReferenceException:
            return self.clicking2(css, name)
        else:
            self.execute_script(f"""
                let evt = document.createEvent("MouseEvents");
                evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                document.querySelector('{css}').dispatchEvent(evt);
            """)
            _lgr.debug(f"-> done clicking non-clickable {name or css}")

    def sign_staff_signature(
        self, btn_css: str, btn_txt: str, img_css: str, name: str = ""
    ):
        """
        Try of sign staff, provided:
        - `btn_css`: the sign button css
        - `btn_txt`: the text on sign button
        - `img_css`: the signature css
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        for _ in range(120):
            try:
                _lgr.debug(f"finding {name} button")
                self.find(btn_css)
            except NoSuchElementException:
                _lgr.debug("-> can't find sign button, finding signature instead")
                try:
                    self.find(img_css)
                except NoSuchElementException:
                    _lgr.debug("-> can't find signature -> next in loop")
                    time.sleep(1)
                    continue
                else:
                    _lgr.info("-> found signature already signed")
                    return
            else:
                break
        else:
            raise NoSuchElementException(f"can't find {btn_css}")

        ele = self.find(btn_css)
        target = btn_txt.strip()
        for _ in range(120):
            if ele.text.strip().startswith(target):
                _lgr.debug("-> found sign button with correct btn_txt")
                break
            else:
                _lgr.debug("-> found sign button but wrong btn_txt -> next in loop")
                time.sleep(1)
                continue
        else:
            raise NoSuchElementException(f"found {btn_css} but not startswith {target}")

        time.sleep(1)
        ele.click()

        try:
            self.waiting(img_css, "signature image")
        except NoSuchElementException:
            self.refresh()
            self.waiting(img_css, "signature image 2nd time")

    def sign_canvas(self, signature: str):
        "use when patient signature needed to be signed"
        self.waiting("canvas")
        script = """
            let c = document.querySelector('canvas');
            let ctx = c.getContext('2d');
            let image = new Image();
            image.onload = function() {{
                ctx.drawImage(image, 0, 0, 400, 200);
            }};
            image.src = '{signature}'
            """.format(signature=signature)

        self.execute_script(script)
        time.sleep(3)
        self.clicking("canvas")
        self.clicking(
            ".ant-modal .bottom-action-right button",
            "save after finish drawing signature",
        )

    def sign_patient_signature(
        self,
        btn_css: str,
        btn_txt: str,
        img_css: str,
        signature: str,
        name: str = "",
    ):
        """
        Try of sign patient signature, provided:
        - `btn_css`: the sign button css
        - `btn_txt`: the text on sign button
        - `img_css`: the signature css
        - `signature`: the signature data
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        for _ in range(120):
            try:
                _lgr.debug(f"finding {name} button")
                ele = self.find(btn_css)
            except NoSuchElementException:
                _lgr.debug("-> can't find sign button, finding signature instead")
                try:
                    self.find(img_css)
                except NoSuchElementException:
                    _lgr.debug("-> can't find signature -> continue")
                    time.sleep(1)
                    continue
                else:
                    _lgr.info("-> found signature already signed")
                    return
            else:
                break
        else:
            raise NoSuchElementException(f"can't find {btn_css}")

        ele = self.find(btn_css)
        target = btn_txt.strip()
        for _ in range(120):
            if ele.text.strip().startswith(target):
                _lgr.debug("-> found sign button with correct btn_txt")
                break
            else:
                _lgr.debug("-> found sign button but wrong btn_txt -> next in loop")
                time.sleep(1)
                continue
        else:
            raise NoSuchElementException(f"found {btn_css} but not startswith {target}")

        time.sleep(1)
        ele.click()
        self.sign_canvas(signature)

        try:
            self.waiting(img_css, "signature image")
        except NoSuchElementException:
            self.refresh()
            self.waiting(img_css, "signature image 2nd time")

    def goto(self, url: str) -> None:
        "Go to `url`"
        _lgr.info(f"---goto {url}")
        self.get(url)
        time.sleep(2)

    def goto_newtab(self, current_tab: str) -> None:
        """
        Go to a tab different than `current_tab`
        - `current_tab`: you can can this using `driver.current_window_handle`
        """
        _lgr.debug("---go to new tab")
        time.sleep(1)
        assert len(self.window_handles) == 2, "there are two tabs"
        for w in self.window_handles:
            if w != current_tab:
                self.switch_to.window(w)
                break
        else:
            _lgr.error("-> can't go to new tab")
            raise Exception("can't go to new tab")

    def do_next_tab_do[T](self, f1: "DriverFn", f2: "DriverFn[T]") -> T:
        "Execute `f1` which open a new tab, execute `f2` then go back"
        current_tab = self.current_window_handle
        f1(self)
        self.goto_newtab(current_tab)
        try:
            return f2(self)
        finally:
            _lgr.debug("---go back to current tab")
            self.close()
            self.switch_to.window(current_tab)
            time.sleep(2)

    def duplicate_tab_do(self, f: "DriverFn"):
        "Duplicate the current tab and execute `f`"
        current_tab = self.current_window_handle
        url = self.current_url
        self.switch_to.new_window("tab")
        self.goto(url)
        try:
            f(self)
        finally:
            _lgr.info("---going back to main tab")
            self.close()
            self.switch_to.window(current_tab)
            time.sleep(2)

    def clear_input(self, css: str) -> WebElement:
        "Find element by `css` then clear it"
        _lgr.debug("clearing input")
        ele = self.waiting(css)
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        time.sleep(2)
        return ele

    def get_input_value(self, css: str, /, name="") -> str:
        """
        Get value attr of an input
        You can also provide a `name` for logging
        Can raise NoSuchElementException
        """
        for _ in range(30):
            time.sleep(1)
            try:
                value = self.find(css).get_attribute("value")
                assert value is not None
                if value == "":
                    continue
                else:
                    _lgr.info(f"-> found {name}={value}")
                    return value
            except NoSuchElementException:
                ...
        else:
            raise NoSuchElementException(f"-> can't find {name}")

    @contextmanager
    def iframe(self, iframe_css: str, close_btn_cs: str):
        "Use as contextmanager for going in and out an iframe inside a modal with close button"
        try:
            _lgr.debug("go into iframe")
            iframe = self.waiting(iframe_css)
            self.switch_to.frame(iframe)
            yield
        finally:
            _lgr.debug("go back to parent frame")
            self.switch_to.parent_frame()
            self.find(close_btn_cs).click()
            self.wait_closing(iframe_css)


class DriverFn[T](Protocol):
    "A function typing hint that accepts Driver as first argument"

    def __call__(self, driver: Driver, /, *args, **kwargs) -> T: ...


@contextmanager
def start_driver(headless: bool, profile_path: str):
    tracing.enter()
    _lgr.info("################## DRIVER STARTING")
    d = Driver(headless, profile_path)
    try:
        yield d
    finally:
        _lgr.info("################## DRIVER QUITTING")
        tracing.close()
        d.quit()
