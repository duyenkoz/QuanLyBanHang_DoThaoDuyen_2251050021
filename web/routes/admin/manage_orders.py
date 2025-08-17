# web/admin/order.py
import datetime
from flask import Blueprint, jsonify, render_template, request
from web.common.api_response import APIResponse, ResponseStatus
from web.models import Order  # Model đơn hàng
from web.services.admin.manage_orders import get_orders_by_status, update_order_status
from web.services import order as orderService
from web import db


admin_order_bp = Blueprint(
    "admin_order_bp", __name__, url_prefix="/admin/manage-orders"
)


# @admin_order_bp.route("/")
# def admin_manage_orders():
#     search = request.args.get("search", "").strip()
    

#     page = int(request.args.get("page", 1))

#     orders, pagination, total_records, total_pages = get_all_orders(
#         search, page, page_size=10
#     )

#     return render_template(
#         "admin/manage_orders/order_list.html",
#         orders=orders,
#         pagination=pagination,
#         currentPage=page,
#         totalPage=total_pages,
#         search=search,
#         total_records=total_records
#     )

@admin_order_bp.route("/admin/manage-orders", methods=["GET"])
def admin_manage_orders():
    status = request.args.get("status") 
    page = int(request.args.get("pageIndex", 1))
    search = request.args.get("search", "").strip()

    has_actions = status in ["WAITING_CONFIRM", "CONFIRMED", "SHIPPING"]

    orders, pagination, total_records, total_pages = get_orders_by_status(status, page, 10, search)

    return render_template(
        "admin/manage_orders/order_list.html",
        orders=orders,
        search=search,
        totalRecords=total_records,
        currentPage=page,
        totalPage=total_pages,
        pagination=pagination,
        status=status,
        has_actions=has_actions
    )

@admin_order_bp.route("/api/detail/<int:order_id>", methods=["GET"])
def api_order_detail(order_id):
    order = orderService.get_order_detail_by_orderid(order_id)
    if not order:
        return jsonify(APIResponse(status=ResponseStatus.ERROR.value, message="Order not found"))
    
    order_details = orderService.get_order_detail_by_orderid(order_id)
    response = APIResponse()
    response.status_code = ResponseStatus.SUCCESS.value
    response.data = render_template(
    "order/order-detail.html",
    order_details=order_details
)
    return jsonify(response.to_dict())

@admin_order_bp.route("/api/update-status/<int:order_id>", methods=["POST"])
def api_update_order_status(order_id):
    new_status = request.json.get("status")

    order, error = update_order_status(order_id, new_status)  

    if error:
        return jsonify(APIResponse(
            status_code=ResponseStatus.ERROR.value,  
            message=error
        ).to_dict()), 400 if "Thiếu" in error else 404
    
    response = APIResponse(
        status_code=ResponseStatus.SUCCESS.value,   
        message="Cập nhật trạng thái thành công",
        data={"order_id": order.ID, "new_status": order.Status}
    )
    return jsonify(response.to_dict()), 200