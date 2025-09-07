from datetime import datetime, timedelta
from web.models.user import User
from web.models.order import Order
from web.models.product import Product
from web.models.category import Category
from web import db


def get_dashboard_data():
    # count_staff = User.query.filter(User.Role==UserRole.staff).count()
    # count_users = User.query.filter(User.Role==UserRole.user).count()
    count_orders = Order.query.count()  # Assuming Order is a model for orders
    count_products = Product.query.count()  # Assuming Product is a model for products
    count_categories = Category.query.count()  # Assuming Category is a model for categories
    total_revenue = Order.query.with_entities(db.func.sum(Order.TotalPayment)).scalar() or 0
    return {
        # "count_staff": count_staff,
        # "count_users": count_users,
        "count_orders": count_orders,
        "count_products": count_products,
        "count_categories": count_categories,
        "total_revenue": total_revenue
    }

def get_revenue_chart_data(from_date: datetime, to_date: datetime, mode: str):
    try:
        query = db.session.query(
            db.func.date(Order.Created).label('date'),
            db.func.sum(Order.TotalPayment).label('total_revenue')
        ).group_by(db.func.date(Order.Created)).order_by(db.func.date(Order.Created))

        if from_date:
            query = query.filter(db.func.date(Order.Created) >= from_date)
        if to_date:
            # Cộng end date thêm một ngày để bao gồm cả ngày
            to_date = to_date + timedelta(days=1)
            query = query.filter(db.func.date(Order.Created) <= to_date)

        results = query.all()
        if mode == "month":
            # Nhóm theo tháng
            monthly_data = {}
            for result in results:
                month = result.date.strftime("%Y-%m")
                if month not in monthly_data:
                    monthly_data[month] = 0
                monthly_data[month] += float(result.total_revenue)
            chart_data = {
                "labels": list(monthly_data.keys()),
                "revenues": list(monthly_data.values())
            }
            return chart_data
        elif mode == "year":
            # Nhóm theo năm
            yearly_data = {}
            for result in results:
                year = result.date.strftime("%Y")
                if year not in yearly_data:
                    yearly_data[year] = 0
                yearly_data[year] += float(result.total_revenue)
            chart_data = {
                "labels": list(yearly_data.keys()),
                "revenues": list(yearly_data.values())
            }
            return chart_data
        else:
            chart_data = {
                "labels": [str(result.date) for result in results],
                "revenues": [float(result.total_revenue) for result in results]
            }
        return chart_data
    except Exception as e:
        raise e
    
def get_orders_chart_data(from_date: datetime, to_date: datetime, mode: str):
    try:
        query = db.session.query(
            db.func.date(Order.Created).label('date'),
            db.func.count(Order.ID).label('total_orders')
        ).group_by(db.func.date(Order.Created)).order_by(db.func.date(Order.Created))

        if from_date:
            query = query.filter(db.func.date(Order.Created) >= from_date)
        if to_date:
            # Cộng end date thêm một ngày để bao gồm cả ngày
            to_date = to_date + timedelta(days=1)
            query = query.filter(db.func.date(Order.Created) <= to_date)
        results = query.all()
        if mode == "month":
            # Nhóm theo tháng
            monthly_data = {}
            for result in results:
                month = result.date.strftime("%Y-%m")
                if month not in monthly_data:
                    monthly_data[month] = 0
                monthly_data[month] += int(result.total_orders)
            chart_data = {
                "labels": list(monthly_data.keys()),
                "orders": list(monthly_data.values())
            }
            return chart_data
        elif mode == "year":
            # Nhóm theo năm
            yearly_data = {}
            for result in results:
                year = result.date.strftime("%Y")
                if year not in yearly_data:
                    yearly_data[year] = 0
                yearly_data[year] += int(result.total_orders)
            chart_data = {
                "labels": list(yearly_data.keys()),
                "orders": list(yearly_data.values())
            }
            return chart_data
        else:
            chart_data = {
                "labels": [str(result.date) for result in results],
                "orders": [int(result.total_orders) for result in results]
            }
        return chart_data
    except Exception as e:
        raise e
    