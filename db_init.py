import sqlite3
import os

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'busnanban.db')

def build_database():
    print("⏳ Synchronizing SQLite Relational Database Engine schema...")
    
    # Establish disk data file stream connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Core Users Table Schema (Mobile Authenticated Layout)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Live Running Fleet Inventory Table Schema
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

    # 3. Booking Transactions and Pass Validation Logs Schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bus_id INTEGER NOT NULL,
            ticket_uid TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'ACTIVE', -- 'ACTIVE', 'USED', 'EXPIRED'
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (bus_id) REFERENCES buses (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()

    # 4. Check & Seed Running Fleet Master Rows Data
    cursor.execute('SELECT COUNT(*) FROM buses')
    if cursor.fetchone()[0] == 0:
        print("🌱 Seeding active Chennai MTC route corridors into inventory...")
        seed_buses = [
            ("51A", "Kilambakkam", "Guindy", "AC", "08:15 AM", "08:40 AM", "25 mins", 35),
            ("A1", "Kilambakkam", "Guindy", "Deluxe", "08:30 AM", "09:00 AM", "30 mins", 18),
            ("E18", "Kilambakkam", "Guindy", "Normal", "08:45 AM", "09:20 AM", "35 mins", 12),
            ("21G", "Vandalur", "Broadway", "Deluxe", "09:00 AM", "10:15 AM", "1 hr 15 mins", 24),
            ("119X", "Sholinganallur", "Velachery", "AC", "10:30 AM", "11:00 AM", "30 mins", 40)
        ]
        cursor.executemany('''
            INSERT INTO buses (bus_number, source, destination, bus_type, departure_time, arrival_time, duration, fare)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_buses)
        conn.commit()
        print(f"✅ Successfully seeded {len(seed_buses)} active bus fleets!")
    else:
        print("📋 Active running fleet data found. Skipping data seed.")

    conn.close()
    print("🚀 Database is fully synchronized and ready for queries!")

if __name__ == '__main__':
    build_database()