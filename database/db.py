import mysql.connector
from flask import current_app, g

def get_db():
    """Connects to the database and stores the connection in Flask's application context variable 'g'."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
    return g.db

def close_db(e=None):
    """Closes the database connection automatically when a web request ends."""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()