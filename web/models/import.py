from web import db
from sqlalchemy import func

class Import(db.Model):
    __tablename__ = "Import"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ImportDate = db.Column(db.DateTime, dserver_default=func.now(), nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey("User.UserId"))
    Note = db.Column(db.Text)

    staff = db.relationship("User", backref="imports", uselist=False)
    details = db.relationship("ImportDetail", backref="import_ref", cascade="all, delete-orphan")
