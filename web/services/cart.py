from flask import session
from web.common.enum import OrderStatusEnum, SaveOrderStatusEnum
from web.dtos.cart_dto import CartDTO
from web.models.product import Product
from web.models.topping import Topping


def get_products_in_cart(cart: list[dict[any, any]]) -> tuple[list[CartDTO], int, int]:
    """Hàm lấy danh sách sản phẩm trong giỏ hàng"""
    list_cart_dto: list[CartDTO] = []
    for item in cart:
        product: Product = Product.query.get(item["productid"])
        if not product:
            continue
        qty = item.get("quantity", 1)
        size = item.get("size", None)
        topping_ids = item.get("toppings", [])
        sugar = item.get("sugar", None)
        ice = item.get("ice", None)

        price = product.Price
        
        if size == "L":
            price += 7000
        
        topping_price = 0
        topping_names = []

        if topping_ids:
            toppings: list[Topping] = Topping.query.filter(Topping.ID.in_(topping_ids)).all()
            for t in toppings:
                topping_price += t.Price
                topping_names.append(t.Name)

        price += topping_price
        total_price = price * qty

        dto = CartDTO(
            id=item["id"],
            productid=product.ID,
            quantity=qty,
            price=price,
            title=product.Title,
            image=f"images/{product.Img}" if product.Img and not product.Img.startswith("images/") else product.Img,
            total_price=total_price,
            size=size,
            sugar=sugar,
            ice=ice,
            toppings=topping_names if topping_names else []
        )
        list_cart_dto.append(dto)
    total_item = len(list_cart_dto)
    total_price = sum(dto.total_price for dto in list_cart_dto)
    return list_cart_dto, total_item, total_price

def save_order(data_payment: dict):
    """Hàm xử lý thanh toán giỏ hàng"""
    cart = data_payment.get("cart", None)
    client_price = data_payment.get("total_price", 0)
    if not cart:
        return SaveOrderStatusEnum.NOT_FOUND_CART.value
    # Xử lý lưu trữ đơn hàng vào cơ sở dữ liệu bảng order và order detail
    try:
        from web.models import Order, OrderDetail
        from web import db
        total_price_all = 0
        payment_type = data_payment.get("payment_type", "COD")
        order = Order(
            CustomerName=data_payment.get("name", ""),
            CustomerPhoneNumber=data_payment.get("phone_number", ""),
            CustomerAddress=data_payment.get("address", ""),
            Notes=data_payment.get("notes", ""),
            CreatedBy=session.get("user_id", 0),
            ShipFee=0,
            TotalPrice=0,
            TotalPayment=0,
            PaymentType=data_payment.get("payment_type", "COD"),
            Promotion=data_payment.get("promotion", ""),
            Status= payment_type == "COD" and OrderStatusEnum.WAITING_CONFIRM.value or OrderStatusEnum.WAITING_PAYMENT.value,
        )
        db.session.add(order)
        db.session.flush()  # Để lấy ID của order mới tạo
        for item in cart:
            product: Product = Product.query.get(item["productid"])
            if not product:
                continue
            
            qty = item.get("quantity", 1)
            size = item.get("size", None)
            sugar = item.get("sugar", None)
            ice = item.get("ice", None)
            topping_ids = item.get("toppings", [])

             # ---- Tính giá sản phẩm ----
            price = product.Price

            if size == "L":
                price += 7000

            # Giá topping từ DB
            topping_price = 0
            topping_names = []
            if topping_ids:
                toppings: list[Topping] = Topping.query.filter(Topping.ID.in_(topping_ids)).all()
                for t in toppings:
                    topping_price += t.Price
                    topping_names.append(t.Name)

            price += topping_price
            total_price_item = price * qty
            total_price_all += total_price_item

            order_detail = OrderDetail(
                OrderID=order.ID,
                ProductID=product.ID,
                Quantity=qty,
                Price=price,
                Size=size,
                Sugar=sugar,
                Ice=ice,
                Topping=",".join(item.get("toppings", [])),
                TotalPrice=total_price_item,
            )
            db.session.add(order_detail)

        if client_price != total_price_all:
            return SaveOrderStatusEnum.DIFF_PRICE.value

        # Set lại tổng giá vào order
        order.TotalPrice = total_price_all
        order.TotalPayment = total_price_all + order.ShipFee  # ShipFee hiện = 0

        db.session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error saving order: {e}")
        db.session.rollback()
        return SaveOrderStatusEnum.FAILED.value

    return SaveOrderStatusEnum.SUCCESS.value