import sqlite3
from flask import g
from database import get_db

def init_ticket_table():
    db = get_db()
    cursor = db.cursor()
    
    if isinstance(db, sqlite3.Connection):
        # --- SQLite syntax for Vercel ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                bus_id INTEGER NOT NULL,
                booking_date TEXT NOT NULL,
                status TEXT DEFAULT 'Booked'
            )
        """)
    else:
        # --- MySQL syntax for your Local PC ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                bus_id INT NOT NULL,
                booking_date DATETIME NOT NULL,
                status VARCHAR(50) DEFAULT 'Booked'
            )
        """)
        
    db.commit()
    cursor.close()

def get_user_active_tickets(user_id):
    db = get_db()
    cursor = db.cursor()
    
    # Query to fetch running active tickets for a passenger profile
    if isinstance(db, sqlite3.Connection):
        cursor.execute("SELECT * FROM tickets WHERE user_id = ?", (user_id,))
        tickets = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM tickets WHERE user_id = %s", (user_id,))
        tickets = cursor.fetchall()
        
    cursor.close()
    return tickets