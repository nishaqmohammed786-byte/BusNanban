import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'busnanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_table():
    """Initializes the user table with mobile authentication fields."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_user_by_phone(phone_number):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,)).fetchone()
    conn.close()
    return user

def create_user(phone_number, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (phone_number, name) VALUES (?, ?)',
        (phone_number, name)
    )
    conn.commit()
    user_id = cursor.lastrow_index if hasattr(cursor, 'lastrow_index') else cursor.lastrowid
    conn.close()
    return user_id

def update_user_name(phone_number, name):
    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ? WHERE phone_number = ?', (name, phone_number))
    conn.commit()
    conn.close()