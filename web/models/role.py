from sqlalchemy import func
from web import db
class Role(db.Model):
    __tablename__ = "Role"

    RoleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoleName = db.Column(db.String(50), unique=True, nullable=False)
    Description = db.Column(db.String(255))
    CreatedAt = db.Column(db.DateTime, default=func.now())
    UpdatedAt = db.Column(db.DateTime, onupdate=func.now())
    IsActive = db.Column(db.Boolean, default=True)

    users = db.relationship("User", backref="role", lazy=True)
    customers = db.relationship("Customer", backref="role", lazy=True)
