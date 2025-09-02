from typing import Literal, TypedDict
import json
from pathlib import PurePath
import os

from validators import url

APP_PATH = PurePath(__file__).parent
FILEPATH = APP_PATH / "config.json"


class LogInfo(TypedDict):
    username: str
    password: str


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


def is_patient_list_valid(cfg: Config) -> bool:
    return (
        len(cfg["todieutri"]) > 0
        and all(
            url(tdt["url"])
            and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in tdt["url"])
            for tdt in cfg["todieutri"]
        )
        and all(
            url(bbhc["url"])
            and ("chi-tiet-nguoi-benh-noi-tru/bien-ban-hoi-chan/" in bbhc["url"])
            for bbhc in cfg["bienbanhoichan"]
        )
    )


def is_valid(
    config: Config, kind: Literal["bacsi", "dieuduong", "truongkhoa", "thanhvienkhac"]
) -> bool:
    return config[kind]["username"] != "" and config[kind]["password"] != ""
