import hashlib
from .customer import Customer
from .user import User, seed_data
from .role import Role
from .category import Category
from .product import Product
from .order import Order
from .orderdetail import OrderDetail
from .topping import Topping
from web import db, app

        
with app.app_context():
    db.create_all()
    seed_data()