from web.dtos.cart_dto import CartDTO
from web.models.product import Product


def get_products_in_cart(cart: list[dict[int, int]]):
    """Hàm lấy danh sách sản phẩm trong giỏ hàng"""
    list_cart_dto: list[CartDTO] = []
    for item in cart:
        product: Product = Product.query.get(item["productid"])
        if not product:
            continue
        qty = item.get("quantity", 1)
        size = item.get("size", None)
        toppings = item.get("toppings", [])
        sugar = item.get("sugar", None)
        ice = item.get("ice", None)

        price = product.Price
        
        if size == "L":
            price += 7000
        
        topping_price = len(toppings) * 5000
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
            toppings=toppings
        )
        list_cart_dto.append(dto)
    total_item = len(list_cart_dto)
    total_price = sum(dto.total_price for dto in list_cart_dto)
    return list_cart_dto, total_item, total_price