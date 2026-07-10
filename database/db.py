import os
import sqlite3
import mysql.connector

def get_db_connection():
    # If running on Vercel, use a local SQLite database file
    if os.environ.get('VERCEL'):
        # Creates or connects to a local file in the Vercel container
        conn = sqlite3.connect('busnanban.db')
        conn.row_factory = sqlite3.Row  
        return conn
    else:
        # Connects to your local MySQL server when running on your computer
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234", # Use your actual PC MySQL password here
            database="bus_nanban"
        )