import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'busnanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_bus_table():
    """Initializes the inventory table for running bus route configurations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            bus_type TEXT NOT NULL, -- 'AC', 'Deluxe', 'Normal'
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            duration TEXT NOT NULL,
            fare INTEGER NOT NULL
        )
    ''')
    conn.commit()
    
    # Let's seed initial data if the inventory table is brand new and empty
    check_empty = cursor.execute('SELECT COUNT(*) FROM buses').fetchone()[0]
    if check_empty == 0:
        seed_data = [
            ("51A", "Kilambakkam", "Guindy", "AC", "08:15 AM", "08:40 AM", "25 mins", 35),
            ("A1", "Kilambakkam", "Guindy", "Deluxe", "08:30 AM", "09:00 AM", "30 mins", 18),
            ("E18", "Kilambakkam", "Guindy", "Normal", "08:45 AM", "09:20 AM", "35 mins", 12)
        ]
        cursor.executemany('''
            INSERT INTO buses (bus_number, source, destination, bus_type, departure_time, arrival_time, duration, fare)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)
        conn.commit()
        
    conn.close()

def search_buses(source, destination, bus_type='Any'):
    """Queries active running fleet based on user filter entries."""
    conn = get_db_connection()
    query = "SELECT * FROM buses WHERE LOWER(source) = LOWER(?) AND LOWER(destination) = LOWER(?)"
    params = [source, destination]
    
    if bus_type != 'Any':
        query += " AND bus_type = ?"
        params.append(bus_type)
        
    results = conn.execute(query, params).fetchall()
    conn.close()
    return results