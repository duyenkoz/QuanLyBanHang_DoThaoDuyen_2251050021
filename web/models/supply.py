from web import db

class Supply(db.Model):
    __tablename__ = "Supply"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Unit = db.Column(db.String(50))
    Quantity = db.Column(db.Integer, default=0)

    products = db.relationship("ProductSupply", backref="supply", cascade="all, delete-orphan")
