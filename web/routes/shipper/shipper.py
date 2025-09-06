from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from web import app
from math import ceil
from web.common.auth import shipper_required
from web.extentions.pagination import calcPagination
from web.models.order import Order
from web.common.api_response import APIResponse, ResponseStatus
from web.services import order as orderService
from web.services.shipper import manage_orders as shipper_orderService 



shipper_bp = Blueprint('shipper', __name__, url_prefix='/shipper')
    
@shipper_bp.route('/', methods=['GET'])
@shipper_required
def shipper_dashboard():
     return render_template("shipper/index.html")

@shipper_bp.route("/manage-orders")
def shipper_manage_orders():
    status = request.args.get("status")
    page = request.args.get("pageIndex", 1, type=int)  # số trang hiện tại
    page_size = app.config.get("PAGE_SIZE", 5)        # số bản ghi mỗi trang (config)
    shipper_id = session.get("user_id")               # lấy từ session

    if not shipper_id:
        return redirect(url_for("auth.login"))

    query = Order.query.filter(Order.ShipperId == shipper_id)

    if status:
        query = query.filter(Order.Status == status)

    total_records = query.count()
    total_pages = ceil(total_records / page_size) if total_records else 1

    orders = (
        query.order_by(Order.Created.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # Pagination hiển thị dãy số trang
    pagination = calcPagination(total_records, page, page_size)

    return render_template(
        "shipper/manage_orders.html",
        orders=orders,
        status=status,
        currentPage=page,
        totalPage=total_pages,
        pagination=pagination,
        total_records=total_records
    )

@shipper_bp.route("/api/order/detail/<int:order_id>", methods=["GET"])
def api_order_detail(order_id):
    order = orderService.get_order_detail_by_orderid(order_id)
    if not order:
        return jsonify(APIResponse(status=ResponseStatus.ERROR.value, message="Order not found"))
    
    order_details = orderService.get_order_detail_by_orderid(order_id)
    response = APIResponse()
    response.status_code = ResponseStatus.SUCCESS.value
    response.data = render_template("order/order-detail.html", order_details=order_details)
    return jsonify(response.to_dict())

@shipper_bp.route("/api/order/update-status", methods=["POST"])
def shipper_update_order_status():
    data = request.get_json()
    order_id = data.get("order_id")
    action = data.get("action")  
    shipper_id = session.get("user_id")
    reason = data.get("reason")

    if not order_id or not action:
        return jsonify({"status": "ERROR", "message": "Thiếu dữ liệu"}), 400

    if action == "CONFIRM":  # Đơn mới -> SHIPPING
        success, message = shipper_orderService.update_order_status(order_id, new_status="SHIPPING", shipper_id=shipper_id)

    elif action == "CANCEL_ASSIGN":  # Hủy gán shipper (ShipId = NULL)
        success, message = shipper_orderService.update_order_status(order_id, remove_shipper=True)

    elif action == "DELIVERED":  # Đang giao -> Hoàn tất
        success, message = shipper_orderService.update_order_status(order_id, new_status="DELIVERED")

    elif action == "CANCEL_SHIPPING":  # Đang giao -> Hủy (có lý do)
        if not reason:
            return jsonify({"status": "ERROR", "message": "Vui lòng nhập lý do hủy"}), 400
        success, message = shipper_orderService.update_order_status(order_id, new_status="CANCELED", cancel_reason=reason)

    else:
        return jsonify({"status": "ERROR", "message": "Hành động không hợp lệ"}), 400

    if success:
        return jsonify({"status": "SUCCESS", "message": message}), 200
    else:
        return jsonify({"status": "ERROR", "message": message}), 500