from flask import Blueprint, flash, redirect, render_template, request, url_for

from web.services.admin.manage_categories import get_categories, create_category


admin_cate_bp = Blueprint("admin_cate_bp", __name__, url_prefix="/admin")


@admin_cate_bp.route("/manage-categories", methods=["GET"])
def admin_manage_categories():
    search = request.args.get("search", "")
    page = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", default=10, type=int)

    categories, pagination, total_records = get_categories(
        search=search, page=page, page_size=page_size
    )

    return render_template(
        "admin/manage_categories/category_list.html",
        categories=categories,
        search=search,
        totalRecords=total_records,
        currentPage=page,
        pagination=pagination,
    )

@admin_cate_bp.route("/manage-categories/create", methods=["GET"])
def create_parent_category():
    return render_template("admin/manage_categories/create_category.html")

@admin_cate_bp.route("/manage-categories/create", methods=["POST"])
def handle_create_parent_category():
    try:
        title = request.form.get("Title")
        type_ = request.form.get("Type")
        status = int(request.form.get("Status", 1))

        create_category(title, type_, status)
        flash("Thêm danh mục lớn thành công!", "success")
        return redirect(url_for("admin_cate_bp.admin_manage_categories"))

    except Exception as e:
        flash(str(e), "danger")
        return redirect(request.url)
    
@admin_cate_bp.route("/manage-categories/create-sub", methods=["POST"])
def create_sub_category():
    try:
        title = request.form.get("SubTitle")
        type_ = request.form.get("SubType")
        status = int(request.form.get("SubStatus", 1))
        parent_id = int(request.form.get("ParentID"))

        create_category(title, type_, status, parent_id)
        flash("Thêm danh mục nhỏ thành công!", "success")
        return redirect(url_for("admin_cate_bp.admin_manage_categories"))

    except Exception as e:
        flash(str(e), "danger")
        return redirect(request.referrer)