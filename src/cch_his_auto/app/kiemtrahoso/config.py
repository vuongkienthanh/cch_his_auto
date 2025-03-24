from typing import TypedDict
import json
import os.path
import os

from . import APP_PATH

FILEPATH = os.path.join(APP_PATH, "config.json")

class Config(TypedDict):
    headless: bool
    username: str
    password: str
    department: str
    listing: str
    discharged: bool
    is_final_day: bool

def save(config: Config):
    os.makedirs(APP_PATH, exist_ok=True)
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
            "listing": "",
            "discharged": False,
            "is_final_day": False,
        }
