from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from web import db
from sqlalchemy.orm.exc import NoResultFound
from web.models.user import User
from web.services.user import get_user_by_id, update_user_profile

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile", methods=["GET", "POST"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        flash("Bạn cần đăng nhập để xem trang này.", "warning")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(user_id)

    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        # address trên form giờ là street (hoặc có thể là full nếu người dùng gửi nhầm) -> lấy phần trước dấu phẩy
        address_raw = request.form.get("address", "") or ""
        street = address_raw.split(",")[0].strip() if address_raw else ""

        ward = request.form.get("ward_text")
        district = request.form.get("district_text")
        province = request.form.get("province_text")

        success, message = update_user_profile(
            user_id, full_name, email, street, ward, district, province
        )
        flash(message, "success" if success else "danger")
        return redirect(url_for("user.update_profile"))

    user = get_user_by_id(user_id)
    return render_template("user/profile.html", user=user)
