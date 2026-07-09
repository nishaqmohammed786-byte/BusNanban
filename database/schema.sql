import sqlite3
import os

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'busnanban.db')
SCHEMA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schema.sql')

def build_database_from_schema():
    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ Error: Could not find schema.sql at {SCHEMA_PATH}")
        return

    print("⏳ Reading schema.sql and setting up database tables...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute your custom schema.sql file directly
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print("✅ Database tables successfully created from schema.sql!")
    except sqlite3.Error as e:
        print(f"❌ SQL Execution Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    build_database_from_schema()