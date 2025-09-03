from typing import TypedDict
import json
from pathlib import PurePath
import os

from cch_his_auto.structs import LogInfo

APP_PATH = PurePath(__file__).parent
FILEPATH = APP_PATH / "config.json"


class Ky_3tra(TypedDict):
    bacsi: tuple[bool, bool, bool, bool, bool]
    dieuduong: tuple[bool, bool, bool, bool, bool]
    benhnhan: tuple[bool, bool, bool, bool, bool]


class Todieutri(TypedDict):
    url: str
    note: str
    ky_xn: bool
    ky_todieutri: bool
    ky_3tra: Ky_3tra


class Bienbanhoichan(TypedDict):
    url: str
    note: str
    ky_thuky: bool
    ky_truongkhoa: bool
    ky_thanhvienkhac: bool
    khac_note: str


class Config(TypedDict):
    bacsi: LogInfo
    dieuduong: LogInfo
    truongkhoa: LogInfo
    thanhvienkhac: LogInfo
    department: str
    todieutri: list[Todieutri]
    bienbanhoichan: list[Bienbanhoichan]


def save(config: Config):
    os.makedirs(APP_PATH, exist_ok=True)
    with open(FILEPATH, "w") as f:
        json.dump(config, f, indent=4)


def load() -> Config:
    try:
        with open(FILEPATH, "r") as f:
            return json.load(f)
    except Exception as _:
        return {
            "bacsi": {
                "username": "",
                "password": "",
            },
            "dieuduong": {
                "username": "",
                "password": "",
            },
            "truongkhoa": {
                "username": "",
                "password": "",
            },
            "thanhvienkhac": {
                "username": "",
                "password": "",
            },
            "department": "",
            "todieutri": [],
            "bienbanhoichan": [],
        }


