import sqlite3
import os.path

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".db")
DB_NAME = "patients"

def create_connection():
    con = sqlite3.Connection(DB_PATH)

    con.executescript(f"""
    CREATE TABLE IF NOT EXISTS {DB_NAME} (
        id INTEGER PRIMARY KEY,
        url TEXT,
        signature TEXT
    );
    """)
    return con

def save_db(con: sqlite3.Connection, _id: int, url: str, signature: str):
    con.execute(
        f"INSERT INTO {DB_NAME} (id, url, signature) VALUES (?, ?, ?)",
        (_id, url, signature),
    )
    con.commit()

def exists_in_db(con: sqlite3.Connection, _id: int) -> bool:
    return bool(
        con.execute(
            f"SELECT EXISTS( SELECT * FROM {DB_NAME} WHERE id =?)", (_id,)
        ).fetchone()[0]
    )

def get_url_from_db(con: sqlite3.Connection, _id: int) -> str:
    return con.execute(f"SELECT url FROM {DB_NAME} WHERE id=?", (_id,)).fetchone()[0]

def get_signature_from_db(con: sqlite3.Connection, _id: int) -> str:
    return con.execute(
        f"SELECT signature FROM {DB_NAME} WHERE id=?", (_id,)
    ).fetchone()[0]
