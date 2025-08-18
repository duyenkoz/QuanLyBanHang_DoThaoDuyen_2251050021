from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for, flash
from web.models import Product
from web.models.user import User
from web.services.product import get_product_by_title, get_all_products
from web.services import category as cateService
from web import db
from werkzeug.utils import secure_filename
import os
from web.common.auth import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
    
@admin_bp.route('/', methods=['GET'])
@admin_required
def admin_dashboard():
    return redirect(url_for('admin_dashboard_bp.dashboard'))

@admin_bp.route("/update_profile", methods=["POST"])
def update_profile():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.Name = name
        user.Phone = phone
        user.Email = email
        db.session.commit()
        updated_user = User.query.get(user_id)

        # Nếu tên rỗng thì set session bằng role
        session['user_name'] = updated_user.Name.strip() if updated_user.Name and updated_user.Name.strip() else session.get('role')
        session['user_phone'] = updated_user.Phone

        return jsonify({
            "success": True,
            "user": {
                "name": session['user_name'],  # Trả về luôn giá trị hiển thị
                "phone": updated_user.Phone,
                "email": updated_user.Email
            }
        })
    return jsonify({"success": False, "message": "Không tìm thấy tài khoản"})

@admin_bp.route('/get_profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "success": True,
            "user": {
                "name": user.Name,
                "phone": user.Phone,
                "email": user.Email
            }
        })
    return jsonify({"success": False, "message": "Không tìm thấy tài khoản"})

