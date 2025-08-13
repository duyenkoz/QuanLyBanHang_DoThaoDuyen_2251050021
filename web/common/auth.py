from functools import wraps
from flask import session, redirect, url_for, flash
from web.models.user import UserRole

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_phone' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
