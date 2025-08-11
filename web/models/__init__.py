import hashlib
from .category import Category
from .product import Product
from .user import UserRole, User
from .order import Order
from .orderdetail import OrderDetail
from .topping import Topping
from web import db, app

        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()