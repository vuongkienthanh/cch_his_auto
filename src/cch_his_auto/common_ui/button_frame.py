import tkinter as tk
from typing import TypedDict
import os.path
import json
import logging

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILEPATH = os.path.join(APP_PATH, "run_config.json")


class RunConfig(TypedDict):
    headless: bool
    debug: bool


def setLogLevel(cfg: RunConfig):
    if cfg["debug"]:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


class ButtonFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.load_btn = tk.Button(self, text="Load", width=10)
        self.load_btn.grid(row=0, column=0, pady=5)
        self.save_btn = tk.Button(self, text="Save", width=10)
        self.save_btn.grid(row=1, column=0, pady=5)
        self.run_btn = tk.Button(
            self,
            text="RUN",
            width=10,
            bg="#ff0073",
            fg="#ffffff",
        )
        self.run_btn.grid(row=3, column=0, pady=5)

        self.headless = tk.BooleanVar()
        self.debug = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Headless",
            variable=self.headless,
        ).grid(row=4, column=0, pady=5)
        tk.Checkbutton(
            self,
            text="Debug",
            variable=self.debug,
        ).grid(row=5, column=0, pady=5)

    def bind_load(self, f):
        self.load_btn.configure(command=f)

    def bind_save(self, f):
        self.save_btn.configure(command=f)

    def bind_run(self, f):
        self.run_btn.configure(command=f)

    def get_config(self) -> RunConfig:
        return {
            "headless": self.headless.get(),
            "debug": self.debug.get(),
        }

    def save_config(self):
        cfg = self.get_config()
        os.makedirs(APP_PATH, exist_ok=True)
        with open(FILEPATH, "w") as f:
            json.dump(cfg, f, indent=4)

    def load_config(self):
        try:
            with open(FILEPATH, "r") as f:
                cfg = json.load(f)
        except Exception as _:
            cfg = {
                "headless": False,
                "debug": False,
            }

        self.headless.set(cfg["headless"])
        self.debug.set(cfg["debug"])


class ButtonFrame2(ButtonFrame):
    def __init__(self, parent, custom_text: str):
        super().__init__(parent)
        self.custom_btn = tk.Button(self, text=custom_text, width=10)
        self.custom_btn.grid(row=2, column=0, pady=5)

    def bind_custom(self, f):
        self.custom_btn.configure(command=f)
