from flask import Blueprint, jsonify, render_template, request, session
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required
from web.extentions.pagination import calcPagination
from web.models.user import User
from web.services.admin.manage_users import get_users_by_role, create_staff, delete_staff
from web.models.user import UserRole

admin_user_bp = Blueprint("admin_user_bp", __name__, url_prefix="/admin")

@admin_user_bp.route("/staff")
@admin_required
def staff_list():
    page = int(request.args.get("pageIndex", 1))
    search = request.args.get("search", "")
    page_size = 5

    users, total_pages, total_records = get_users_by_role(UserRole.staff, page, page_size, search)
    pagination = calcPagination(page, total_pages)

    return render_template("admin/manage_users/user_list.html",
                           users=users,
                           currentPage=page,
                           totalPage=total_pages,
                           totalRecords = total_records,
                           pagination=pagination,
                           search=search)

@admin_user_bp.route("/user")
@admin_required
def user_list():
    page = int(request.args.get("pageIndex", 1))
    search = request.args.get("search", "")
    page_size = 5

    users, total_pages, total_records = get_users_by_role(UserRole.user, page, page_size, search)
    pagination = calcPagination(page, total_pages)

    return render_template("admin/manage_users/user_list.html",
                           users=users,
                           currentPage=page,
                           totalPage=total_pages,
                           totalRecords = total_records,
                           pagination=pagination,
                           search=search)

@admin_user_bp.route("/api/staff/add", methods=["POST"])
@admin_required
def api_add_staff():
    data = request.get_json() or {}
    phone = data.get("phone")
    password = data.get("password")

    staff, error = create_staff(phone, password)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    return jsonify({
        "status": "success",
        "staff": {
            "id": staff.Id, 
            "phone": staff.Phone,
            "role": staff.Role.value,  
            "created_at": (
                staff.Created_at.strftime("%Y-%m-%d %H:%M")
                if staff.Created_at else None
            )
        }
    })

@admin_user_bp.route("/api/staff/delete/<int:staff_id>", methods=["DELETE"])
@admin_required
def api_delete_staff(staff_id):
    success, message = delete_staff(staff_id)

    if not success:
        return jsonify({"status": "error", "message": message}), 404

    return jsonify({"status": "success", "message": message})