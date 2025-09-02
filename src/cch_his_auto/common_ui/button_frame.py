"""
This is the right side (tk.Frame) of an app.
Its layout consists of 3 buttons [Save, Load, Run] and 2 checkboxes [Headless, Debug].
Its config is typed hint to `RunConfig`.
The frame provides `save_config`, and `load_config` for `RunConfig`.
You can `bind_save`, `bind_load`, `bind_run` functions onto the corresponding buttons.
"""

import tkinter as tk
from typing import TypedDict
from pathlib import PurePath
import os
import json
import logging


APP_PATH = PurePath(__file__).parent.parent
FILEPATH = APP_PATH / "run_config.json"


class RunConfig(TypedDict):
    headless: bool
    debug: bool


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
            command=self.setLogLevel,
        ).grid(row=5, column=0, pady=5)

    def setLogLevel(self):
        if self.debug.get():
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def bind_load(self, f):
        self.load_btn.configure(command=f)

    def bind_save(self, f):
        self.save_btn.configure(command=f)

    def bind_run(self, f):
        self.run_btn.configure(command=f)

    def get_config(self) -> RunConfig:
        self.setLogLevel()
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
