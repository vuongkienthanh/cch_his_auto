from typing import TypedDict


class LogInfo(TypedDict):
    username: str
    password: str


def is_user_valid(cfg: LogInfo) -> bool:
    return cfg["username"] != "" and cfg["password"] != ""
