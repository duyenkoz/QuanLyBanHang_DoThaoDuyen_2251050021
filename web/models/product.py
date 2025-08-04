from .category import Category
from web import db

class Product(db.Model):
    __tablename__ = 'Product'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(200), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text)
    Img = db.Column(db.Unicode(200))
    Status = db.Column(db.Integer, nullable=False, default=1)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Category.ID'), nullable=False)

    # Quan hệ ngược lại với Category
    category = db.relationship('Category', back_populates='products')
