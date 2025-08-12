from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_phone' not in session:
            flash("Vui lòng đăng nhập để truy cập trang quản trị.", "error")
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash("Bạn không có quyền truy cập trang quản trị.", "error")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
