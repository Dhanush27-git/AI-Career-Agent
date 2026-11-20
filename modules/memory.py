
import sqlite3
from datetime import datetime

DB_NAME = "career_memory.db"


def initialize_memory():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE,
            preference_value TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_history (role, content, created_at) VALUES (?, ?, ?)",
        (role, content, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_chat_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT 20"
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"role": role, "content": content}
        for role, content in reversed(rows)
    ]


def save_preference(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_preferences (preference_key, preference_value)
        VALUES (?, ?)
        ON CONFLICT(preference_key)
        DO UPDATE SET preference_value = excluded.preference_value
    """, (key, value))

    conn.commit()
    conn.close()


def get_preferences():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT preference_key, preference_value FROM user_preferences"
    )

    preferences = dict(cursor.fetchall())
    conn.close()

    return preferences
def clear_chat_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chat_history")

    conn.commit()
    conn.close()
