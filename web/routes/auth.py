from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from web.services.auth import check_login, register_user

from web import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        result = check_login(phone, password)
        if result:
            obj = result["obj"]
            role_name = obj.role.RoleName   # nhờ backref role trong model

            session["user_id"] = obj.UserId if result["type"] == "user" else obj.CustomerId
            session["user_phone"] = obj.Phone
            session["role"] = role_name
            session["user_name"] = obj.Name.strip() if obj.Name else role_name

            # Điều hướng theo role
            if role_name == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif role_name == "staff":
                return redirect(url_for("admin.admin_dashboard"))
            elif role_name == "shipper":
                return redirect(url_for("shipper.shipper_dashboard"))
            else:  # customer
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
    session.clear()
    flash("Đăng xuất thành công!", "success")
    return redirect(url_for("home"))  