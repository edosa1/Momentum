import sqlite3
from pathlib import Path

# Store the database in the user's home folder, so it works no matter
# which directory you run "habit" from.
DB_PATH = Path.home() / ".habit_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["name"]
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id),
            UNIQUE (habit_id, completed_date)
        )
    """)

    conn.commit()
    conn.close()
