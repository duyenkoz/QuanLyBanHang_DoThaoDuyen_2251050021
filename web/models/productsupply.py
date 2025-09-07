from web import db

class ProductSupply(db.Model):
    __tablename__ = "ProductSupply"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductID = db.Column(db.Integer, db.ForeignKey("Product.ID"), nullable=False)
    SupplyID = db.Column(db.Integer, db.ForeignKey("Supply.ID"), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", backref="product_supplies", uselist=False)