from web.dtos.cart_dto import CartDTO
from web.models.product import Product


def get_products_in_cart(cart: list[dict[int, int]]):
    ids = [item["id"] for item in cart]
    products: list[Product] = Product.query.filter(Product.ID.in_(ids)).all()

    list_cart_dto = []
    for product in products:
        qty = next(item["quantity"] for item in cart if item["id"] == product.ID)
        dto = CartDTO(
            id==product.ID,
            quantity=qty,
            price=product.Price,
            title=product.Title,
            image=f"images/{product.Img}" if product.Img and not product.Img.startswith("images/") else product.Img,
            total_price=product.Price * qty
        )
        list_cart_dto.append(dto)
    total_item = len(products)
    return list_cart_dto, total_item