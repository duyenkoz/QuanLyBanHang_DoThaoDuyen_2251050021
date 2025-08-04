import hashlib
from .category import Category
from .product import Product
from .user import Users, UserRole
from web import db, app

        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()