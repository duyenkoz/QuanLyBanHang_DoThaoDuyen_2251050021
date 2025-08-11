from web import db
from sqlalchemy import func

class Topping(db.Model):
    __tablename__ = 'topping'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.SmallInteger, default=1)  # tinyint trong MySQL
    Created = db.Column(db.DateTime, server_default=func.now())
    CreatedBy = db.Column(db.Integer, nullable=True)
    Modified = db.Column(db.DateTime, nullable=True, onupdate=func.now())
    ModifiedBy = db.Column(db.Integer, nullable=True)