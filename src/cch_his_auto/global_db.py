import sqlite3
import os.path

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".db")
DB_NAME = "ma_ho_so"


def create_connection():
    con = sqlite3.Connection(DB_PATH)

    con.executescript(f"""
    CREATE TABLE IF NOT EXISTS {DB_NAME} (
        ma_hs INTEGER PRIMARY KEY,
        signature TEXT
    );
    """)
    return con


def save_db(con: sqlite3.Connection, ma_hs: int, signature: str):
    con.execute(
        f"INSERT INTO {DB_NAME} (ma_hs, signature) VALUES (?, ?)",
        (ma_hs, signature),
    )
    con.commit()


def get_signature_from_db(con: sqlite3.Connection, ma_hs: int) -> str | None:
    if ret := con.execute(
        f"SELECT signature FROM {DB_NAME} WHERE ma_hs=?", (ma_hs,)
    ).fetchone():
        return ret[0]
