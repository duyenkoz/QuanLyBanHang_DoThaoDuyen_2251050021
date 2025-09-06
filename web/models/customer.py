from web import db
from sqlalchemy import func

class Customer(db.Model):
    __tablename__ = "Customer"

    CustomerId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Phone = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    RoleId = db.Column(db.Integer, db.ForeignKey("Role.RoleId"), nullable=False, default=3)
    Name = db.Column(db.String(100), nullable=True)
    Email = db.Column(db.String(100), unique=True, nullable=True)
    Address = db.Column(db.String(255))
    Status = db.Column(db.Integer, default=1)
    CreatedAt = db.Column(db.DateTime, server_default=func.now())