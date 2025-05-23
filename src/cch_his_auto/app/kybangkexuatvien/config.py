from typing import TypedDict
import os.path
import json
import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
FILEPATH = os.path.join(APP_PATH, "config.json")


class Config(TypedDict):
    username: str
    password: str
    department: str
    listing: str


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
            "username": "",
            "password": "",
            "department": "",
            "listing": "",
        }
