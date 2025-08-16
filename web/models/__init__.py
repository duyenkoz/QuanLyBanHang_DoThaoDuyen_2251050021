import hashlib
from .category import Category
from .product import Product
from .user import UserRole, User, seed_data
from .order import Order
from .orderdetail import OrderDetail
from .topping import Topping
from web import db, app

        
with app.app_context():
    db.create_all()
    seed_data()