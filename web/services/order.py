from math import ceil
from typing import List
from web.extentions.pagination import calcPagination
from web.models import Order, OrderDetail, Topping

def get_user_order(user_id, page=1, page_size=10):
    """
    Fetches the orders for a specific user.
    :param user_id: ID of the user
    :return: List of orders for the user
    """
    query = Order.query.filter_by(CreatedBy=user_id)
    total_records = query.count()
    total_pages = ceil(total_records / page_size)
    query = query.order_by(Order.ID.desc())
    orders = query.offset((page - 1) * page_size).limit(page_size).all()
    pagination = calcPagination(page, total_pages)

    return orders, pagination, total_records, total_pages

def get_order_detail_by_orderid(order_id):
    """
    Fetches the details of an order by its ID.
    :param order_id: ID of the order
    :return: List of order details for the specified order
    """
    details: List[Order] = OrderDetail.query.filter_by(OrderID=order_id).all()
    result = []
    if not details:
        return None
    for detail in details:
        result.append({
            "ID": detail.ID,
            "ProductID": detail.product.ID,
            "Title": detail.product.Title,
            "Image": f'images/{detail.product.Img}' if detail.product.Img and not detail.product.Img.startswith('images/') else detail.product.Img,
            "OrderID": detail.OrderID,
            "Quantity": detail.Quantity,
            "Price": detail.Price,
            "Size": detail.Size,
            "Sugar": detail.Sugar,
            "Ice": detail.Ice,
            "Toppings": [topping.Name for topping in get_toppings_byid(detail.Topping.split(','))] if detail.Topping else [],
            "TotalPrice": detail.TotalPrice
        })
    return result

def get_toppings_byid(topping_ids):
    """
    Fetches toppings by their IDs.
    :param topping_ids: List of topping IDs
    :return: List of toppings
    """
    return Topping.query.filter(Topping.ID.in_(topping_ids)).all()