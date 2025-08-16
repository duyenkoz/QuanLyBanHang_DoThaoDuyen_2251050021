from flask import Blueprint, jsonify, render_template, request, session
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required
from web.models.user import User
from web.services.admin.manage_users import  add_user, get_users_by_role

admin_user_bp = Blueprint("admin_user_bp", __name__, url_prefix="/admin")

@admin_user_bp.route("/manage-users", methods=["GET"])
@admin_required
def admin_manage_users():
    current_role = session.get("role")
    users = get_users_by_role(current_role)
    return render_template(
        "admin/manage_users/user_list.html",
        users=users, 
        currentPage=1,
        totalPage=1,
        search="",
        pagination=[],
        role=current_role,
        has_actions=(current_role == "admin")
    )

@admin_user_bp.route('/manage-users/add-user', methods=['POST'])
@admin_required
def add_user_route():
    data = request.form
    phone = data.get('phone')
    password = data.get('password')

    result = add_user(phone, password)

    if result['success']:
        # Lấy user vừa thêm từ DB để lấy ID
        user = User.query.filter_by(Phone=phone).first()
        result['new_user'] = {
            'ID': user.Id,
            'CreatedAt': user.CreatedAt.strftime('%d-%m-%Y')
        }

    return jsonify(result)