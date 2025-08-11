from web import db
from sqlalchemy import func

class Order(db.Model):
    __tablename__ = 'Order'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(255), nullable=True)  # varchar(255)
    CustomerPhoneNumber = db.Column(db.String(20), nullable=False)
    CustomerAddress = db.Column(db.String(500), nullable=False)
    Notes = db.Column(db.String(500), nullable=True)
    Created = db.Column(db.DateTime, server_default=func.now())  # datetime default current_timestamp
    CreatedBy = db.Column(db.Integer, nullable=True)
    ShipFee = db.Column(db.Integer, nullable=True)
    TotalPrice = db.Column(db.Integer, nullable=False)
    TotalPayment = db.Column(db.Integer, nullable=False)
    PaymentType = db.Column(db.String(20), nullable=False)
    Promotion = db.Column(db.String(50), nullable=True)
    Status = db.Column(db.String(45), nullable=False)
