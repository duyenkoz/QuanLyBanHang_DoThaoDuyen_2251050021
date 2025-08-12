import hashlib
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
import enum
from web import db

Base = declarative_base()

class UserRole(enum.Enum):
    staff = 'staff'
    admin = 'admin'
    user = 'user'

class User(Base):
    __tablename__ = 'users'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Phone = Column(String(20), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Role = Column(Enum(UserRole), default=UserRole.user)
    Name = Column(String(100))
    Email = Column(String(100))
    Address = Column(String(255))
    Created_at = Column(TIMESTAMP, server_default=func.now())

def seed_data():
    if not User.query.first():
        admin = User(
            name="Admin",
            username="admin",
            password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),
            user_role=UserRole.ADMIN
        )
        db.session.add(admin)
        db.session.commit()