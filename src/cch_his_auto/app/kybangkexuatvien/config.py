from typing import TypedDict
import os.path
import json
import os

from . import APP_PATH

FILEPATH = os.path.join(APP_PATH, "config.json")

class Config(TypedDict):
    headless: bool
    username: str
    password: str
    department: str
    ds_ma_hs: str

def save(config: Config):
    os.makedirs(APP_PATH)
    with open(FILEPATH, "w") as f:
        json.dump(config, f, indent=4)

def load() -> Config:
    try:
        with open(FILEPATH, "r") as f:
            return json.load(f)
    except:
        return {
            "headless": False,
            "username": "",
            "password": "",
            "department": "",
            "ds_ma_hs": "",
        }
