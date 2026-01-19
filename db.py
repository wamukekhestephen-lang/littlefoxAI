import sqlite3
from contextlib import closing

DB_PATH = "database.db"  # SQLite file

def get_connection():
    """Get a new SQLite connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Allows dict-like access
    return conn

def init_db():
    """Create tables if they don't exist"""
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def save_message(chat_id, role, message):
    """Save a chat message to the database"""
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO chats (chat_id, role, message)
        VALUES (?, ?, ?)
        """, (chat_id, role, message))
        conn.commit()

def get_chats(chat_id):
    """Retrieve all messages for a chat session"""
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM chats WHERE chat_id = ? ORDER BY timestamp ASC
        """, (chat_id,))
        return cursor.fetchall()
