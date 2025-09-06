from functools import wraps
from flask import session, redirect, url_for, flash
# from web.models.user import UserRole

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = session.get("role")
        if not session.get("user_phone"):
            flash("Vui lòng đăng nhập trước.", "warning")
            return redirect(url_for("auth.login"))

        # Chỉ cho phép admin và staff
        if role not in ("admin", "staff"):
            flash("Bạn không có quyền truy cập trang này.", "danger")
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    return decorated_function

def shipper_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("role") != "shipper":
            flash("Bạn không có quyền truy cập trang này!", "danger")
            return redirect(url_for("admin_user.login"))
        return f(*args, **kwargs)
    return decorated_function