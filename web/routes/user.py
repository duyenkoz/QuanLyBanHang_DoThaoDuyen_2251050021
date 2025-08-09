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
        address = request.form.get("address")
        ward = request.form.get("ward")
        district = request.form.get("district")
        province = request.form.get("province")

        success, message = update_user_profile(
            user_id, full_name, address, ward, district, province
        )
        flash(message, "success" if success else "danger")

        # Reload lại user sau khi cập nhật
        user = get_user_by_id(user_id)

    return render_template("user/profile.html", user=user)
