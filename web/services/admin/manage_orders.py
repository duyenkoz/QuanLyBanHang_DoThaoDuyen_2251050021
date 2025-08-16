from sqlalchemy import desc
from web.common.enum import OrderStatusEnum
from web.extentions.pagination import calcPagination
from web.models import Order
from math import ceil
from web import db


# def get_all_orders(search=None, page=1, page_size=10):
#     query = Order.query

#     # Nếu có từ khóa tìm kiếm, lọc theo ID hoặc tên khách hàng (tuỳ DB)
#     if search:
#         like_pattern = f"%{search}%"
#         query = query.filter(
#             (Order.ID.like(like_pattern)) |
#             (Order.CustomerName.like(like_pattern))
#         )

#     # Tổng số bản ghi
#     total_records = query.count()
#     total_pages = ceil(total_records / page_size) if total_records > 0 else 1

#     # Lấy dữ liệu theo trang
#     query = query.order_by(Order.ID.desc())
#     orders = query.offset((page - 1) * page_size).limit(page_size).all()

#     # Tính phân trang
#     pagination = calcPagination(page, total_pages)

#     return orders, pagination, total_records, total_pages

def get_orders_by_status(status=None, page=1, page_size=10, search=None):
    query = Order.query

    if status:
        try:
            status_enum = OrderStatusEnum[status]
            query = query.filter(Order.Status == status_enum.value)
        except KeyError:
            pass 

    # Lọc theo từ khóa tìm kiếm (nếu có)
    if search:
        query = query.filter(Order.CustomerName.like(f"%{search}%"))

    total_records = query.count()
    total_pages = ceil(total_records / page_size) if total_records > 0 else 1
    orders = (
        query.order_by(desc(Order.Created))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    pagination = calcPagination(page, total_pages)


    return orders, pagination, total_records, total_pages
