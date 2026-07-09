from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
import os

admin_bp = Blueprint('admin', __name__)

def get_db_connection():
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'busnanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    conn = get_db_connection()
    buses = conn.execute('SELECT * FROM buses').fetchall()
    tickets_count = conn.execute('SELECT COUNT(*) FROM tickets').fetchone()[0]
    users_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()
    
    return render_template(
        'admin_dashboard.html', 
        buses=buses, 
        tickets_count=tickets_count, 
        users_count=users_count
    )

@admin_bp.route('/bus/add', methods=['POST'])
def add_bus():
    bus_number = request.form.get('bus_number')
    source = request.form.get('source')
    destination = request.form.get('destination')
    bus_type = request.form.get('bus_type')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    duration = request.form.get('duration')
    fare = request.form.get('fare')

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO buses (bus_number, source, destination, bus_type, departure_time, arrival_time, duration, fare)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bus_number, source, destination, bus_type, departure_time, arrival_time, duration, fare))
    conn.commit()
    conn.close()
    
    flash(f"Bus service {bus_number} added to active inventory successfully!", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/bus/delete/<int:bus_id>', methods=['POST'])
def delete_bus(bus_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM buses WHERE id = ?', (bus_id,))
    conn.commit()
    conn.close()
    
    flash("Bus service removed from operation.", "success")
    return redirect(url_for('admin.dashboard'))