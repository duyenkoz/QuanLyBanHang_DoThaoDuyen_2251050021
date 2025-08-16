import hashlib
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
import enum
from web import db
from werkzeug.security import generate_password_hash

class UserRole(enum.Enum):
    staff = 'staff'
    admin = 'admin'
    user = 'user'

class User(db.Model):
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
    admin_user = User.query.filter_by(Role=UserRole.admin).first()
    if not admin_user:
        admin = User(
            Phone="0123456789", 
            Password=generate_password_hash("admin"),
            Role=UserRole.admin,
            Name="Admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Seeded default admin account")
    else:
        print("Admin account already exists")