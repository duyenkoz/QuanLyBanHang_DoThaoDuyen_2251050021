from web.models import Product
from web.models import Topping

def get_all_products():
    products = Product.query.all()
    return products

def get_product_filter(keyword: str = None, cate_id: int = None, cursor: int = None, top: int = 2):
    products_query = Product.query
    if keyword:
        products_query = products_query.filter(Product.Title.icontains(keyword))
    if cate_id:
        products_query = products_query.filter(Product.CategoryID == cate_id)
    if cursor:
        products_query = products_query.filter(Product.ID < cursor)

    products_query = products_query.order_by(Product.ID.desc()).limit(top)

    products = products_query.all()
    last_cursor = None
    if products:
        last_cursor = products[-1].ID
    return products, last_cursor

def get_products_by_cate_id(cate_id: int):
    products = Product.query.filter_by(CategoryID=cate_id).all()
    return products

def get_product_by_id(product_id: int):
    product = Product.query.get(product_id)
    return product

def get_product_by_title(product_title: str):
    products = Product.query.filter(Product.Title.like(f'%{product_title}%')).all()
    return products

def get_toppings():
    toppings = Topping.query.all()
    return toppings
