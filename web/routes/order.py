from flask import Blueprint, jsonify, render_template, request, session
from web.services import cart as cartService
from web.common.api_response import APIResponse, ResponseStatus
from web.services import order as orderService

order_bp = Blueprint("order", __name__)


@order_bp.route("/order/me", methods=["GET"])
def my_order_page():
    user_id = session.get("user_id")
    page = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", default=10, type=int)
    if not user_id:
        return render_template("auth/login.html", next_url=request.url)
    orders, pagination, total_records, total_pages = orderService.get_user_order(user_id, page, page_size)
    return render_template(
        "order/user-order.html",
        orders=orders,
        pagination=pagination,
        total_records=total_records,
        currentPage=page,
        totalPage=total_pages,
    )


@order_bp.route("/api/order/detail/<int:order_id>", methods=["GET"])
def api_order_detail(order_id):
    order = orderService.get_order_detail_by_orderid(order_id)
    if not order:
        return jsonify(
            APIResponse(status=ResponseStatus.ERROR.value, message="Order not found")
        )

    order_details = orderService.get_order_detail_by_orderid(order_id)
    response = APIResponse()
    response.status_code = ResponseStatus.SUCCESS.value
    response.data = render_template(
        "order/order-detail.html", order_details=order_details
    )
    return jsonify(response.to_dict())
