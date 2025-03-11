from typing import TypedDict
import json

from validators import url
import os.path

FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
PHCN_ORDER = ["bú nuốt", "giao tiếp", "hô hấp", "vận động"]

class LogInfo(TypedDict):
    username: str
    password: str

class Ky_3tra(TypedDict):
    bacsi: tuple[bool, bool, bool, bool, bool]
    dieuduong: tuple[bool, bool, bool, bool, bool]

class Patient(TypedDict):
    url: str
    note: str
    ky_xetnghiem: bool
    ky_todieutri: bool
    ky_3tra: Ky_3tra
    phcn: tuple[bool, bool, bool, bool]

class Config(TypedDict):
    headless: bool
    bacsi: LogInfo
    dieuduong: LogInfo
    patients: list[Patient]

def save(config: Config):
    with open(FILEPATH, "w") as f:
        json.dump(config, f, indent=4)

def load() -> Config:
    try:
        with open(FILEPATH, "r") as f:
            return json.load(f)
    except:
        return {
            "headless": False,
            "bacsi": {
                "username": "",
                "password": "",
            },
            "dieuduong": {
                "username": "",
                "password": "",
            },
            "patients": [],
        }

def is_patient_list_valid(config: Config) -> bool:
    return (len(config["patients"]) > 0) & all(
        [
            url(p["url"]) and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in p["url"])
            for p in config["patients"]
        ]
    )

def is_bs_valid(config: Config) -> bool:
    return (len(config["bacsi"]["username"]) > 0) & (
        len(config["bacsi"]["password"]) > 0
    )

def is_dd_valid(config: Config) -> bool:
    return (len(config["dieuduong"]["username"]) > 0) & (
        len(config["dieuduong"]["password"]) > 0
    )
