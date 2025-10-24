"""
This is the right side (tk.Frame) of an app.
Its layout consists of 3 buttons [Save, Load, Run] and 1 checkboxes [Headless].
Its config is the class `RunConfig` with save load methods.
You can `bind_save`, `bind_load`, `bind_run` functions onto the corresponding buttons.
"""

from dataclasses import dataclass
from typing import Self
import tkinter as tk
from pathlib import PurePath

from cch_his_auto.common_structs import ABCConfig


@dataclass(repr=False, eq=False, frozen=True)
class RunConfig(ABCConfig):
    APP_PATH = PurePath(__file__).parent.parent
    FILE_PATH = APP_PATH / "run_config.json"

    headless: bool = True

    @classmethod
    def from_dict(cls, value) -> Self:
        return cls(value["headless"])

    def is_valid(self) -> bool:
        return True


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
        tk.Checkbutton(
            self,
            text="Headless",
            variable=self.headless,
        ).grid(row=4, column=0, pady=5)

    def bind_load(self, f):
        self.load_btn.configure(command=f)

    def bind_save(self, f):
        self.save_btn.configure(command=f)

    def bind_run(self, f):
        self.run_btn.configure(command=f)

    def get_config(self) -> RunConfig:
        return RunConfig(self.headless.get())

    def save_config(self):
        self.get_config().save()

    def load_config(self):
        cfg = RunConfig.load()

        self.headless.set(cfg.headless)
