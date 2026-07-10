import sqlite3
from flask import g
from database import get_db  # Double-check if your database file is named 'database.py' or 'db.py'

def init_bus_table():
    db = get_db()
    cursor = db.cursor()
    
    if isinstance(db, sqlite3.Connection):
        # --- SQLite syntax for Vercel ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS buses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bus_number TEXT NOT NULL,
                route_name TEXT NOT NULL,
                total_seats INTEGER NOT NULL
            )
        """)
    else:
        # --- MySQL syntax for your Local PC ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS buses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bus_number VARCHAR(50) NOT NULL,
                route_name VARCHAR(100) NOT NULL,
                total_seats INT NOT NULL
            )
        """)
        
    db.commit()
    cursor.close()