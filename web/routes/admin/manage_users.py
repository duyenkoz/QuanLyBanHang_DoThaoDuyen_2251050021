from flask import Blueprint, jsonify, render_template, request, session
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required
from web.extentions.pagination import calcPagination
from web.models.role import Role
from web.models.user import User
from web.services.admin.manage_users import (
    get_users,
    create_staff,
    delete_staff,
    create_role,
    toggle_role_status,
    update_role_service,
    get_customers
)


admin_user_bp = Blueprint("admin_user_bp", __name__, url_prefix="/admin")


@admin_user_bp.route("/staff")
@admin_required
def staff_list():
    page = int(request.args.get("pageIndex", 1))
    search = request.args.get("search", "")
    page_size = 5

    users, total_pages, total_records = get_users(
        page, page_size, search
    )
    pagination = calcPagination(page, total_pages)
    roles = Role.query.filter(Role.RoleName != "customer").all()

    return render_template(
        "admin/manage_users/user_list.html",
        accounts=users,
        users=users,
        currentPage=page,
        totalPage=total_pages,
        totalRecords=total_records,
        pagination=pagination,
        search=search,
        roles=roles,
        type="STAFF",
    )

@admin_user_bp.route("/customer")
@admin_required
def customer_list():
    page = int(request.args.get("pageIndex", 1))
    search = request.args.get("search", "")
    page_size = 5

    customers, total_pages, total_records = get_customers(page, page_size, search)
    pagination = calcPagination(page, total_pages)

    return render_template(
        "admin/manage_users/user_list.html",
        accounts=customers,
        customers=customers,
        currentPage=page,
        totalPage=total_pages,
        totalRecords=total_records,
        pagination=pagination,
        search=search,
        type="CUSTOMER"
    )


@admin_user_bp.route("/api/staff/add", methods=["POST"])
@admin_required
def api_add_staff():
    data = request.get_json() or {}
    phone = data.get("phone")
    password = data.get("password")
    role_id = data.get("role_id")

    staff, error = create_staff(phone, password, role_id)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    return jsonify(
        {
            "status": "success",
            "staff": {
                "id": staff.UserId,
                "phone": staff.Phone,
                "created_at": (
                    staff.CreatedAt.strftime("%Y-%m-%d %H:%M")
                    if staff.CreatedAt
                    else None
                ),
                "role": {"RoleId": staff.role.RoleId, "RoleName": staff.role.RoleName},
            },
        }
    )

@admin_user_bp.route("/api/staff/delete/<int:staff_id>", methods=["DELETE"])
@admin_required
def api_delete_staff(staff_id):
    success, message = delete_staff(staff_id)

    if not success:
        return jsonify({"status": "error", "message": message}), 404

    return jsonify({"status": "success", "message": message})

@admin_user_bp.route("/api/role/add", methods=["POST"])
@admin_required
def add_role():
    data = request.get_json()
    role_name = data.get("roleName", "")
    role_desc = data.get("roleDesc", "")
    
    result, status = create_role(role_name, role_desc)
    return jsonify(result), status

@admin_user_bp.route("/api/role/<int:role_id>/toggle", methods=["POST"])
@admin_required
def toggle_role(role_id):
    result, status = toggle_role_status(role_id)
    return jsonify(result), status

@admin_user_bp.route("/api/role/<int:role_id>/update", methods=["PUT"])
@admin_required
def update_role(role_id):
    data = request.get_json()
    role_name = data.get("roleName", "").strip()
    role_desc = data.get("roleDesc", "").strip()

    result, status = update_role_service(role_id, role_name, role_desc)
    return jsonify(result), status