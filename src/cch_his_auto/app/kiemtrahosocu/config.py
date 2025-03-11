from typing import TypedDict
import json

import os.path

FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

class Config(TypedDict):
    headless: bool
    username: str
    password: str
    csv_path: str

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
            "username": "",
            "password": "",
            "csv_path": "",
        }
