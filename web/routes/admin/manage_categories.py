from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from web.services.admin.manage_categories import (
    get_categories, 
    get_category_by_id, 
    get_children_by_parent_id, 
    update_category_status,
    create_child_category,
    update_inline_category_service,
    get_all_parent_categories,
    create_category)


admin_cate_bp = Blueprint("admin_cate_bp", __name__, url_prefix="/admin")
from web.common.auth import admin_required

@admin_cate_bp.route("/manage-categories", methods=["GET"])
@admin_required
def admin_manage_categories():
    search = request.args.get("search", "")
    page = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", default=10, type=int)

    categories, pagination, total_records = get_categories(
        search=search, page=page, page_size=page_size
    )
    role = session.get("role")

    return render_template(
        "admin/manage_categories/category_list.html",
        categories=categories,
        search=search,
        totalRecords=total_records,
        currentPage=page,
        pagination=pagination,
        role=role
    )

@admin_cate_bp.route("/manage-categories/<int:parent_id>/children", methods=["GET"])
@admin_required
def manage_child_categories(parent_id):
    parent = get_category_by_id(parent_id)
    if not parent:
        flash("Không tìm thấy danh mục cha.", "danger")
        return redirect(url_for("admin_cate_bp.admin_manage_categories"))

    children = get_children_by_parent_id(parent_id)

    return render_template(
        "admin/manage_categories/create_child.html",
        parent=parent,
        children=children
    )

@admin_cate_bp.route("/manage-categories/create", methods=["GET", "POST"])
@admin_required
def admin_create_category():
    if request.method == "POST":
        title = request.form.get("Title")
        parent_id = request.form.get("ParentID") or None  # Nếu rỗng thì None
        status = request.form.get("Status")
        type_value = request.form.get("Type")  # Chỉ có khi là danh mục cha
        type_code_value = request.form.get("TypeCode")  # Chỉ có khi là danh mục con

        result = create_category(title, parent_id, type_value, type_code_value, status)

        if result["success"]:
            flash("Thêm danh mục thành công", "success")
            return redirect(url_for("admin_cate_bp.admin_manage_categories"))
        else:
            flash(f"Lỗi: {result['error']}", "danger")

    parent_categories = get_all_parent_categories()
    return render_template("admin/manage_categories/create_category.html", parent_categories=parent_categories)
    
#API
@admin_cate_bp.route("/api/manage-categories/update-status/<int:category_id>", methods=["POST"])
@admin_required
def api_update_category_status(category_id):

    result = update_category_status(category_id)
    if result:
        return {
            "status_code": "SUCCESS",
            "message": "Cập nhật trạng thái thành công",
            "data": result
        }
    else:
        return {
            "status_code": "ERROR",
            "message": "Không tìm thấy danh mục"
        }, 404
    
@admin_cate_bp.route("/api/manage-categories/<int:parent_id>/children", methods=["POST"])
@admin_required
def api_create_child_category(parent_id):
    try:
        title = request.form.get("Title")
        type_code = request.form.get("TypeCode")
        type = request.form.get("Type")
        status = int(request.form.get("Status", 1))

        result = create_child_category(title, parent_id, type, type_code, status)

        return {
            "status_code": "SUCCESS",
            "message": "Thêm danh mục con thành công",
            "data": result
        }
    except Exception as e:
        return {
            "status_code": "ERROR",
            "message": str(e)
        }, 500

@admin_cate_bp.route("/api/manage-categories/update-inline/<int:cate_id>", methods=["POST"])
@admin_required
def update_inline_category(cate_id):
    data = request.get_json()
    title = data.get("title")
    type = data.get("type")
    is_parent = data.get("is_parent")
    type_code = data.get("type_code")  # Lấy thêm cho child

    result = update_inline_category_service(cate_id, title, type, is_parent, type_code)
    return jsonify(result)