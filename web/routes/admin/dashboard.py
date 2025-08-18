from flask import Blueprint, jsonify, render_template, request, session
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required
from web.services.admin import dashboard as dashboard_service

admin_dashboard_bp = Blueprint("admin_dashboard_bp", __name__, url_prefix="/admin")

@admin_dashboard_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    data = dashboard_service.get_dashboard_data()
    print(data)
    return render_template("admin/dashboard/index.html", data=data)
