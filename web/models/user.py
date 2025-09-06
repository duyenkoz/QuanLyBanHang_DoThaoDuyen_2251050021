import hashlib
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
import enum
from web import db
from werkzeug.security import generate_password_hash
from web.models.role import Role


class User(db.Model):
    __tablename__ = "User"

    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Phone = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    RoleId = db.Column(db.Integer, db.ForeignKey("Role.RoleId"), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=True)
    Address = db.Column(db.String(255))
    Status = db.Column(db.Integer, default=1)
    CreatedAt = db.Column(db.DateTime, server_default=func.now())

def seed_data():
    # Kiểm tra role "admin" đã có chưa
    admin_role = Role.query.filter_by(RoleName="admin").first()
    if not admin_role:
        admin_role = Role(RoleName="admin", Description="Quản trị hệ thống")
        db.session.add(admin_role)
        db.session.commit()

    # Kiểm tra user admin đã có chưa
    admin_user = User.query.filter_by(RoleId=admin_role.RoleId).first()
    if not admin_user:
        admin = User(
            Phone="0123456789",
            Password=generate_password_hash("admin123"),  
            RoleId=admin_role.RoleId,
            Name="Administrator"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Seeded default admin account")
    else:
        print("ℹ️ Admin account already exists")