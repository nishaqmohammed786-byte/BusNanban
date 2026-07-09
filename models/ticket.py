import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'busnanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_ticket_table():
    """Initializes the tickets table to log transactions and digital passes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bus_id INTEGER NOT NULL,
            ticket_uid TEXT UNIQUE NOT NULL, -- Format e.g., BN-2026-XXXX
            status TEXT DEFAULT 'ACTIVE',    -- 'ACTIVE', 'USED', 'EXPIRED'
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')
    conn.commit()
    conn.close()

def create_ticket(user_id, bus_id):
    """Generates a secure digital boarding pass transaction record."""
    import random
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate a professional ticket reference UID string for 2026
    ticket_uid = f"BN-2026-{random.randint(1000, 9999)}"
    
    cursor.execute(
        'INSERT INTO tickets (user_id, bus_id, ticket_uid) VALUES (?, ?, ?)',
        (user_id, bus_id, ticket_uid)
    )
    conn.commit()
    conn.close()
    return ticket_uid

def get_user_active_tickets(user_id):
    """Fetches valid digital passes for a passenger dashboard."""
    conn = get_db_connection()
    query = '''
        SELECT t.ticket_uid, t.status, b.bus_number, b.source, b.destination, 
               b.bus_type, b.departure_time, b.arrival_time, b.fare
        FROM tickets t
        JOIN buses b ON t.bus_id = b.id
        WHERE t.user_id = ? AND t.status = 'ACTIVE'
        ORDER BY t.booking_time DESC
    '''
    tickets = conn.execute(query, (user_id,)).fetchall()
    conn.close()
    return tickets