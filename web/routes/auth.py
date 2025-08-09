from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from web.services.auth import check_login, register_user

from web import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        user = check_login(phone, password)
        if user:
            session["user_phone"] = user.Phone
            session["user_id"] = user.Id
            return redirect(url_for("home"))

        flash("Số điện thoại hoặc mật khẩu không đúng.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        success, message = register_user(phone, password, confirm_password)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))  
        else:
            flash(message, 'danger')

    return render_template('auth/sign_up.html')

@auth_bp.route("/logout")
def logout():
    # Xóa session đăng nhập
    session.clear()
    flash("Đăng xuất thành công!", "success")
    return redirect(url_for("home"))  