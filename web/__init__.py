import hashlib
from flask import Flask
from flask_login import LoginManager, UserMixin
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:%s@localhost/shopmanagement?charset=utf8mb4"
    % quote("Quocviet318<3")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "thien-dao-18-1988"
app.config["PAGE_SIZE"] = 10

db = SQLAlchemy(app)
