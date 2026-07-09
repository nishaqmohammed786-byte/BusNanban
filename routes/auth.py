from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import get_user_by_phone, create_user, update_user_name

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number', '').strip()
        otp = request.form.get('otp', '').strip()
        username = request.form.get('username', '').strip()

        # 1. Enforce validation on our simulated OTP (1234)
        if otp != "1234":
            flash("Incorrect OTP entered. Please try again with '1234'!", "error")
            return render_template('login.html')

        # 2. Look up if the commuter exists in our database file
        user = get_user_by_phone(phone_number)

        if user:
            # Existing User: Log them straight into the browser session
            session['user_id'] = user['id']
            # If they provided a name, update their account profile details
            if username:
                update_user_name(phone_number, username)
                session['username'] = username
            else:
                session['username'] = user['name'] if user['name'] else "Commuter"
                
            session['phone_number'] = user['phone_number']
            flash(f"Welcome back to BusNanban! 👋", "success")
        else:
            # New User registration flow
            fallback_name = username if username else "Commuter"
            new_user_id = create_user(phone_number, fallback_name)
            
            session['user_id'] = new_user_id
            session['username'] = fallback_name
            session['phone_number'] = phone_number
            flash("Account created and verified successfully! 🎫", "success")

        return redirect(url_for('profile'))

    # GET Request serves the login layout template
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out from terminal session.", "success")
    return redirect(url_for('index'))