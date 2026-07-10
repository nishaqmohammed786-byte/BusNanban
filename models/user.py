import sqlite3
from flask import g
# Import your actual get_db function from wherever your db/database file is located
# For example, if it's in a file named database.py in your root: from database import get_db
from database import get_db 

def init_user_table():
    db = get_db()
    cursor = db.cursor()
    
    # Check if the connection type is SQLite (Vercel) or MySQL (Local PC)
    if isinstance(db, sqlite3.Connection):
        # --- SQLite syntax for Vercel ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
    else:
        # --- MySQL syntax for your Local PC ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        
    db.commit()
    cursor.close()
    # Note: Do NOT call db.close() here because your close_db() function 
    # automatically handles closing it when the web request ends!