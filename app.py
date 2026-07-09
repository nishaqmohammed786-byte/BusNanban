import os
from flask import Flask, render_template, session
from models.user import init_user_table
from models.bus import init_bus_table
from models.ticket import init_ticket_table

def create_app():
    app = Flask(__name__)
    
    # Secure random secret key for customer sessions and security flash messaging
    app.secret_key = os.urandom(24)

    # Boot up and synchronize database schema across all subsystem modules
    with app.app_context():
        init_user_table()
        init_bus_table()
        init_ticket_table()

    # Import and register Blueprints
    # Import and register Blueprints
    from routes.auth import auth_bp
    from routes.search import search_bp
    from routes.admin import admin_bp  # Make sure it says routes.admin here!

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Core Application Global Mapping Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/payment')
    def payment():
        return render_template('payment.html')

    @app.route('/profile')
    def profile():
        # Session checking barrier for secure client profile rendering
        if not session.get('user_id'):
            return render_template('login.html')
        return render_template('profile.html')
    
    @app.route('/profile')
    def profile_dashboard():  # Changed from "profile" to "profile_dashboard"
        # Session security barrier: send to login if not authenticated
        if not session.get('user_id'):
            return render_template('login.html')
            
        from models.ticket import get_user_active_tickets
        # Fetch active running tickets using the verified passenger's unique system id
        passenger_tickets = get_user_active_tickets(session['user_id'])
        
        return render_template('profile.html', tickets=passenger_tickets)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Adding host='0.0.0.0' tells Flask to open up to mobile connections
    app.run(host='0.0.0.0', port=5000, debug=True)