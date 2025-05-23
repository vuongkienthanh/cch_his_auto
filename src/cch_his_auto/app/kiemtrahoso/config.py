from typing import TypedDict
import json
import os.path
import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
FILEPATH = os.path.join(APP_PATH, "config.json")


class Config(TypedDict):
    username: str
    password: str
    department: str
    listing: str
    discharged: bool
    is_final_day: bool


def save(cfg: Config):
    os.makedirs(APP_PATH, exist_ok=True)
    with open(FILEPATH, "w") as f:
        json.dump(cfg, f, indent=4)


def load() -> Config:
    try:
        with open(FILEPATH, "r") as f:
            return json.load(f)
    except Exception as _:
        return {
            "username": "",
            "password": "",
            "department": "",
            "listing": "",
            "discharged": False,
            "is_final_day": False,
        }


def is_valid(cfg: Config) -> bool:
    return (
        cfg["username"] != ""
        and cfg["password"] != ""
        and cfg["department"] != ""
        and len(cfg["listing"].strip().splitlines()) > 0
    )
