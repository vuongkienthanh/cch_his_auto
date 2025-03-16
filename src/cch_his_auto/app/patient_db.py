import sqlite3
import os.path

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".db")
DB_NAME = "patients"

def create_connection():
    con = sqlite3.Connection(DB_PATH)

    con.executescript(f"""
    CREATE TABLE IF NOT EXISTS {DB_NAME} (
        id INTEGER PRIMARY KEY,
        url BLOB,
        signature BLOB
    );
    """)
    return con

def save_db(con: sqlite3.Connection, url: bytes, signature: bytes):
    con.execute(
        f"INSERT INTO {DB_NAME} (id, url, signature) VALUES (?, ?, ?)",
        (id, url, signature),
    )
    con.commit()

def exists(con: sqlite3.Connection, id: int) -> bool:
    return bool(
        con.execute(
            f"SELECT EXISTS( SELECT * FROM {DB_NAME} WHERE id =?)", (id,)
        ).fetchone()[0]
    )

def get_url(con: sqlite3.Connection, id: int) -> bytes:
    return con.execute(f"SELECT url FROM {DB_NAME} WHERE id=?", (id,)).fetchone()[0]

def get_signature(con: sqlite3.Connection, id: int) -> bytes:
    return con.execute(f"SELECT signature FROM {DB_NAME} WHERE id=?", (id,)).fetchone()[
        0
    ]
