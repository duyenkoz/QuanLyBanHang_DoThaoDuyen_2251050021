from web import db


class ImportDetail(db.Model):
    __tablename__ = "ImportDetail"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ImportID = db.Column(db.Integer, db.ForeignKey("Import.ID"), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey("Product.ID"), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Integer)

    product = db.relationship("Product", backref="import_details", uselist=False)
    import_ = db.relationship("Import", backref="details")