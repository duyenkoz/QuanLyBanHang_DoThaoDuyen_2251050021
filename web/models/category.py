from web import db


class Category(db.Model):
    __tablename__ = 'Category'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(200), nullable=False)
    ParentID = db.Column(db.String(5), db.ForeignKey('Category.ID'), nullable=True)
    Type = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.Integer, nullable=False, default=1)
    TypeCode = db.Column(db.String(50))

    # Đệ quy: Danh mục con
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[ID]), lazy=True)

    # Mối quan hệ 1-n với Product (liên kết ngược từ product.py)
    products = db.relationship('Product', back_populates='category', lazy=True)
