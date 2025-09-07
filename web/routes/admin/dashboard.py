from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, session
from web.common.api_response import APIResponse, ResponseStatus
from web.common.auth import admin_required
from web.services.admin import dashboard as dashboard_service

admin_dashboard_bp = Blueprint("admin_dashboard_bp", __name__, url_prefix="/admin")

@admin_dashboard_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    data = dashboard_service.get_dashboard_data()
    return render_template("admin/dashboard/index.html", data=data)

#API to get dashboard statistics
@admin_dashboard_bp.route("/api/chart/revenue", methods=["GET"])
def get_revenue_chart():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")
        mode = request.args.get("mode", "day")
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(from_date, date_format) if from_date else None
        end_date = datetime.strptime(to_date, date_format) if to_date else None
        data = dashboard_service.get_revenue_chart_data(start_date, end_date, mode)
        return jsonify(APIResponse(data=data, status_code=ResponseStatus.SUCCESS.value).to_dict())
    except Exception as e:
        return jsonify(APIResponse(message=str(e), status_code=ResponseStatus.ERROR.value).to_dict())
    
@admin_dashboard_bp.route("/api/chart/order", methods=["GET"])
def get_orders_chart():
    try:
        from_date = request.args.get("from")
        to_date = request.args.get("to")
        mode = request.args.get("mode", "day")
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(from_date, date_format) if from_date else None
        end_date = datetime.strptime(to_date, date_format) if to_date else None
        data = dashboard_service.get_orders_chart_data(start_date, end_date, mode)
        return jsonify(APIResponse(data=data, status_code=ResponseStatus.SUCCESS.value).to_dict())
    except Exception as e:
        return jsonify(APIResponse(message=str(e), status_code=ResponseStatus.ERROR.value).to_dict())