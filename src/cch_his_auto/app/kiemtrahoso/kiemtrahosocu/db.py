import sqlite3
import os.path
from . import APP_PATH

DB_PATH = os.path.join(APP_PATH, ".db")
DB_NAME = "kiemtrahosocu"

def create_connection():
    con = sqlite3.Connection(DB_PATH)

    con.executescript(f"""
    CREATE TABLE IF NOT EXISTS {DB_NAME} (
        id INTEGER PRIMARY KEY
    );
    """)
    return con

def save_db(con: sqlite3.Connection, id: int):
    con.execute(f"INSERT INTO {DB_NAME} VALUES (?)", (id,))
    con.commit()

def filter_listing(con: sqlite3.Connection, csv_path: str) -> list[int]:
    listing = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        for id in f.readlines():
            if con.execute(
                f"SELECT EXISTS( SELECT * FROM {DB_NAME} WHERE id =?)", (id,)
            ).fetchone() == (0,):
                listing.append(int(id))
    return listing
