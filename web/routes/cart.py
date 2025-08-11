from flask import Blueprint, jsonify, render_template, request
from web.services import cart as cartService
from web.common.api_response import APIResponse, ResponseStatus

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart", methods=["GET"])
def cart_page():
    return render_template("cart/index.html")


# API
@cart_bp.post("/api/cart")
def api_get_product_filter():
    data = request.get_json()
    cart = data.get("cart", None)
    response = APIResponse()
    if not cart:
        response.status_code = ResponseStatus.ERROR.value
        response.message = "Không tìm thấy giỏ hàng"
        return jsonify(response.to_dict())

    cart_items, total_item, total_price = cartService.get_products_in_cart(cart)
    response.status_code = ResponseStatus.SUCCESS.value
    response.data = render_template(
        "components/cart_items.html",
        cart_items=cart_items,
        total_item=total_item,
        total_price=total_price,
    )
    return jsonify(response.to_dict())

@cart_bp.post("/api/cart/checkout")
def api_checkout():
    data_payment = request.get_json()
    cart = data_payment.get("cart", None)
    response = APIResponse()
    if not cart:
        response.status_code = ResponseStatus.ERROR.value
        response.message = "Không tìm thấy giỏ hàng"
        return jsonify(response.to_dict())

    checkout_result = cartService.save_order(data_payment)
    if checkout_result == "SUCCESS":
        response.status_code = ResponseStatus.SUCCESS.value
    else:
        response.status_code = ResponseStatus.ERROR.value
        response.message = checkout_result

    return jsonify(response.to_dict())
