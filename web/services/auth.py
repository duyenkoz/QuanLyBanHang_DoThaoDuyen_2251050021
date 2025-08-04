import hashlib

from web.models.user import Users


def login(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = Users.query.filter(Users.username == username, Users.password == password).first()

    return u