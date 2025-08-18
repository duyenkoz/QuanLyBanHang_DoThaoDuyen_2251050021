import json
from math import ceil
from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for, flash
from web.models import Product
from web.services.admin.manage_products import (
    check_product_exists,
    get_products,
    update_product,
    update_product_status,
    create_product,
    get_product_by_id,
    delete_product
)
from web.services import category as cateService
from werkzeug.utils import secure_filename
import os
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required

admin_prod_bp = Blueprint("admin_prod_bp", __name__, url_prefix="/admin")


@admin_prod_bp.route("/manage-products", methods=["GET"])
@admin_required
def admin_manage_products():
    search = request.args.get("search", "")
    page = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", default=10, type=int)

    products, pagination, total_records = get_products(
        search=search, page=page, page_size=page_size
    )

    role = session.get("role")

    return render_template(
        "admin/manage_products/product_list.html",
        products=products,
        search=search,
        totalRecords=total_records,
        currentPage=page,
        pagination=pagination,
        role=role
    )

@admin_prod_bp.route("/manage-products/create", methods=["GET", "POST"])
@admin_required
def bp_create_product():
    if request.method == "POST":
        title = request.form.get("Title")
        price = request.form.get("Price")
        description = request.form.get("Description")
        status = int(request.form.get("Status"))
        category_id = int(request.form.get("CategoryID"))
        image_file = request.files.get("Image")
        image_filename = None
        if image_file and image_file.filename != "":
            image_filename = secure_filename(image_file.filename)
            image_folder = os.path.join(os.getcwd(), "web/static", "images")
            os.makedirs(image_folder, exist_ok=True)  # Tạo thư mục nếu chưa có
            image_path = os.path.join(image_folder, image_filename)
            image_file.save(image_path)
        result = create_product(
            title=title,
            price=price,
            description=description,
            status=status,
            category_id=category_id,
            image_filename=image_filename,
        )

        if result:
            flash("Thêm sản phẩm thành công!", "success")
        else:
            flash("Thêm sản phẩm thất bại!", "danger")
        return redirect(url_for("admin_prod_bp.admin_manage_products"))

    categories = cateService.get_categories_parent_id_notnull()
    return render_template(
        "admin/manage_products/create_product.html", categories=categories
    )


@admin_prod_bp.route("/manage-products/edit/<int:product_id>", methods=["GET"])
@admin_required
def edit_product_get(product_id):
    product = get_product_by_id(product_id)

    if not product:
        flash("Không tìm thấy sản phẩm!", "danger")
        return redirect(url_for("admin.admin_manage_products"))
    if product.Img and not product.Img.startswith("images/"):
        product.Img = f"images/{product.Img}"

    categories = cateService.get_categories_parent_id_notnull()
    return render_template(
        "admin/manage_products/edit_product.html",
        product=product,
        categories=categories,
    )


@admin_prod_bp.route("/manage-products/edit/<int:product_id>", methods=["POST"])
@admin_required
def edit_product_post(product_id):
    product = check_product_exists(product_id)
    if not product:
        flash("Không tìm thấy sản phẩm!", "danger")
        return redirect(url_for("admin.admin_manage_products"))

    title = request.form.get("Title")
    price = request.form.get("Price")
    description = request.form.get("Description")
    status = int(request.form.get("Status"))
    category_id = int(request.form.get("CategoryID"))
    image_file = request.files.get("Image")
    image_filename = None
    if image_file and image_file.filename != "":
        image_filename = secure_filename(image_file.filename)
        image_folder = os.path.join(os.getcwd(), "web/static/images")
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, image_filename)
        image_file.save(image_path)

    result = update_product(
        product_id=product_id,
        title=title,
        price=price,
        description=description,
        status=status,
        category_id=category_id,
        image_filename=image_filename,
    )

    if not result:
        flash("Cập nhật sản phẩm thất bại!", "danger")
        return redirect(url_for("admin.admin_manage_products"))

    flash("Cập nhật sản phẩm thành công!", "success")
    return redirect(url_for("admin_prod_bp.admin_manage_products"))


# API
@admin_prod_bp.route("api/manage-products/update-status/<int:product_id>", methods=["POST"])
@admin_required
def bp_update_product_status(product_id):
    result = update_product_status(product_id)
    response = APIResponse()
    if result is not None:
        response.status_code = ResponseStatus.SUCCESS.value
        response.message = "Cập nhật trạng thái thành công!"
        response.data = {"new_status": result}
    else:
        response.status_code = ResponseStatus.ERROR.value
        response.message = "Có lỗi xảy ra"
    return jsonify(response.to_dict())

@admin_prod_bp.route("api/manage-products/delete-product/<int:product_id>", methods=["DELETE"])
@admin_required
def bp_delete_product(product_id):
    result = delete_product(product_id)
    response = APIResponse()
    if result is not None:
        response.status_code = ResponseStatus.SUCCESS.value
        response.message = "Xóa sản phẩm thành công!"
        response.data = {"new_status": result}
    else:
        response.status_code = ResponseStatus.ERROR.value
        response.message = "Có lỗi xảy ra"
    return jsonify(response.to_dict())

