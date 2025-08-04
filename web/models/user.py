from web import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as RoleEnum

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class Users(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.username