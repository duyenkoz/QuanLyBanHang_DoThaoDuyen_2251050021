from web import db

class OrderDetail(db.Model):
    __tablename__ = 'orderdetail'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Order.ID'), nullable=False)
    ProductID = db.Column(db.Integer, nullable=False)
    Size = db.Column(db.String(10), nullable=True)
    Sugar = db.Column(db.SmallInteger, nullable=True)  # tinyint trong MySQL
    Ice = db.Column(db.SmallInteger, nullable=True)    # tinyint trong MySQL
    Topping = db.Column(db.String(50), nullable=True)
    Price = db.Column(db.Integer, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    TotalPrice = db.Column(db.Integer, nullable=False)

    # Quan hệ với bảng Order (một order có nhiều orderdetail)
    order = db.relationship('Order', backref=db.backref('details', lazy=True))
