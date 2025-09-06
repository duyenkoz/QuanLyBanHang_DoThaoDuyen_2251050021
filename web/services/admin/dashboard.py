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