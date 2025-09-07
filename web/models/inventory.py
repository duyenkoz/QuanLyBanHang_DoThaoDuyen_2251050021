from web import db

class Inventory(db.Model):
    __tablename__ = "Inventory"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductID = db.Column(db.Integer, db.ForeignKey("Product.ID"), nullable=False)
    Quantity = db.Column(db.Integer, default=0)

    product = db.relationship("Product", backref="inventory", uselist=False)