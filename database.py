import sqlite3
from settings import DATABASE_FILE


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS download_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            title TEXT NOT NULL,
            url TEXT,
            file_path TEXT,
            quality TEXT,
            status TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    connection.commit()
    connection.close()


def add_download_history(video_id, title, url, file_path, quality, status):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO download_history
        (video_id, title, url, file_path, quality, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (video_id, title, url, file_path, quality, status))
    connection.commit()
    connection.close()


def get_download_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, video_id, title, url, file_path,
               quality, status, downloaded_at
        FROM download_history
        ORDER BY downloaded_at DESC, id DESC
    """)
    rows = cursor.fetchall()
    connection.close()
    return rows


def delete_history_item(history_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM download_history WHERE id = ?", (history_id,))
    connection.commit()
    connection.close()


def clear_download_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM download_history")
    connection.commit()
    connection.close()


def save_setting(key, value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO app_settings (key, value)
        VALUES (?, ?)
    """, (key, str(value)))
    connection.commit()
    connection.close()


def get_setting(key, default=None):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    connection.close()
    return row["value"] if row else default


initialize_database()
