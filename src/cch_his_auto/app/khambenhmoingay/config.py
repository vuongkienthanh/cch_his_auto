from typing import Literal, TypedDict
import json
import os.path
import os

from validators import url

APP_PATH = os.path.dirname(os.path.abspath(__file__))
FILEPATH = os.path.join(APP_PATH, "config.json")
PHCN_ORDER = ["bú nuốt", "giao tiếp", "hô hấp", "vận động"]


class LogInfo(TypedDict):
    username: str
    password: str


class Ky_3tra(TypedDict):
    bacsi: tuple[bool, bool, bool, bool, bool]
    dieuduong: tuple[bool, bool, bool, bool, bool]
    benhnhan: tuple[bool, bool, bool, bool, bool]


class Patient(TypedDict):
    url: str
    note: str
    ky_xetnghiem: bool
    ky_ct: bool
    ky_mri: bool
    ky_bbhc: bool
    ky_todieutri: bool
    ky_3tra: Ky_3tra


class Config(TypedDict):
    bacsi: LogInfo
    dieuduong: LogInfo
    truongkhoa: LogInfo
    department: str
    patients: list[Patient]


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
            "department": "",
            "patients": [],
        }


def is_patient_list_valid(config: Config) -> bool:
    return (len(config["patients"]) > 0) & all(
        [
            url(p["url"]) and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in p["url"])
            for p in config["patients"]
        ]
    )


def is_valid(config: Config, kind: Literal["bacsi", "dieuduong", "truongkhoa"]) -> bool:
    return config[kind]["username"] != "" and config[kind]["password"] != ""
