from flask import Blueprint, jsonify, render_template, request, session
from web.models.topping import Topping
from web.services import cart as cartService
from web.common.api_response import APIResponse, ResponseStatus
from web.services import product as productService
from web.services import user as userService
from web.sockets import socketio


cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart", methods=["GET", "POST"])
def cart_page():
    user_id = session.get("user_id")

    user = userService.get_user_by_id(user_id)

    return render_template("cart/index.html", user=user)

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
        # Socket để thông báo cho admin
        socketio.emit("new_order", {"id": 123}, namespace="/admin", room="admin_room")
        response.status_code = ResponseStatus.SUCCESS.value
    else:
        response.status_code = ResponseStatus.ERROR.value
        response.message = checkout_result

    return jsonify(response.to_dict())

@cart_bp.post("/api/cart/edit/<int:product_id>")
def api_edit_detail(product_id):
    product = productService.get_product_by_id(product_id)
    if not product:
        return jsonify(APIResponse(status_code=ResponseStatus.ERROR.value, message="Sản phẩm không tồn tại"))
    toppings = productService.get_toppings()
    data = request.get_json()
    cart_item = data.get("cart_item", {})
    size = cart_item.get("size", "M")
    qty = cart_item.get("quantity", 1)
    topping_ids = cart_item.get("toppings", [])
    price = product.Price
        
    if size == "L":
        price += 7000
    
    topping_price = 0
    topping_names = []

    if topping_ids:
        for t_id in topping_ids:
            topping = next((tp for tp in toppings if tp.ID == int(t_id)), None)
            if topping:
                topping_price += topping.Price
                topping_names.append(topping.Name)

    price += topping_price
    total_price = price * qty
    cart_item["price_item"] = price
    cart_item["total_price"] = total_price
        
    return render_template(
        "components/product_cart_detail.html", 
        product=product, 
        toppings=toppings,
        cart_item=cart_item
    )

