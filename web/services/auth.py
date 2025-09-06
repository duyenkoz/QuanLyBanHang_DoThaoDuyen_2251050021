
from web.models.customer import Customer
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from web import db
from web.models.user import User

def register_user(phone, password, confirm_password):
    if password != confirm_password:
        return False, "Mật khẩu không khớp"

    hashed_password = generate_password_hash(password)

    new_customer  = Customer(
        Phone=phone,
        Password=hashed_password
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
        return True, "Đăng ký thành công"
    except IntegrityError:
        db.session.rollback()
        return False, "Số điện thoại đã được sử dụng"

def check_login(phone: str, password: str):
    user = db.session.query(User).filter_by(Phone=phone).first()
    if user and check_password_hash(user.Password, password):
        return {"type": "user", "obj": user}

    # Nếu không thấy thì check trong Customer
    customer = db.session.query(Customer).filter_by(Phone=phone).first()
    if customer and check_password_hash(customer.Password, password):
        return {"type": "customer", "obj": customer}

    return None