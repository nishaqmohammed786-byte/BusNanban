import os

class Config:
    # Secret key for signing cookies and session data (keep this secure!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bus_nanban_chennai_secret_key_2026'
    
    # Database Configuration for XAMPP MariaDB on Port 3307
    DB_HOST = '127.0.0.1'
    DB_PORT = 3307
    DB_USER = 'root'
    DB_PASSWORD = ''  # XAMPP root has no password by default
    DB_NAME = 'bus_nanban'